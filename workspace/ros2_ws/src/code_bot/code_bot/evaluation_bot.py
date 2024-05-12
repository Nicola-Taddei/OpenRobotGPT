import rclpy
from rclpy.node import Node
from robotgpt_interfaces.srv import CodeExecution
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from .bots import DecisionBot, CorrectionBot, EvaluationBot, ChatGPT
import pkg_resources
import json
import re
import os
import json

class BotNode(Node):
    def __init__(self):
        super().__init__('bot_node')
        print('Hello from bot_node!')

        # TODO: tune
        self.SERVICE_TIMEOUT = 60
        service_group = MutuallyExclusiveCallbackGroup()

        self.client = self.create_subscription(ObjectStates, 'goal_states', self.evaluation_callback, 10)
        self.evaluation_service = self.create_service(EvaluationCode, 'evaluation_code', self.service_callback, callback_group = service_group)

    def evaluation_callback(self, msg):
        objects = msg.objects
        states = msg.states
        states = [states[i].pose for i in range(len(states))]
        self.objStates = {object:list(state) for object,state in zip(objects, states)}

def main(args=None):
    rclpy.init(args=args)
    node = BotNode()

    def read_json_to_dict(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data
    

    def create_json_from_txt(txt_file, json_file):
        # Open the text file for reading
        with open(txt_file, 'r') as file:
            # Read the content of the text file
            content = file.read().strip()  # Remove any leading/trailing whitespace

        content = content.replace('\n', ' ')
        
        # Construct the JSON object with a fixed role and the content from the text file
        data = {
            "role": "user",
            "content": content
        }
        
        # Open the JSON file for writing
        with open(json_file, 'w') as file:
            # Write the dictionary as a JSON formatted string into the file
            json.dump(data, file, indent=4)

    config_path = "/root/workspace/ros2_ws/install/code_bot/share/code_bot/config/config_bot.json"
    secret_path = os.environ.get("API_KEY_PATH")
    secret_path = "/root/workspace/secrets/api_key.json"
    print(secret_path)
    decision_bot = ChatGPT(config_path, secret_path)
    evaluation_bot = ChatGPT(config_path, secret_path)
    correction_bot = ChatGPT(config_path, secret_path)

    decision_context_json_path="/root/workspace/contexts/decision_context.json"
    decision_context_txt_path="/root/workspace/contexts/decision_context.txt"

    eval_context_json_path="/root/workspace/contexts/evaluation_context.json"
    eval_context_txt_path="/root/workspace/contexts/evaluation_context.txt"

    # create the json file:
    create_json_from_txt(decision_context_txt_path, decision_context_json_path)
    create_json_from_txt(eval_context_txt_path, eval_context_json_path)

    while True:
        task = input("Enter the task: ")

        decision_context = read_json_to_dict(decision_context_json_path)
        decision_bot.set_context([decision_context])
        code = decision_bot.chat(task)

        print("ChatGPT code (raw): \n", code)
        x = input("Press a key to proceed or type 'QUIT' to quit: ")
        if x.strip().upper() == 'QUIT':
            break

        # Clean the code from the overhead
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, code, re.DOTALL)

        if matches:
            code = matches[0]
        else:
            pass

        print("ChatGPT code (cleaned): \n", code)
        x = input("Press a key to proceed or type 'QUIT' to quit: ")
        if x.strip().upper() == 'QUIT':
            break

        evaluation_context = read_json_to_dict(eval_context_json_path)
        evaluation_bot.set_context([evaluation_context])
        evaluation_code = evaluation_bot.chat(code)

        print("ChatGPT evaluation code (raw): \n", evaluation_code)
        x = input("Press a key to proceed or type 'QUIT' to quit: ")
        if x.strip().upper() == 'QUIT':
            break

        # Clean the code from the overhead
        pattern = r"```python(.*?)```"
        evaluation_code_list = re.findall(pattern, evaluation_code, re.DOTALL)
        if evaluation_code_list:
            evaluation_code = evaluation_code_list[0]

        print("ChatGPT evaluation code (cleaned): \n", evaluation_code)
        x = input("Press a key to proceed or type 'QUIT' to quit: ")
        if x.strip().upper() == 'QUIT':
            break

        code_is_working, code_error, eval_error = node.call_service(code, evaluation_code)

        if code_is_working:
            print("WORKING!")
        else:
            print("NOT working!")
            print("Code error: ", code_error)
            print("Evaluation error: ", eval_error)

        x = input("Press a key to proceed or type 'QUIT' to quit: ")
        if x.strip().upper() == 'QUIT':
            break


    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

