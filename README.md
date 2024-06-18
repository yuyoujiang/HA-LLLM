# HA-LLLM
HomeAssistant + Local LLM



### Prepare the local LLM inference server

For convenience, we deploy `ollama` to `jetson` using [`jetson-examples`](https://github.com/Seeed-Projects/jetson-examples) and use ollama to load the local LLM.

**Step1.** Deploy ollama using the following command:
```bash
pip3 install jetson-examples
reComputer run ollama
exit
```

**Step2.** Run the Docker container in the background:
```bash
sudo docker run --runtime nvidia -dt --network host --volume /home/seeed/reComputer/jetson-containers/data:/data --name ollama dustynv/ollama:r35.4.1
```
**Step3.** Configure the model.

- Download llama3 by ollama:
    ```bash
    sudo docker exec ollama /bin/ollama run llama3
    ```
- Load home-3b :

    ```bash
    # Download home-3b model.
    sudo wget "https://huggingface.co/acon96/Home-3B-v2-GGUF/resolve/main/Home-3B-v2.q4_k_m.gguf?download=true" -O /home/seeed/reComputer/jetson-containers/data/homeassistant/Home-3B-v2.q4_k_m.gguf

    # Create the model profile.
    sudo echo "FROM ./Home-3B-v2.q4_k_m.gguf" > /home/seeed/reComputer/jetson-containers/data/homeassistant/home.mf

    # Build the corresponding OLLAMA model
    sudo docker exec ollama /bin/ollama create home-3b -f /data/homeassistant/home.mf
    ```

- Load `agent-llama3`:

    ```bash
    # Create the model profile.
    sudo vim /home/seeed/reComputer/jetson-containers/data/homeassistant/agent-llama3.mf
    ```
    Copy the contents below to a file and save.
    ```txt
    FROM llama3

    PARAMETER temperature 0.2

    SYSTEM 
    """
    You are a chat assistant named seeed-home. Please select the most appropriate response from the following options based on the user's input and provide the output:[home-control, video-search, network-search, just-chat].
    home-control: If you need to control smart furniture, please select this option.
    video-search: If you need to retrieve relevant information from a video, please select this option.
    network-search: If you need to search for answers to questions via an internet browser, please select this option.
    just-chat: If the user has no other intention and just wants to chat, please select this option.
    Please note, you can only choose one from options [home-control, video-search, network-search, just-chat]  as the output, and do not generate additional content.
    """
    ```

    ```bash
    # Build the corresponding OLLAMA model
    sudo docker exec ollama /bin/ollama create home-3b -f /data/homeassistant/agent-llama3.mf
    ```





```bash
python3 app.py
```


You can use the following script to test the project:
```python
import requests

url = 'http://192.168.49.124:5000/process'

data = {
    "prompt": "Control smart furniture for me to turn on the office light"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
```






