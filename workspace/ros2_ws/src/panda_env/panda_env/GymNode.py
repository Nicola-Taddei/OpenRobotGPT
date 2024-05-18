import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node
import time

from robotgpt_interfaces.msg import StateReward, Action, State, ObjectStatesRequest, ObjectStates, ObjectPose, TrajCompletionMsg, EECommandsM
from robotgpt_interfaces.srv import EECommands, Trajectory, ObjectStatesR
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState

import gym_example
import gymnasium
import numpy as np
import threading
from queue import Queue

class PandaEnvROSNode(Node):
    def __init__(self):
        super().__init__('panda_env_node')

        self.env = gymnasium.make('PandaEnv-v0')

        self.SERVICE_TIMEOUT = 60
        client_cb_group = MutuallyExclusiveCallbackGroup()
        completion_cb_group = MutuallyExclusiveCallbackGroup()
        service_group = ReentrantCallbackGroup()
        timer_group = ReentrantCallbackGroup()

        #publisher for environment state
        self.curr_state = None
        self.state_pub = self.create_publisher(JointState, '/current_position', 10)
        timer_period = 1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback, timer_group)
        print("--------- state pub created -------")


        # Client for robot movement
        self.move_client = self.create_client(Trajectory, 'traj', callback_group=client_cb_group)
        while not self.move_client.wait_for_service(timeout_sec=self.SERVICE_TIMEOUT):
            self.get_logger().info('move service not available, waiting again...')
        self.req = Trajectory.Request()
        print("--------- movement sub created -------")

        #Action service
        #Service to be called by the API or the Agent to step the environment
        # self.action_service = self.create_service(EECommands, 'trajectory_execution', self.step_callback, callback_group=service_group)
        self.action_sub = self.create_subscription(EECommandsM, 'trajectory_execution', self.step_callback, 10, callback_group=service_group)
        self.initial_object_states = self.create_service(ObjectStatesR, '/panda_env/InitialObjectStates', self.InObj_callback, callback_group=service_group)

        # Perception
        # Object states pusblisher
        self.ObjectStatesPublisher = self.create_publisher(ObjectStates, '/panda_env/ObjectStates', 1)

        # Trajectory completion
        self.trajCompletionPub = self.create_publisher(TrajCompletionMsg, 'traj_completion', 10, callback_group=completion_cb_group)

        self.executing_trajectory = False
        self.end_task = False
        self.lock = threading.Lock()
        self.request_queue = Queue()
        self.height_map = []

    def InObj_callback(self, request, response):
        objStates = self.env.getObjStates()
        response.objects = objStates.keys()
        states = []
        for state in objStates.values():
            op = ObjectPose()
            op.pose = state
            states.append(op)
        response.states = states
        return response


    def timer_callback(self):
        #timer to publish the current state of the robot end effector
        # print("spinning")
        if self.curr_state is not None:
            state_msg = State(state=self.curr_state)
            # self.state_pub.publish(state_msg)
    
    def _traj_generation(self, goal_position, gripper_state, end_task):
        request = Trajectory.Request()
        print("[INFO] endt task = ", end_task)
        self.end_task = end_task
        joint_names, joint_states_np = self.env.get_joint_states()
        joint_states = joint_states_np.tolist()
        request.current_position.name = joint_names
        request.current_position.position = joint_states[0]
        request.current_position.velocity = joint_states[1]
        request.ending_position = goal_position
        request.gripper_state = gripper_state
        future = self.move_client.call_async(request)
        future.add_done_callback(self._traj_generation_callback)

    def _traj_generation_callback(self, future):
        if future.result() is not None:
            result = future.result()
            self._handle_trajectory(result.completion_flag, result.plan)
            with self.lock:
                self.executing_trajectory = False  # Mark trajectory execution as completed
                # Signal trajectory completion to the API node
                msg = TrajCompletionMsg()
                msg.flag = True
                print("Starting to publish trajectory completion message")
                self.trajCompletionPub.publish(msg)
                print("Trajectory completion message published")
                if not self.request_queue.empty():
                    # Process next request in the queue
                    position, gripper, end_task = self.request_queue.get()
                    self._traj_generation(position, gripper, end_task)
                    
        else:
            self.get_logger().error('Failed to get trajectory')
            with self.lock:
                self.executing_trajectory = False  # Mark trajectory execution as completed
                # Signal trajectory completion to the API node

    def _handle_trajectory(self, done, plan):
        print("Starting trajectory")
        # curr_state = traj[-1,0:7]
        # get setpoints from plan
        t = 0
        for step in plan.points:
            # print("step")
            # We change the content of time_from_start, so that it now contains the timestep
            delta_t = step.time_from_start - t
            t = step.time_from_start
            step.time_from_start = delta_t

            next_state, _, done, _, _ = self.env.step((plan.joint_names,step))
            self.env.render()
            self.curr_state = next_state[0:8]
        
        if self.end_task == True:
            objStates = self.env.getObjStates()
            msg = ObjectStates()
            msg.objects = objStates.keys()
            states = []
            for state in objStates.values():
                op = ObjectPose()
                op.pose = state
                states.append(op)
            msg.states = states
            self.ObjectStatesPublisher.publish(msg)
            print("[INFO] published message")
            print(msg)

    def reset(self):
        print("Initialising the env .....")
        state, info = self.env.reset()
        self.curr_state = state[0:8]
        self.env.render()
        joint_names, joint_state_np = self.env.get_joint_states()
        state_msg = JointState()
        state_msg.header.stamp = self.get_clock().now().to_msg()
        state_msg.name = joint_names
        state_msg.position = joint_state_np[0,:]
        state_msg.velocity = joint_state_np[1,:]
        state_msg.effort = joint_state_np[2,:]
        print(state_msg)
        self.state_pub.publish(state_msg)
    
    def step_callback(self, msg):
        position = msg.target_state
        gripper = msg.pick_or_place
        end_task = msg.end_task
        with self.lock:
            if self.executing_trajectory:
                # Another trajectory is already in progress, queue the request
                self.request_queue.put((position, gripper, end_task))
                return True

            # Mark trajectory execution as in progress
            self.executing_trajectory = True
        self._traj_generation(position, gripper, end_task)
        # response.completion_flag = True
        return True

def main(args=None):
    #prova
    rclpy.init(args=args)
    panda_env_node = PandaEnvROSNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(panda_env_node)
    panda_env_node.reset()
    executor.spin()
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    panda_env_node.env.close()
    panda_env_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
