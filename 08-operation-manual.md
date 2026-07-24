# 08 — 操作使用说明

**项目：** USB PD 多功能测试仪
**日期：** 2026-07-13

---

## 一、开箱检查

收到板子后先目检：

1. **TYPE-C 母座**焊接是否饱满，16 个引脚有无连锡/虚焊
2. **USB-A 公头** 4 个引脚焊接是否牢固（直插，插入被检测设备端）
3. **OLED 屏幕**是否插紧（如果用排针/排母连接）
4. **四个按键**（MODE/CONFIRM/BOOT/RST）按压手感是否正常
5. **SWD 和 UART 排针**有无歪斜短路
6. **10mΩ 分流电阻**（0805 合金）方向、焊盘是否正常

> ⚠️ 首次上电前，建议用万用表蜂鸣档测 **VBUS 与 GND 之间是否短路**。正常应不导通。

---

## 二、首次上电

### 2.1 供电方式

本设备由 **USB-C PD 充电器供电**，不内置电池。两种供电来源都可以：

| 来源 | 操作 | 说明 |
|------|------|------|
| **PD 充电器** | 直接插 USB-C | 支持全档位（5V~20V），可完整测试 PD 协议 |
| **电脑 USB 口** | 直接插 USB-C | 只能 5V，适合烧录固件和基本功能验证 |

> 插电脑 USB 口时，CC1/CC2 的 5.1kΩ 下拉会让电脑识别为 Sink 设备并输出 5V VBUS。

### 2.2 上电检查

插上 USB-C 后，正常现象：

1. OLED 屏幕亮起，显示开机画面
2. 如果没有烧录固件，OLED 不亮是正常的（空白芯片）
3. 用万用表测 LDO 输出（HT7533S OUT 脚）：**3.3V ±0.15V**

---

## 三、烧录固件（USB ISP）

> 这是最方便的烧录方式，**只需要一根 USB-C 线**，不需要 WCH-LinkE。

### 3.1 准备工作

1. 电脑安装 **WCHISPTool**
   - 下载地址：https://www.wch.cn/downloads/WCHISPTool_Setup_exe.html
   - 安装时驱动全部勾选

2. 准备编译好的固件文件（`.hex` 格式）

### 3.2 烧录步骤

```
┌──────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐    ┌──────┐
│ 步骤1 │ → │   步骤2   │ → │    步骤3    │ → │   步骤4   │ → │ 步骤5 │
│ 按住  │    │ 插 USB-C │    │ 松开 BOOT  │    │ WCHISPTool│    │ 拔掉  │
│ BOOT  │    │  到电脑  │    │    按键    │    │  点下载   │    │ 重插  │
└──────┘    └──────────┘    └────────────┘    └──────────┘    └──────┘
```

**详细操作：**

1. **按住 BOOT 键不松手**（最右边那个按键）
2. 保持按住，**把 USB-C 线插到电脑上**
3. **松开 BOOT 键**
4. 打开 WCHISPTool：
   - 芯片系列选：**CH32V20x**
   - 下载接口选：**USB**
   - 点击"搜索设备"→ 应识别到 `CH32V203`
   - 点击"选择文件"→ 加载 `.hex` 固件
   - 点击 **"下载"**
5. 等待进度条走完，提示"下载成功"
6. **拔掉 USB-C 线再重新插上**（或按一下 NRST 复位）→ 程序开始运行

### 3.3 常见烧录失败原因

| 现象 | 原因 | 解决 |
|------|------|------|
| WCHISPTool 搜不到设备 | BOOT 键没按住就上电了 | 重试，确认按住 BOOT 不松手再插线 |
| 搜不到设备 | 电脑没识别 USB | 检查 CC1/CC2 5.1kΩ 下拉是否焊接正确 |
| 搜不到设备 | USB D+/D- 走线断路 | 用万用表蜂鸣档测 USB-C D+ → MCU PA12 |
| 下载中途报错 | USB 线质量差 | 换一根短一点的 USB-C 数据线（不要用充电线） |
| 下载成功但程序不跑 | BOOT 键没弹起来 | 检查 BOOT 按键是否卡住 |
| 下载成功 OLED 不亮 | 固件问题 / OLED 焊接 | 先用 SWD 调试确认固件正常 |

