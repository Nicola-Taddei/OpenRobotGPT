#!/bin/bash

# Define the ROS distribution
ROS_DISTRO="noetic"  # Replace with your ROS distribution if different

# Clone repo and change branch
git clone https://github.com/Nicola-Taddei/OpenRobotGPT.git
git checkout sim
cd OpenRobotGPT
git checkout sim
cd ..

# Create the Catkin workspace directory
mkdir -p ~/catkin_ws/src

# Navigate to the Catkin workspace directory
cd ~/catkin_ws

# Initialize the Catkin workspace
catkin_init_workspace src

# Navigate back to the workspace root
cd ..

# Copy ROS package inside working directory
cp -r ../OpenRobotGPT/src/openrobotgpt src

# Make the ros python file executable
chmod +x src/openrobotgpt/openrobotgpt.py

# Build the Catkin workspace
catkin_make

# Source the setup file to set up the ROS environment
source devel/setup.bash

# Print a message indicating successful setup
echo "ROS workspace setup complete."
