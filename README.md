# 奶鼠

亮黄色、柔软绒感的小鼠动画角色，包含九种动作及十六个注视方向。素材由 AI 图像生成并经动画整理和颜色一致性处理完成。

![奶鼠完整动画](previews/naishu-complete-preview.apng)

**[领养奶鼠](https://chatgpt.com/s/sharepet_6ac8c0924cd0819182f5a53f675ea63c)** · [下载原图集](assets/spritesheet.png?raw=1) · [查看 MP4 预览](previews/naishu-complete-preview.mp4)

## 让奶鼠成为你的 dot

打开上面的领养链接并登录，领养会把奶鼠复制到你自己的宠物库。然后在你想使用奶鼠的 dot 会话中，让助手将这份副本设为当前 dot 的形象。

也可以直接把下面这句话复制给你的 dot：

```text
请领养这个奶鼠，并将它设为当前 dot 的形象：https://chatgpt.com/s/sharepet_6ac8c0924cd0819182f5a53f675ea63c
```

Work 的宠物选择与当前 dot 的形象分别保存。领养或选择 Work 宠物后，仍需为当前 dot 单独设置形象；领养链接不会自动改变所有 dot。

领养和使用奶鼠无需安装 Python。下方脚本仅供开发者验证或导出素材。

## 下载与预览

完整项目可在本仓库页面点击 **Code → Download ZIP** 下载。也可单独下载[最终透明图集](assets/spritesheet.png?raw=1)和[动画配置](assets/animation.json?raw=1)。仓库内的素材链接长期随项目保存。

![十六个注视方向](previews/naishu-look-directions.apng)

部分平台不播放 APNG，可下载后在支持 APNG 的浏览器打开，或查看[完整 MP4](previews/naishu-complete-preview.mp4)。MP4 使用不透明底色；APNG 保留透明边缘。另有[方向联系表](previews/naishu-look-directions.png)和[全部姿势联系表](previews/naishu-all-poses.png)。

## 文件

- assets/spritesheet.png：最终透明 RGBA 图集，1536×2288 像素
- assets/animation.json：帧数、方向和预览时长配置
- previews/：完整动画、各动作循环、待机→跳跃→待机回归、方向循环和联系表
- scripts/apng_fullframes.py：完整画布 APNG 编码器，保存后逐帧核对像素和时长
- scripts/verify_export.py：文件哈希、布局、透明空槽、标准预览一致性检查及无改图导出
- manifest.json：各发布文件的大小和 SHA-256

## 图集布局

图集使用 8 列、11 行，每格 192×208 像素。行号从 0 开始。

| 行 | 动作 | 有效帧数 |
|---|---|---|
| 0 | idle，待机 | 6 |
| 1 | running-right，向右移动 | 8 |
| 2 | running-left，向左移动 | 8 |
| 3 | waving，挥手 | 4 |
| 4 | jumping，跳跃 | 5 |
| 5 | failed，失败反应 | 8 |
| 6 | waiting，等待输入 | 6 |
| 7 | running，处理任务 | 6 |
| 8 | review，检查结果 | 6 |
| 9 | 注视方向前半圈 | 8 |
| 10 | 注视方向后半圈 | 8 |

共 73 个有效格，15 个空格全透明。角度按屏幕坐标顺时针：0°向上、90°向右、180°向下、270°向左；每步 22.5°。第 9 行为 0°至157.5°，第 10 行为180°至337.5°。帧应保留原尺寸与注册位置，不要逐帧缩放到内容边界，否则会破坏动作中的尺度与重心连续性。

## 开发者验证与导出

仅在需要验证或重新导出素材时，使用 Python 3 和 Pillow。可在自己的虚拟环境安装 requirements.txt 中的依赖，然后运行：

```sh
python scripts/verify_export.py
python scripts/verify_export.py --export
```

第二条命令将从图集直接裁出各行，在 exported/ 中生成透明 APNG；不改变像素、颜色或轮廓。方向的两行分别导出；完整16方向循环已随项目提供。

主预览为192×208、132帧、21.76秒；方向循环为16帧、2.88秒。APNG采用完整帧替换，避免透明增量合成引起残影。已有最终检查覆盖布局、透明度、动作播放、方向语义和编码解码一致性。本仓库脚本只负责其明确列出的可复现检查，不替代人工动作审阅，也不包含服务端创建或激活操作。

## 权利与发布

本项目未附加开源许可证。
