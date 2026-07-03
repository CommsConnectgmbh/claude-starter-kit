# Mitmachen

Danke, dass du reinschaust. Das Kit lebt von echten Praxis-Ergänzungen.

**Bug gefunden?** Mach ein [Issue](../../issues/new/choose) auf — mit Befehl, Fehlermeldung und OS.

**Idee oder eigener Skill?** Auch ein Issue, oder direkt ein PR. Klein und fokussiert ist besser als groß und ungeprüft.

## Ein Skill/Agent beitragen

- Ein Skill ist ein Ordner unter `skills/<name>/` mit einer `SKILL.md` (siehe die vorhandenen als Vorlage).
- Ein Agent ist eine einzelne `.md` unter `agents/` mit Frontmatter (`name`, `description`, `tools`).
- Deutsch als Default, Klartext, keine erfundenen Fakten. Domain-Agents (Recht/Steuer) immer mit Quellenpflicht + Disclaimer.
- Additiv halten: nichts Bestehendes umbauen, ohne dass es nötig ist.

## Bevor du einen PR aufmachst

- `bash -n install.sh` (und geänderte `.sh`) — keine Syntaxfehler.
- Referenzierst du eine neue Datei im README? Dann muss sie auch existieren.
- Keine Secrets, keine echten Keys, keine Personendaten — alles über `.env`/Platzhalter.

Lizenz ist MIT. Was du beiträgst, steht unter derselben Lizenz.
