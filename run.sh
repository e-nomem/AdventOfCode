#!/bin/bash
set -euo pipefail

YEAR=2019
if [[ "$#" -eq 3 ]]; then
    YEAR=$1
    shift
fi

printf -v DAY '%02d' ${1:-1}
SOLUTION=${2:-1}

if [[ ! -f "$YEAR/day_$DAY/solution$SOLUTION.py" ]]; then
    echo "[ERROR] Unable to find $YEAR/day_$DAY/solution$SOLUTION.py" >&2
    exit 1
fi

exec python3 -m ${YEAR}.day_${DAY}.solution${SOLUTION}
