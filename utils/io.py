import bpy

import os
import json

from ..constants import COMMAND_FILENAME_PREFIX, STORAGE_MACROS_DIR

from typing import Union

def get_text_data(name: str):
    _name = COMMAND_FILENAME_PREFIX + name
    if _name in bpy.data.texts:
        return bpy.data.texts[_name]

    return None


def get_or_create_text_data(name: str):
    _name = COMMAND_FILENAME_PREFIX + name
    if _name in bpy.data.texts:
        return bpy.data.texts[_name]

    return bpy.data.texts.new(_name)


def add_to_text_data(name: str, data: str):
    text_data = get_or_create_text_data(name)
    text_data.write(f"{data}\n")


def read_from_text_data(name: str):
    text_data = get_text_data(name)
    texts = []
    for line in text_data.lines:
        texts.append(line.body)

    return "\n".join(texts)


def write_to_storage(name: str, data: str):
    path = f"{STORAGE_MACROS_DIR}/{name}.py"

    if not os.path.exists(STORAGE_MACROS_DIR):
        os.makedirs(STORAGE_MACROS_DIR)

    with open(path, "w") as f:
        f.write(data)


def read_from_storage(name: str) -> Union[str, None]:
    path = f"{STORAGE_MACROS_DIR}/{name}.py"

    if not os.path.exists(path):
        return None

    with open(path) as f:
        return f.read()

def save_json(path:str, data:dict):
    json_string = json.dumps(data, indent=2)
    