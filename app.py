#!/usr/bin/env python3

import requests
from flask import Flask, request, jsonify
from llm import OllamaAPIAgent
from ha import HA


class HomeAgent:
    def __init__(self, name):
        self.app = Flask(name)
        self.setup_routes()

        self.ollama = OllamaAPIAgent()
        self.ha = HA()

        # A word to describe the tool's functionality
        # TODO： The dictionary should be read from the configuration file
        self.tools = {
            "home-control": {
                "calling_fun": self.ha.voice_assistant,
                "args": {}
                },
            "video-search": None, 
            "network-search": None, 
            "just-chat": {
                "calling_fun": self.ollama.request,
                "args": {"model": "llama3"}
                }
        }

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return "Welcome to the Home Agent!"

        @self.app.route('/process', methods=['POST'])
        def process():
            # step1. get user input.
            user_input = request.get_json()
            prompt = user_input["prompt"]
            print(f"User input : {prompt}")

            # step2. based on user input, select the appropriate model.
            # `agent-llama3` is a llama3 with system prompt,
            # check here for more infermation.
            intent_cls = self.ollama.request(model='agent-llama3', prompt=prompt)
            intent_cls = intent_cls["response"]
            print(f"Intent classification: {intent_cls}")

            # step3. select tools based on user intent.
            tool = self.select_tool(intent_cls)
            print(f"Selected tool: {tool}")
            
            # step4. use the appropriate tools to respond to user needs and return processing results
            if tool is not None:
                rst = tool["calling_fun"](prompt=prompt, **tool["args"])
                if "response" in rst:
                    rst = rst["response"]
                    print(f"result: {rst} ")
                    return jsonify({"response": rst})
            else:
                return jsonify({"response": f"Invalid tool:{tool}"})
            return jsonify({"response": rst})

    
    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)
            
    def select_tool(self, model_description):
        if model_description in self.tools:
            return self.tools[model_description]
        else:
            print(f"ERROR: The corresponding model could not be found: {model_description}")
            return None


if __name__ == "__main__":
    agent = HomeAgent(__name__)
    agent.run()



