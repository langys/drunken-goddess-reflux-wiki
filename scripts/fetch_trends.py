#!/usr/bin/env python3
"""Fetch Google Trends evidence for a keyword and turn it into a go/no-go signal.

Replaces the manual "open Trends, eyeball the curve, screenshot it" step with
something scriptable and repeatable. The judgment thresholds match stage A of the
playbook (references/01-keyword-and-domain-selection.md), so the verdict this
prints is the same call you would make by hand — just faster and on the record.

Usage:
    python3 scripts/fetch_trends.py "Witchbrook"
    python3 scripts/fetch_trends.py "Witchbrook" --geo US --timeframe "today 3-m"
    python3 scripts/fetch_trends.py "Witchbrook" --compare "Stardew Valley"
    python3 scripts/fetch_trends.py "Witchbrook" --out research/trends-witchbrook.json

Why a baseline is on by default: Trends returns *relative* indices, so "63" is
meaningless alone — the scale is normalised to the window's own peak. Comparing
against GPTS (broad, steady, English) turns it into a magnitude you can act on:
peak at or above GPTS means real, sustainable search demand worth building for.

Caveat worth knowing: pytrends is an unofficial client. Google rate-limits it
aggressively (HTTP 429), and the numbers are relative indices, not volumes. It is
excellent for *shape* — rising, peaking, flat, declining — which is exactly what
the decision needs. For absolute volume, use SimilarWeb or a keyword tool.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import warnings

# pytrends calls DataFrame.fillna in a way pandas now warns about; the warning is
# noise on every run and says nothing about our data, so it is filtered before
# pytrends is imported.
warnings.filterwarnings("ignore", category=FutureWarning, module="pytrends")

try:
    from pytrends.request import TrendReq
except ImportError:
    print(
        "pytrends is required. Install with:\n  pip install pytrends",
        file=sys.stderr,
    )
    raise SystemExit(1)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build_client(hl: str, tz: int, retries: int = 3, backoff: float = 5.0):
    """Retry on Google's rate limiting instead of failing the whole run."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return TrendReq(hl=hl, tz=tz, timeout=(10, 25))
        except Exception as error:  # noqa: BLE001 - pytrends raises bare exceptions
            last_error = error
            if attempt < retries:
                time.sleep(backoff * attempt)
    raise SystemExit(f"could not create a Trends client: {last_error}")


def fetch(pytrends, terms: list[str], timeframe: str, geo: str, retries: int = 3):
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            pytrends.build_payload(terms, timeframe=timeframe, geo=geo)
            interest = pytrends.interest_over_time()
            related = pytrends.related_queries()
            return interest, related
        except Exception as error:  # noqa: BLE001
            last_error = error
            message = str(error)
            if "429" in message or "too many" in message.lower():
                wait = 20 * attempt
                print(f"  rate limited by Google, waiting {wait}s (attempt {attempt}/{retries})", file=sys.stderr)
                time.sleep(wait)
            elif attempt < retries:
                time.sleep(5 * attempt)
    raise SystemExit(
        f"Trends request failed after {retries} attempts: {last_error}\n"
        "  Google rate-limits pytrends. Wait a few minutes, or check the curve "
        "manually at https://trends.google.com/trends/explore"
    )


