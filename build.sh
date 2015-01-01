#!/bin/bash

if [ ! -d "venv" ]; then
    echo "venv dir does not exist, creating one"
    python3 -m venv venv
    echo "sourcing venv activate"
    source venv/bin/activate
    echo "installing requirements"
    pip3 install commonmark
    echo "done venv setup"
    /bin/bash $0
    exit
fi

echo "starting build"
echo "sourcing venv activate"
source venv/bin/activate
echo "building"
python3 build.py
echo "waiting for more changes, ctrl-c to close"
while inotifywait -e modify,close,move,create,delete posts; do
    echo "building"
    python3 build.py
done
