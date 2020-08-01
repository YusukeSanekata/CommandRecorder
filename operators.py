import bpy
from bpy.props import StringProperty, IntProperty

from .utils.report import flush_recent_operations, get_recent_operations
from .utils.io import (
    add_to_local_macro,
    create_local_macro,
    read_from_global_macro,
    read_from_local_macro,
)
from .state import state


class TestOpOperator(bpy.types.Operator):
    bl_idname = "command_recorder.testop"
    bl_label = "TestOp"

    def execute(self, context):
        recent = get_recent_operations()
        print("####################")
        print("recent:" + str(recent))
        print("####################")

        return {"FINISHED"}


def record_command():
    commands = get_recent_operations()

    if state["local_macro_active_name"] is None:
        raise ValueError("No macro is selected.")

    print('state["local_macro_active_name"]:' + str(state["local_macro_active_name"]))
    add_to_local_macro(state["local_macro_active_name"], commands)


def play_command(category: str, name: str):
    commands = None

    print("category:" + str(category))
    print("name:" + str(name))

    if category == "global":
        commands = read_from_global_macro(name)

    if category == "local":
        commands = read_from_local_macro(name)

    print("commands:" + str(commands))
    if commands is not None:
        exec(commands)
        return

    raise ValueError("No commands!")


class RecordCommandOperator(bpy.types.Operator):
    bl_idname = "command_recorder_xxrefactoringxx.recordcommand"
    bl_label = "RecordCommand"

    state_running = False

    def cls(self):
        return RecordCommandOperator

    @classmethod
    def poll(cls, self):
        return state["local_macro_active_name"] is not None

    def __start(self, context):
        self.cls().state_running = True
        flush_recent_operations()
        self.report({"INFO"}, "Record Start")

    def __end(self, context):
        self.cls().state_running = False
        record_command()
        self.report({"INFO"}, "Record End")

    def invoke(self, context, event):
        if not self.cls().state_running:
            self.__start(context)
            return {"FINISHED"}
        else:
            self.__end(context)
        return {"FINISHED"}

    def execute(self, context):
        return {"FINISHED"}


class PlayCommandOperator(bpy.types.Operator):
    bl_idname = "command_recorder_xxrefactoringxx.playcommand"
    bl_label = "PlayCommand"

    type = StringProperty(
        name="MacroCategory", description="local or global", default="Local",
    )

    name = StringProperty(name="MacroName", description="name of a macro", default="",)

    @classmethod
    def poll(cls, self):
        return not RecordCommandOperator.state_running

    def execute(self, context):
        self.report({"INFO"}, str((self.type)))
        self.report({"INFO"}, str((self.name)))
        play_command(self.type, self.name)
        return {"FINISHED"}


class SelectGlobalMacroOperator(bpy.types.Operator):
    bl_idname = "object.selectglobalmacro"
    bl_label = "SelectGlobalMacro"

    index = IntProperty(
        name="Global Macro Index", description="index of global macro", default=0,
    )

    name = StringProperty(name="Macro Name", description="name of macro", default="",)

    @classmethod
    def poll(cls, self):
        return not RecordCommandOperator.state_running

    def execute(self, context):
        state["global_macro_active_index"] = self.index
        return {"FINISHED"}


class SelectLocalMacroOperator(bpy.types.Operator):
    bl_idname = "object.selectlocalmacro"
    bl_label = "SelectLocalMacro"

    index = IntProperty(
        name="Local Macro Index", description="index of global macro", default=0,
    )

    name = StringProperty(name="Macro Name", description="name of macro", default="",)

    @classmethod
    def poll(cls, self):
        return not RecordCommandOperator.state_running

    def execute(self, context):
        state["local_macro_active_index"] = self.index
        state["local_macro_active_name"] = self.name
        return {"FINISHED"}


class AddLocalMacroOperator(bpy.types.Operator):
    bl_idname = "object.addlocalmacro"
    bl_label = "AddLocalMacro"

    @classmethod
    def poll(cls, self):
        return not RecordCommandOperator.state_running

    def execute(self, context):
        create_local_macro("NEW MACRO")
        return {"FINISHED"}

