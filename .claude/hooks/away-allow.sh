#!/bin/sh
# Away mode (owner, 28 Oct: "if I don't accept a prompt in a given time, the prompt can run and no wait"). Runs only
# when Claude Code is about to ask for permission. While the owner is away it answers for them, so no helper sits on a
# prompt for hours; while they are here it says nothing and the prompt shows as normal.
# Away = asleep, 21:00-06:00 Ireland time, every day; or the away flag, ~/.claude/gidi-away, holding the time it ends
# (written when the owner says they are away, as their shifts move: "my work is not specifically weekdays").
# While away: downloads are refused ("the downloads should be locked when I'm away"), and so are deletes and history
# rewrites, which can't be taken back; everything else, the GTA folder too ("that works too"), is allowed.
# Every answer is logged to ~/.claude/gidi-away.log for the morning.
input=$(cat)
log="$HOME/.claude/gidi-away.log"
flag="$HOME/.claude/gidi-away"
now=$(TZ=Europe/Dublin date +%s)
hour=${GIDI_AWAY_TEST_HOUR:-$(TZ=Europe/Dublin date +%H)}  # the test hour is for testing this script only
away=""
case "$hour" in 21|22|23|00|01|02|03|04|05) away="asleep";; esac
if [ -z "$away" ] && [ -f "$flag" ]; then
  until=$(head -1 "$flag" | tr -dc 0-9)
  if [ -n "$until" ] && [ "$until" -gt "$now" ]; then away="away flag"; else rm -f "$flag"; fi
fi
[ -z "$away" ] && exit 0

tool=$(printf "%s" "$input" | jq -r '.tool_name // ""')
what=$(printf "%s" "$input" | jq -r '.tool_input.command // .tool_input.url // .tool_input.file_path // (.tool_input | tostring)' | tr '\n' ' ' | cut -c1-300)
stamp=$(TZ=Europe/Dublin date '+%a %d %b %H:%M')
held=""
if [ "$tool" = "Bash" ]; then
  if printf "%s" "$what" | grep -Eq '(^|[^A-Za-z_-])(curl|wget|aria2c|yt-dlp|scp|sftp|ftp|huggingface-cli|hf download|git clone|git lfs (pull|fetch)|gh release download|gh repo clone|(pip3?|uv pip|npm|pnpm|yarn|bun|brew|gem|cargo) (install|add)|softwareupdate)([^A-Za-z_-]|$)'; then
    held="a download: downloads wait for the owner"
  elif printf "%s" "$what" | grep -Eq '(^|[^A-Za-z_-])(rm|rmdir|trash|shred|srm)( |$)|git (reset --hard|clean|push (-f|--force)|branch -D|filter-branch|filter-repo)|gh (repo|release) delete|find .* -delete'; then
    held="a delete or history rewrite: those wait for the owner"
  fi
fi
case "$tool" in mcp__*meshy_*) held="Meshy spends credits: that waits for the owner";; esac
if [ -n "$held" ]; then
  printf "%s  REFUSED (%s)  %s  %s  [%s]\n" "$stamp" "$away" "$tool" "$what" "$held" >> "$log"
  jq -n --arg m "Away mode ($away): $held. Note it as not run, and carry on with other work." \
    '{hookSpecificOutput:{hookEventName:"PermissionRequest",decision:{behavior:"deny",message:$m,interrupt:false}}}'
  exit 0
fi
printf "%s  allowed (%s)  %s  %s\n" "$stamp" "$away" "$tool" "$what" >> "$log"
jq -n '{hookSpecificOutput:{hookEventName:"PermissionRequest",decision:{behavior:"allow"}}}'
