#!/bin/bash
cd "/Users/mini/dancinlab/anima/.claude/worktrees/h1410-g6-fals-depth"
export CKPT="/Users/mini/dancinlab/anima/state/g6-deep-mouth-ladder/ckpts/clm303_L8_d3020.clm"
exec /Users/mini/.hx/bin/hexa run "/Users/mini/dancinlab/anima/.claude/worktrees/h1410-g6-fals-depth/state/1410_g6_fals_vs_conv_depth/g6_fals_depth_probe.hexa"
