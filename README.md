# Real-Time Object Detection and Tracking using ROS2 & Gazebo

## Overview
This project implements a real-time object detection and tracking system using a simulated TurtleBot3 robot in Gazebo. The robot captures live camera data and processes it using OpenCV to detect and track colored objects (Red, Green, Blue) in real time.

The system integrates:
- ROS2 (communication)
- Gazebo (simulation)
- OpenCV (computer vision)

---

## Features
- Real-time object detection using color segmentation
- Detection of multiple objects simultaneously
- Frame-by-frame tracking as the robot moves
- Bounding box visualization with labels
- Interactive robot control using keyboard

---

## Tech Stack
- ROS2 (Humble)
- Gazebo Simulator
- Python
- OpenCV
- TurtleBot3

---

## Setup & Running the Project

### Step 1 — Launch Gazebo Simulation

```bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
- This starts the simulation environment with the TurtleBot3 robot.

### Step 2 — Spawn Objects in Environment

# RED
```bash
echo "<sdf version='1.6'><model name='red'><static>true</static><link name='l'><visual name='v'><geometry><box><size>1 1 1</size></box></geometry><material><ambient>1 0 0 1</ambient></material></visual></link></model></sdf>" | ros2 run gazebo_ros spawn_entity.py -entity red -stdin -x 1 -y 0 -z 0.5


# GREEN
- "echo "<sdf version='1.6'><model name='green'><static>true</static><link name='l'><visual name='v'><geometry><box><size>1 1 1</size></box></geometry><material><ambient>0 1 0 1</ambient></material></visual></link></model></sdf>" | ros2 run gazebo_ros spawn_entity.py -entity green -stdin -x -1 -y 1 -z 0.5"

# BLUE
- "echo "<sdf version='1.6'><model name='blue'><static>true</static><link name='l'><visual name='v'><geometry><box><size>1 1 1</size></box></geometry><material><ambient>0 0 1 1</ambient></material></visual></link></model></sdf>" | ros2 run gazebo_ros spawn_entity.py -entity blue -stdin -x 1 -y 2 -z 0.5"

- These commands spawn colored objects into the simulation.

### Step 3 — Run Detection Node

```bash
- cd ~/turtlebot3_ws
- source install/setup.bash
- ros2 run object_tracking detect_final

- This starts the object detection system using OpenCV.

### Step 4 — Control the Robot

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

- Use keyboard controls to move the robot and observe real-time detection.

---

### How It Works
- The robot camera publishes images to /camera/image_raw
- A ROS2 node subscribes to the image topic
- Images are converted using CvBridge
- OpenCV processes each frame:
- Convert to HSV color space
- Apply color thresholding
- Detect contours
- Draw bounding boxes
- Objects are continuously detected as the robot moves
