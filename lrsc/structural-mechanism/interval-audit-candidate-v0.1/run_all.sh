#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 build_operator.py
gcc -O3 -std=c11 -Wall -Wextra -o lrsc_interval_search search.c -lm
./lrsc_interval_search channels.bin 10 | tee VERIFICATION_OUTPUT_independent.txt
python3 interval_certificate.py | tee INTERVAL_AUDIT_OUTPUT.txt
