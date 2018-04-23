import http.client
import json
import io
import config as cfg


client = http.client.HTTPConnection(cfg.MICROSERVICE_CONNECTION)
headers = {'Content-type': 'application/json'}


def polish(sentence):
    data = {'sentence': sentence}
    json_data = json.dumps(data)
    client.request('POST', '/spolszcz', json_data, headers)

    response = client.getresponse()
    if response.status != 200:
        raise Exception("Connection to polisher failed.")
    polished = response.read().decode()
    return polished


def preprocess_file(input_file, output_file):
    data = json.load(io.open(input_file))
    
    processed_messages = []
    for message in data:
        processed_messages.append({
            "author": message["author"],
             "sentence": polish(message["sentence"])})
    
    with io.open(output_file, 'w') as outfile:
        json.dump(processed_messages, outfile)


if __name__=="__main__":
    #preprocess_file(cfg.DATA_MESSAGES_PATH, cfg.PROCESSED_DATA_OUTPUT_PATH)
    data = json.load(io.open(cfg.PROCESSED_DATA_OUTPUT_PATH))
    
    print(data[0]["sentence"])
