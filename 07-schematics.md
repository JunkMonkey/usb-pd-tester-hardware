# 07 — 模块原理图（立创 EDA 专业版 绘制指南）

**项目：** USB PD 多功能测试仪
**日期：** 2026-07-15
**格式：** 立创 EDA 专业版 操作手册（逐步放置 → 连线 → 检查）
**配套文件：** `usb-pd-tester-schematic.json`（实验性导入文件，如立创 EDA 无法直接打开，请使用本指南手工绘制）

---

## 绘制前准备

1. 打开**立创 EDA 专业版**
2. 新建工程：`USB-PD-Tester`
3. 新建原理图页，命名为 `Main`
4. 页面尺寸设为 A4 横版（297×210mm）

---

## 第一步：放置核心 IC（按 LCSC 编号搜索，一键放置）

在立创 EDA 专业版的器件搜索框中输入**立创商城编号**，直接放置。立创 EDA 会自动加载对应的**原理图符号 + PCB 封装**。

| 顺序 | 位号 | 立创商城编号 | 型号 | 封装 | 放置位置(大致) |
|------|------|-------------|------|------|---------------|
| 1 | **U2** | `C3001172` | CH32V203C8T6 | LQFP-48 | 页面中央偏右 |
| 2 | **U3** | `C970725` | CH224K | ESSOP-10 | 页面中央偏上 |
| 3 | **U4** | `C49851` | INA226AIDGSR | VSSOP-10 | 页面中央偏下 |
| 4 | **U1** | `C347215` | HT7533S | SOT-23-3 | 左下角 |
| 5 | **U5** | 搜 `USBLC6-2SC6` | USBLC6-2SC6 | SOT-23-6 | USB-C 右侧 |
| 6 | **U6** | 搜 `USBLC6-2SC6` | USBLC6-2SC6 | SOT-23-6 | USB-C 公头左侧 |

> **提示：** 立创 EDA 器件搜索支持立创商城编号直接跳转，输入 `C3001172` 回车即可看到 CH32V203C8T6，双击放置。

### USBLC6-2SC6 引脚注意事项

```
        ┌──────────┐
 I/O1 ──┤ 1      6 ├── I/O1    (Pin1 与 Pin6 内部直连——信号穿通)
  GND ──┤ 2      5 ├── VBUS    (Pin5 = VBUS 电源轨保护)
 I/O2 ──┤ 3      4 ├── I/O2    (Pin3 与 Pin4 内部直连——信号穿通)
        └──────────┘
```

**U5 (USB-C 端):** D+ 进 Pin1 → 出 Pin6 → MCU；D- 进 Pin3 → 出 Pin4 → MCU；Pin2=GND；Pin5=VBUS

**U6 (USB-C 公头端):** D+ (J2.A6) 进 Pin1 → Pin6 悬空；D- (J2.A7) 进 Pin3 → Pin4 悬空；Pin2=GND；Pin5=VBUS_OUT（分流电阻负载侧）

---

## 第二步：放置连接器

| 位号 | 搜索词 | 说明 |
|------|--------|------|
| **J1** | `TYPE-C 16P 卧贴` | USB-C 母座，PD 输入 |
| **J2** | `USB-C 公头 24P` | USB-C 公头，插入被检测设备 (DUT)，CC1/CC2 各 56kΩ 上拉 |
| **J3** | `排针 1x4P 2.54mm` | SWD 调试接口 |
| **J4** | `排针 1x3P 2.54mm` | UART 调试串口 (TX/RX/GND) |

---

## 第三步：放置晶振

| 位号 | 立创商城编号 | 型号 | 封装 | 频率 |
|------|-------------|------|------|------|
| **Y2** | `C49158084` | Y32258MCBCX | SMD3225-4P | 8MHz HSE |

Y2 是 4-pin 封装：Pin1/2 = XTAL 脚，Pin3/4 = GND（接地）。

