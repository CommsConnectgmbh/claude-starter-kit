# council-demo

`../council-demo.gif` (Deutsch) und `../council-demo-en.gif` (English) zeigen
jeweils eine **echte** `/council`-Antwort.

- `answer.txt` / `answer-en.txt` sind die verbatim-Ausgaben realer Läufe von
  `claude -p '/council …'` — nichts daran ist erfunden.
- `record.sh` / `record-en.sh` tippen den echten Befehl und spielen die reale
  Antwort in lesbarem Tempo ab (Claude denkt real ~1 Min; im GIF gekürzt).

Neu aufnehmen:

```bash
# einmalig
brew install asciinema agg
# echte Antwort neu erzeugen (optional)
claude -p '/council <deine Frage>' > answer.txt
# aufnehmen + zu GIF konvertieren
asciinema rec council.cast --window-size 100x30 --overwrite -c "bash record.sh"
agg --font-size 15 council.cast ../council-demo.gif
```
