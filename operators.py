import bpy

from .utils.report import flush_recent_operations, get_recent_operations
from .utils.io import add_to_text_data, read_from_text_data


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
    add_to_text_data("test_record", commands)


def play_command():
    commands = read_from_text_data("test_record")
    exec(commands)


class RecordCommandOperator(bpy.types.Operator):
    bl_idname = "command_recorder_xxrefactoringxx.recordcommand"
    bl_label = "RecordCommand"

    __state_running = False

    def cls(self):
        return RecordCommandOperator

    def __start(self, context):
        self.cls().__state_running = True
        flush_recent_operations()
        self.report({"INFO"}, "Record Start")

    def __end(self, context):
        self.cls().__state_running = False
        record_command()
        self.report({"INFO"}, "Record End")

    def invoke(self, context, event):
        if not self.cls().__state_running:
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

    def execute(self, context):
        play_command()
        return {"FINISHED"}
