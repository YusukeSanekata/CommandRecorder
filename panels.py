import bpy

from .operators import PlayCommandOperator, RecordCommandOperator, TestOpOperator


"""

■グローバルマクロ一覧パネル
Storageに保存する、グローバルに使用するマクロ。
[番号ボタン, コマンドボタン]
で表示。
・削除、上に移動、下に移動

■コマンド移動パネル
・グローバルに移動ボタン
・ローカルに移動 ボタン
番号ボタンで選択されているアイテムを操作

■ローカルマクロ（ファイル固有マクロ）一覧パネル
ファイルにテキストとして保存するマクロの一覧。
[番号ボタン, コマンドボタン]
で表示。デフォルトショートカットがついている。
・追加、削除、複製、上に移動、下に移動

■ローカルマクロ編集パネル
番号で選択されているローカルマクロを編集する。
リストの上下などで順番を変更したりする
・Recボタン
・マクロ名
・オペレーションリスト編集

"""

class CommandRecorderPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CommandRecorder_xxrefactoringxx"


###############################################################


class CommandRecorder_MainPanel(CommandRecorderPanel, bpy.types.Panel):
    bl_label = "CommandRecorder"
    bl_idname = "CommandRecorderMainPanel"

    def draw(self, context):
        layout = self.layout
        # layout.label(text="MainPanel")

        pass

###############################################################

class CommandRecorder_GlobalMacroListPanel(CommandRecorderPanel, bpy.types.Panel):
    bl_label = "develop"
    bl_parent_id = CommandRecorder_MainPanel.bl_idname

    def draw(self, context):
        layout = self.layout



###############################################################
class CommandRecorder_MiscPanel(CommandRecorderPanel, bpy.types.Panel):
    bl_label = "develop"
    bl_parent_id = CommandRecorder_MainPanel.bl_idname

    def draw(self, context):
        layout = self.layout
        layout.label(text="test")
        layout.operator(TestOpOperator.bl_idname)
        layout.operator(RecordCommandOperator.bl_idname)
        layout.operator(PlayCommandOperator.bl_idname)


classes = [CommandRecorder_MainPanel, CommandRecorder_MiscPanel]

