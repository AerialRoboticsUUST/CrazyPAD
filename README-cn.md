#crazyflie-数据集

## 软件解决方案位于src目录下
1. 飞行计划
2. 解密二进制数据的脚本位于decrypt_data目录中。 该目录包含 readme.md 文件，其中包含程序的详细描述

## 收集到的实验数据呈现在data目录下
  - 'add_weight_W1_near_M3_M4' - 附加重量 W1 粘贴到 M3 和 M4 螺旋桨附近的胶带上
  - 'add_weight_W1_near_M3' - 附加配重 W1 粘贴在 M3 螺旋桨附近的胶带上
  - 'add_weight_W1_near_M4' - 附加配重 W1 贴在 M4 螺旋桨附近的胶带上
  - 'add_weight_W3_near_M3' - 附加配重 W3 贴在 M3 螺旋桨附近的胶带上
  - 'cut_propeller_M3_1mm' - 螺旋桨损坏（长度减少 1mm）M3
  - 'cut_propeller_M3_2mm' - 螺旋桨损坏（长度减少 2mm）M3
  - 'cut_propeller_M3_3mm' - 螺旋桨损坏（长度减少 3mm）M3
  - 'normal_flight' - 正常模式下的航班
  - 'tape_on_propeller_M1_M3' - 模仿粘附在螺旋桨 M1 和 M3 上的碎片（胶带）
  - 'tape_on_propeller_M1_M3_M4' - 模拟粘附在螺旋桨 M1 和 M3、M4 上的碎片（胶带）
  - 'tape_on_propeller_M3' - 模仿粘在 M3 螺旋桨上的碎片（胶带）
  - 'tape_on_propeller_M3_M4' - 模仿粘附在螺旋桨 M3 和 M4 上的碎片（胶带）
  - 'weight_on_string_W2_near_M3' - 附加重量 W2 附加到 M3 螺旋桨附近的 63 厘米长螺纹上
  - 'weight_on_string_W3_near_M3' - 在 M3 螺旋桨附近的 63 厘米长螺纹上附加一个重量为 W3 的附加重物

## Bitcraze 的示例项目
[Bitcraze 示例](https://github.com/bitcraze/crazyflie-lib-python/tree/master/examples)

## 安装项目依赖
`pip install cflib`