def analyse_baseline(series: list[int], baseline: list[int], name: str) -> dict:
    """Compare the subject against a stable anchor term.

    Trends returns relative indices: a value of "63" means nothing on its own,
    because the scale is normalised to the highest point in the window. Comparing
    against a term whose magnitude you already understand turns that into a real
    signal. GPTS is the anchor this playbook uses — broad, steady, and English-
    language, so it behaves like a yardstick rather than a moving target.

    The peak comparison is deliberately the headline: current values in a 7-day
    window collapse to 0 for anything short of a breakout, while the peak ratio is
    stable across windows.
    """
    if not series or not baseline:
        return {}

    peak_ratio = max(series) / max(max(baseline), 1)

    # The trailing ratio is the headline, not the peak ratio.
    #
    # Trends normalises the whole window to one mutual peak, so if the anchor
    # peaked months ago its maximum sits at 100 while its current level is far
    # lower — which makes an all-time peak ratio understate a term that is rising
    # right now. Comparing both series over the same trailing window is immune to
    # that, and gives the same answer whether you ask for 1 month or 3.
    window = min(8, len(series), len(baseline))
    recent = series[-window:]
    recent_base = baseline[-window:]
    recent_ratio = (sum(recent) / window) / max(sum(recent_base) / window, 1)

    if recent_ratio >= 1.0:
        verdict = "量级不错（当前不低于基准）"
    elif recent_ratio >= 0.5:
        verdict = "中等（当前约为基准的一半以上）"
    elif recent_ratio >= 0.2:
        verdict = "偏小（当前约为基准的 1/5–1/2）"
    else:
        verdict = "量级偏小（当前不足基准的 1/5）"

    # Below ~5 the index is too coarse for a ratio to mean anything.
    reliable = max(max(series), max(baseline)) >= 5

    return {
        "anchor": name,
        "peakRatio": round(peak_ratio, 2),
        "recentRatio": round(recent_ratio, 2),
        "subjectPeak": max(series),
        "anchorPeak": max(baseline),
        "reliable": reliable,
        "verdict": verdict if reliable else "数据过稀，比值不可靠（换更长的时间范围）",
    }


