#!/bin/sh

tmux split-window -h ". venv/bin/activate && python ./s.py"
tmux split-window -h ". venv/bin/activate && python ./m.py"
tmux select-layout even-horizontal
. venv/bin/activate && python ./m.py
