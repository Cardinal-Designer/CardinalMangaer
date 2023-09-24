# -*- coding: utf-8 -*-
from subprocess import PIPE,Popen
import sys,shutil,os

shield_path = [
  "C:\\Windows\\"
]

dependeces = []

def search_dependeces(msys2_target : str):
  with Popen(["ntldd",msys2_target],stdout=PIPE) as p:
    dep_raw = p.stdout.read()

  dep_raw = dep_raw.decode(encoding="utf-8")
  dep_raw = dep_raw.replace("\r","")
  dep_raw = dep_raw.replace("\t","")
  dep_raw = dep_raw.split("\n")

  def processing_data(data:str):
    # 删除字符串里面写的指针数据
    pointer_index = data.find(" (0x")
    if pointer_index != -1: # 没有找到该字符串返回值为 -1
      name,path = data[:pointer_index].split(" => ")

      for s_p in shield_path: # 屏蔽掉系统自带的库
        if s_p in path:
          return None

      return (name,path)
    return None

  for i in dep_raw:
    if i: # i 不为空则值不为 0
      processed = processing_data(i)
      if processed: # 不为None则是有效数据

        if processed in dependeces:
          continue

        print(processed)
        dependeces.append(processed)

        search_dependeces(processed[1]) # 递归搜索

def copy_dep(target_path:str):
  origin_files = os.listdir(target_path)

  for i in dependeces:
    if i[0] in origin_files:
      continue

    shutil.copy(i[1],target_path)


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("[Error] 参数过少")
    exit

  print("依赖的dll：")

  search_dependeces(sys.argv[1])
  copy_dep(sys.argv[2])

  print("拷贝到：",sys.argv[2])
