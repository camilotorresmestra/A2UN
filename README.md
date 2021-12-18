# A2UN

## Instructions
- Download this branch into your catkin_ws
- add src folder to your own src folder
- build your catkin_ws or execute autorun.sh to build and launch the node
- Use the html files under robout_gui_bridge to remotely control the robot. 

This work is based on the roslibjs prackage that uses the Websocket protocol, messages are published and listened as JSON packages on the localhost:9090 port.

## Robot control
- autorun.sh starts the cell_listener.py rosservice node, this publishes the machine status onto the rostopic vmd_model/status as a std
- to shutdown the automatic control, kill cell_listener node
- To publish a command, publish to rostopic vmd_model/cell_command (std_msgs/Int32). (You can modify the cell codes and coordinates modifyng the cell_listener.py source file, but you¿d have to recompile and build again, but don't worry since autorun.sh does it anyways)
- The robot should start moving and messages start being published in vmd_model/status
- The robot will stop and wait for sdv confirmation, publish and latch a std_msgs/Bool type message to rostopic vmd_model/sdv_pos and set its value to true. You are simulating a signal sent froma sensor that detects if SDV is in loading position.
- The robot will start to simulate the unloading, and then it will return to HOME postion
