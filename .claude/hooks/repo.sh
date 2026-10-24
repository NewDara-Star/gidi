#!/bin/sh
# Shared by the hooks (CLAUDE.md, "Nothing is claimed without proof"). Work happens in worktrees
# (~/gidi-worktrees/<dir>) and in gidi-game, so the repo a git command acts on is read from the command itself:
# the last `cd <dir>` before the git call, or `git -C <dir>`; failing that, the session's own folder.
# Sets $repo (that checkout's top folder) and $kind (gidi, gidi-game, or other).
repo_of() {
  cmd=$1
  dir=$(printf "%s\n" "$cmd" | sed -n 's/.*git -C \([^ ;&|]*\).*/\1/p' | head -1)
  [ -z "$dir" ] && dir=$(printf "%s\n" "$cmd" | sed 's/git .*//' | grep -oE '(^|[;&|( ])cd +[^ ;&|]+' | tail -1 | sed -E 's/^[;&|( ]?cd +//')
  [ -z "$dir" ] && dir=$(printf "%s" "$input" | jq -r '.cwd // ""')
  [ -z "$dir" ] && dir=$CLAUDE_PROJECT_DIR
  case "$dir" in "~"*) dir="$HOME${dir#\~}" ;; esac
  dir=$(eval printf "%s" "$dir")    # $HOME and quotes, as the shell would read them
  repo=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)
  url=$(git -C "$repo" remote get-url origin 2>/dev/null)
  case "$url" in
    *gidi-game*) kind=gidi-game ;;
    *gidi*) kind=gidi ;;
    *) kind=other ;;
  esac
}

# The checks every commit, push and stop runs, for one checkout. Prints what failed and returns 1, or returns 0.
# A check that can't run is a failure, never a pass.
PY=$HOME/.venvs/gidi/bin/python
run_checks() {
  r=$1; k=$2
  if [ "$k" = gidi ]; then
    [ -x "$PY" ] || { echo "The checks can't run: no $PY."; return 1; }
    out=$(cd "$r" && "$PY" scripts/check_rules.py 2>&1) || { echo "check_rules.py fails (a rule with no row in CHECKS.md, or a check that fails):"; printf "%s\n" "$out" | grep -v '^GAP\|^PASS' | tail -20; return 1; }
    out=$(cd "$r" && "$PY" scripts/check_map.py map 2>&1) || { echo "check_map.py map fails:"; printf "%s\n" "$out" | grep -v '^TODO' | tail -20; return 1; }
    inv=$(mktemp -d)
    out=$(cd "$r" && "$PY" scripts/inventory.py --untracked --out "$inv" 2>&1) || { echo "inventory.py can't run:"; printf "%s\n" "$out" | tail -10; rm -rf "${inv:?}"; return 1; }
    # A line this change adds that names a file of ours that exists nowhere: the name is wrong, or the file was never
    # committed. Lines already there are in SUSPECTS.md; a line that says the file is lost or not here is honest.
    bad=$(cd "$r" && "$PY" - "$inv/inventory.json" <<'EOF'
import json, re, subprocess, sys
broken = json.load(open(sys.argv[1]))['broken']
diff = subprocess.run(['git', 'diff', '-U0', 'origin/main', '--'], capture_output=True, text=True).stdout
added, f = {}, None
for line in diff.splitlines():
    if line.startswith('+++ '):
        f = line[6:] if line.startswith('+++ b/') else None
    elif f and line.startswith('+') and not line.startswith('+++'):
        added.setdefault(f, []).append(line[1:])
new = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True).stdout
for f in new.split():
    try:
        added[f] = open(f, encoding='utf-8').read().splitlines()
    except (UnicodeDecodeError, OSError):
        pass
HONEST = re.compile(r'never committed|lost|not in this repo|isn.t in this repo|exists nowhere|deleted|removed', re.I)
for f, lines in added.items():
    for p in broken.get('gidi:' + f, []):
        if any(p in l and not HONEST.search(l) for l in lines):
            print(f'{f} names {p}, which exists nowhere')
EOF
)
    rm -rf "${inv:?}"
    [ -n "$bad" ] && { echo "A changed file names a file that doesn't exist (fix the name, commit the file, or mark it lost):"; printf "%s\n" "$bad"; return 1; }
  elif [ "$k" = gidi-game ]; then
    out=$(cd "$r" && python3 tools/kit_fields.py --map="$HOME/gidi" 2>&1) || { echo "tools/kit_fields.py fails (a builder reads a field the map can't say):"; printf "%s\n" "$out" | tail -20; return 1; }
  fi
  return 0
}
