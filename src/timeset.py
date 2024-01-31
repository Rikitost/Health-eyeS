# 入力内容確認の関数
def value_check(entry_text, warning_label):
    # 数字の判定
    if entry_text.get().isdigit() or entry_text.get() == "":
        return True
    else:
        warning_label.config(text='数字を入力してください')
        return
# 数値のみ


def on_validate_time(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return (P.isdigit() and len(P) <= 4) or P == ""


def on_validate_pass(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return (P.isdigit() and len(P) <= 4) or P == ""
