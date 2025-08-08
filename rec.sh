#!/bin/bash
#
# Requires: pip install asciinema asciinema-gif-generator
#
set -euo pipefail

do_with_log() {
    echo "=== Executing: $*" >&2
    "$@"
}

test "$#" -gt 0 || {
    echo "Usage: rec.sh COMMAND"
    exit 1
}

outfile="${outfile:-rec.gif}"

do_with_log asciinema rec --rows 24 --cols 32 -t "ALGCHESS" --overwrite -c "$*" rec.cast
do_with_log agg --font-size 36 rec.cast "$outfile"
