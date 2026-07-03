# council-demo

`../council-demo.gif` zeigt eine **echte** `/council`-Antwort.

- `answer.txt` ist die verbatim-Ausgabe eines realen Laufs von
  `claude -p '/council SaaS-Feature erst fertig bauen oder sofort an zehn Nutzer geben?'`
  — nichts daran ist erfunden.
- `record.sh` tippt den echten Befehl und spielt diese reale Antwort in
  lesbarem Tempo ab (Claude denkt in Wirklichkeit ~1 Min; im GIF gekürzt).

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
