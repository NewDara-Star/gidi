#!/bin/sh
# The owner's timeline (28 Oct: "check what the current time is every time you are sending a message or every time
# you receive a message"). On a message from the owner it tells Claude the time and logs it; on Claude's reply (Stop)
# it logs the time. Log: ~/gidi-journal/TIMELINE.md, outside the repos. Ireland time, which the owner lives by.
input=$(cat)
event=$(printf "%s" "$input" | jq -r '.hook_event_name // ""')
stamp=$(TZ=Europe/Dublin date '+%a %d %b %Y %H:%M:%S %Z')
mkdir -p "$HOME/gidi-journal"
case "$event" in
  UserPromptSubmit)
    printf -- "- %s  received\n" "$stamp" >> "$HOME/gidi-journal/TIMELINE.md"
    echo "Time now (Ireland): $stamp. Message received.";;
  Stop)
    [ "$(printf "%s" "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
    printf -- "- %s  sent\n" "$stamp" >> "$HOME/gidi-journal/TIMELINE.md";;
esac
exit 0
