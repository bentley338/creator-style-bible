# Contributing

1. Fork the repository and create a branch for your change.
2. Keep the skill generic: no creator's style, channel, or personal data as a default.
3. Add or update a test in `scripts/tests/` for any checker change, and run `python3 -m unittest discover -s scripts/tests -v`.
4. Update `CHANGELOG.md` and the plugin version in `plugins/creator-style-bible/.claude-plugin/plugin.json` when the skill behavior changes.
5. Open a pull request with a short description and the test output.
