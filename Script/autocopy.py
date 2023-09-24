# -*- coding: utf-8 -*-
from subprocess import PIPE,Popen
import sys

shield_path = [
  "C:\\Windows\\"
]

dependeces = []

dep_tmp = []

def search_dependeces(msys2_target : list):

  with Popen(["ntldd"] + msys2_target,stdout=PIPE) as p:
    dep_raw = p.stdout.read()

  dep_raw = dep_raw.decode(encoding="utf-8") # byte 数据转换到str，方便处理

  for i in msys2_target:
    if i in dep_raw:
      dep_raw = dep_raw.replace(i + ":","")


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
        dep_tmp.append(processed)

def search_dependeces_bfs(msys2_target : list):
  global dep_tmp
  global dependeces
  # bfs : 广度优先搜索

  search_dependeces(msys2_target)

  target_tmp = []
  while dep_tmp != []: # 只要还有搜索结果，就继续搜索
    for i in dep_tmp:
      target_tmp.append(i[1]) # 将dll路径汇总
      dependeces = dependeces + dep_tmp # 将上一层搜索结果合并到主线
      dep_tmp = [] # 清除上一次搜索结果

      search_dependeces(target_tmp) # 开始下一层搜索
      target_tmp = [] # 搜索结束，清除临时路径列表

def copy_dep(target_path:str):
  for i in dependeces:
    with Popen(["xcopy",i[1],target_path]) :
      pass



if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("[Error] 参数过少")
    exit

  search_dependeces_bfs([sys.argv[1]])
  copy_dep(sys.argv[2])
