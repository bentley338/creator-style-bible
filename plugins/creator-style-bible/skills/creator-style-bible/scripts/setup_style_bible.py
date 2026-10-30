#!/usr/bin/env python3
"""Create a style-bible.yaml from the template, in under a minute.

Usage:
  python3 setup_style_bible.py --out style-bible.yaml --name "My Channel" --language English
  python3 setup_style_bible.py --out style-bible.yaml   # interactive, asks 7 questions

This script only writes the file you name. It sends nothing anywhere.
"""
import argparse
import pathlib
import sys


QUESTIONS = [
    ("creator_name", "Creator or channel name"),
    ("primary_color", "Main color, for example #F5E9D3 (leave blank if none)"),
    ("language", "Language, for example English"),
    ("tone", "Tone, for example plain and specific"),
    ("hook_pattern", "Hook pattern, for example one specific sentence at the start"),
    ("banned_phrases", "Banned phrases, comma separated (leave blank if none)"),
    ("previous_topics", "Topics already used, comma separated (leave blank if none)"),
]


def split_list(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def build(answers):
    banned = split_list(answers.get("banned_phrases", ""))
    topics = split_list(answers.get("previous_topics", ""))
    lines = [
        f'creator_name: "{answers.get("creator_name", "")}"',
        "channels:",
        '  primary: ""',
        "  others: []",
        "",
        "visual:",
        f'  primary_color: "{answers.get("primary_color", "")}"',
        '  accent_color: ""',
        '  outline: ""',
        '  font: ""',
        '  style: ""',
        "  banned_visuals:",
        '    - "watermark"',
        "",
        "voice_and_language:",
        f'  language: "{answers.get("language", "")}"',
        f'  tone: "{answers.get("tone", "")}"',
        '  narration_voice: ""',
        f'  hook_pattern: "{answers.get("hook_pattern", "")}"',
        '  script_structure: ""',
        '  caption_ending: "a comment-prompting question"',
        "",
        "phrases:",
        "  banned:",
    ]
    lines += [f'    - "{phrase}"' for phrase in banned] or ['    - ""']
    lines += ["  preferred:", '    - ""', "", "previous_work:", "  topics:"]
    lines += [f'    - "{topic}"' for topic in topics] or ['    - ""']
    lines += [
        "  titles:",
        '    - ""',
        "  animations_used:",
        '    - ""',
        "",
        "animation_rules:",
        "  consecutive_repeat: false",
        '  rule: "As soon as one clip finishes, move to the next animation that matches the audio and speech at that moment."',
        "",
        "publishing_rules:",
        '  mode: "check-first"',
        '  note: "Hand over for review first, publish only after the user says OK, unless there is an explicit instruction otherwise."',
        "",
        "working_rules:",
        "  backup_each_stage: true",
        "  never_overwrite_single_copy: true",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Create a style-bible.yaml.")
    parser.add_argument("--out", required=True)
    aliases = {"creator_name": ["--name"], "banned_phrases": ["--banned-phrases"], "previous_topics": ["--previous-topics"], "primary_color": ["--primary-color"], "hook_pattern": ["--hook-pattern"]}
    for key, _ in QUESTIONS:
        parser.add_argument(f"--{key}", *aliases.get(key, []), default="")
    args = parser.parse_args()
    answers = {key: getattr(args, key) for key, _ in QUESTIONS}
    if not any(answers.values()):
        for key, question in QUESTIONS:
            try:
                answers[key] = input(f"{question}: ").strip()
            except EOFError:
                break
    out = pathlib.Path(args.out)
    if out.exists():
        print(f"Refusing to overwrite existing file: {out}", file=sys.stderr)
        return 2
    out.write_text(build(answers), encoding="utf-8")
    print(f"Wrote {out}")
    print("Next: fill in the remaining fields, then run check_style.py against your script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