> **32.768kHz LSE 晶振已移除。** 本项目无需 RTC——没有电池备份、没有时间戳需求、固件时间基准走 SysTick。PC14/PC15 留作预留 GPIO。

---

## 第四步：放置无源器件（电阻、电容、电感）

> 无源器件可使用立创 EDA 通用库（`Resistor` / `Capacitor` / `Inductor`）+ 指定封装。

### 电容

| 位号 | 容值 | 封装 | 用途 |
|------|------|------|------|
| C1 | 10µF/50V | 0805 | VBUS 输入滤波 |
| C2 | 100nF/50V | 0603 | VBUS 高频去耦 |
| C3 | 10µF/16V | 0805 | 3.3V 输出滤波 |
| C4 | 100nF/16V | 0603 | 3.3V 高频去耦 |
| C5 | 10µF/16V | 0805 | VDDA 模拟滤波 |
| C6 | 100nF/16V | 0603 | VDDA 高频去耦 |
| ~~C7~~ | — | — | **已移除（随 LSE 晶振）** |
| ~~C8~~ | — | — | **已移除（随 LSE 晶振）** |
| C9~C12 | 100nF | 0603 | MCU VDD 去耦 (×4) |
| C13 | 10µF/50V | 0805 | CH224K VBUS 滤波 |
| C14 | 100nF | 0603 | CH224K 高频去耦 |
| C15 | 0.1µF | 0603 | INA226 VBUS 滤波 |
| C16 | 100nF | 0603 | INA226 VS 去耦 |
| C17 | 12pF NPO | 0603 | 8MHz HSE 负载电容 |
| C18 | 12pF NPO | 0603 | 8MHz HSE 负载电容 |
| C_NRST | 100nF | 0603 | 复位引脚滤波 |

### 电阻

| 位号 | 阻值 | 封装 | 用途 |
|------|------|------|------|
| R_SHUNT | 10mΩ/±1% | 0805 | 电流采样分流电阻 |
| R_SENSE+ | 0Ω | 0603 | Kelvin S+ 调试跳线 |
| R_SENSE- | 0Ω | 0603 | Kelvin S- 调试跳线 |
| R_VBUS | 100Ω | 0603 | INA226 VBUS 检测限流 |
| R_SCL | 4.7kΩ | 0603 | I²C SCL 上拉 |
| R_SDA | 4.7kΩ | 0603 | I²C SDA 上拉 |
| R_MODE | 10kΩ | 0603 | KEY_MODE 上拉 |
| R_CONFIRM | 10kΩ | 0603 | KEY_CONFIRM 上拉 |
| R_BOOT | 10kΩ | 0603 | BOOT0 下拉 |
| R_NRST | 10kΩ | 0603 | NRST 上拉 |
| R_CC1 | 5.1kΩ | 0603 | USB-C CC1 下拉 (Sink识别) |
| R_CC2 | 5.1kΩ | 0603 | USB-C CC2 下拉 (Sink识别) |

### 电感

| 位号 | 感值 | 封装 | 用途 |
|------|------|------|------|
| L1 | 10µH (600Ω@100MHz) | 0805 | VDDA LC 滤波 |

---

## 第五步：放置其他器件

| 位号 | 搜索词 | 说明 |
|------|--------|------|
| **OLED1** | `HS96L01W4S03` 或放置 1×7P 排母 | 0.96" 128×64 SPI OLED 模块 (GND/VCC/D0/D1/RES/DC/CS)，立创 C5139758 |
| **SW1** | `TS-1102S` | KEY_MODE 触觉按键 |
| **SW2** | `TS-1102S` | KEY_CONFIRM 触觉按键 |
| **SW3** | `TS-1102S` | KEY_BOOT 触觉按键（BOOT0 控制） |
| **SW4** | `TS-1102S` | KEY_RST 复位按键（NRST 控制） |

---

## 第六步：连线（按模块依次完成）

> 先连电源网络（VBUS / +3V3 / GND），再连信号网络。每连完一个网络，在立创 EDA 中用**网络标号 (Net Label)** 标注。

