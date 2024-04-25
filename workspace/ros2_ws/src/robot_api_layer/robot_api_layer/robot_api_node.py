import rclpy
from rclpy.node import Node
import copy
from robotgpt_interfaces.srv import CodeExecution
from robotgpt_interfaces.msg import StateReward, Action, State
from robot_api_layer.PlannerInterface import PlannerInterface
import numpy as np
from geometry_msgs.msg import Point
import time
from collections import deque

class RobotAPINode(Node):

    def __init__(self):
        super().__init__('test_code')
        print("Hello from test_code!")
        #implement argument for chosing between use with chatgpt and use with imitation learning

        #create service for current position
        self.planner = PlannerInterface()
        self.cur_state_sub = self.create_subscription(State, '/panda_env/state', self.state_callback, 10)
        self.cur_state = np.array([0.4315144419670105, -5.4939169533141374e-12, 0.2346152812242508, 1, 0, 0, 0, 0])
        self.EPSILON = 1e-3


        '''
        #Example of trajectory generation, done by chatgpt
        # API available:
        #     - move_to(stateA)
        #     - pick_cube(stateA)
        #     - release_cube(stateA) 

        #test ending point ---
        ending_state = np.array([0.6,0.1,0.05, 1, 0, 0, 0])
        #                  ---

        self.traj = planner.plan_trajectory(self.starting_state, ending_state)
        self.traj = np.vstack((self.traj, planner.pick_cube([0.6,0.1,0.05, 1, 0, 0, 0])))
        self.traj = np.vstack((self.traj, planner.plan_trajectory(ending_state, self.starting_state)))
        '''

        #initialize trajectory list
        self.traj = None
        self.vel_traj = None
        #publisher for point of the trajectory to follow
        self.state_pub = self.create_publisher(Action, 'traj', 20)
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        #chatgpt service
        self.srv = self.create_service(CodeExecution, 'test_code', self.test_callback)

    def move_to(self, final_pose:np.ndarray):
        # final pose must be a numpy array of dimension 7 (3+4)
        traj, vel_traj = self.planner.plan_trajectory(self.cur_state[0:7], final_pose)
        self.traj = traj
        self.vel_traj = vel_traj
        print("mode_to")
        #while np.linalg.norm(self.cur_state - self.traj[-1][0:8]) < self.EPSILON:
        #    pass

    def pick_cube(self, cube_position):
        # cube position is the 3d position of the cube + 4 components
        # that are the quaternion related to the grip orientation
        # in order to pick the cube
        
        traj, vel_traj = self.planner.pick_cube(cube_position)
        self.traj += traj
        self.vel_traj += vel_traj
        print("pick_cube")
        #while np.linalg.norm(self.cur_state - self.traj[-1][:8]) < self.EPSILON:
        #    pass

    def release_cube(self):
        #  cube_position: np array of 7: where and with witch orientation
        #  to release the cube
        traj, vel_traj = self.planner.release_cube(self.cur_state)
        self.traj += traj
        self.vel_traj += vel_traj
        print("release_cube")
        #while np.linalg.norm(self.cur_state - self.traj[-1][:8]) < self.EPSILON:
        #    pass

    def timer_callback(self):
        if self.traj is not None:
            if len(self.traj) > 0:

                action = self.traj[0]
                self.traj.popleft()

                vel_action = self.vel_traj[0]
                self.vel_traj.popleft()
                print("vel action", vel_action)
                print("action", action)
                traj_msg = Action(action=action, vel=vel_action)
                print(traj_msg)
                self.state_pub.publish(traj_msg)
                print("[Info] publishing  ", traj_msg)
                self.get_logger().info('Publishing: "%s"' % traj_msg)

    def state_callback(self, msg):
        self.curr_state =  msg.state


    def test_callback(self, request, response):
        print("received code")
        code = request.code
        evaluation_code = request.evaluation_code

        # Create a dictionary to hold the local scope
        scope = {'self': self}

        except_occurred = False
        completion_flag = False
        code_except = ""
        eval_except = ""

        # Define wrapper functions for your instance methods in the scope
        #scope['move_to'] = lambda pos: self.move_to(pos)
        #scope['pick_cube'] = lambda pos: self.pick_cube(pos)

        # Execute the received code
        try:
            exec(code, globals(), scope)
            if 'execution_func' in scope:
                # Convert the `execution_func` in the scope to a method of self
                from types import MethodType
                execution_func = MethodType(scope['execution_func'], self)
                execution_func()
        except Exception as e:
            except_occurred = True
            code_except = str(e)
            print("Code exception: ", code_except)

        # Execute the evaluation code
        try:
            exec(evaluation_code, globals(), scope)
            if 'evaluation_func' in scope:
                evaluation_func = MethodType(scope['evaluation_func'], self)
                completion_flag = evaluation_func()
        except Exception as e:
            except_occurred = True
            eval_except = str(e)
            print("Eval exception: ", eval_except)

        response.completion_flag = completion_flag and not except_occurred
        response.code_except = code_except
        response.eval_except = eval_except

        return response
    

def main(args=None):
    rclpy.init(args=args)
    node = RobotAPINode()

    # ***** DEBUG *****
    #node.move_to(np.array([0.6, 0.1, 0.05, 1, 0, 0, 0]))
    #node.pick_cube(np.array([0.6, 0.1, 0.05, 1, 0, 0, 0]))
    # *****************

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

