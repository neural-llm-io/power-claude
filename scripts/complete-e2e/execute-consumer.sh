#!/bin/sh
exec python3 "$(dirname "$0")/execute-consumer.py" "$@"
