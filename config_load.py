def load():
    import json
    with open("config.json","r") as f:
        json_data=f.read()
    return json.loads(json_data)