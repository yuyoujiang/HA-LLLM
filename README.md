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
docker run --runtime nvidia -dt --network host --volume /home/seeed/reComputer/jetson-containers/data:/data --name ollama dustynv/ollama:r35.4.1
```

```bash
docker exec ollama /bin/ollama run llama3
```







