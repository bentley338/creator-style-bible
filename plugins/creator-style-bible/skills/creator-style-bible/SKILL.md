---
name: creator-style-bible
description: Check a script, video, title, or caption against the creator's own style-bible and prevent repeated topics, titles, and animations. Use when a creator wants new work to match their previous style and pass a check-first review before publishing.
---

# Creator Style-Bible — A Public Skill Anyone Can Use

This skill keeps a creator's style consistent across scripts, videos, and captions. It ships with no one's style built in. The style always comes from the user's own references, in a single style-bible file they fill in.

## When to use it

Use this skill when the user asks to:
- Check a script, video, title, or caption against their own style.
- Make new work that feels like their previous work, not generic work.
- Prevent repetition: topics, hooks, animations, or visuals already used.
- Prepare a check-first package before publishing.

Do not use this skill to judge someone else's taste, or to force one style onto a different creator.

## Core principles

1. The user's references are the source of truth, not the examples in this skill.
2. If no style-bible file exists, create one from the user's references first. Do not guess their style.
3. Report every violation with an exact location: which sentence, which second, or which file.
4. Apply fixes only after the user agrees, unless they gave an explicit instruction otherwise.
5. Back up every finished stage before moving on. Never overwrite or delete the only copy of a finished file.

## Step 1: Load or create the user's style-bible

Look for the user's style-bible file in this order:
1. `style-bible.yaml` in the user's working folder.
2. `references/style-bible.md` or a similar file they point to.
3. Previous works they sent as references.

If none exists, ask only these 7 questions:
- Main colors, font, and visual style.
- Narration voice and language tone.
- Hook pattern and script structure they normally use.
- Banned phrases and preferred phrases.
- Topics, titles, and animations already used.
- Publishing rule: check-first or publish directly.
- Main platform: YouTube, TikTok, Facebook, or another.

Save the answers to the template in `references/style-bible-template.yaml`. That file belongs to the user, not to this public skill. Never put credentials, tokens, API keys, addresses, or personal data in it.

## Quick start: effective in 5 minutes

1. Create your style-bible in under a minute, without overwriting an existing one:
```
python3 scripts/setup_style_bible.py --out style-bible.yaml --name "My Channel" --language English
```
2. Try the demo to see a failing report before you use your own files:
```
python3 scripts/check_style.py --bible examples/demo/demo-style-bible.yaml --script examples/demo/demo-script.txt --timeline examples/demo/demo-timeline.txt
```
The demo script intentionally contains a banned phrase, a repeated topic, a repeated title, and a back-to-back animation repeat, so the checker exits with FAIL and lists all four. Replace the demo files with your own style-bible and script to get a real report.
3. Use the checker on every new script, before the human review. It is fast, offline, and deterministic: the same inputs always give the same report.

## What makes a check effective

- Check early, not at the end. A banned phrase found in a draft costs one sentence to fix. The same phrase found after rendering costs a whole re-render.
- Fix the highest-cost problem first: repeated topics and back-to-back animation repeats, then banned phrases, then hook and caption polish.
- Do not chase a perfect score. A PASS with warnings about numbers to verify is still a PASS, but those numbers must be verified before publishing.
- Keep the style-bible short. Ten banned phrases you actually use beat fifty phrases you never check.

## Step 2: Check new work against the style-bible

First run the automated checker, then do the human checks below. The checker catches banned phrases, repeated topics and titles, and back-to-back animation repeats. It does not judge visual quality, hook strength, or factual accuracy, so those still need the manual checks.

```
python3 scripts/check_style.py --bible style-bible.yaml --script script.txt --timeline timeline.txt --caption caption.txt --json
```

The `--caption` check fails only when a caption file is given and does not end with a question. The `--json` output is for tools and CI: the same result, problems, warnings, and word count in machine-readable form.

Check these 6 items, one by one, and record the result:

### 1. Visual identity
- Do colors, outline, font, and composition match the style-bible?
- Is there a watermark or production label that is banned?

### 2. Language and tone
- Is the hook strong at the start, specific, and supported by the content?
- Does it contain any banned phrase from the style-bible?
- Does the caption end with a comment-prompting question, if that is the user's rule?

### 3. Facts and numbers
- Does every number and claim have a source, or at least a not-yet-verified flag?
- Do not add new facts without confirmation. Do not claim a duration, file size, or render result before verifying it.

### 4. Topic and title repetition
- Is this topic or title already in the list of previous works?
- If it is, report it as a repetition. Do not silently pass it.

### 5. Animation and visual repetition
- Is any clip or visual repeated back-to-back to cover one narration block?
- The rule: as soon as one clip finishes, move to the next animation that matches the audio and speech at that moment.
- If a clip must be reused, separate it with other clips, change its speed or starting frame, and honestly report it as a spaced repetition, not a new clip.
- To check a clip order, run `scripts/check_no_consecutive_repeat.py` with a timeline file, one clip per line. That script only reads the file given and sends nothing anywhere.

### 6. Publishing rule
- If the user's rule is check-first, hand the package over for review first. Do not publish or upload before the user says OK, unless there is an explicit instruction otherwise.

## Step 3: Report the check result

Deliver the report in this format, short and concrete:
- Passed: the checks that passed, without generic praise.
- Needs fixing: exact location, what violates the style-bible, and a one-sentence fix suggestion.
- Repetition: topics, titles, or animations detected as already used, with the previous work.
- Not yet verified: numbers, claims, durations, or files not yet checked.

Never say the work is finished while the report still has unverified items.

## Step 4: Update the style-bible after approval

After the user approves the new work:
- Add the new topic, title, and animations to the list of previous works.
- Add any new banned or preferred phrases they mentioned.
- Save the old style-bible as a backup before overwriting it.

Do not update the style-bible from work that has not been approved.

## Files produced

For each job, produce at least:
- `check-report.md`: the result of the 6 checks above.
- `style-bible.yaml`: the updated version, only if the user approved it.
- The fixed work, with a backup of the previous version.

## Explicit limits

- This skill contains no style, color, channel name, or reference from any one person as a default. Every example in `references/` is clearly labeled as an example and must be replaced.
- It contains no credentials, tokens, API keys, or personal data.
- It does not claim text passes an AI detector, a video passes platform moderation, or any viewer numbers.
- It does not use copyrighted photos, images, music, or videos as final assets without permission.
- If a visual or video generation tool fails on one beat, report that beat and offer an alternative. Do not silently replace moving animation with a slow zoom on a still photo.

## Troubleshooting

- Checker exits with code 2: an argument is missing or a file path is wrong. Re-check the `--bible`, `--script`, and `--timeline` paths.
- Checker passes but the work still feels off-style: the style-bible is probably too empty. Add the banned phrases and previous topics that actually matter to that creator, then re-run.
- A workflow file cannot be created by the GitHub App: that is a GitHub App permission limit, not a skill bug. The skill itself does not need a workflow file to install or run.

## Status

Version 1.2.0, with an automated checker, a setup wizard, a runnable demo, and tests. Ready for public use once the user fills in their own style-bible and tests it on one real work.
