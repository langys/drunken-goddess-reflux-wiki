---
name: wb-video-facts
description: Extract and frame-verify game facts from videos (YouTube / Steam trailers) — captions, chapters, targeted clips, sharpest-frame extraction, proper-noun spelling checks. Triggers: 视频, 视频核验, 采集视频, 抓视频, 下载视频, 字幕, 抽帧, 验证名字, 名字拼写, boss 名字, 实机演示, 预告片, walkthrough 视频, video facts, frame check, yt-dlp.
---

# wb-video-facts — Video Fact Extraction & Frame Verification

Use when a fact lives in footage rather than text: on-screen names, UI wording, encounter order, mechanics demos.

## The rule: a proper noun needs one of three sources

1. **Frame level (strongest)** — the game's own dialogue name-tag / UI panel, read letter by letter in an extracted frame;
2. **Hand-written chapter list** — the uploader typed it; no ASR involved;
3. **2+ independent sources agreeing** — ⚠️ but two ASR transcripts can agree and still be wrong (measured: both transcripts wrote "Broner" while the on-screen label reads **Brauner**; "Talos" heard as "Tygalos"). **If a frame is reachable, read the frame.**

Anything resting on ASR alone stays marked `[frame check pending]` and does not go into pages.

## Environment (ready on this machine)

```bash
YTDLP=~/.workbuddy/binaries/python/envs/default/bin/yt-dlp   # ships yt-dlp-ejs
PY=~/.workbuddy/binaries/python/envs/default/bin/python
KEYFRAMES=~/.workbuddy/skills/game-wiki-site-builder/scripts/extract_video_keyframes.py
```

Anti-bot trio (all three or nothing): `--cookies-from-browser chrome` (first Keychain read needs time — a 10 s probe misreads it as failure) + the venv's `yt-dlp[default]` + `--js-runtimes node`.

Symptoms: `Sign in to confirm you're not a bot` → cookies not read; `n challenge solving failed` → EJS/Node missing.
**Known trap**: `--extractor-args "youtube:player_client=android_vr,web"` is inert here — yt-dlp skips `android_vr` when cookies are supplied, and without cookies it cannot pass the bot wall. Do not rely on it.

Media directories (already gitignored — never commit footage):

- `research/transcripts/` — caption library (official / community subdirs)
- `research/videos/segments/` — targeted clips → `frames/` — extracted frames

## The five-step chain (do not skip steps; skipping wastes bandwidth)

```bash
# 1) Search candidates — flat mode answers in seconds; pick before downloading
$YTDLP --cookies-from-browser chrome --js-runtimes node \
  "ytsearch8:<keywords>" --flat-playlist --skip-download \
  --print "%(id)s | %(duration)s | %(title)s"

# 2) Captions first — hours-long video, tens-of-KB text library
$YTDLP --cookies-from-browser chrome --js-runtimes node --no-warnings \
  --skip-download --write-auto-subs --sub-langs "en-orig,en" --sub-format vtt \
  -o "research/transcripts/community/%(id)s.%(ext)s" "<URL>"

# 3) Chapters — cleanest name source (human-typed, zero ASR errors)
$YTDLP ... --skip-download --print "%(chapters)j" "<URL>"

# 4) Once a keyword hits in a caption, pull only the 15–30 s low-res clip
$YTDLP ... -f "18/worst[height<=720]" \
  --download-sections "*48:15-48:40" --force-keyframes-at-cuts \
  -o "research/videos/segments/<name>.mp4" "<URL>"

# 5) Micro-window sharpest-frame extraction (±2 s, 0.3 s steps,
#    Laplacian-variance + contrast score picks the clearest frame)
$PY $KEYFRAMES research/videos/segments/<name>.mp4 \
  -o research/videos/segments/frames -t <clip-relative seconds> --topic-name <name>
```

**Clip-relative seconds** = absolute timestamp − clip start (clip 48:15–48:40, hit at 48:26 → `-t 11`).

**Never hand-roll fixed-interval ffmpeg sampling** — measured on the same target: fixed sampling took 11.0 s, the sharpest-frame chain took 12.65 s and that was the frame where the dialogue text is actually readable.

## Reading and archiving

1. Read frames **fully, letter by letter** — names hide inside whole sentences on the dialogue box;
2. Archive each batch as `research/<source>-extraction-YYYY-MM-DD.md`: video ledger + per-fact findings with `&t=seconds` deep links + explicit boundaries;
3. Register sources and boundaries in `research/fact-check-ledger.md`;
4. Cite in pages as `[source](URL&t=seconds)` so a reader lands on the evidence second;
5. **Verify GSC terms before writing content for them** — a zero-hit term may be another game's collision (measured: "blightrock cestus" is Arcane Lineage gear, matched via "cestus"). Never manufacture content for a mis-match.

## Measured lessons (portable across projects)

| Lesson | Evidence |
| --- | --- |
| ASR mangles proper nouns | Talos→"Tygalos"; Brauner→"Broner" |
| Two-source ASR agreement is NOT enough | both transcripts wrote "Broner"; the on-screen label settled it |
| Chapter lists are trustworthy | human-typed boss list supplied Succubus / Shadow Rose |
| Pull clips, not films | 15–30 s at 360p around the hit only |
| Keep footage out of git | `research/videos|transcripts` gitignored; reports carry timestamp links only |