def analyse(series: list[int]) -> dict:
    """Classify the curve shape, mirroring the manual decision table."""
    if not series:
        return {"shape": "no-data", "verdict": "无法判断", "detail": "Trends 未返回数据（词太新或太冷门）"}

    peak = max(series)
    peak_at = series.index(peak)
    recent = series[-7:] if len(series) >= 7 else series
    recent_avg = sum(recent) / len(recent)
    first_half = series[: len(series) // 2] or series
    second_half = series[len(series) // 2 :] or series
    trend_up = (sum(second_half) / len(second_half)) > (sum(first_half) / len(first_half)) * 1.1

    # Where the peak sits tells you whether you are early or late.
    position = peak_at / max(len(series) - 1, 1)
    tail = series[peak_at:]
    decayed = len(tail) > 3 and (sum(tail[-3:]) / 3) < peak * 0.35

    if recent_avg == 0:
        return {"shape": "flat-zero", "verdict": "放弃", "detail": "近期搜索量为 0"}
    if decayed:
        return {
            "shape": "peaked-and-falling",
            "verdict": "放弃",
            "detail": f"峰值为 {peak}（第 {peak_at + 1}/{len(series)} 期），之后已跌破峰值 35%——在追尾巴",
        }
    if position > 0.85 and recent_avg >= peak * 0.8:
        return {
            "shape": "rising",
            "verdict": "立刻上站",
            "detail": f"峰值出现在最近（第 {peak_at + 1}/{len(series)} 期），当前均值 {recent_avg:.0f} ≈ 峰值 {peak}",
        }
    if trend_up:
        return {
            "shape": "rising-slow",
            "verdict": "可做",
            "detail": f"后半段高于前半段 10% 以上，当前均值 {recent_avg:.0f}",
        }
    return {
        "shape": "flat-or-declining",
        "verdict": "放弃",
        "detail": f"曲线走平或下降，当前均值 {recent_avg:.0f}，峰值 {peak}",
    }


def rising_queries(related: dict, term: str) -> list[dict]:
    """Extract the 'Rising' related queries — stage A's highest-value output."""
    entry = related.get(term) or {}
    rising = entry.get("rising")
    if rising is None or getattr(rising, "empty", True):
        return []
    out = []
    for _, row in rising.head(25).iterrows():
        out.append({"query": str(row.get("query", "")), "growth": int(row.get("value", 0))})
    return out


def intent_score(queries: list[dict]) -> tuple[int, list[str]]:
    """Count usable search intents, weighted by the themes the corpus showed matter."""
    themes = {
        "codes": 5, "tier": 5, "best": 4, "build": 3, "guide": 3, "release": 4,
        "download": 3, "wiki": 3, "how": 2, "tips": 2, "steam": 2, "date": 3,
        "map": 2, "boss": 2, "class": 2, "character": 2, "mod": 2, "discord": 2,
    }
    hits: list[str] = []
    score = 0
    for item in queries:
        lowered = item["query"].lower()
        for theme, weight in themes.items():
            if theme in lowered:
                score += weight
                hits.append(item["query"])
                break
    return score, sorted(set(hits))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("keyword", help="game or subject to check")
    parser.add_argument("--compare", action="append", default=[], help="extra term(s) to compare against (adds context)")
    parser.add_argument(
        "--baseline",
        default="GPTS",
        help="stable anchor term used to judge magnitude (default: GPTS). "
        "Trends indices are relative, so a raw number means nothing without one.",
    )
    parser.add_argument("--no-baseline", action="store_true", help="skip the anchor comparison")
    parser.add_argument("--geo", default="", help="region code, e.g. US; empty = worldwide")
    parser.add_argument("--timeframe", default="today 3-m", help="Trends timeframe (default: today 3-m)")
    parser.add_argument("--hl", default="en-US")
    parser.add_argument("--tz", type=int, default=0)
    parser.add_argument("--out", type=pathlib.Path, default=None, help="write the full result as JSON")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a report")
    args = parser.parse_args()

    baseline = None if args.no_baseline else args.baseline
    terms = [args.keyword, *([baseline] if baseline else []), *args.compare][:5]  # Trends allows at most 5 terms
    pytrends = build_client(args.hl, args.tz)
    print(f"querying Trends: {', '.join(terms)}  geo={args.geo or 'worldwide'}  {args.timeframe}", file=sys.stderr)
    interest, related = fetch(pytrends, terms, args.timeframe, args.geo)

    series = [int(v) for v in interest[args.keyword].tolist()] if not interest.empty and args.keyword in interest else []
    verdict = analyse(series)
    rising = rising_queries(related, args.keyword)
    score, hits = intent_score(rising)

    baseline_series = (
        [int(v) for v in interest[baseline].tolist()]
        if baseline and not interest.empty and baseline in interest
        else []
    )
    baseline_result = analyse_baseline(series, baseline_series, baseline) if baseline_series else {}

    result = {
        "keyword": args.keyword,
        "compared": args.compare,
        "baseline": baseline,
        "baselineSeries": baseline_series,
        "magnitude": baseline_result,
        "geo": args.geo or "worldwide",
        "timeframe": args.timeframe,
        "series": series,
        "analysis": verdict,
        "risingQueries": rising,
        "intentScore": score,
        "intentHits": hits,
        "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"\n=== {args.keyword} ===")
    print(f"  曲线形态 : {verdict['shape']}")
    print(f"  判断     : {verdict['verdict']}")
    print(f"  依据     : {verdict['detail']}")
    if series:
        spark = "".join("▁▂▃▄▅▆▇█"[min(7, v * 8 // max(max(series), 1))] for v in series[-40:])
        print(f"  近 40 期 : {spark}")
    if baseline_result:
        b = baseline_result
        print(
            f"  量级对比 : 当前 {b['recentRatio']}× {b['anchor']}"
            f"（峰值 {b['subjectPeak']} vs {b['anchorPeak']} = {b['peakRatio']}×）"
        )
        print(f"  量级判断 : {b['verdict']}")
        if not b["reliable"]:
            print("             （样本过稀：试试 --timeframe 'today 3-m'）")
    print(f"  意图得分 : {score}  （打分矩阵里'衍生需求丰富度'最多 20 分）")
    if hits:
        print(f"  可用意图 : {', '.join(hits[:10])}")
    if rising:
        print(f"\n  上升中的相关查询（前 10）：")
        for item in rising[:10]:
            growth = "Breakout" if item["growth"] >= 5000 else f"+{item['growth']}%"
            print(f"    {growth:>9}  {item['query']}")
    else:
        print("\n  未返回相关查询（词太新或数据不足）")

    if args.out:
        print(f"\n完整结果已写入 {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
