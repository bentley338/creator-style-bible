# Creator Style-Bible

A skill that keeps a creator's style consistent and prevents repeated topics, titles, and animations.

This skill ships with no one's style built in. All style comes from the user's own references, in a single `style-bible.yaml` file they fill in.

## Install

The commands below use the proposed repository `bentley338/creator-style-bible`. They will only work after that repository is created and published.

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
      check_no_consecutive_repeat.py
    examples/
      check-report-example.md
      timeline-example.txt
```

## What is not in this skill

- No style, color, channel name, or reference from any one person as a default.
- No credentials, tokens, API keys, or personal data.
- No claim of passing an AI detector, passing platform moderation, or reaching any viewer numbers.

## License

See `LICENSE`. This project is licensed under MIT.
