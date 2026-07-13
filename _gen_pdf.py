#!/usr/bin/env python3
"""Generate hardware-solution.pdf from hardware-solution.md with Chinese font."""
import re, os

from fpdf import FPDF

MD_FILE = os.path.join(os.path.dirname(__file__), "hardware-solution.md")
PDF_OUT = os.path.join(os.path.dirname(__file__), "hardware-solution.pdf")

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=14)
pdf.set_left_margin(16)
pdf.set_right_margin(16)

# Register fonts
pdf.add_font("CN",  "", "C:/Windows/Fonts/Noto Sans SC (TrueType).otf")
pdf.add_font("CNB", "", "C:/Windows/Fonts/Noto Sans SC Bold (TrueType).otf")
# Italic fallback
pdf.add_font("CNI", "", "C:/Windows/Fonts/Noto Sans SC (TrueType).otf")


def clean_md(line: str) -> str:
    """Remove markdown formatting, return stripped text."""
    line = line.strip()
    if not line:
        return ""
    line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
    line = re.sub(r'\*(.+?)\*', r'\1', line)
    line = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)
    line = re.sub(r'>\s?', '', line)
    line = re.sub(r'`([^`]+)`', r'\1', line)
    return line


# ============== COVER PAGE ==============
pdf.add_page()
pdf.ln(50)
pdf.set_font("CNB", "", 24)
pdf.set_text_color(27, 79, 114)
pdf.cell(0, 10, "USB PD 多功能测试仪", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("CN", "", 13)
pdf.set_text_color(110, 110, 110)
pdf.cell(0, 8, "硬件方案报告", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)
pdf.set_draw_color(27, 79, 114)
pdf.set_line_width(0.5)
pdf.line(55, pdf.get_y(), pdf.w - 55, pdf.get_y())
pdf.ln(8)
pdf.set_font("CN", "", 9.5)
pdf.set_text_color(120, 120, 120)
cover_lines = [
    "全沁恒国产芯片架构 | RISC-V MCU | 硬件 PD 触发 | 高精度测量",
    "",
    "比赛: 立创开源硬件平台 - AI 创意硬件挑战征集令",
    "平台: 沁恒 CH32V203C8T6 + 嘉立创 EDA 专业版",
    "BOM 核心成本 <= 60 元 | 全部器件立创商城可采购",
    "2026-07-12",
]
for t in cover_lines:
    pdf.cell(0, 7, t, align="C", new_x="LMARGIN", new_y="NEXT")

# ============== CONTENT ==============
with open(MD_FILE, 'r', encoding='utf-8') as f:
    md_text = f.read()

lines = md_text.split('\n')
i = 0
n = len(lines)

while i < n:
    raw = lines[i]
    s = raw.strip()

    # blank
    if not s:
        pdf.ln(1.5)
        i += 1
        continue

    # --- Horizontal rule ---
    if s.startswith('---'):
        pdf.ln(1)
        y = pdf.get_y()
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(2)
        i += 1
        continue

    # --- H1 section (page break) ---
    m = re.match(r'^#\s+(.+)', s)
    if m:
        pdf.add_page()
        title = clean_md(m.group(1))
        pdf.set_font("CNB", "", 16)
        pdf.set_text_color(27, 79, 114)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(27, 79, 114)
        pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y() + 1.5, pdf.w - pdf.r_margin, pdf.get_y() + 1.5)
        pdf.ln(5)
        i += 1
        continue

    # --- H2 ---
    m = re.match(r'^##\s+(.+)', s)
    if m:
        pdf.ln(3)
        pdf.set_font("CNB", "", 12.5)
        pdf.set_text_color(30, 130, 80)
        pdf.cell(0, 6, clean_md(m.group(1)), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        i += 1
        continue

    # --- H3 ---
    m = re.match(r'^###\s+(.+)', s)
    if m:
        pdf.ln(2.5)
        pdf.set_font("CNB", "", 11)
        pdf.set_text_color(46, 134, 193)
        pdf.cell(0, 5.5, clean_md(m.group(1)), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
        i += 1
        continue

    # --- Table separator ---
    if s.startswith('|---') or s.startswith('| --'):
        i += 1
        continue

    # --- Table row ---
    if s.startswith('|') and s.endswith('|'):
        cells_raw = [c.strip() for c in s.split('|')[1:-1]]
        cells = [clean_md(c) for c in cells_raw]
        ncols = len(cells)
        if ncols == 0:
            i += 1
            continue

        # Is this a header row? (next line is separator)
        next_s = lines[i+1].strip() if i+1 < len(lines) else ""
        is_header = next_s.startswith('|---') or next_s.startswith('| --')

        font_size = 7.2
        pdf.set_font("CNB" if is_header else "CN", "", font_size)

        if is_header:
            pdf.set_fill_color(27, 79, 114)
            pdf.set_text_color(255, 255, 255)
        else:
            pdf.set_text_color(55, 55, 55)

        usable = pdf.epw
        col_w = [usable / ncols] * ncols

        row_h = 5.2
        y_before = pdf.get_y()

        # Check page break
        if y_before + row_h > pdf.h - pdf.b_margin:
            pdf.add_page()
            if is_header:
                pdf.set_fill_color(27, 79, 114)
                pdf.set_text_color(255, 255, 255)
            else:
                pdf.set_text_color(55, 55, 55)
            pdf.set_font("CNB" if is_header else "CN", "", font_size)
            y_before = pdf.get_y()

        for j, cell in enumerate(cells):
            x = pdf.l_margin + j * col_w[j]
            pdf.set_xy(x, y_before)
            if is_header:
                pdf.cell(col_w[j], row_h, cell, border=0, fill=True, align='L')
            else:
                pdf.cell(col_w[j], row_h, cell, border=0, align='L')

        pdf.set_y(y_before + row_h)

        # thin separator line
        if not is_header:
            pdf.set_draw_color(220, 220, 220)
            pdf.set_line_width(0.08)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(0.8)
        i += 1
        continue

    # --- Bullet list - or * ---
    m = re.match(r'^[-*]\s+(.+)', s)
    if m:
        pdf.set_font("CN", "", 9)
        pdf.set_text_color(55, 55, 55)
        text = clean_md(m.group(1))
        bullet_x = pdf.l_margin + 4
        text_w = pdf.epw - 4
        pdf.set_x(bullet_x)
        pdf.cell(3, 4.8, chr(0x2022))
        pdf.set_x(bullet_x + 3)
        pdf.multi_cell(text_w, 4.8, text)
        i += 1
        continue

    # --- Code block/ASCII art ---
    if s.startswith('```') or s.startswith('    '):
        # Skip code blocks in PDF (they don't render well)
        while i < n and (lines[i].strip().startswith('```') or not lines[i].strip()):
            i += 1
        i += 1
        continue

    # --- Normal paragraph ---
    text = clean_md(s)
    if not text:
        i += 1
        continue

    # Skip ASCII art lines
    if text and (text[0] in '┌└├┘┐│─╔╚═'):
        i += 1
        continue

    pdf.set_font("CN", "", 9)
    pdf.set_text_color(55, 55, 55)
    pdf.multi_cell(0, 4.8, text, align='L')
    i += 1

# ============== SAVE ==============
pdf.output(PDF_OUT)
print(f"[OK] PDF saved: {PDF_OUT}")
print(f"[OK] Pages: {pdf.pages_count}")
