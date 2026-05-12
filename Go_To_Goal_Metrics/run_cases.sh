#!/bin/bash
source install/setup.bash

function prepare_sim() {
    echo "Resetting Turtlesim..."
    ros2 service call /reset std_srvs/srv/Empty {}
    sleep 1
    echo "Drawing Markers (X roja en meta, punto verde en inicio)..."
    python3 draw_markers.py
    sleep 1
}

prepare_sim
echo "Running Case A..."
ros2 run go_to_goal_metrics turtle_go_to_goal_metrics --ros-args \
    -p x_goal:=8.0 -p y_goal:=8.0 -p k_linear:=0.8 -p k_angular:=3.0 -p case_name:=case_A

prepare_sim
echo "Running Case B..."
ros2 run go_to_goal_metrics turtle_go_to_goal_metrics --ros-args \
    -p x_goal:=8.0 -p y_goal:=8.0 -p k_linear:=1.0 -p k_angular:=4.0 -p case_name:=case_B

prepare_sim
echo "Running Case C..."
ros2 run go_to_goal_metrics turtle_go_to_goal_metrics --ros-args \
    -p x_goal:=8.0 -p y_goal:=8.0 -p k_linear:=1.5 -p k_angular:=6.0 -p case_name:=case_C

echo "All cases finished."
