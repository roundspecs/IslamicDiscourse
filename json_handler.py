import json
from constants import FILE_NAME

def get_nodes():
    with open(FILE_NAME) as f:
        data = json.load(f)
    return {node["id"]: node for node in data["nodes"]}

def update_nodes(nodes):
    with open(FILE_NAME, "w") as f:
        json.dump({"nodes": list(nodes.values())}, f, indent=4)