#!/bin/sh
# CLAUDE.md, "Search before saying or building" (owner, 31 Oct: "we need to add a rule that has you searching the code
# or searching the repo before you tell me things"). On every message from the owner, the reminder; what holds a new
# code file is checked-before-commit.sh, and the push review catches a second copy.
echo "Search before saying or building: before saying how anything in Gidi works or is done, proposing an idea, or writing new code, run python3 ~/gidi/scripts/find.py <words> and answer from what it found (file:line), or say it found nothing. A miss that existed: add its words to decisions/WORDS.md."
exit 0
