#!/bin/sh

# Create all panes
tmux split-window -h ". venv/bin/activate && python ./s.py"
tmux split-window -h ". venv/bin/activate && python ./m.py"

# Apply even-horizontal layout first
tmux select-layout even-horizontal

# Manually resize panes
tmux resize-pane -t 0 -x 25%  # Left pane to 20%
tmux resize-pane -t 2 -x 25%  # Right pane to 20%
# Middle pane automatically gets 60%

tmux select-pane -t 1
. venv/bin/activate && python ./m.py
