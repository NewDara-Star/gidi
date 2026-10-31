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
file=$(printf "%s" "$cmd" | sed -n 's/.*-F[= ]\([^ -][^ ]*\).*/\1/p' | head -1)
has() { printf "%s" "$cmd" | grep -q "$1" || { [ -n "$file" ] && [ "$file" != "-" ] && [ -f "$file" ] && grep -q "$1" "$file"; }; }
# CLAUDE.md, "Search before saying or building" (owner, 31 Oct: "we're going to have like two times the same thing in
# the code base"): a commit that adds a new code file says what was searched first (scripts/find.py and its words) and
# what it found, so a second copy of something we have is caught before it goes in.
case "$kind" in
  gidi) newcode="scripts web tests .claude" ;;
  gidi-game) newcode="tools Source Content/Python .claude" ;;
esac
new=$(cd "$repo" && git status --porcelain --untracked-files=all -- $newcode | grep -E '^(A.|\?\?) ' | grep -E '\.(py|sh|js|mjs|html|cpp|h|usf|ush)$' | head -3 | cut -c4-)
if [ -n "$new" ] && ! has "Searched:"; then
  echo "Blocked: this commit adds new code ($(printf "%s" "$new" | tr '\n' ' ')) and its message has no Searched: paragraph. Run python3 ~/gidi/scripts/find.py <words for what it does>, read what exists, and say what you searched and what it found (or that nothing like it exists), so the same thing isn't built twice (CLAUDE.md, \"Search before saying or building\")." >&2
  exit 2
fi
# Everything changed, staged or not: `git add -A && git commit` stages after this runs.
changed=$(cd "$repo" && git status --porcelain -- $code | head -1)
[ -z "$changed" ] && exit 0
has "Checked:" && exit 0
echo "Blocked: this commit changes code or the map ($code) and its message has no Checked: paragraph. Say what you ran or looked at and what it printed or showed, in numbers; say \"by eye\" for what you judged by eye, and say what you didn't check (CLAUDE.md, \"Nothing is claimed without proof\"). If you haven't checked it, check it first." >&2
exit 2
