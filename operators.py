import bpy

def get_recent_operations():
    window = bpy.context.window_manager.windows[0]

    override_context = bpy.context.copy()
    override_context["window"] = window
    override_context["screen"] = window.screen
    override_context["area"] = window.screen.areas[0]
    override_context["area"]["type"] = "INFO"

    bpy.ops.info.select_all(override_context, action="SELECT")
    bpy.ops.info.report_copy(override_context)

    clipboard = bpy.context.window_manager.clipboard

    return clipboard


"""
start operation
  履歴クリアしちゃうのが楽ではあるが
  現在長を保存しておくのがまぁ無難か

  あるいは特定文字列を埋め込む。
  Record Started

  こっちのがいいのでは？

  保存場所はオペレータでいいかも。
  シーンとかに保存するとまた開いたときにまずい

end operation
  操作履歴を取得する。
  アクティブなテキストに追記する

保存すべきメタデータってなんかある？特になくない？

ボタンの順番は保存しないといけない
ファイル名でどうこうするのはよくない

commandrecorder_local_data.jsonみたいのを用意してそこにかいていく
グローバルはstorageにglobal_data.jsonをおく
グローバル設定はsettigs.jsonを置く？
さすがにアドオン設定を利用すべき？でもないか…


"""