### 6.1 VBUS 网络（红色线，粗线）

```
USB-C VBUS (J1.VBUS)
  ├── CH224K.VBUS (Pin9)
  ├── HT7533S.IN
  ├── C1(+) / C2 → GND          ← VBUS 输入滤波
  ├── C13(+) / C14 → GND        ← CH224K 去耦
  ├── U5.Pin5 (VBUS ESD)        ← USBLC6-2SC6 VBUS 电源轨保护
  └── R_SHUNT.Pad1 (分流电阻 VBUS 侧)
```

### 6.2 VBUS_OUT 网络（分流电阻后 → USB-C 公头 → 被检测设备）

```
R_SHUNT.Pad2 (分流电阻负载侧)
  ├── USB-C.VBUS (J2.A4/A9/B4/B9) → 被检测设备供电
  ├── U6.Pin5 (VBUS ESD)   ← USBLC6-2SC6 VBUS 电源轨保护
  ├── R_CC1 (56kΩ) → J2.CC1 (A5)   ← Source Rp 上拉
  ├── R_CC2 (56kΩ) → J2.CC2 (B5)   ← Source Rp 上拉
  └── R_VBUS (100Ω) → INA226.VBUS (Pin2)
      └── C15 (0.1µF) → GND    ← VBUS 检测滤波
```

> ⚠️ CC1/CC2 的 56kΩ Rp 上拉至 VBUS_OUT 是 USB-C Source（DFP）规范要求。对端 Sink 检测到 Rp 后才会打开 VBUS 受电通路。56kΩ = Default USB Power（最大 3A）。

### 6.3 Kelvin Sense（四线开尔文接法—关键精度保证！）

```
R_SHUNT.Pad1 ── R_SENSE+ (0Ω) ── INA226.IN+ (Pin8)   ← Kelvin S+
R_SHUNT.Pad2 ── R_SENSE- (0Ω) ── INA226.IN- (Pin7)   ← Kelvin S-
```

> ⚠️ **PCB 布局注意：** Sense+ / Sense- 走线必须从分流焊盘两端独立引出（四线 Kelvin），**不要**把 Sense 线接在功率线上。这直接影响电流测量精度。

### 6.4 +3V3 网络

```
HT7533S.OUT
  ├── C3(+) / C4 → GND          ← 3.3V 输出滤波
  ├── L1 → C5(+) / C6 → GND     ← LC 滤波 → +3V3_ANA
  │   └── CH32V203.VDDA (Pin9)
  ├── CH32V203.VBAT (Pin1)
  ├── CH32V203.VDD_1 (Pin24) + C9 → GND
  ├── CH32V203.VDD_2 (Pin36) + C10 → GND
  ├── CH32V203.VDD_3 (Pin48) + C11 → GND
  │   + C12 → GND (VDD_3 额外去耦)
  ├── INA226.VS (Pin6) + C16 → GND
  ├── OLED1.VCC
  ├── J3.Pin4 (SWD 3.3V 参考)
  ├── R_NRST (10kΩ 上拉) → NRST
  ├── R_SCL (4.7kΩ 上拉) → I2C_SCL
  ├── R_SDA (4.7kΩ 上拉) → I2C_SDA
  ├── R_MODE (10kΩ 上拉) → KEY_MODE
  ├── R_CONFIRM (10kΩ 上拉) → KEY_CONFIRM
  └── SW3.PinA → KEY_BOOT (按下 = BOOT0 拉高至 +3V3)
```

### 6.5 GND 网络

所有以下引脚接地。**使用立创 EDA 的 GND 符号**统一标注：

