"""
Utility functions for data processing.
"""
import os
import json

def join_json_files_in_directory(directory="."):
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    data = []
    for json_file in json_files:
        with open(os.path.join(directory, json_file), "r") as file:
            file_data = json.load(file)
            data.extend(file_data)
    return data

def index_list_on_attribute(raw_data: list[dict], index_attr: str):
    indexed_data = {}
    for datum in raw_data:
        key = datum[index_attr]
        if not indexed_data.get(key):
            indexed_data[key] = {}
        for attr, value in datum.items():
            indexed_data[key][attr] = value
    return indexed_data