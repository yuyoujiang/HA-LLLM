import requests
import json



class HA:
    def __init__(self) -> None:
        self.interest_entity = ['fan', 'light']
        self.ha_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwZTFiMmU0NjlkYTk0ZDIzYTE1OTQwNzU2ZTRiYTkzNCIsImlhdCI6MTcxODU3MDkyMywiZXhwIjoyMDMzOTMwOTIzfQ.8fOrO_1xiK_hog2MrOMtXFz-Ok5j_Ms5jgqdzhvPxo0"
        self.ha_url = "http://192.168.49.120:8123/api/"
        self.headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json"
        }
    

    def voice_assistant(self, prompt):
        url = self.ha_url + "conversation/process"
        data = {
            "text": prompt,
            "agent_id":"981527753ec1971e8ad4487e21323ab4"
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            speech = response_data['response']['speech']['plain']['speech']
            speech = speech.split('\n')[0]
            return speech
        else:
            print(f"Failed to call voice assistant. Status code: {response.status_code}")
            return None

    def get_entity_states(self, target_entity=None):
        url = self.ha_url + "states"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()

            rst_entity = []
            if target_entity is None:
                for entity in data:
                    for itst in self.interest_entity:
                        if itst in entity["entity_id"]:
                            rst_entity.append(entity)
            else:
                for entity in data:
                    if target_entity == entity["entity_id"]:
                        rst_entity.append(entity)
                        break
            
            with open('response.json', 'w', encoding='utf-8') as f:
                json.dump(rst_entity, f, ensure_ascii=False, indent=4)
            print("JSON data has been saved to response.json")
        else:
            print(f"Failed to get data. Status code: {response.status_code}")

    def get_services(self):
        url = self.ha_url + "services"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            filename = "ha_service.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"JSON data has been saved to {filename}")
        else:
            print(f"Failed to get data. Status code: {response.status_code}")

    def template(self, data=None):
        url = self.ha_url + "template"
        if data is None:
            data = "It is {{ now() }}!"
        data = {"template": data}
        print(data)
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Failed to get data. Status code: {response.status_code}")
            print(response.text)




if __name__ == "__main__":
    ha = HA()
    ha.voice_assistant("turn off the light")


