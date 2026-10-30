#!/usr/bin/env python3
"""Check a script against a style-bible, fast and offline.

Usage:
  python3 check_style.py --bible style-bible.yaml --script script.txt [--timeline timeline.txt] [--caption caption.txt] [--json]

The script file is plain text. The first line is treated as the title.
The timeline file is one clip name per line, in playback order.
The caption file, if given, is checked for a closing question.

Output is a Markdown check report on stdout, or JSON with --json.
Exit 0 when no banned phrase, repetition, or consecutive animation repeat is found.
Exit 1 when any of those is found.
Warnings (hook length, numbers to verify) never change the exit code on their own.
This script only reads the files given. It sends nothing anywhere.
"""
import argparse
import json
import re


def load_bible(path):
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        return _load_bible_simple(path)


def _load_bible_simple(path):
    data = {"phrases": {"banned": [], "preferred": []},
            "previous_work": {"topics": [], "titles": []}}
    current = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped in ("banned:", "preferred:", "topics:", "titles:"):
                current = stripped[:-1]
            elif stripped.startswith("- ") and current:
                value = stripped[2:].strip().strip('"').strip("'")
                if value:
                    if current in ("banned", "preferred"):
                        data["phrases"][current].append(value)
                    else:
                        data["previous_work"][current].append(value)
    return data


def get_list(data, *keys):
    node = data
    for key in keys:
        if not isinstance(node, dict):
            return []
        node = node.get(key, [])
    if isinstance(node, list):
        return [str(x) for x in node if str(x).strip()]
    return []


def first_sentence(text):
    match = re.split(r"[.!?]\s+", text.strip())
    return match[0] if match else ""


def main():
    parser = argparse.ArgumentParser(description="Check a script against a style-bible.")
    parser.add_argument("--bible", required=True)
    parser.add_argument("--script", required=True)
    parser.add_argument("--timeline")
    parser.add_argument("--caption")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    bible = load_bible(args.bible)
    banned = get_list(bible, "phrases", "banned")
    preferred = get_list(bible, "phrases", "preferred")
    topics = get_list(bible, "previous_work", "topics")
    titles = get_list(bible, "previous_work", "titles")

    with open(args.script, encoding="utf-8") as f:
        text = f.read()
    lines = [line for line in text.splitlines() if line.strip()]
    title = lines[0].strip() if lines else ""
    body = text.lower()
    words = re.findall(r"\S+", text)
    hook = first_sentence(" ".join(lines[1:])) if len(lines) > 1 else ""
    hook_words = len(re.findall(r"\S+", hook))

    problems = []
    for phrase in banned:
        if phrase and phrase.lower() in body:
            suggestion = f" Try a preferred phrase instead: {preferred[0]!r}." if preferred else ""
            problems.append(f"Banned phrase found: {phrase!r}.{suggestion}")
    for topic in topics:
        if topic and topic.lower() in body:
            problems.append(f"Topic already used: {topic!r}")
    for old_title in titles:
        if old_title and title and old_title.lower() == title.lower():
            problems.append(f"Title already used: {old_title!r}")
    if args.timeline:
        with open(args.timeline, encoding="utf-8") as f:
            clips = [line.strip() for line in f if line.strip()]
        for i in range(1, len(clips)):
            if clips[i] == clips[i - 1]:
                problems.append(f"Segment {i} repeats clip {clips[i]!r} back-to-back")
    if args.caption:
        with open(args.caption, encoding="utf-8") as f:
            caption = f.read().strip()
        if caption and not caption.endswith("?"):
            problems.append("Caption does not end with a question")

    warnings = []
    if hook_words > 30:
        warnings.append(f"Hook is long: {hook_words} words. Aim for one short, specific sentence.")
    elif hook and hook_words < 3:
        warnings.append(f"Hook is very short: {hook_words} words.")
    numbers = sorted(set(re.findall(r"\d+(?:[.,]\d+)?\s*(?:million|billion|km|million years)?", text)))
    if numbers:
        warnings.append(f"Numbers to verify before publishing: {', '.join(numbers)}")

    result = "FAIL" if problems else "PASS"
    stats = {
        "words": len(words),
        "reading_minutes": round(len(words) / 150, 1),
        "hook_words": hook_words,
    }
    if args.json:
        print(json.dumps({"result": result, "problems": problems, "warnings": warnings, "stats": stats}, indent=2))
        return 1 if problems else 0

    print("# Check Report")
    print()
    print(f"- Words: {stats['words']} (about {stats['reading_minutes']} minutes at 150 words per minute)")
    print()
    if problems:
        print("## Needs fixing")
        for problem in problems:
            print(f"- {problem}")
        print()
    else:
        print("## Passed")
        print("- No banned phrase found.")
        print("- No repeated topic or title found.")
        if args.timeline:
            print("- No animation repeated back-to-back.")
        if args.caption:
            print("- Caption ends with a question.")
        print()
    if warnings:
        print("## Warnings (do not change the result on their own)")
        for warning in warnings:
            print(f"- {warning}")
        print()
    print(f"## Result: {result}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