---

## 四、烧录固件（SWD — 备选方案）

如果 USB ISP 暂时不可用（比如读保护锁了），用 SWD。

### 4.1 硬件连接

| WCH-LinkE | → | SWD 排针 |
|-----------|---|----------|
| 3V3 | → | Pin 4 (3.3V) |
| GND | → | Pin 3 (GND) |
| SWDIO | → | Pin 2 (SWDIO) |
| SWCLK | → | Pin 1 (SWCLK) |

> WCH-LinkE 需要处于 **RISC-V 模式**（设备管理器显示 "WCH-LinkRV"）。

### 4.2 烧录步骤

1. 接好 SWD 排线
2. USB-C 给板子供电
3. 打开 MounRiver Studio
4. 点击下载配置 → Query → 选择 WCH-LinkRV
5. 点击下载按钮

---

## 五、查看调试日志（USART1 printf）

程序运行时可以通过 USART1 输出日志到电脑的串口助手。

### 5.1 硬件连接

```
UART 排针（板上 3-pin）      USB-TTL 模块
     TX (Pin1)        →        RX
     RX (Pin2)        →        TX
     GND (Pin3)       →        GND
```

> USB-TTL 模块不要接 VCC！板子已经由 USB-C 供电。

### 5.2 串口助手设置

| 参数 | 值 |
|------|-----|
| 端口 | 设备管理器查 USB-TTL 对应的 COM 号 |
| 波特率 | 115200 |
| 数据位 | 8 |
| 停止位 | 1 |
| 校验 | None |

### 5.3 预期输出

```
USB PD Tester v1.0
MCU: CH32V203C8T6 @ 144MHz
INA226 detected @ 0x40
OLED initialized @ 0x3C

PD Trigger: 5V  (CFG=000)
Voltage: 5.123V
Current: 0.456A
Power:   2.336W
```

---

## 六、按键操作

设备有 **4 个按键**，排列如下：

```
┌──────┐  ┌───────┐  ┌──────┐  ┌──────┐
│ MODE │  │CONFIRM│  │ BOOT │  │ RST  │
│  模式 │  │  确认  │  │  烧录 │  │ 复位  │
└──────┘  └───────┘  └──────┘  └──────┘
```

### 6.1 正常运行模式

| 按键 | 短按 | 长按 (>1s) |
|------|------|------------|
| **MODE** | 切换显示页面 | — |
| **CONFIRM** | 锁定/解锁当前 PD 档位 | — |
| **BOOT** | 无功能 | — |
| **RST** | 硬件复位 MCU | — |

### 6.2 显示页面

| 页面 | 显示内容 |
|------|----------|
| 首页 | 实时电压 / 电流 / 功率（大字） |
| 详情页 | 电压、电流、功率 + PD 协议版本 + 当前档位 |
| 统计页 | 累计最大值 / 最小值 / 平均值 |
| 协议页 | 充电器支持的 PD/PPS/QC 档位列表 |

### 6.3 固件更新模式

| 操作 | 结果 |
|------|------|
| **按住 BOOT 再插 USB-C** | 进入 USB Bootloader，等待烧录 |
| **松开 BOOT，正常上电** | 从 Flash 启动 APP |
| **按 RST** | 硬件复位，等同于拔插 USB-C |

---

## 七、测试 PD 充电器

### 7.1 完整测试流程

```
① 把 PD 充电器插到 USB-C 口
② 把被测设备（或电子负载）插到 USB-A 口
③ OLED 显示 PD 协议版本、当前电压电流
④ 短按 MODE 切换页面查看更多信息
⑤ 短按 CONFIRM 可锁定当前档位（不对 PD 重新协商）
```

### 7.2 测试各 PD 档位

按 MODE 键进入档位选择模式，设备会自动切换 CFG1/CFG2/CFG3 驱动 CH224K 请求不同电压：