- U1.GND, U2.VSSA, U2.VSS_1, U2.VSS_2, U2.VSS_3
- U3.GND (Pin5 + Pin8)
- U4.A0 (Pin1), U4.A1 (Pin10), U4.GND (Pin9)
- U5.Pin2, U6.Pin2
- J1.GND, J2.GND, J3.Pin3, J4.Pin3
- OLED1.GND
- C1~C6, C9~C18, C_NRST 的 GND 侧
- R_CC1, R_CC2 → GND 侧
- R_BOOT → GND (BOOT0 下拉)
- Y2.Pin3, Y2.Pin4 (HSE 晶振 GND 脚)
- C17, C18 的 GND 侧

### 6.6 NRST 复位网络

```
+3V3 ── R_NRST (10kΩ) ──┬── CH32V203.NRST (Pin7)
                         └── C_NRST (100nF) ── GND
```

### 6.7 USB D+/D- 差分信号（穿通 ESD）

```
USB-C.D+ (J1) ── U5.Pin1 (I/O1 IN) ──[内部穿通]── U5.Pin6 (I/O1 OUT) ── CH32V203.PA12 (Pin33)
USB-C.D- (J1) ── U5.Pin3 (I/O2 IN) ──[内部穿通]── U5.Pin4 (I/O2 OUT) ── CH32V203.PA11 (Pin32)
```

> 使用网络标号：`USB_DP` / `USB_DM`。在 PCB 中这对线需要 **90Ω 差分阻抗控制**。

### 6.8 USB-C 公头 D+/D- + VBUS + CC（ESD 保护 + Source 通告）

```
USB-C.D+ (J2.A6)  ── U6.Pin1 (I/O1 IN) ── U6.Pin6 NC (悬空)
USB-C.D- (J2.A7)  ── U6.Pin3 (I/O2 IN) ── U6.Pin4 NC (悬空)
USB-C.VBUS (J2.A4/A9/B4/B9) ── U6.Pin5 (VBUS)  ← VBUS_OUT 网络，ESD 电源轨保护

USB-C.CC1 (J2.A5) ── R_CC1 (56kΩ) ── VBUS_OUT  ← Source Rp 上拉
USB-C.CC2 (J2.B5) ── R_CC2 (56kΩ) ── VBUS_OUT  ← Source Rp 上拉

USB-C.GND (J2.A1/A12/B1/B12) ── GND
USB-C.B6/B7 (D+/D- B面) ── NC
USB-C SuperSpeed/SBU 引脚 ── 全部 NC
```

> USB-C 公头插入被检测设备 (DUT)，仅输出功率。D+/D- 不接 MCU，但保留 ESD 防护。U6.Pin5 接 VBUS_OUT（分流电阻负载侧），为 VBUS 线提供完整 ESD 保护路径（I/O→VBUS→GND 泄放回路）。Pin6/Pin4 悬空（D+/D- 不穿通到 MCU）。
>
> ⚠️ CC1/CC2 必须通过 56kΩ Rp 上拉至 VBUS_OUT，告知对端 Sink "我是 Source"。不加 Rp 则对端不会打开 VBUS 受电通路。USB 2.0 仅用 A 面 D+/D-（A6/A7），B 面（B6/B7）及 SuperSpeed 引脚全部 NC。

### 6.9 CC1/CC2（PD 协议 + Sink 识别）

```
USB-C.CC1 (J1) ──┬── CH224K.CC1 (Pin4)    ← PD 协议通信
                   └── R_CC1 (5.1kΩ) ── GND  ← Sink 识别

USB-C.CC2 (J1) ──┬── CH224K.CC2 (Pin3)    ← PD 协议通信 (可不接)
                   └── R_CC2 (5.1kΩ) ── GND  ← Sink 识别
```

> ⚠️ **CC1/CC2 的 5.1kΩ 下拉电阻是必须的！** 这告诉 USB-C 主机端这是一个 Sink 设备，电脑才会输出 VBUS 供电。不加 USB ISP 无法工作。

### 6.10 PD CFG 档位选择

```
CH32V203.PA2 (Pin12) ── CH224K.CFG1 (Pin6)    网络标号: CFG1
CH32V203.PA3 (Pin13) ── CH224K.CFG2 (Pin7)    网络标号: CFG2
CH32V203.PA4 (Pin14) ── CH224K.CFG3 (Pin10)   网络标号: CFG3
```

