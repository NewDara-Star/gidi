#!/bin/sh
# The owner's two switches for away mode (owner, 28 Oct, at 21:26, after the night rule held a prompt while they were
# up: "an I'm here switch and a goodnight switch"). Runs on every message the owner sends.
# "I'm here": away mode stays off, the night hours too, while they keep talking: the switch holds 2 hours from their
# last message in the session they said it in, so if they fall asleep without saying goodnight away mode comes back 2
# hours later (the 28 Oct rule: "if I don't accept a prompt in a given time, the prompt can run"). Written to
# ~/.claude/gidi-here as the time it ends in epoch seconds, then that session's id; away-allow.sh reads the time.
# "goodnight" (or "good night"): the here switch off and away mode on until 06:00 Ireland time, day or night, through
# the away flag ~/.claude/gidi-away that away-allow.sh already reads.
# Each switch is logged to ~/.claude/gidi-away.log, and said back so Claude can tell the owner.
input=$(cat)
here="$HOME/.claude/gidi-here"
flag="$HOME/.claude/gidi-away"
log="$HOME/.claude/gidi-away.log"
now=$(TZ=Europe/Dublin date +%s)
stamp=$(TZ=Europe/Dublin date '+%a %d %b %H:%M')
# Only the owner's own short message is a switch: it starts with the phrase and is 30 letters or fewer ("I'm here
# oooo", "Goodnight fam"). A longer prompt that only quotes the words (the push reviewer reading a commit message,
# pasted text) is not: the first push of this hook let the review's own prompt fire goodnight.
msg=$(printf "%s" "$input" | jq -r '.prompt // ""' | tr '\n' ' ' | sed "s/’/'/g" | tr '[:upper:]' '[:lower:]' \
  | tr -cd "a-z' " | tr -s ' ' | sed 's/^ //; s/ $//')
[ "${#msg}" -gt 30 ] && msg=""
sid=$(printf "%s" "$input" | jq -r '.session_id // ""')
if printf "%s" "$msg" | grep -Eq "^good ?night([^a-z]|$)"; then
  six=$(TZ=Europe/Dublin date -j -f '%Y-%m-%d %H:%M' "$(TZ=Europe/Dublin date +%Y-%m-%d) 06:00" +%s)
  [ "$six" -le "$now" ] && six=$((six + 86400))
  rm -f "$here"
  echo "$six" > "$flag"
  printf "%s  SWITCH goodnight: away until %s\n" "$stamp" "$(TZ=Europe/Dublin date -r "$six" '+%a %H:%M')" >> "$log"
  echo "Goodnight switch: away mode on until $(TZ=Europe/Dublin date -r "$six" '+%a %H:%M') (Ireland); the here switch is off."
elif printf "%s" "$msg" | grep -Eq "^(i'?m|i am) here([^a-z]|$)"; then
  rm -f "$flag"
  printf "%s\n%s\n" $((now + 7200)) "$sid" > "$here"
  printf "%s  SWITCH here: away off while the owner talks (2 h from each message)\n" "$stamp" >> "$log"
  echo "Here switch: away mode off while the owner keeps talking, 2 hours from each message; goodnight turns it back on."
elif [ -f "$here" ]; then
  until=$(head -1 "$here" | tr -dc 0-9)
  if [ -n "$until" ] && [ "$until" -gt "$now" ]; then
    # renewed only by the session the owner said it in: the push reviewer's own prompts must not keep it on
    [ -n "$sid" ] && [ "$(sed -n 2p "$here")" = "$sid" ] && printf "%s\n%s\n" $((now + 7200)) "$sid" > "$here"
  else
    rm -f "$here"
  fi
fi
exit 0
