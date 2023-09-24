# CardinalMangaer

该项目是 Cardinal 的官方启动器，Cardinal 的多版本共存、更新升级、以及一些 Cardinal 专属的开发工具都使用本管理器进行管理。

# 关于编译

CardinalManager 在开发之初就使用 xmake + clang (ucrt) 的方案，使用 gcc 编译也许会成功，但是可能产生不可预知的 bug。为了节省您的精力，请在参与开发或自行编译的时候都以官方操作为准。

> 编译方法请参考 [xmake 官方文档](https://xmake.io/#/zh-cn/)，在这里不过多赘述。

下面是一些可能遇到的问题，请在出问题后来这里参考，无法解决请按照要求写issus。

## 配置 msys2

默认在 ucrt64 环境下编译

安装所有的依赖：

```shell
pacman -Sy mingw-w64-ucrt-x86_64-libadwaita \
           mingw-w64-ucrt-x86_64-clang \
           mingw-w64-ucrt-x86_64-clang-tools-extra \
           mingw-w64-ucrt-x86_64-toolchain \
           mingw-w64-ucrt-x86_64-ntldd
```

觉得速度慢可以考虑换个源，我自己用的是 tuna 的源，更换的教程也在 tuna 的文档中包含了，自己找一下就行。

## xmake 远程包仓库无法更新导致的编译失败

CardinalManager 不依赖 xmake 远程包，可以考虑将 xmake 配置成内网状态来解决问题：

请在终端里面使用如下命令
```shell
xmake g --network=private
```

## 在 msys2 中安装了 xmake 并正确配置了PATH，但是 xmake 在cmd中不工作（报错：16位应用程序...）

我花了一个下午来研究这个问题，一开始以为是软连接错误，后来认为是exe损坏，最后忍无可忍对 ucrt64/bin 下的 xmake.exe 进行了反汇编，结果......

发现这个 xmake.exe 竟然本质上是一个sh脚本（你可以理解成xmake.sh改了个后缀名）

> 解决方法：卸载 msys2 中的 xmake ，用 winget、scoop 之类工具安装 xmake，或直接去官方仓库的 release 里面下载最新版安装。
