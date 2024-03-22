#!/bin/bash

# Define the ROS distribution
ROS_DISTRO="noetic"  # Replace with your ROS distribution if different

# Move to home
cd ~

# Clone repository and change branch
git clone https://github.com/Nicola-Taddei/OpenRobotGPT.git && cd OpenRobotGPT && git checkout sim && cd ..

# Create the Catkin workspace directory
mkdir -p ~/catkin_ws/src

# Navigate to the Catkin workspace directory
cd ~/catkin_ws

# Source ROS setup script
source /opt/ros/noetic/setup.bash

# Initialize the Catkin workspace
catkin_make

# Copy ROS package inside working directory
cp -r ../OpenRobotGPT/src/openrobotgpt src

# Make the ros python file executable
chmod +x ../OpenRobotGPT/src/openrobotgpt/openrobotgpt.py

# Build the Catkin workspace
catkin_make

# Source the setup file to set up the ROS environment
source devel/setup.bash

# Print a message indicating successful setup
echo "ROS workspace setup complete."

# Run a command that keeps the container running
tail -f /dev/null
