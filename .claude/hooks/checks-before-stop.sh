#!/bin/sh
# CLAUDE.md, "Nothing is claimed without proof": a turn doesn't end on broken checks. When Claude stops with code or
# the map changed but not committed, in any checkout of gidi or gidi-game (the main ones and every worktree), with a
# change in the last 6 hours, the checks run there; a failure sends Claude back to fix them. Only once per stop (stop_hook_active), so it can't
# loop, and never inside the review's own model (GIDI_REVIEW).
input=$(cat)
[ "$(printf "%s" "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
[ -n "$GIDI_REVIEW" ] && exit 0
. "$(dirname "$0")/repo.sh"
fails=""
for main in "$HOME/gidi" "$HOME/gidi-game"; do
  [ -d "$main" ] || continue
  for r in $(git -C "$main" worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p'); do
    [ -d "$r" ] || continue
    # Only code changed in the last 6 hours: this session's work. An old unfinished worktree is listed in
    # decisions/CODEBASE.md for the owner, not checked on every stop (a check that always complains gets ignored).
    recent=$(cd "$r" && git status --porcelain 2>/dev/null | sed 's/^...//; s/.* -> //' | grep -E '^(scripts|schema|map|map-stamps|web|tools|Source|\.claude)/.*\.(py|js|json|sh|html|cpp|h)$' |
      while read -r f; do [ -f "$f" ] && [ "$(stat -f %m "$f")" -gt "$(( $(date +%s) - 21600 ))" ] && echo "$f"; done | head -1)
    [ -z "$recent" ] && continue
    repo_of "cd $r"
    out=$(run_checks "$repo" "$kind") || fails="$fails\n--- $r\n$out"
  done
done
[ -z "$fails" ] && exit 0
printf "Code or the map changed and the checks fail. Fix them before stopping (CLAUDE.md).%b\n" "$fails" | tail -40 >&2
exit 2