| 请求电压 | CFG3/CFG2/CFG1 | 说明 |
|----------|----------------|------|
| 5V | 000 | 默认档位 |
| 9V | 001 | 常见快充档 |
| 12V | 010 | — |
| 15V | 011 | — |
| 20V | 100 | 最高档，需充电器支持 |

> 如果充电器不支持某档位，CH224K 会回退到上一有效档位，屏幕会显示 "NOT SUPPORTED"。

### 7.3 测试数据线

将 USB-C 端插充电器，USB-A 端通过数据线接负载，对比 USB-A 端电压 vs 充电器标称电压，可判断线材的压降和载流能力。

---

## 八、固件开发环境搭建

### 8.1 安装 MounRiver Studio

1. 官网下载：http://www.mounriver.com/
2. 安装（Windows 用户建议默认路径）
3. 安装时会自动装 WCH-Link 驱动
4. 打开后设备管理器确认出现 **"WCH-LinkRV"**

### 8.2 导入 EVT 例程

1. 沁恒官网下载 CH32V203 EVT 包：
   https://www.wch.cn/downloads/CH32V20xEVT_ZIP.html
2. 解压后在 MounRiver Studio 中 `File → Import → Existing Project`
3. 选择 `EVT/EXAM/GPIO/GPIO_Toggle` 作为起点

### 8.3 printf 重定向

在固件中加入以下代码，printf 输出重定向到 USART1：

```c
// 在 main.c 中加入
int _write(int fd, char *buf, int size)
{
    for (int i = 0; i < size; i++)
    {
        while (USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);
        USART_SendData(USART1, buf[i]);
    }
    return size;
}
```

初始化 USART1（PA9 TX, PA10 RX, 115200 8N1）：

```c
USART_InitTypeDef USART_InitStructure = {0};
GPIO_InitTypeDef GPIO_InitStructure = {0};

RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_USART1, ENABLE);

// PA9 = TX
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
GPIO_Init(GPIOA, &GPIO_InitStructure);

// PA10 = RX
GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
GPIO_Init(GPIOA, &GPIO_InitStructure);

USART_InitStructure.USART_BaudRate = 115200;
USART_InitStructure.USART_WordLength = USART_WordLength_8b;
USART_InitStructure.USART_StopBits = USART_StopBits_1;
USART_InitStructure.USART_Parity = USART_Parity_No;
USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
USART_Init(USART1, &USART_InitStructure);
USART_Cmd(USART1, ENABLE);
```

---

## 九、常见问题排查

| 问题 | 可能原因 | 排查顺序 |
|------|----------|----------|
| OLED 不亮 | 固件未烧录 / SPI 不通 / 模块损坏 | ① 确认已烧录固件 ② 测 SPI SCK/MOSI 波形 ③ 检查 RES/DC/CS 接线 ④ 换模块 |
| 电压读数偏差大 | INA226 未校准 / 分流焊点不良 | ① 用万用表对比校准 ② 检查 Kelvin 走线 |
| 电流读数始终为 0 | INA226 I²C 不通 / 分流断路 | ① 测 I²C SCL/SDA 波形 ② 测分流电阻是否断路 |
| PD 不触发 | CH224K CFG 线错误 / CC 未连接 | ① 测 CFG1/2/3 引脚电平 ② 测 CC1 对 GND 电压 |
| 特定档位不出 | 充电器不支持该档位 | 换一个已知支持该档位的充电器交叉验证 |
| USB ISP 搜不到 | BOOT 键没按住 / CC 下拉电阻未焊 | ① 万用表测 BOOT0 上电时是否 3.3V ② 测 CC1/CC2 对 GND 阻值是否为 5.1kΩ |
| WCH-Link 连不上 | 模式不对 / 接线反了 | ① 确认设备管理器显示 WCH-LinkRV ② 对调 SWDIO/SWCLK |
| LDO 发烫 | 输入电压过高 / 负载过大 | ① 确认输入不超过 30V ② 测 3.3V 轨电流是否 >100mA |

---

## 十、安全注意事项

