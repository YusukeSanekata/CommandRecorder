import enum
import bpy

import os
import re
import json
from pprint import pprint

from .metadata import (
    create_local_metadata,
    get_local_metadata,
    move_metadata_to_global,
    move_metadata_to_local,
    read_from_global_metadata,
    read_from_local_metadata,
    read_metadata,
    remove_global_metadata,
    remove_local_metadata,
    rename_local_metadata,
    write_metadata,
    write_to_global_metadata,
    write_to_local_metadata,
)
from ..state import set_local_active, state
from ..constants import (
    COMMAND_FILENAME_PREFIX,
    METADATA_FILENAME_PREFIX,
    REGION_GLOBAL,
    REGION_LOCAL,
    STORAGE_MACROS_DIR,
)

from typing import List, Union


def get_local_macro(name: str):
    _name = COMMAND_FILENAME_PREFIX + name
    if _name in bpy.data.texts:
        return bpy.data.texts[_name]

    return None


def create_local_macro(name: str):
    _name = COMMAND_FILENAME_PREFIX + name
    text_data = bpy.data.texts.new(_name)
    macro_name = str(text_data.name).replace(COMMAND_FILENAME_PREFIX, "")
    set_local_active(macro_name)
    return text_data, macro_name


def get_or_create_local_macro(name: str):
    text_data = get_local_macro(name)

    if text_data is not None:
        return text_data

    return create_local_macro(name)


def add_to_local_macro(name: str, data: str):
    text_data, name = get_or_create_local_macro(name)
    text_data.write(f"{data}\n")


def read_from_local_macro(name: str):
    text_data = get_local_macro(name)

    if text_data is None:
        return None

    texts = []
    for line in text_data.lines:
        texts.append(line.body)

    return "\n".join(texts)


def remove_local_macro(name: str):
    macro = get_local_macro(name)
    bpy.data.texts.remove(macro)

    metadata = get_local_metadata(name)
    if metadata is not None:
        remove_local_metadata(name)


def rename_local_macro(old_name: str, new_name: str):
    macro = get_local_macro(old_name)
    macro.name = COMMAND_FILENAME_PREFIX + new_name

    metadata = get_local_metadata(old_name)
    if metadata is not None:
        rename_local_metadata(old_name, new_name)


def __load_local_macro_names():
    names = bpy.data.texts.keys()
    filtered = list(
        filter(lambda key: re.search(COMMAND_FILENAME_PREFIX, key) is not None, names)
    )
    modified = list(
        map(lambda name: str(name).replace(COMMAND_FILENAME_PREFIX, ""), filtered)
    )

    return modified


def list_local_macro_names():
    names = __load_local_macro_names()
    return order_names_with_metadata(names, REGION_LOCAL)


def order_names_with_metadata(names: List[str], region: str):
    metadata_dict = {}

    not_indexed_names = []

    for name in names:
        metadata_body = read_metadata(name, region)

        if metadata_body is None:
            not_indexed_names.append(name)
            continue

        if "index" not in metadata_body:
            not_indexed_names.append(name)
            continue

        metadata_dict[name] = metadata_body

    sorted_names = sorted(
        metadata_dict.keys(), key=lambda name: metadata_dict[name]["index"]
    )

    for index, name in enumerate(not_indexed_names):
        metadata_body = read_metadata(name, region)

        if metadata_body is None:
            metadata_body = {}

        metadata_body["index"] = index + len(sorted_names)
        write_metadata(name, metadata_body, region)

    sorted_names.extend(not_indexed_names)

    # update metadata
    for index, name in enumerate(sorted_names):
        metadata_body = read_metadata(name, region)

        should_update = False
        if metadata_body is None:
            metadata_body = {}
            should_update = True

        elif "index" not in metadata_body:
            should_update = True

        elif metadata_body["index"] != index:
            should_update = True

        if should_update:
            metadata_body["index"] = index
            write_metadata(name, metadata_body, region)

    return sorted_names


def __load_global_macro_names():
    names = os.listdir(STORAGE_MACROS_DIR)
    filtered = list(filter(lambda name: METADATA_FILENAME_PREFIX not in name, names))
    modified = list(map(lambda name: str(name).replace(".py", ""), filtered))
    return modified


def list_global_macro_names(update=False):
    global global_macro_names

    if state["global_macro_names"] is None or update:
        names = __load_global_macro_names()
        state["global_macro_names"] = order_names_with_metadata(names, REGION_GLOBAL)

        return state["global_macro_names"]

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


def remove_global_macro(name: str):
    path = f"{STORAGE_MACROS_DIR}/{name}.py"
    os.remove(path)
    list_global_macro_names(True)

    metadata = read_from_global_metadata(name)
    if metadata is not None:
        remove_global_metadata(name)


def rename_global_macro(old_name: str, new_name: str):
    path = f"{STORAGE_MACROS_DIR}/{old_name}.py"
    new_path = f"{STORAGE_MACROS_DIR}/{new_name}.py"
    os.rename(path, new_path)
    list_global_macro_names(True)


def move_to_global(local_macro_name: str):
    global_macro_data = read_from_global_macro(local_macro_name)
    if global_macro_data is not None:
        raise ValueError("Already exists!")

    metadata = read_from_local_metadata(local_macro_name)
    if metadata is not None:
        move_metadata_to_global(local_macro_name)

    data = read_from_local_macro(local_macro_name)
    if data is not None:
        write_to_global_macro(local_macro_name, data)
        remove_local_macro(local_macro_name)
        list_global_macro_names(True)


def move_to_local(global_macro_name: str):
    local_macro_data = read_from_local_macro(global_macro_name)
    if local_macro_data is not None:
        raise ValueError("Already exists!")

    metadata = read_from_global_metadata(global_macro_name)
    if metadata is not None:
        move_metadata_to_local(global_macro_name)

    data = read_from_global_macro(global_macro_name)
    if data is not None:
        add_to_local_macro(global_macro_name, data)
        remove_global_macro(global_macro_name)


def move(name: str, amount: int, region: str):
    names = []
    if region == REGION_LOCAL:
        names = list_local_macro_names()
    if region == REGION_GLOBAL:
        names = list_global_macro_names()

    current_name = name

    current_index = names.index(current_name)

    target_index = current_index + amount

    if target_index < 0 or target_index > len(names):
        ValueError("Index is out of range!")

    target_name = names[target_index]

    current_metadata = read_metadata(current_name, region)

    if current_metadata is None:
        current_metadata = {}

    target_metadata = read_metadata(target_name, region)
    if target_metadata is None:
        target_metadata = {}

    current_metadata["index"] = target_index
    target_metadata["index"] = current_index

    write_metadata(current_name, current_metadata, region)
    write_metadata(target_name, target_metadata, region)
