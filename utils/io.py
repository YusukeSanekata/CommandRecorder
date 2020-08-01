import bpy

import os
import re
import json

from ..state import state
from ..constants import COMMAND_FILENAME_PREFIX, STORAGE_MACROS_DIR

from typing import Union


def get_local_macro(name: str):
    _name = COMMAND_FILENAME_PREFIX + name
    if _name in bpy.data.texts:
        return bpy.data.texts[_name]

    return None

def create_local_macro(name:str):
    _name = COMMAND_FILENAME_PREFIX + name
    return bpy.data.texts.new(_name)

def get_or_create_local_macro(name: str):
    macro = get_local_macro(name)

    if macro is not None:
        return macro

    return create_local_macro(name)


def add_to_local_macro(name: str, data: str):
    text_data = get_or_create_local_macro(name)
    text_data.write(f"{data}\n")


def read_from_local_macro(name: str):
    text_data = get_local_macro(name)

    if text_data is None:
        return None

    texts = []
    for line in text_data.lines:
        texts.append(line.body)

    return "\n".join(texts)


def list_local_macro_names():
    names = bpy.data.texts.keys()
    filtered = list(
        filter(lambda key: re.search(COMMAND_FILENAME_PREFIX, key) is not None, names)
    )
    modified = list(
        map(lambda name: str(name).replace(COMMAND_FILENAME_PREFIX, ""), filtered)
    )
    return modified


def list_global_macro_names(update=False):
    global global_macro_names

    if state["global_macro_names"] is None or update:
        names = os.listdir(STORAGE_MACROS_DIR)
        modified = list(map(lambda name: str(name).replace(".py", ""), names))
        state["global_macro_names"] = modified
        return modified

    return state["global_macro_names"]


def write_to_global_macro(name: str, data: str):
    path = f"{STORAGE_MACROS_DIR}/{name}.py"

    if not os.path.exists(STORAGE_MACROS_DIR):
        os.makedirs(STORAGE_MACROS_DIR)

    with open(path, "w") as f:
        f.write(data)


def read_from_global_macro(name: str) -> Union[str, None]:
    path = f"{STORAGE_MACROS_DIR}/{name}.py"

    if not os.path.exists(path):
        return None

    with open(path) as f:
        return f.read()


def __save_json(path: str, data: dict):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def __read_json(path: str):
    if not os.path.exists(path):
        return None

    with open(path) as f:
        object = json.load(f)

    return object