档位编码表：

| CFG3 | CFG2 | CFG1 | 请求电压 |
|------|------|------|----------|
| 0 | 0 | 0 | 5V |
| 0 | 0 | 1 | 9V |
| 0 | 1 | 0 | 12V |
| 0 | 1 | 1 | 15V |
| 1 | 0 | 0 | 20V |

### 6.11 I²C 总线（仅 INA226）

```
CH32V203.PB6 (Pin42) ──┬── INA226.SCL (Pin4)
                        └── R_SCL (4.7kΩ) ── +3V3

CH32V203.PB7 (Pin43) ──┬── INA226.SDA (Pin5)
                        └── R_SDA (4.7kΩ) ── +3V3
```

INA226 地址：A0=GND, A1=GND → 7-bit 地址 **0x40**

### 6.12 SPI OLED 显示屏（HS96L01W4S03）

OLED 模块使用 **SPI1** 接口，驱动芯片 SSD1315，分辨率 128×64。

**HS96L01W4S03 引脚定义（7-pin，从左到右）：**

| Pin | 名称 | 功能 | 连接 MCU 引脚 |
|-----|------|------|---------------|
| 1 | GND | 电源地 | GND |
| 2 | VCC | 电源正 (3.3V) | +3V3 |
| 3 | D0 (SCLK) | SPI 时钟 | PA5 (Pin15) — SPI1_SCK |
| 4 | D1 (MOSI) | SPI 数据输入 | PA7 (Pin17) — SPI1_MOSI |
| 5 | RES | 硬件复位（低有效） | PB0 (Pin18) — GPIO 输出 |
| 6 | DC | 数据/命令选择 | PB1 (Pin19) — GPIO 输出 |
| 7 | CS | 片选（低有效） | PA8 (Pin29) — GPIO 输出 |

**接线图：**

```
OLED1.Pin1 (GND)  ── GND
OLED1.Pin2 (VCC)  ── +3V3
OLED1.Pin3 (D0)   ── CH32V203.PA5 (Pin15, SPI1_SCK)
OLED1.Pin4 (D1)   ── CH32V203.PA7 (Pin17, SPI1_MOSI)
OLED1.Pin5 (RES)  ── CH32V203.PB0 (Pin18, GPIO_OUT)
OLED1.Pin6 (DC)   ── CH32V203.PB1 (Pin19, GPIO_OUT)
OLED1.Pin7 (CS)   ── CH32V203.PA8 (Pin29, GPIO_OUT)
```

**去耦电容：** OLED1.VCC 引脚旁放 **100nF (C_OLED)** 到 GND。

> ⚠️ PA6 (SPI1_MISO, Pin16) **不连接**（NC）。SSD1315 OLED 为只写设备，无 MISO 输出。PA6 可留作 GPIO 预留。

> 💡 **SPI 模式：** 使用 SPI1 硬件外设（Mode 0: CPOL=0, CPHA=0），时钟频率建议 ≤10MHz。RES/DC/CS 三个控制引脚用 GPIO 软件控制。

### 6.13 按键（4 个）

**SW1 — KEY_MODE（模式切换）：**
```
+3V3 ── R_MODE (10kΩ) ──┬── CH32V203.PA0 (Pin10)
                         └── SW1 ── GND
```
逻辑：松开 → PA0 = HIGH；按下 → PA0 = LOW（下拉到 GND）。

**SW2 — KEY_CONFIRM（确认）：**
```
+3V3 ── R_CONFIRM (10kΩ) ──┬── CH32V203.PA1 (Pin11)
                            └── SW2 ── GND
```
逻辑：同 SW1。

**SW3 — KEY_BOOT（进入 USB Bootloader）：**
```
+3V3 ── SW3 ──┬── CH32V203.BOOT0 (Pin44)
               └── R_BOOT (10kΩ) ── GND
```
逻辑：松开 → R_BOOT 拉低 BOOT0 = Flash 正常启动；按下 → BOOT0 拉高 = 进入 USB Bootloader。

