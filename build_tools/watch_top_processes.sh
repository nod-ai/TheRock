#!/bin/bash
# Reports top processes periodically. Meant to be run in the background before
# starting a build with high latency tasks so that some progress can be seen.

while true; do
  echo ""
  echo ":::: TOP PROCESSES $(date) ::::"
  ps aux | sort -nrk 3,3 | head -n 5
  sleep 30
  echo ""
done
