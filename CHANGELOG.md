# Changelog
## 1.2.0 - 2026-10-30

- Checker now reports word count, reading time, hook length, and numbers to verify as warnings that do not change the PASS or FAIL result.
- Checker now supports --caption for the closing question check and --json for machine-readable output.
- New setup wizard scripts/setup_style_bible.py: creates a style-bible.yaml in under a minute and refuses to overwrite an existing file.
- SKILL.md now includes a 5-minute effective workflow and a "what makes a check effective" section.


## 1.1.0 - 2026-10-30

- New automated checker `scripts/check_style.py`: banned phrases, repeated topics and titles, and back-to-back animation repeats, with a Markdown report and exit code 0 for pass, 1 for fail.
- New runnable demo in `examples/demo/`: a style-bible, a script, and a timeline that intentionally fail on all four checks.
- New tests in `scripts/tests/` for the checker.
- SKILL.md now starts with a 30-second demo and a troubleshooting section.
- Plugin version bumped to 1.1.0.

## 1.0.0 - 2026-10-29

- First installable release.
- Claude Code marketplace structure: `.claude-plugin/marketplace.json` and `plugins/creator-style-bible/.claude-plugin/plugin.json`.
- SKILL.md with `name` and `description` frontmatter, following the Agent Skills specification.
- Empty `style-bible.yaml` template, checklist, and an example clearly labeled as an example.
- Script `check_no_consecutive_repeat.py` to check for back-to-back animation repetition.
- README with 4 install methods, a local install script, and CI validation.
- No credentials, tokens, or personal data in this repository.

