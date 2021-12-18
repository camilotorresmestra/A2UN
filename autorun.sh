#!/bin/bash
catkin_make
source devel/setup.bash
roslaunch robout_gui_bridge websocket_test.launch
