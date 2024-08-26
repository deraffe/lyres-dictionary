#!/bin/sh
for morph in data/morphs-*.json; do
  jq -r '.[] | (.key) + ": " + (.gloss|if type=="array" then join("; ") else . end)' < "$morph"
done
