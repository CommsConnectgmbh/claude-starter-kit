#!/usr/bin/env bash
export PS1=
clear
sleep 0.6
printf '\033[1;36m~/my-saas\033[0m $ '
sleep 0.5
cmd="claude -p '/council Ship my half-built feature to ten users now — or finish it first?'"
for ((i=0; i<${#cmd}; i++)); do printf '%s' "${cmd:$i:1}"; sleep 0.028; done
sleep 0.5
printf '\n'
sleep 0.9
printf '\n'
while IFS= read -r line; do
  printf '%s\n' "$line"
  if [ -z "$line" ]; then sleep 0.12; else sleep 0.24; fi
done < /tmp/council_answer_en.txt
sleep 1.8
