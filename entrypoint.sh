#!/bin/sh
ARGS=""
if [ "$SERVER" = "true" ]; then ARGS="$ARGS --server"; fi
if [ -n "$HOST" ]; then ARGS="$ARGS --host $HOST"; fi
if [ -n "$PORT" ]; then ARGS="$ARGS --port $PORT"; fi
if [ -n "$URL" ]; then ARGS="$ARGS --url $URL"; fi
if [ -n "$RANDOM" ]; then ARGS="$ARGS --random $RANDOM"; fi
if [ -n "$ALL_URLS" ]; then ARGS="$ARGS --all-urls $ALL_URLS"; fi
if [ -n "$CONFIG" ]; then ARGS="$ARGS --config $CONFIG"; fi
if [ -n "$PROXY" ]; then ARGS="$ARGS --proxy $PROXY"; fi
if [ "$ENABLE_PROXY" = "true" ]; then ARGS="$ARGS --enable-proxy"; fi
if [ "$DISABLE_PROXY" = "true" ]; then ARGS="$ARGS --disable-proxy"; fi
if [ -n "$COVER" ]; then ARGS="$ARGS --cover $COVER"; fi
if [ -n "$ENCODE" ]; then ARGS="$ARGS --encode $ENCODE"; fi
if [ -n "$QUALITY" ]; then ARGS="$ARGS --quality $QUALITY"; fi

python /app/main.py $ARGS
