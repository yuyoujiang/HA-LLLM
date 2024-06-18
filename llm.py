#!/usr/bin/env python3

import requests


class OllamaAPIAgent:
    def __init__(self, url="http://192.168.49.124:11434"):
        self.url = url
        self.debug = False

    def request(self, model, prompt):
        url = self.url + "/api/generate"
        data = {
            "model": model, 
            "prompt": prompt, 
            "stream": False,
            "options": {
                "num_predict": 100,
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            if self.debug:
                print("Response:", response.json())
            return response.json()
        else:
            print(f"Failed to call ollama. Status code: {response.status_code}")
            return None

if __name__ == "__main__":
    ollama = OllamaAPIAgent()
    ollama.request('home-3b', 'turn on the light')