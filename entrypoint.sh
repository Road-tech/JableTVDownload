#!/bin/sh
ARGS=""
if [ -n "$URL" ]; then ARGS="$ARGS --url $URL"; fi
if [ -n "$RANDOM" ]; then ARGS="$ARGS --random $RANDOM"; fi
if [ -n "$ALL_URLS" ]; then ARGS="$ARGS --all-urls $ALL_URLS"; fi
if [ -n "$PROXY" ]; then ARGS="$ARGS --proxy $PROXY"; fi
python /app/main.py $ARGS
