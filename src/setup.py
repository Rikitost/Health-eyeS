# インストーラー(msi)をつくる
# coding: utf-8
# cx_Freeze 用セットアップファイル

import sys
from cx_Freeze import setup, Executable

# プラットフォームに応じてbaseパラメータを設定
if sys.platform == "win32":
    base = "Win32GUI"  # Windows用にGUIアプリケーションとして設定
elif sys.platform == "darwin":
    base = "MacOSXApp"  # macOS用にGUIアプリケーションとして設定
else:
    base = None

build_exe_options = {
    "packages": ["data", "plyer"],  # 依存するパッケージを指定
    # 参照するフォルダやリソースを指定
    "include_files": ["data/", "end_flg_value.py", "favicon.ico", "limit.txt", "pass_sec_value.py", "password_form_end_flg.py", "password_input.py", "password.txt",   "setting.py", "time_limit.py", "timeset.py", "warning_flg.py", "warning.py"],
    "include_msvcr": True,
    "silent": True,
}

shortcut_common_setting = (
    "HEALTHEYESuper",
    "TARGETDIR",
    "[TARGETDIR]Health-eyeS.exe",
    None,
    None,
    None,
    None,
    None,
    None,
    "TARGETDIR",
)
shortcut_table = [
    # アプリショートカットをスタートメニューに追加
    ("ProgramMenuShortcut", "ProgramMenuFolder") + shortcut_common_setting,
    # アプリショートカットを shell:startup に追加 (PC起動時に自動起動されるようにする)
    ("StartupShortcut", "StartupFolder") + shortcut_common_setting,
]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {
    'data': msi_data,
    # 任意の UUID を生成して設定
    'upgrade_code': '{1DE2105C-063C-4766-9BA6-20FBB473D7A6}',
}

setup(
    name="Health-eyeS",
    version="2.1.1",
    description="Health-eyeS",
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[Executable("HealtheyeS.py",  base=base,
                            shortcut_name="Health-eyeS",)],
)

# ---------------------------------------------------------------
# import sys
# from cx_Freeze import setup, Executable

# # プラットフォームに応じてbaseパラメータを設定
# if sys.platform == "win32":
#     base = "Win32GUI"  # Windows用にGUIアプリケーションとして設定
# elif sys.platform == "darwin":
#     base = "MacOSXApp"  # macOS用にGUIアプリケーションとして設定
# else:
#     base = None

# build_exe_options = {
#     "packages": ["data"],  # 依存するパッケージを指定
#     "include_files": ["data/"],  # 参照するフォルダやリソースを指定
# }

# setup(
#     name="Heltheye",
#     version="1.4",
#     description="Your application description",
#     options={
#         "build_exe": build_exe_options,
#         "bdist_msi": {
#             # 一意のGUIDを指定
#             "upgrade_code": "{2697469D-38D6-43DD-88B4-2512B735119B}",
#         },
#     },
#     executables=[Executable("Heltheye.py", base=base)],
# )
