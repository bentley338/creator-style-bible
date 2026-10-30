#!/usr/bin/env python3
"""Check a timeline file for consecutive repeats.

Usage: python3 check_no_consecutive_repeat.py timeline.txt
Format: one clip name per line, in playback order.
Exit 0 if no consecutive repeat, exit 1 if a repeat is found.
This script reads only the file given. It sends nothing anywhere.
"""
import sys

def main(path):
    with open(path, encoding="utf-8") as f:
        clips = [line.strip() for line in f if line.strip()]
    repeats = []
    for i in range(1, len(clips)):
        if clips[i] == clips[i - 1]:
            repeats.append((i, clips[i]))
    if repeats:
        print(f"FAIL: {len(repeats)} consecutive repeat(s) found")
        for idx, name in repeats:
            print(f"  segment {idx} repeats {name}")
        return 1
    print(f"PASS: {len(clips)} segments, no consecutive repeat")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_no_consecutive_repeat.py timeline.txt")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
