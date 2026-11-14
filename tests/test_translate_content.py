"""Tests for scripts/translate_content.py's validate() gate.

These exist because an edit once left the proper-noun, title-budget and
list-count checks *after* a `return problems`, turning them into unreachable
dead code. `py_compile` passes on unreachable code and nothing else called
validate(), so a gate that had silently stopped gating went unnoticed. Two of
the tests below (proper noun, list count) are the ones that would have failed.

Run: python3 -m unittest discover -s tests -v   (from the skill root)
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts.translate_content import body_blocks, validate  # noqa: E402

EN_BODY = (
    "Nivalis has more than 130 characters to meet. The relationships you build "
    "with them are the confirmed backbone of the whole experience, and this page "
    "explains how the documented systems work in practice for a new operator.\n\n"
    "## Four relationship types\n\n"
    "- Friendship is the first of the four documented relationship types here.\n"
    "- Rivalry is a relationship type, not the absence of one, per the developers.\n"
)


def make_item(**overrides):
    """An item shaped like one entry of a `translate_content.py plan` queue."""
    source = "Nivalis has more than 130 characters. Unity powers the world here."
    item = {
        "file": "Nivalis-Nights-character-guide.md",
        "targetLocale": "es",
        "frontmatter": {"slug": "Nivalis-Nights-character-guide", "hub": "guide"},
        "shape": {**body_blocks(EN_BODY), "words": len(EN_BODY.split())},
        "properNouns": ["unity"],
        "titleBudget": 90,
        "descriptionBudget": 172,
        "frontmatterLists": {"quickGuide": 0, "cards": 0, "faq": 0},
        "source": source,
    }
    item.update(overrides)
    return item


def with_body(body: str, **overrides):
    item = make_item(**overrides)
    item["shape"] = {**body_blocks(body), "words": len(EN_BODY.split())}
    return item, body


class ValidateGateTests(unittest.TestCase):
    """The gate must reject, not just accept."""

    def test_accepts_a_faithful_translation(self):
        item, body = with_body(EN_BODY + "\nThe game runs on Unity.")
        self.assertEqual(validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set()), [])

    def test_rejects_missing_proper_noun(self):
        # Regression: this check sat after an early return and never ran.
        item, body = with_body(EN_BODY)
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(
            any("proper noun missing" in p for p in problems),
            f"a missing proper noun must be rejected; got {problems}",
        )

    def test_proper_noun_matches_as_a_word_not_a_substring(self):
        # "unity" must not be satisfied by "community"; this false positive is
        # what pushed a translator into inventing a sentence.
        item, body = with_body(EN_BODY + "\nThe community is friendly.")
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(any("proper noun missing" in p for p in problems))

    def test_proper_noun_accepts_a_real_mention(self):
        item, body = with_body(EN_BODY + "\nThe game runs on Unity.")
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertFalse([p for p in problems if "proper noun" in p], problems)

    def test_rejects_lost_list_items(self):
        # Regression: also unreachable, and list loss drops rendered sections.
        item, body = with_body(EN_BODY, frontmatterLists={"quickGuide": 3})
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(any("quickGuide items" in p for p in problems), problems)

    def test_counts_nested_list_items(self):
        block = (
            "slug: x\nquickGuide:\n  - one\n  - two\ncards:\n  - title: a\n    body: b\n"
            "  - title: c\n    body: d\n"
        )
        item = make_item(frontmatterLists={"quickGuide": 2, "cards": 2})
        problems = validate(item, f"---\n{block}---\n\n{EN_BODY}", pathlib.Path('.'), set())
        self.assertEqual([p for p in problems if "items" in p], [], problems)

    def test_rejects_over_budget_title(self):
        item, body = with_body(EN_BODY)
        problems = validate(
            item, f"---\nslug: x\ntitle: {'z' * 95}\n---\n\n{body}", pathlib.Path('.'), set()
        )
        self.assertTrue(any("title 95 over budget" in p for p in problems), problems)

    def test_rejects_frozen_frontmatter_change(self):
        item, body = with_body(EN_BODY)
        problems = validate(item, f"---\nslug: changed\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(any(p.startswith("slug changed") for p in problems), problems)

    def test_rejects_dropped_url(self):
        item, body = with_body(EN_BODY)
        item["source"] = "See https://example.com/spec for the spec."
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(any("URL dropped" in p for p in problems), problems)

    def test_rejects_summarised_body(self):
        item, body = with_body("Too short a translation of the whole page.")
        problems = validate(item, f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}", pathlib.Path('.'), set())
        self.assertTrue(any("body too short" in p for p in problems), problems)

    def test_rejects_no_frontmatter(self):
        self.assertEqual(
            validate(make_item(), "no frontmatter here", pathlib.Path('.'), set()),
            ["no frontmatter block"],
        )


class CJKSpacingTests(unittest.TestCase):
    """分かち書き spacing is a rendering artefact, not a translation."""

    JA = (
        "ニヴァリスには130人以上のキャラクターがいます。関係を築くことが体験の"
        "背骨であることは確認済みです。このページでは仕組みを説明します。"
    )

    def _item(self, body):
        item = make_item(targetLocale="ja", properNouns=[])
        item["shape"] = {**body_blocks(body), "words": 20}
        return item

    def _problems(self, tail: str):
        body = self.JA + tail
        return validate(
            self._item(body),
            f"---\nslug: Nivalis-Nights-character-guide\nhub: guide\n---\n\n{body}",
            pathlib.Path('.'),
            set(),
        )

    def test_flags_ascii_space_after_a_date(self):
        # Regression: two published files shipped U+0020 before a particle.
        # Escapes are explicit here because the two space kinds are visually
        # identical, which is what made the original artefact invisible.
        problems = self._problems(
            "調整値は2026年9月29日\u0020のローンチ前に変更される可能性があります。"
        )
        self.assertTrue(any("stray space after a number" in p for p in problems), problems)

    def test_allows_ideographic_comma_after_a_date(self):
        # U+3001 (、) sits inside the CJK ranges but is punctuation: a class-based
        # pattern would flag "9月29日、" as an artefact and reject valid Japanese.
        problems = self._problems("調整値は2026年9月29日、ローンチ前に変更されます。")
        self.assertFalse([p for p in problems if "stray space" in p], problems)

    def test_allows_mixed_script_spacing(self):
        # "Unity で" / "SSD を" are correct Japanese, not artefacts.
        problems = self._problems("本作は Unity で作られ、推奨構成では SSD を求めます。")
        self.assertFalse([p for p in problems if "stray space" in p], problems)

    def test_allows_ideographic_space_after_a_date(self):
        # U+3000 is correct Japanese spacing after a date; treating it as an
        # artefact would reject good translations.
        problems = self._problems("調整値は2026年9月29日\u3000のローンチ前に変更されます。")
        self.assertFalse([p for p in problems if "stray space" in p], problems)


class ReachabilityTests(unittest.TestCase):
    """A gate that cannot run is not a gate."""

    def test_validate_has_no_statements_after_its_return(self):
        import ast

        source = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "translate_content.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        fn = next(
            n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "validate"
        )
        returns = [i for i, node in enumerate(fn.body) if isinstance(node, ast.Return)]
        self.assertEqual(
            returns,
            [len(fn.body) - 1],
            "validate() has statements after a return; its later checks are dead code",
        )


if __name__ == "__main__":
    unittest.main()