**SW4 — KEY_RST（硬件复位）：**
```
+3V3 ── R_NRST (10kΩ) ──┬── CH32V203.NRST (Pin7) ── C_NRST (100nF) ── GND
                          │
                          └── SW4 ── GND
```
逻辑：正常运行时 NRST 被 R_NRST 上拉到 3.3V，C_NRST 滤除瞬态干扰；按下 SW4 → NRST 拉低 → MCU 复位。

> **按键布局：** 4 个按键横向排列，SW3(BOOT) 和 SW4(RST) 靠板边放置，便于单指操作且防止误触。SW1(MODE) 和 SW2(CONFIRM) 居中放置。

### 6.14 SWD 调试口

```
J3.Pin1 (SWCLK) ── CH32V203.PA14 (Pin37)
J3.Pin2 (SWDIO) ── CH32V203.PA13 (Pin34)
J3.Pin3 (GND)   ── GND
J3.Pin4 (3.3V)  ── +3V3
```

### 6.15 UART 调试串口

```
J4.Pin1 (TX)  ── CH32V203.PA9 (Pin30)    网络标号: UART_TX
J4.Pin2 (RX)  ── CH32V203.PA10 (Pin31)   网络标号: UART_RX
J4.Pin3 (GND) ── GND
```

> 仅 3-pin (TX/RX/GND)，不对外供电。波特率 115200 8N1。

### 6.16 晶振电路

```
CH32V203.OSC_IN (Pin5)
  ├── Y2.Pin1 (8MHz)
  └── C17 (12pF) ── GND

CH32V203.OSC_OUT (Pin6)
  ├── Y2.Pin2 (8MHz)
  └── C18 (12pF) ── GND

Y2.Pin3 ── GND
Y2.Pin4 ── GND

CH32V203.PC14 (Pin3) ── NC (预留 GPIO)
CH32V203.PC15 (Pin4) ── NC (预留 GPIO)
```

> HSE 晶振必须靠近 MCU Pin5/Pin6 放置，走线 <10mm，周圈包 GND 护环。PC14/PC15 为预留 GPIO，不做连接。

---

## 第七步：放置电源符号和 GND 符号

在立创 EDA 中使用工具栏中的：
- **VCC 符号** → 标注 `+3V3`
- **GND 符号** → 所有接地点
- 可选：**VBUS 电源端口**（Power Flag），用于 ERC 检查

---

## 第八步：检查和验证

完成连线后，运行以下检查：

| 检查项 | 方法 |
|--------|------|
| ERC (电气规则检查) | 立创 EDA → 设计 → 电气规则检查 (ERC) |
| 单网络高亮 | 点击网络标号，确认连通性与预期一致 |
| 未连接引脚 | ERC 会报告浮空输入引脚，逐一确认 |
| BOM 一致性 | 设计 → BOM 导出，对比 `03-components.md` 中的位号和型号 |

### 关键交叉检查清单

