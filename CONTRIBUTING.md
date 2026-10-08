# Contributing

Thanks for taking a look. This kit grows through additions drawn from real work.

**Found a bug?** Open an [issue](../../issues/new/choose) with the command, error message, and operating system.

**Have an idea or a skill to share?** Open an issue or submit a PR. Small, focused contributions are better than large, untested ones.

## Contribute a skill or agent

- A skill is a folder under `skills/<name>/` containing a `SKILL.md`. Use the existing skills as examples.
- An agent is a single `.md` file under `agents/` with frontmatter (`name`, `description`, `tools`).
- Use English by default, write plainly, and do not invent facts. Domain agents for law or tax must require sources and include a disclaimer.
- Keep changes additive: only rework existing material when necessary.

## Before opening a PR

- Run `bash -n install.sh` and check any changed `.sh` files for syntax errors.
- If you reference a new file in the README, make sure it exists.
- No secrets, real keys, or personal data. Use `.env` or placeholders.

The license is MIT. Your contributions use the same license.