1. ⚡ **不要输入超过 20V 的 VBUS** — 虽然 HT7533S 标称 30V，但 CH224K 和 INA226 的 20V/36V 上限不应挑战
2. 🔥 **最大输出电流 3A** — 10mΩ 分流在 3A 下功耗 90mW，超载会导致分流发热、阻值漂移
3. 🛡️ **不要在 PCB 通电时触碰高压路径** — 20V VBUS 虽然不是危险电压，但意外短路可能烧毁器件
4. 🔌 **USB-A 输出口不要反插** — 无防反接保护
5. 💧 **不防水、不防尘** — 仅限室内桌面使用

---

## 十一、物料清单速查

| 物料 | 购买渠道 | 备注 |
|------|----------|------|
| WCH-LinkE 调试器 | 淘宝搜 `WCH-LinkE` | ¥9.9，开发调试必买 |
| USB-TTL 模块 | 淘宝搜 `USB转TTL CH340` | ¥5，调试日志用 |
| USB-C 数据线 | 任意 | ⚠️ 必须用**数据线**，充电线（只有 VBUS/GND 没有 D+/D-）不行 |
| USB-C PD 充电器 | 任意 ≥20W PD 充电器 | 建议 65W（支持 20V 档位） |
| 电子负载 | 淘宝搜 `电子负载 150W` | 可选，精确测试用 |
| M2 螺丝 + 尼龙柱 | 淘宝 | 固定 PCB 用 |

---

## 附录 A：引脚速查卡

```
CH32V203C8T6 LQFP-48 功能引脚
(来源: CH32V203 数据手册 V2.8, 表 3-1-1)

         ┌─────────────────────┐
  VBAT  1┤○                 48┤ VDD_IO_3
  PC13  2┤                   47┤ VSS_3
  PC14  3┤ (预留 GPIO)      46┤ PB9
  PC15  4┤ (预留 GPIO)      45┤ PB8
  OSC_IN5┤ (8MHz HSE→Y2)    44┤ BOOT0
  OSC_OUT6┤(8MHz HSE→Y2)    43┤ PB7 (I2C1_SDA)
  NRST  7┤                   42┤ PB6 (I2C1_SCL)
  VSSA  8┤                   41┤ PB5
  VDDA  9┤                   40┤ PB4
  PA0  10┤ KEY_MODE          39┤ PB3
  PA1  11┤ KEY_CONFIRM       38┤ PA15
  PA2  12┤ CFG1 → CH224K     37┤ PA14 (SWCLK)
  PA3  13┤ CFG2 → CH224K     36┤ VDD_2
  PA4  14┤ CFG3 → CH224K     35┤ VSS_2
  PA5  15┤ OLED_D0 (SPI_SCK) 34┤ PA13 (SWDIO)
  PA6  16┤ NC (SPI_MISO)     33┤ PA12 (USB_DP → USB ISP)
  PA7  17┤ OLED_D1 (SPI_MOSI)32┤ PA11 (USB_DM → USB ISP)
  PB0  18┤ OLED_RES          31┤ PA10 (UART_RX → Debug)
  PB1  19┤ OLED_DC           30┤ PA9  (UART_TX → Debug)
  PB2  20┤ (BOOT1, 内部下拉)   29┤ PA8  (OLED_CS)
  PB10 21┤                   28┤ PB15
  PB11 22┤                   27┤ PB14
  VSS_1 23┤                   26┤ PB13
  VDD_IO_1 24┤               25┤ PB12
         └─────────────────────┘
```

## 附录 B：WCHISPTool 截图式操作指南

```
┌─────────────────────────────────────────────────┐
│  WCHISPTool                          —  □  ×   │
├─────────────────────────────────────────────────┤
│  芯片系列:  [CH32V20x        ▼]                │
│  芯片型号:  [CH32V203C8T6    ▼]                │
│  下载接口:  [USB  ▼]                            │
│                                                 │
│  设备列表:  [CH32V203 - USB Device]  [搜索]     │
│                                                 │
│  下载文件:  [C:\...\pd_tester.hex   ]  [浏览]   │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  >>> 下载成功!                          │    │
│  │  Flash: 64KB                            │    │
│  │  用时: 2.3s                             │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  [下载]  [校验]  [解除保护]  [清除]  [退出]     │
└─────────────────────────────────────────────────┘
```
