# Naming conventions

Conventions matter most for memory files, because the index loads on every conversation and bad names make stale entries invisible.

## Memory file naming

Pattern: `<type>_<topic>.md` in snake_case.

Examples:
- `user_you.md`
- `feedback_no_emojis.md`
- `feedback_test_db_required.md`
- `project_acme_app.md`
- `project_billing_v2_launch.md`
- `reference_grafana_dashboards.md`
- `reference_team_handles.md`

Why this pattern:
- The prefix groups related entries when you `ls`.
- The topic word is searchable — `grep -l acme memory/` finds all entries about Acme.
- Underscores avoid shell-escaping headaches.

## Skill naming

Pattern: `<verb-or-noun>-<scope>` in kebab-case.

Examples:
- `council` (single verb, decision-making)
- `code-review` (verb + scope)
- `when-stuck` (situational trigger)
- `root-cause-tracing` (technique)
- `compliance-audit` (verb + scope)

Avoid:
- `my-skill`, `helper`, `utils` — meaningless
- Underscores — Claude's docs use kebab-case
- Capital letters — case sensitivity bites on some filesystems

## Agent naming

Pattern: `<domain>-<region-or-spec>` in kebab-case.

Examples:
- `legal-de` (legal, German)
- `tax-de` (tax, German)
- `security-review` (domain only)
- `code-reviewer` (role)

Region suffixes (`-de`, `-us`, `-eu`) help when the same domain has wildly different rules per jurisdiction. Don't add them when the domain is universal.

## Slash commands

If a skill is `user-invocable: true`, the slash command equals the skill name. Pick the skill name so `/foo` makes sense at the prompt.

Good:
- `/council`
- `/review`
- `/verify`
- `/run`

Bad:
- `/strategicDecisionEvaluator` — too long, camelCase
- `/r` — collides with too many things

## Frontmatter `description` field

This is the most important text in any skill or agent — Claude uses it to decide whether to invoke. Write it like a trigger document:

1. Lead with the use case in plain English.
2. Include 3-5 example trigger phrases.
3. List negative cases ("NOT for X") if the scope is ambiguous.
4. End with cross-references to sibling skills/agents if relevant.

Bad description:
```yaml
description: Helps with code review
```

Good description:
```yaml
description: "Review code changes for bugs, style violations, and security issues before commit. Trigger phrases: 'review this', 'check my code', 'find bugs', 'audit the diff'. NOT for design review (use frontend-design skill) or for full architectural review (use a planning agent)."
```

The good version costs 10 seconds to write and saves Claude from picking the wrong tool a dozen times a week.
