#!/usr/bin/env python3
"""Generate hardware-solution.pdf by merging all .md files with fpdf2 + OTF Chinese font."""

import os, re, textwrap
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_OUT = os.path.join(OUT_DIR, "hardware-solution.pdf")

FONT_REGULAR = "C:/Windows/Fonts/Noto Sans SC (TrueType).otf"
FONT_BOLD    = "C:/Windows/Fonts/Noto Sans SC Bold (TrueType).otf"

# ── Collect all .md files in sorted order ──
md_files = sorted(
    [f for f in os.listdir(OUT_DIR) if f.endswith('.md') and f != 'hardware-solution.md'],
    key=lambda x: x
)
md_files.append("hardware-solution.md")  # put summary last

# ── PDF setup ──
class HWPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(True, 14)
        self.set_left_margin(16)
        self.set_right_margin(16)
        self.add_font("CN",  "", FONT_REGULAR)
        self.add_font("CNB", "", FONT_BOLD)
        # colours
        self.C_PRIMARY = (15, 118, 110)      # teal-green
        self.C_H2      = (30, 132, 73)
        self.C_H3      = (46, 134, 193)
        self.C_BODY    = (44, 62, 80)
        self.C_GREY    = (100, 100, 100)
        self.C_CODE_BG = (253, 242, 233)
        self.C_THEAD   = (15, 118, 110)
        self.C_WHITE   = (255, 255, 255)
        self.C_ROW_SEP = (220, 220, 220)
        self.C_BQ_BG   = (245, 245, 245)
        self.C_BQ_BAR  = (15, 118, 110)
        self.page_count = 0

    def header(self):
        pass  # handled by footer only

    def footer(self):
        self.set_y(-12)
        self.set_font("CN", "", 7)
        self.set_text_color(*self.C_GREY)
        self.set_draw_color(*self.C_PRIMARY)
        self.set_line_width(0.15)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        self.cell(0, 4, f"USB PD 多功能测试仪 — 硬件方案报告    第 {self.page_no()} 页", align='C')

    def cover_page(self):
        self.add_page()
        self.ln(50)
        self.set_font("CNB", "", 26)
        self.set_text_color(*self.C_PRIMARY)
        self.cell(0, 11, "USB PD 多功能测试仪", align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font("CN", "", 13)
        self.set_text_color(*self.C_GREY)
        self.cell(0, 8, "硬件方案报告", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_draw_color(*self.C_PRIMARY)
        self.set_line_width(0.4)
        self.line(55, self.get_y(), self.w - 55, self.get_y())
        self.ln(6)
        self.set_font("CN", "", 9)
        self.set_text_color(120, 120, 120)
        for t in [
            "全沁恒国产芯片架构 | RISC-V MCU | 硬件 PD 触发 | 高精度测量",
            "",
            "比赛: 立创开源硬件平台 — AI 创意硬件挑战征集令",
            "平台: 沁恒 CH32V203C8T6 + 嘉立创 EDA 专业版",
            "BOM 核心成本 ≤ ¥60 | 全部器件立创商城可采购",
            f"2026-07-13",
        ]:
            self.cell(0, 6.5, t, align='C', new_x="LMARGIN", new_y="NEXT")

pdf = HWPDF()

# ══════════════ COVER ══════════════
pdf.cover_page()

# ══════════════ CONTENT ══════════════
for md_file in md_files:
    path = os.path.join(OUT_DIR, md_file)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    i = 0
    n = len(lines)
    in_code_block = False
    in_ascii_art = False

    while i < n:
        raw = lines[i]
        s = raw.rstrip()

        # code block fence
        if s.startswith('```'):
            in_code_block = not in_code_block
            i += 1
            continue
        if in_code_block:
            i += 1
            continue

        # blank
        if not s.strip():
            pdf.ln(1.5)
            i += 1
            continue

        # --- hr ---
        if s.strip().startswith('---') and len(s.strip()) <= 5:
            pdf.ln(1)
            y = pdf.get_y()
            pdf.set_draw_color(210, 210, 210)
            pdf.set_line_width(0.15)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(2)
            i += 1
            continue

        # ASCII art lines
        if any(c in s for c in '┌└├┘┐│─╔╚═╗╝║╠╣╦╩'):
            i += 1
            continue

        # --- H1 ---
        m = re.match(r'^#\s+(.+)', s)
        if m:
            pdf.add_page()
            pdf.set_font("CNB", "", 16)
            pdf.set_text_color(*pdf.C_PRIMARY)
            pdf.cell(0, 7, m.group(1).strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*pdf.C_PRIMARY)
            pdf.set_line_width(0.35)
            pdf.line(pdf.l_margin, pdf.get_y() + 1.5, pdf.w - pdf.r_margin, pdf.get_y() + 1.5)
            pdf.ln(5)
            i += 1
            continue

        # --- H2 ---
        m = re.match(r'^##\s+(.+)', s)
        if m:
            pdf.ln(3)
            pdf.set_font("CNB", "", 12.5)
            pdf.set_text_color(*pdf.C_H2)
            pdf.cell(0, 6, m.group(1).strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            i += 1
            continue

        # --- H3 ---
        m = re.match(r'^###\s+(.+)', s)
        if m:
            pdf.ln(2.5)
            pdf.set_font("CNB", "", 10.5)
            pdf.set_text_color(*pdf.C_H3)
            pdf.cell(0, 5.5, m.group(1).strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1.5)
            i += 1
            continue

        # --- Table (skip separator rows) ---
        if re.match(r'^\|[\s\-:|]+\|$', s):
            i += 1
            continue

        if s.startswith('|') and s.endswith('|'):
            cells_raw = [c.strip() for c in s.split('|')[1:-1]]
            cells = [re.sub(r'\*\*(.+?)\*\*', r'\1', c) for c in cells_raw]
            cells = [re.sub(r'\*(.+?)\*', r'\1', c) for c in cells]
            cells = [re.sub(r'\[(.+?)\]\(.+?\)', r'\1', c) for c in cells]
            cells = [re.sub(r'`([^`]+)`', r'\1', c) for c in cells]
            ncols = len(cells)
            if ncols == 0:
                i += 1
                continue

            next_s = lines[i+1].strip() if i+1 < n else ""
            is_header = bool(re.match(r'^\|[\s\-:|]+\|$', next_s))

            fs = 6.5
            pdf.set_font("CNB" if is_header else "CN", "", fs)

            if is_header:
                pdf.set_fill_color(*pdf.C_THEAD)
                pdf.set_text_color(*pdf.C_WHITE)
            else:
                pdf.set_text_color(*pdf.C_BODY)

            usable = pdf.w - pdf.l_margin - pdf.r_margin
            col_w = usable / ncols
            row_h = 4.8
            y0 = pdf.get_y()

            if y0 + row_h > pdf.h - pdf.b_margin:
                pdf.add_page()
                y0 = pdf.get_y()

            for j, cell in enumerate(cells):
                pdf.set_xy(pdf.l_margin + j * col_w, y0)
                if is_header:
                    pdf.cell(col_w, row_h, cell[:40], border=0, fill=True, align='L')
                else:
                    pdf.cell(col_w, row_h, cell[:45], border=0, align='L')

            pdf.set_y(y0 + row_h)
            if not is_header:
                pdf.set_draw_color(*pdf.C_ROW_SEP)
                pdf.set_line_width(0.06)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(0.6)
            i += 1
            continue

        # --- Blockquote ---
        if s.startswith('>'):
            # collect contiguous blockquote lines
            bq_lines = []
            while i < n and lines[i].strip().startswith('>'):
                bq_lines.append(re.sub(r'^>\s?', '', lines[i].strip()))
                i += 1
            text = ' '.join(bq_lines)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
            text = re.sub(r'`([^`]+)`', r'\1', text)
            pdf.ln(1)
            pdf.set_fill_color(*pdf.C_BQ_BG)
            pdf.set_draw_color(*pdf.C_BQ_BAR)
            pdf.set_line_width(0.6)
            bx = pdf.l_margin + 2
            bw = pdf.w - pdf.r_margin - bx - 2
            by0 = pdf.get_y()
            pdf.set_font("CN", "", 8)
            pdf.set_text_color(80, 80, 80)
            pdf.set_x(bx + 3)
            pdf.multi_cell(bw - 3, 4.2, text)
            pdf.set_draw_color(*pdf.C_BQ_BAR)
            pdf.line(bx, by0, bx, pdf.get_y())
            pdf.ln(1)
            continue

        # --- Bullet ---
        m = re.match(r'^[-*]\s+(.+)', s)
        if m:
            text = m.group(1)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
            text = re.sub(r'`([^`]+)`', r'\1', text)
            pdf.set_font("CN", "", 8.5)
            pdf.set_text_color(*pdf.C_BODY)
            bx = pdf.l_margin + 4
            bw = pdf.w - pdf.r_margin - bx
            pdf.set_x(bx)
            pdf.cell(3, 4.5, "•")
            pdf.set_x(bx + 3)
            pdf.multi_cell(bw - 3, 4.5, text)
            i += 1
            continue

        # --- Normal paragraph ---
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', s.strip())
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'^>\s?', '', text)

        if not text.strip():
            i += 1
            continue

        pdf.set_font("CN", "", 8.5)
        pdf.set_text_color(*pdf.C_BODY)
        txt_w = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.set_x(pdf.l_margin)
        try:
            pdf.multi_cell(txt_w, 4.6, text, align='L')
        except Exception:
            for chunk in [text[j:j+100] for j in range(0, len(text), 100)]:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(txt_w, 4.6, chunk, align='L')
        i += 1

# ══════════════ SAVE ══════════════
pdf.output(PDF_OUT)
size_kb = os.path.getsize(PDF_OUT) / 1024
print(f"[OK] PDF saved: {PDF_OUT}")
print(f"[OK] Pages: {pdf.page_no()}, Size: {size_kb:.0f} KB")
print(f"[OK] Files merged: {len(md_files)}")
