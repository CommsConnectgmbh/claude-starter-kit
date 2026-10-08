# council-demo

`../council-demo.gif` (German) and `../council-demo-en.gif` (English) each show
an **actual** `/council` response.

- `answer.txt` / `answer-en.txt` contain verbatim output from real runs of
  `claude -p '/council …'`. None of it is invented.
- `record.sh` / `record-en.sh` type the actual command and replay the real
  response at a readable pace (Claude's actual thinking takes ~1 min; shortened in the GIF).

To record again:

```bash
# one-time setup
brew install asciinema agg
# generate a new real response (optional)
claude -p '/council <your question>' > answer.txt
# record and convert to GIF
asciinema rec council.cast --window-size 100x30 --overwrite -c "bash record.sh"
agg --font-size 15 council.cast ../council-demo.gif
```
