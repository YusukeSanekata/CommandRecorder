import bpy
import os
import json
from typing import Union
from ..state import state
from ..constants import (
    METADATA_FILENAME_PREFIX,
    REGION_GLOBAL,
    REGION_LOCAL,
    STORAGE_MACROS_DIR,
)


def to_dict(data: str):
    return json.loads(data)


def to_json(data: dict):
    return json.dumps(data)


def get_local_metadata(name: str):
    _name = METADATA_FILENAME_PREFIX + name
    if _name in bpy.data.texts:
        return bpy.data.texts[_name]

    return None


def create_local_metadata(name: str):
    _name = METADATA_FILENAME_PREFIX + name
    macro = bpy.data.texts.new(_name)
    return macro


def get_or_create_local_metadata(name: str):
    macro = get_local_metadata(name)

    if macro is not None:
        return macro

    return create_local_metadata(name)


def write_to_local_metadata(name: str, data: dict):
    text_data = get_or_create_local_metadata(name)
    text_data.clear()
    text_data.write(to_json(data))


def read_from_local_metadata(name: str) -> Union[dict, None]:
    text_data = get_local_metadata(name)

    if text_data is None:
        return None

    texts = []
    for line in text_data.lines:
        texts.append(line.body)
    text = "\n".join(texts)

    return to_dict(text)


def remove_local_metadata(name: str):
    macro = get_local_metadata(name)
    bpy.data.texts.remove(macro)


def rename_local_metadata(old_name: str, new_name: str):
    macro = get_local_metadata(old_name)
    macro.name = METADATA_FILENAME_PREFIX + new_name


def write_to_global_metadata(name: str, data: dict):
    path = f"{STORAGE_MACROS_DIR}/{METADATA_FILENAME_PREFIX}{name}.py"

    if not os.path.exists(STORAGE_MACROS_DIR):
        os.makedirs(STORAGE_MACROS_DIR)

    with open(path, "w") as f:
        f.write(to_json(data))

    state["global_metadata_caches"][name] = data


def read_from_global_metadata(name: str, update=False) -> Union[dict, None]:
    path = f"{STORAGE_MACROS_DIR}/{METADATA_FILENAME_PREFIX}{name}.py"

    if not update and name in state["global_metadata_caches"]:
        return state["global_metadata_caches"][name]

    if not os.path.exists(path):
        return None

    with open(path) as f:
        data = to_dict(f.read())
        state["global_metadata_caches"][name] = data

    return data


def remove_global_metadata(name: str):
    path = f"{STORAGE_MACROS_DIR}/{METADATA_FILENAME_PREFIX}{name}.py"
    if os.path.exists(path):
        os.remove(path)


def rename_global_metadata(old_name: str, new_name: str):
    path = f"{STORAGE_MACROS_DIR}/{METADATA_FILENAME_PREFIX}{old_name}.py"
    new_path = f"{STORAGE_MACROS_DIR}/{METADATA_FILENAME_PREFIX}{new_name}.py"
    os.rename(path, new_path)


def move_metadata_to_global(local_metadata_name: str):
    global_metadata_data = read_from_global_metadata(local_metadata_name, True)
    if global_metadata_data is not None:
        raise ValueError("Already exists!")

    data = read_from_local_metadata(local_metadata_name)
    if data is not None:
        write_to_global_metadata(local_metadata_name, data)
        remove_local_metadata(local_metadata_name)


def move_metadata_to_local(global_metadata_name: str):
    local_macro_data = read_from_local_metadata(global_metadata_name)
    if local_macro_data is not None:
        raise ValueError("Already exists!")

    data = read_from_global_metadata(global_metadata_name)
    if data is not None:
        write_to_local_metadata(global_metadata_name, data)
        remove_global_metadata(global_metadata_name)


def read_metadata(name: str, region: str):
    if region == REGION_LOCAL:
        return read_from_local_metadata(name)

    if region == REGION_GLOBAL:
        return read_from_global_metadata(name)


def write_metadata(name: str, data: dict, region: str):
    if region == REGION_LOCAL:
        write_to_local_metadata(name, data)

    if region == REGION_GLOBAL:
        write_to_global_metadata(name, data)

