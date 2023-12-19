# coding: utf-8
# cx_Freeze 用セットアップファイル

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["data"],  # 依存するパッケージを指定
    "include_files": ["data/"],  # 参照するフォルダやリソースを指定
}

# プラットフォームに応じてbaseパラメータを設定
if sys.platform == "win32":
    base = "Win32GUI"  # Windows用にGUIアプリケーションとして設定
elif sys.platform == "darwin":
    base = "MacOSXApp"  # macOS用にGUIアプリケーションとして設定
else:
    base = None


setup(
    name="Heltheye",
    version="1.2",
    description="Your application description",
    options={"build_exe": build_exe_options},
    executables=[Executable("Heltheye.py", base=base)],
)