- [ ] CH32V203 所有 VDD 引脚 (×4) 均接 +3V3 + 100nF 去耦
- [ ] CH32V203 所有 VSS 引脚 (×4) 均接 GND
- [ ] VDDA 经 LC 滤波 (L1 + C5//C6) 后接 +3V3_ANA
- [ ] INA226 A0/A1 均接 GND（地址 0x40）
- [ ] INA226 ALERT (Pin3) 悬空
- [ ] CH224K NC1/NC2 (Pin1/Pin2) 悬空
- [ ] CC1/CC2 均接 5.1kΩ 下拉至 GND
- [ ] D+/D- 经 U5 (USBLC6-2SC6) 穿通后到 MCU PA11/PA12
- [ ] USB-C 公头 U6 (USBLC6-2SC6) Pin5 接 VBUS_OUT（J2 VBUS 侧），Pin6/Pin4 悬空
- [ ] J2 CC1(A5)/CC2(B5) 各经 56kΩ Rp 上拉至 VBUS_OUT（Source 通告）
- [ ] J2 SuperSpeed (TX/RX)、SBU、B 面 D+/D- 全部 NC
- [ ] BOOT0 有 10kΩ 下拉 + SW3 上拉至 +3V3
- [ ] NRST 有 10kΩ 上拉 + 100nF 滤波电容 + SW4 下拉至 GND
- [ ] HSE 晶振 Y2 Pin3/Pin4 接地
- [ ] I²C 总线 SCL/SDA 各有 4.7kΩ 上拉至 +3V3（仅 INA226，无 OLED）
- [ ] OLED SPI：D0→PA5, D1→PA7, RES→PB0, DC→PB1, CS→PA8，VCC 旁 100nF 去耦
- [ ] OLED PA6 (MISO) 不连接（NC）
- [ ] 分流电阻采用 Kelvin 四线接法

---

## 模块布局建议（原理图页面）

```
 ┌──────────────────────────────────────────────────────────────┐
 │  [USB-C J1]──[U5 ESD]──[U3 CH224K]                           │
 │  左侧入口        (D+/D-穿通)   (PD触发, 中上)                   │
 │     │                                                         │
 │     ├── [R_SHUNT 分流] ── [U4 INA226] ── [U2 CH32V203 MCU] ──┤
 │     │    (中左, Kelvin)     (中, 电流检测)   (中央, 主控)       │
 │     │                                                    │    │
 │     ├── [U1 HT7533S]                                     │    │
 │     │    (左下, 3.3V LDO)                                 │    │
 │     │                                                     │    │
 │     ├── [OLED1 SPI 7-pin]                                   │    │
 │     │    (顶部, 竖装或局部加宽, 见 04-constraints 3.2)      │    │
 │     │    D0→PA5, D1→PA7, RES→PB0, DC→PB1, CS→PA8          │    │
 │     │                                                     │    │
 │     ├── [SW1 MODE][SW2 CONF]  2×2 按键矩阵                │    │
 │     │   [SW3 BOOT][SW4 RST ]  (底部, 占 12×8mm)           │    │
 │     │                                                     │    │
 │     └── [J3 SWD][J4 UART] 调试口 ── [J2 USB-C 公头→DUT]   │    │
 │          (底部)                       (右侧, SMD)           │    │
 └──────────────────────────────────────────────────────────────┘
```

---

## BOM 导出注意

在立创 EDA 中导出 BOM 时，确认以下器件的**立创商城编号**已正确关联：

| 位号 | 立创编号 | 备注 |
|------|----------|------|
| U1 | C347215 | HT7533S |
| U2 | C3001172 | CH32V203C8T6 |
| U3 | C970725 | CH224K |
| U4 | C49851 | INA226AIDGSR |
| Y2 | C49158084 | 8MHz HSE 晶振 |
| U5, U6 | C7829 | USBLC6-2SC6 |
| OLED1 | C5139758 | HS96L01W4S03 0.96" SPI OLED 128×64 |
| SW1~SW4 | 搜 `TS-1102S` | 4 个触觉按键 (MODE/CONFIRM/BOOT/RST) |
| J1 | C2765186 | USB-C 16P 卧贴 |
| J2 | 搜 `USB-C 公头 24P` | USB-C 公头，插入被检测设备 (DUT)，CC1/CC2 各 56kΩ 上拉 |

无源器件可使用立创 EDA 基础库器件，投板前替换为立创商城编号对应器件以确保封装正确。

---

## 参考资料

- CH32V203 数据手册：`docs/hardware/datasheets/C3001172_*.PDF`
- CH224K 数据手册：参考 `03-components.md` 中链接
- INA226 数据手册：参考 `03-components.md` 中链接
- 完整 BOM + 采购链接：`03-components.md`
- 完整约束 + PCB 要求：`04-constraints.md`
