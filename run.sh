#!/bin/bash
set -euo pipefail

YEAR=2019
if [[ "$#" -eq 3 ]]; then
    YEAR=$1
    shift
fi

printf -v DAY '%02d' ${1:-1}
SOLUTION=${2:-1}


run() {
    local fname
    fname="$1/day_$2/solution$3.py"
    if [[ ! -f "$fname" ]]; then
        echo "[ERROR] Unable to find $fname" >&2
        exit 1
    else
        echo "[INFO] Running $fname"
    fi
    exec python3 -m $1.day_$2.solution$3
}

run "$YEAR" "$DAY" "$SOLUTION"
