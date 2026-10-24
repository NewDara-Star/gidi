#!/bin/sh
# CLAUDE.md, "Nothing is claimed without proof": a commit that changes code or the map carries a `Checked:`
# paragraph: what was run or looked at, and what it printed or showed, in numbers where there are numbers. What was
# judged by eye says so ("by eye: ..."), and what wasn't checked says that too. The review before push reads it
# against the diff. Checked against the commit command itself, since the message is in it (-m, a heredoc, or -F).
input=$(cat)
cmd=$(printf "%s" "$input" | jq -r '.tool_input.command // ""')
case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac
case "$cmd" in
  *--amend*--no-edit*) exit 0 ;;
esac
. "$(dirname "$0")/repo.sh"
repo_of "$cmd"
[ -z "$repo" ] && exit 0
case "$kind" in
  gidi) code="scripts schema map map-stamps web .claude" ;;
  gidi-game) code="tools Source Config .claude" ;;
  *) exit 0 ;;
esac
# Everything changed, staged or not: `git add -A && git commit` stages after this runs.
changed=$(cd "$repo" && git status --porcelain -- $code | head -1)
[ -z "$changed" ] && exit 0
printf "%s" "$cmd" | grep -q "Checked:" && exit 0
file=$(printf "%s" "$cmd" | sed -n 's/.*-F[= ]\([^ -][^ ]*\).*/\1/p' | head -1)
[ -n "$file" ] && [ "$file" != "-" ] && [ -f "$file" ] && grep -q "Checked:" "$file" && exit 0
echo "Blocked: this commit changes code or the map ($code) and its message has no Checked: paragraph. Say what you ran or looked at and what it printed or showed, in numbers; say \"by eye\" for what you judged by eye, and say what you didn't check (CLAUDE.md, \"Nothing is claimed without proof\"). If you haven't checked it, check it first." >&2
exit 2
