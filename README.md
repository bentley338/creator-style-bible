# Creator Style-Bible

A skill that keeps a creator's style consistent and prevents repeated topics, titles, and animations.

This skill ships with no one's style built in. All style comes from the user's own references, in a single `style-bible.yaml` file they fill in.

## Try it in 30 seconds

No setup needed to see what a failing check looks like:

```
python3 plugins/creator-style-bible/skills/creator-style-bible/scripts/check_style.py \
  --bible plugins/creator-style-bible/skills/creator-style-bible/examples/demo/demo-style-bible.yaml \
  --script plugins/creator-style-bible/skills/creator-style-bible/examples/demo/demo-script.txt \
  --timeline plugins/creator-style-bible/skills/creator-style-bible/examples/demo/demo-timeline.txt
```

The demo intentionally fails on four points at once: a banned phrase, a repeated topic, a repeated title, and a back-to-back animation repeat. A clean script passes with exit code 0.

## Automated checker

```
python3 scripts/check_style.py --bible style-bible.yaml --script script.txt --timeline timeline.txt --caption caption.txt --json
```

The checker only reads the files you give it. It sends nothing anywhere, asks for no token, and needs no network. It reports word count and reading time, flags long hooks and numbers to verify as warnings, and fails only on banned phrases, repeated topics or titles, back-to-back animation repeats, and a caption without a closing question. Tests live in `scripts/tests/` and run with `python3 -m unittest discover -s scripts/tests -v`.

## Setup in under a minute

```
python3 scripts/setup_style_bible.py --out style-bible.yaml --name "My Channel" --language English
```

The wizard refuses to overwrite an existing style-bible, so running it twice cannot delete your work.

## Install

The commands below use the repository `bentley338/creator-style-bible`.

### Method 1: Plugin marketplace (Claude Code, recommended)

Inside a Claude Code session:

```
/plugin marketplace add bentley338/creator-style-bible
/plugin install creator-style-bible@creator-style-bible-marketplace
```

Then restart Claude Code so the skill loads. The marketplace name comes from `.claude-plugin/marketplace.json`, not from the repository name.

### Method 2: Only this skill, without the plugin

```
npx skills add https://github.com/bentley338/creator-style-bible --skill creator-style-bible
```

This puts the skill in your project's skill folder. If `npx skills` is not available on your machine, use Method 3.

### Method 3: Manual copy

```
git clone https://github.com/bentley338/creator-style-bible.git
cp -r creator-style-bible/plugins/creator-style-bible/skills/creator-style-bible ~/.claude/skills/
```

For Muse, copy the same skill folder to `~/workspace/custom-skills/` instead.

### Method 4: Local install script

```
bash scripts/install.sh
```

This script only copies the skill folder to `~/.claude/skills/creator-style-bible`. It sends nothing anywhere, asks for no token, and changes no other file.

## How to use it after install

1. Copy `plugins/creator-style-bible/skills/creator-style-bible/references/style-bible-template.yaml` to `style-bible.yaml` in your working folder.
2. Fill in the 7 fields with your own references: visual style, voice, hook, banned and preferred phrases, previous work, animation rules, and publishing rules.
3. Ask the agent to run this skill for every new script or video.
4. Read `check-report.md` before publishing. Fix what is reported, then update the style-bible after the work is approved.

## What it checks

- Visual identity: colors, font, outline, watermark.
- Language and tone: hook, banned phrases, caption ending.
- Facts and numbers: verified, or flagged as not yet verified.
- Topic and title repetition.
- Animation repetition: as soon as one clip finishes, move to the next animation that matches the audio. No back-to-back looping of the same clip.
- Publishing rule: check-first by default.

## Repository structure

```
.claude-plugin/marketplace.json
plugins/creator-style-bible/
  .claude-plugin/plugin.json
  skills/creator-style-bible/
    SKILL.md
    references/
      style-bible-template.yaml
      checklist.md
      example-style-bible.md
    scripts/
      check_style.py
      check_no_consecutive_repeat.py
      tests/
    examples/
      check-report-example.md
      timeline-example.txt
      demo/
```

## What is not in this skill

- No style, color, channel name, or reference from any one person as a default.
- No credentials, tokens, API keys, or personal data.
- No claim of passing an AI detector, passing platform moderation, or reaching any viewer numbers.

## License

See `LICENSE`. This project is licensed under MIT.
