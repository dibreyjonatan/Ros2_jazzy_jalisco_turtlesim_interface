# TURTLESIM INTERFACE 

*overview*
> This is a Graphical user interface written in python using PyQt5 framework to control turtles from the turtlesim package.This project is a demonstration of the use of Graphical user interfaces in robotics.

### Dependencies used 
- ROS2 Jazzy Jalisco 
- Python 3.12.3
- PyQt5 5.15.10
- Ubuntu 24.04.01
- Qt Designer 

## HOW TO RUN THE INTERFACE 
1. Build wrokspace
```
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```
2. Add project to the workspace
```
cd ~/ros2_ws/src
git clone https://github.com/dibreyjonatan/Ros2_jazzy_jalisco_turtlesim_interface.git
cd -
colcon build 
```

3. Run the interface
```
source install/setup.bash
ros2 run turtlesim_interface show_gui
```

## Results of the project

![demo_execution](ressource/turtlesim_interface.gif)

