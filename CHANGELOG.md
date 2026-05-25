# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-25

### Added
- Initial public release.
- Skill: `council` — 5-role decision-making framework (Visionär, Kritiker, Kreativer, Skeptiker, Logiker).
- Agent: `legal-de` — German legal research with mandatory source citation and § 2 RDG disclaimer.
- Agent: `tax-de` — German tax research with mandatory source citation and § 2 StBerG disclaimer.
- Script: `scripts/sanitize-dotclaude.sh` — pattern-based scanner for personal data in `~/.claude/`.
- Script: `install.sh` — interactive installer with per-component prompts and diff-before-overwrite.
- Templates: `CLAUDE.example.md` and a worked `templates/memory/` example.
- Docs: 5-part documentation (getting started, memory system, skills vs agents, third-party, naming).
- Example: `examples/council-publish-decision.md` showing real council output structure.
- CI: shellcheck on the sanitizer and installer.
- Standard OSS hygiene: `LICENSE` (MIT), `SECURITY.md`, `CONTRIBUTING.md`, `.gitignore`.

[Unreleased]: https://github.com/CommsConnectgmbh/claude-starter-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/CommsConnectgmbh/claude-starter-kit/releases/tag/v0.1.0
