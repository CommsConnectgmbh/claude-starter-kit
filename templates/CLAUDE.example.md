# {{ProjectName}}

One-line description of what this project is and who uses it.

## Stack

- Language: {{e.g. TypeScript / Python / Swift}}
- Framework: {{e.g. Next.js 14 / FastAPI / SwiftUI}}
- Database: {{e.g. Postgres on Supabase / SQLite / none}}
- Deploy target: {{e.g. Vercel / Fly.io / TestFlight}}

## Run / build / test

```bash
# Dev
{{e.g. npm run dev}}

# Build
{{e.g. npm run build}}

# Test
{{e.g. npm test}}
```

## Project conventions

Short rules that override Claude Code defaults for this project. Add only things that aren't obvious from reading the code.

Examples:
- "Never mock the database in integration tests — use the local Supabase stack."
- "All user-facing strings live in `i18n/de.json` — never hardcode."
- "Migrations are in `supabase/migrations/`. After editing schema, run `npm run db:types` to regenerate types."

## Things NOT to do

Counter-rules that catch the most common wrong moves. Be specific.

Examples:
- "Don't run `npm install` — this repo uses pnpm."
- "Don't bypass the pre-commit hook with `--no-verify`. If it fails, fix the underlying issue."
- "Don't write to `dist/` — that's a build artifact, regenerate via `npm run build`."

## Where things live

| What | Where |
|---|---|
| API routes | `app/api/` |
| UI components | `components/` |
| Background jobs | `workers/` |
| Secrets template | `.env.example` |

## Open questions / known gotchas

- {{Anything weird about this codebase that a new contributor would trip over}}
