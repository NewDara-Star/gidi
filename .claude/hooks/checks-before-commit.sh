#!/bin/sh
# CLAUDE.md, "Nothing is claimed without proof": before any git commit or push Claude makes in gidi or gidi-game,
# the checks run on the checkout the command acts on (repo.sh). A failure blocks it (exit 2) and the output goes
# back to Claude to fix. A check that can't run blocks too: a check that quietly doesn't happen is no check.
input=$(cat)
cmd=$(printf "%s" "$input" | jq -r '.tool_input.command // ""')
case "$cmd" in
  *"git commit"*|*"git push"*) ;;
  *) exit 0 ;;
esac
. "$(dirname "$0")/repo.sh"
repo_of "$cmd"
[ -z "$repo" ] && exit 0
out=$(run_checks "$repo" "$kind") || { printf "Blocked: the checks fail in %s. Fix what they found before committing; never loosen a check to pass it (CLAUDE.md).\n%s\n" "$repo" "$out" | tail -40 >&2; exit 2; }
exit 0
