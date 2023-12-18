# coding: utf-8
# cx_Freeze 用セットアップファイル

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["data"],  # 依存するパッケージを指定
    "include_files": ["data/"],  # 参照するフォルダやリソースを指定
}

setup(
    name="Heltheye",
    version="1.2",
    description="Your application description",
    options={"build_exe": build_exe_options},
    executables=[Executable("Heltheye.py")],
)
