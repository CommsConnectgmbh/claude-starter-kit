#!/usr/bin/env bash
# Der Befehl ist echt, die Antwort ist verbatim die reale Ausgabe eines
# vorherigen `claude -p '/council …'`-Laufs — nur in lesbarem Tempo abgespielt.
export PS1=
clear
sleep 0.6
printf '\033[1;36m~/mein-saas\033[0m $ '
sleep 0.5
cmd="claude -p '/council SaaS-Feature erst fertig bauen oder sofort an zehn Nutzer geben?'"
for ((i=0; i<${#cmd}; i++)); do printf '%s' "${cmd:$i:1}"; sleep 0.03; done
sleep 0.5
printf '\n'
sleep 0.9
printf '\n'
while IFS= read -r line; do
  printf '%s\n' "$line"
  if [ -z "$line" ]; then sleep 0.12; else sleep 0.24; fi
done < /tmp/council_answer.txt
sleep 1.8
