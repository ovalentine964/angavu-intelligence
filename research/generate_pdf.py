#!/usr/bin/env python3
"""
Angavu Intelligence Research Compendium — PDF Generator
Generates a thesis-grade PDF from 10 research reports.
Author: Valentine Owuor — BSc Economics & Statistics, Masinde Muliro University
Date: July 2026
"""

import os
import re
import textwrap
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable,
    Image, NextPageTemplate, PageTemplate, Frame,
    BaseDocTemplate, Flowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.graphics import renderPDF
from io import BytesIO

# ─── Configuration ───────────────────────────────────────────────────
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "ANGAVU_INTELLIGENCE_RESEARCH_COMPENDIUM.pdf")
RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

# Colors
PRIMARY = HexColor("#1a3a5c")      # Dark navy
SECONDARY = HexColor("#2c5f8a")    # Medium blue
ACCENT = HexColor("#d4a843")       # Gold
LIGHT_BG = HexColor("#f5f5f0")     # Light cream
TABLE_HEADER = HexColor("#1a3a5c")
TABLE_ALT = HexColor("#eef2f7")
BORDER_COLOR = HexColor("#cccccc")

# ─── Styles ──────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_styles():
    s = {}
    s['title'] = ParagraphStyle(
        'CompTitle', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=white, alignment=TA_CENTER, spaceAfter=12
    )
    s['subtitle'] = ParagraphStyle(
        'CompSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18,
        textColor=HexColor("#e0e0e0"), alignment=TA_CENTER, spaceAfter=6
    )
    s['author'] = ParagraphStyle(
        'CompAuthor', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=HexColor("#cccccc"), alignment=TA_CENTER
    )
    s['h1'] = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=20, leading=26,
        textColor=PRIMARY, spaceBefore=24, spaceAfter=12,
        borderWidth=0, borderPadding=0
    )
    s['h2'] = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=15, leading=20,
        textColor=SECONDARY, spaceBefore=18, spaceAfter=8
    )
    s['h3'] = ParagraphStyle(
        'H3', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=PRIMARY, spaceBefore=12, spaceAfter=6
    )
    s['body'] = ParagraphStyle(
        'CompBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=black, alignment=TA_JUSTIFY,
        spaceBefore=4, spaceAfter=4
    )
    s['body_bold'] = ParagraphStyle(
        'CompBodyBold', parent=s['body'],
        fontName='Helvetica-Bold'
    )
    s['quote'] = ParagraphStyle(
        'CompQuote', parent=s['body'],
        fontName='Helvetica-Oblique', fontSize=10, leading=14,
        leftIndent=20, rightIndent=20, textColor=HexColor("#444444"),
        spaceBefore=8, spaceAfter=8, borderWidth=1, borderColor=ACCENT,
        borderPadding=(8, 8, 8, 12)
    )
    s['bullet'] = ParagraphStyle(
        'CompBullet', parent=s['body'],
        leftIndent=20, bulletIndent=8, spaceBefore=2, spaceAfter=2
    )
    s['toc_h1'] = ParagraphStyle(
        'TOCH1', fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=PRIMARY, leftIndent=0, spaceBefore=8, spaceAfter=2
    )
    s['toc_h2'] = ParagraphStyle(
        'TOCH2', fontName='Helvetica', fontSize=10, leading=14,
        textColor=black, leftIndent=20, spaceBefore=2, spaceAfter=2
    )
    s['footer'] = ParagraphStyle(
        'Footer', fontName='Helvetica', fontSize=8, leading=10,
        textColor=grey, alignment=TA_CENTER
    )
    s['header'] = ParagraphStyle(
        'Header', fontName='Helvetica', fontSize=8, leading=10,
        textColor=grey, alignment=TA_RIGHT
    )
    s['table_header'] = ParagraphStyle(
        'TableHeader', fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=white, alignment=TA_CENTER
    )
    s['table_cell'] = ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=black, alignment=TA_LEFT
    )
    s['table_cell_center'] = ParagraphStyle(
        'TableCellCenter', parent=s['table_cell'], alignment=TA_CENTER
    )
    return s

S = make_styles()


# ─── Helper Functions ────────────────────────────────────────────────

def clean_md(text):
    """Strip markdown syntax, return plain text suitable for Paragraph."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9">\1</font>', text)
    text = text.replace('&', '&amp;').replace('<b>', '«B»').replace('</b>', '«/B»')
    text = text.replace('<i>', '«I»').replace('</i>', '«/I»')
    text = text.replace('<font', '«FONT').replace('/>', '/»')
    # Restore
    text = text.replace('«B»', '<b>').replace('«/B»', '</b>')
    text = text.replace('«I»', '<i>').replace('«/I»', '</i>')
    text = text.replace('«FONT', '<font').replace('/»', '/>')
    return text.strip()


def escape_para(text):
    """Escape XML special chars but preserve our tags."""
    # First protect our formatting tags
    protected = text
    tags = re.findall(r'</?[bi]>|<font[^>]*>|</font>', protected)
    for i, tag in enumerate(tags):
        protected = protected.replace(tag, f'§TAG{i}§')
    protected = protected.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    for i, tag in enumerate(tags):
        protected = protected.replace(f'§TAG{i}§', tag)
    return protected


def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    header_cells = [Paragraph(escape_para(str(h)), S['table_header']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(escape_para(str(c)), S['table_cell']) for c in row])

    if col_widths is None:
        n = len(headers)
        col_widths = [CONTENT_W / n] * n

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    # Alternate row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t


class HRule(Flowable):
    """Horizontal rule."""
    def __init__(self, width=CONTENT_W, thickness=1, color=BORDER_COLOR):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.color = color
    def wrap(self, aW, aH):
        return (self.width, self.thickness + 4)
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 2, self.width, 2)


def draw_cover_page(canvas, doc):
    """Draw full-page cover on first page."""
    canvas.saveState()
    c = canvas
    # Background
    c.setFillColor(PRIMARY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold accent bar
    c.setFillColor(ACCENT)
    c.rect(0, PAGE_H * 0.42, PAGE_W, 4, fill=1, stroke=0)

    # Title
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 30)
    title = "Angavu Intelligence"
    c.drawCentredString(PAGE_W / 2, PAGE_H * 0.62, title)

    c.setFont('Helvetica', 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H * 0.56,
                       "AI for Africa's Informal Economy")

    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H * 0.50,
                       "Research Compendium")

    # Author block
    c.setFillColor(HexColor("#e0e0e0"))
    c.setFont('Helvetica', 12)
    y = PAGE_H * 0.34
    c.drawCentredString(PAGE_W / 2, y, "Valentine Owuor")
    y -= 20
    c.setFont('Helvetica', 11)
    c.drawCentredString(PAGE_W / 2, y,
                       "BSc Economics & Statistics")
    y -= 18
    c.drawCentredString(PAGE_W / 2, y,
                       "Masinde Muliro University of Science and Technology")
    y -= 30
    c.setFont('Helvetica', 11)
    c.drawCentredString(PAGE_W / 2, y, "July 2026")

    # Footer
    c.setFillColor(HexColor("#888888"))
    c.setFont('Helvetica', 9)
    c.drawCentredString(PAGE_W / 2, MARGIN,
                       "A comprehensive research document integrating AI development analysis, "
                       "degree unit mapping, and strategic positioning for Africa's 600M+ informal workers.")
    canvas.restoreState()


def header_footer(canvas, doc):
    """Draw header and footer on each page."""
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - MARGIN + 8, PAGE_W - MARGIN, PAGE_H - MARGIN + 8)

    # Header text
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(grey)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 14,
                          "Angavu Intelligence — Research Compendium")

    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(grey)
    canvas.drawCentredString(PAGE_W / 2, MARGIN - 14, f"— {doc.page} —")

    # Footer line
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.line(MARGIN, MARGIN - 4, PAGE_W - MARGIN, MARGIN - 4)
    canvas.restoreState()


# ─── Content Parsing ─────────────────────────────────────────────────

def parse_md_sections(filepath):
    """Parse a markdown file into structured sections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove markdown TOC links like [text](#anchor)
    text = re.sub(r'\[([^\]]+)\]\(#[^)]+\)', r'\1', text)

    lines = text.split('\n')
    sections = []
    current = {'level': 0, 'title': '', 'content': []}

    for line in lines:
        # Detect headings
        m = re.match(r'^(#{1,4})\s+(.+)$', line)
        if m:
            if current['content'] or current['title']:
                sections.append(current)
            level = len(m.group(1))
            title = m.group(2).strip()
            title = re.sub(r'\*\*([^*]+)\*\*', r'\1', title)
            title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
            current = {'level': level, 'title': title, 'content': []}
        else:
            current['content'].append(line)

    if current['content'] or current['title']:
        sections.append(current)

    return sections


def md_to_flowables(filepath, title_prefix=""):
    """Convert a markdown file to reportlab flowables."""
    sections = parse_md_sections(filepath)
    flowables = []

    for sec in sections:
        title = sec['title']
        level = sec['level']
        content = '\n'.join(sec['content']).strip()

        # Skip empty sections or table of contents
        if not title and not content:
            continue
        if title.lower().startswith('table of contents'):
            continue
        if title.lower().startswith('appendix') and not content:
            continue

        # Add heading
        if title:
            if level == 1:
                flowables.append(Paragraph(escape_para(title), S['h1']))
                flowables.append(HRule())
            elif level == 2:
                flowables.append(Paragraph(escape_para(title), S['h2']))
            elif level == 3:
                flowables.append(Paragraph(escape_para(title), S['h3']))
            else:
                flowables.append(Paragraph(escape_para(title), S['body_bold']))

        # Process content
        if content:
            flowables.extend(process_content(content))

    return flowables


def process_content(content):
    """Convert markdown content block to flowables."""
    result = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            result.append(HRule())
            i += 1
            continue

        # Table detection
        if '|' in line and i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i+1].strip()):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            result.append(parse_table(table_lines))
            continue

        # Bullet lists
        m = re.match(r'^(\s*)[-*•]\s+(.+)$', line)
        if m:
            bullet_text = clean_md(m.group(2))
            result.append(Paragraph(
                f"• {escape_para(bullet_text)}", S['bullet']
            ))
            i += 1
            continue

        # Numbered lists
        m = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if m:
            list_text = clean_md(m.group(2))
            result.append(Paragraph(
                f"• {escape_para(list_text)}", S['bullet']
            ))
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            quote_text = line.strip().lstrip('> ').strip()
            quote_text = clean_md(quote_text)
            result.append(Paragraph(escape_para(quote_text), S['quote']))
            i += 1
            continue

        # Code blocks (skip)
        if line.strip().startswith('```'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            i += 1
            continue

        # Regular paragraph
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') \
                and not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*') \
                and '|' not in lines[i] and not lines[i].strip().startswith('>') \
                and not re.match(r'^\d+\.', lines[i].strip()):
            para_lines.append(lines[i])
            i += 1

        para_text = ' '.join(para_lines)
        para_text = clean_md(para_text)
        if para_text.strip():
            try:
                result.append(Paragraph(escape_para(para_text), S['body']))
            except Exception:
                # Fallback for problematic text
                safe = para_text.replace('<', '').replace('>', '').replace('&', 'and')
                result.append(Paragraph(safe, S['body']))

    return result


def parse_table(lines):
    """Parse markdown table lines into a reportlab Table."""
    rows = []
    for line in lines:
        line = line.strip()
        if re.match(r'^[\s|:-]+$', line):
            continue  # separator row
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]  # remove empty edges
        if cells:
            rows.append(cells)

    if not rows:
        return Spacer(1, 6)

    # Determine column count
    max_cols = max(len(r) for r in rows)
    # Normalize rows
    for r in rows:
        while len(r) < max_cols:
            r.append('')

    headers = rows[0]
    data_rows = rows[1:] if len(rows) > 1 else []

    col_w = CONTENT_W / max_cols
    widths = [col_w] * max_cols

    # Adjust first column width for tables with many columns
    if max_cols >= 4:
        widths[0] = col_w * 1.3
        remaining = CONTENT_W - widths[0]
        for j in range(1, max_cols):
            widths[j] = remaining / (max_cols - 1)

    return make_table(headers, data_rows, widths)


# ─── Document Builder ────────────────────────────────────────────────

def build_executive_summary():
    """Build the executive summary section."""
    elements = []
    elements.append(Paragraph("Executive Summary", S['h1']))
    elements.append(HRule())
    elements.append(Spacer(1, 12))

    paragraphs = [
        "This research compendium synthesizes findings from nine specialized research reports "
        "and a comprehensive degree-units mapping exercise, conducted between February and July 2026, "
        "to assess the technological landscape, strategic positioning, and implementation pathway for "
        "Angavu Intelligence — the operating system for Africa's 600 million-plus informal workers.",

        "The research was organized across nine swarm teams, each investigating a critical domain: "
        "(1) Voice AI developments, (2) Reasoning models, (3) Agentic AI systems, (4) Agent loops and "
        "orchestration, (5) Quantum computing convergence, (6) The AGI race and emerging systems, "
        "(7) New architectures and on-device AI, (8) Humanity-first AI and African language training, "
        "and (9) Missing degree units analysis. A tenth report maps 42 Economics and Statistics degree "
        "units to Angavu's four product lines: Soko Pulse, Biashara Pulse, Alama Score, and Jamii Insights.",

        "<b>Key Finding 1: The AI landscape has reached an inflection point for African deployment.</b> "
        "Voice AI has achieved sub-500ms latency matching human conversation (OpenAI GPT-Realtime-2, "
        "ElevenLabs v3). The market reached $22.5 billion in 2026 at 34.8% CAGR. Microsoft's Paza "
        "benchmark now covers 39 African languages with 51 state-of-the-art ASR models. On-device "
        "inference on $50 Android phones is now viable with models like Qwen 3.5-0.8B and LFM2.5-1.2B.",

        "<b>Key Finding 2: Reasoning models have matured for financial applications.</b> "
        "Every frontier model in 2026 uses 'thinking' tokens as a core capability. Small reasoning models "
        "(LFM2.5-1.2B-Thinking, Qwen3-1.7B) run in under 1GB of memory with meaningful reasoning "
        "capability. Cloud reasoning costs have fallen to $0.20 per million input tokens (DeepSeek V4 Flash, "
        "GPT-5.4 nano), making cloud fallback economically viable even for micro-transactions.",

        "<b>Key Finding 3: Agentic AI has crossed from experimentation to production.</b> "
        "More than 4 in 10 organizations have AI agents in production. The AI agents market reached "
        "$7.84 billion in 2025, projected to hit $52.62 billion by 2030 at 46.3% CAGR. The Agent-to-Agent "
        "(A2A) Protocol surpassed 150 supporting organizations, and the Model Context Protocol (MCP) "
        "became the universal standard for tool integration.",

        "<b>Key Finding 4: Quantum computing offers one immediately actionable capability.</b> "
        "Post-quantum cryptography (PQC) migration is deployable and urgent — NIST standards are finalized "
        "and the White House mandated federal migration by 2030. Quantum optimization and quantum ML remain "
        "3–7 years from practical deployment for informal economy applications.",

        "<b>Key Finding 5: The architecture revolution makes Angavu viable.</b> "
        "Mixture-of-Experts architectures dominate open-source models. Inference costs have collapsed — "
        "DeepSeek V4-Flash offers 1M-token context at rock-bottom prices. Sub-billion-parameter models "
        "now perform tasks that required 7B+ models in 2023. The convergence of MoE architectures, "
        "collapsing inference costs, and capable on-device models creates a once-in-a-decade window.",

        "<b>Key Finding 6: Angavu has a 12–18 month first-mover window in African language AI.</b> "
        "No existing model speaks African languages with native fluency, especially for code-switched "
        "varieties like Sheng. Recent breakthroughs in on-device fine-tuning (MobileFineTuner, Confidant) "
        "make it technically feasible to train models on $50 Android phones using LoRA/PEFT.",

        "<b>Key Finding 7: Valentine's degree provides strong foundations with identifiable gaps.</b> "
        "The 42 Economics and Statistics units map systematically to Angavu's four product lines, with "
        "probability theory (STA 142) powering Alama Score's Bayesian credit scoring, econometrics "
        "enabling causal impact evaluation, and development economics providing the theoretical framework "
        "for understanding informality. The 68 identified missing units span machine learning, software "
        "engineering, spatial statistics, and NLP — the applied computation layer the degree doesn't cover.",

        "This compendium provides the analytical foundation for Angavu Intelligence's development "
        "as a thesis-grade reference document, integrating technological feasibility analysis, "
        "economic theory, and strategic implementation guidance for building AI that serves "
        "the most underserved economic population on Earth."
    ]

    for p in paragraphs:
        elements.append(Paragraph(p, S['body']))
        elements.append(Spacer(1, 6))

    return elements


def build_key_recommendations():
    """Synthesize recommendations from all reports."""
    elements = []
    elements.append(Paragraph("Key Recommendations", S['h1']))
    elements.append(HRule())
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Synthesized from nine research reports, the following recommendations "
                              "represent the highest-priority actions for Angavu Intelligence:", S['body']))
    elements.append(Spacer(1, 8))

    recs = [
        ("Immediate: On-Device Model Upgrade",
         "Upgrade from Qwen 0.5B to Qwen3.5-0.8B (Apache 2.0, same footprint, dramatically better "
         "multilingual and reasoning). Add multimodal capability via Gemma 4 E2B or LFM2.5-VL-1.6B "
         "for camera-based receipt scanning and inventory tracking. Deploy via existing llama.cpp NDK pipeline."),

        ("Immediate: Voice Pipeline",
         "Implement Whisper ASR for Swahili with code-switching support. Build voice-first confirmation "
         "patterns for financial transactions. Target sub-1,000ms round-trip latency for natural conversation. "
         "Speechmatics' on-device model achieving 90% of server accuracy validates the approach."),

        ("Immediate: Post-Quantum Cryptography",
         "Begin PQC migration for all transaction systems using NIST-standardized ML-KEM (Kyber) and "
         "ML-DSA (Dilithium). The 'store now, decrypt later' threat means encrypted financial data "
         "captured today could be decrypted by future quantum computers. This is the one quantum-adjacent "
         "technology that is deployable, necessary, and urgent."),

        ("Q4 2026: Federated Learning Infrastructure",
         "Deploy federated learning with differential privacy (epsilon=1.0) for privacy-preserving "
         "model improvement. Raw voice data must never leave the device. Implement cohort-based "
         "aggregation by language-dialect groups (Swahili-Core, Sheng-Nairobi, Yoruba-Core, etc.)."),

        ("Q4 2026: Cloud Reasoning Backend",
         "Establish hybrid architecture: on-device (80% of queries, free, instant, private) with "
         "cloud fallback (20%) using DeepSeek V4 Flash at $0.20/M input tokens. Total cost: ~$0.013 "
         "per user per month. At 1M users, cloud inference costs ~$13,000/month."),

        ("Q1 2027: Protocol Adoption",
         "Adopt MCP for all external tool/data access (M-Pesa API, government databases, market feeds). "
         "Implement A2A for inter-agent communication. This positions Msaidizi to participate in the "
         "emerging agent marketplace ecosystem while maintaining sovereignty over its agent network."),

        ("Q2 2027: Agentic Architecture Evolution",
         "Evolve from event bus to event-sourced orchestration with CQRS. Implement saga coordination "
         "for multi-step processes (procurement, logistics, payment, delivery). Add progressive autonomy "
         "framework — agents earn increasing autonomy as they demonstrate reliability."),

        ("Ongoing: Humanity-First Positioning",
         "Build on the documented pattern of Big Tech ethical failures (OpenAI's Kenyan exploitation, "
         "safety team departures) to position Angavu as the ethical alternative. Federated learning "
         "is both a privacy guarantee and a competitive moat. Contribute African language models to "
         "Masakhane and other open-source communities."),
    ]

    for i, (title, desc) in enumerate(recs, 1):
        elements.append(Paragraph(f"<b>{i}. {escape_para(title)}</b>", S['body_bold']))
        elements.append(Paragraph(desc, S['body']))
        elements.append(Spacer(1, 6))

    return elements


# ─── Main Build ──────────────────────────────────────────────────────

def build_pdf():
    """Main function to build the complete PDF."""
    print("Building Angavu Intelligence Research Compendium...")

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 8, bottomMargin=MARGIN + 4,
        title="Angavu Intelligence: Research Compendium",
        author="Valentine Owuor",
        subject="AI for Africa's Informal Economy"
    )

    story = []

    # ── Cover Page (drawn via page template, just need a minimal flowable + break) ──
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # ── Table of Contents ──
    story.append(Paragraph("Table of Contents", S['h1']))
    story.append(HRule())
    story.append(Spacer(1, 16))

    toc_items = [
        ("Executive Summary", 1),
        ("Key Recommendations", 1),
        ("Section 1: Voice AI Models (Feb–Jul 2026)", 1),
        ("Section 2: Reasoning Models (Feb–Jul 2026)", 1),
        ("Section 3: Agentic AI Systems (Feb–Jul 2026)", 1),
        ("Section 4: Agent Loops & Orchestration (Feb–Jul 2026)", 1),
        ("Section 5: Quantum Computing × AI (Feb–Jul 2026)", 1),
        ("Section 6: AGI Race & Emerging Systems (Feb–Jul 2026)", 1),
        ("Section 7: Emerging AI Systems — Architecture & On-Device (Feb–Jul 2026)", 1),
        ("Section 8: Humanity-First AI & African Language Training", 1),
        ("Section 9: Missing Degree Units Analysis", 1),
        ("Section 10: Degree Units to Angavu Functions Mapping", 1),
        ("Section 11: Missing Degree Units — Detailed Analysis", 1),
        ("Appendix A: Complete Citation Index", 1),
        ("Appendix B: Statistical Tables & Benchmark Data", 1),
    ]

    for title, level in toc_items:
        style = S['toc_h1'] if level == 1 else S['toc_h2']
        story.append(Paragraph(escape_para(title), style))

    story.append(PageBreak())

    # ── Executive Summary ──
    story.extend(build_executive_summary())
    story.append(PageBreak())

    # ── Key Recommendations ──
    story.extend(build_key_recommendations())
    story.append(PageBreak())

    # ── Section 1-9: Swarm Reports ──
    swarm_files = [
        ("Section 1: Voice AI Models", "SWARM_1_VOICE_MODELS.md"),
        ("Section 2: Reasoning Models", "SWARM_2_REASONING_MODELS.md"),
        ("Section 3: Agentic AI Systems", "SWARM_3_AGENTIC_SYSTEMS.md"),
        ("Section 4: Agent Loops & Orchestration", "SWARM_4_LOOPS_ORCHESTRATION.md"),
        ("Section 5: Quantum Computing × AI", "SWARM_5_QUANTUM_COMPUTING.md"),
        ("Section 6: AGI Race & Emerging Systems", "SWARM_6_AGI_EMERGING.md"),
        ("Section 7: Emerging AI Systems", "SWARM_7_EMERGING_SYSTEMS.md"),
        ("Section 8: Humanity-First AI & African Languages", "SWARM_8_HUMANITY_ETHICS_LANGUAGE.md"),
        ("Section 9: Missing Degree Units Analysis", "SWARM_9_MISSING_UNITS.md"),
    ]

    for section_title, filename in swarm_files:
        filepath = os.path.join(RESEARCH_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  WARNING: {filename} not found, skipping")
            continue

        print(f"  Processing {filename}...")

        # Section header
        story.append(Paragraph(escape_para(section_title), S['h1']))
        story.append(HRule())
        story.append(Spacer(1, 12))

        # Transition paragraph
        transitions = {
            "SWARM_1_VOICE_MODELS.md": (
                "The following report examines the voice AI landscape from February to July 2026, "
                "covering breakthroughs in speech-foundation-model architectures, market acceleration, "
                "and the critical development of low-resource language coverage — all directly relevant "
                "to Msaidizi's 14-dialect voice-first interface for informal workers."
            ),
            "SWARM_2_REASONING_MODELS.md": (
                "Building on the voice AI foundations, this report analyzes the reasoning model landscape "
                "which has undergone a paradigm shift during this period. The distinction between 'reasoning' "
                "and 'standard' models has effectively dissolved, with profound implications for on-device "
                "financial reasoning in Msaidizi's hybrid architecture."
            ),
            "SWARM_3_AGENTIC_SYSTEMS.md": (
                "While voice and reasoning models provide the interface and intelligence layers, this report "
                "examines the agentic systems that orchestrate them. The February–July 2026 period represents "
                "a watershed moment: agentic AI has shifted from experimental prototypes to production "
                "infrastructure transforming enterprises worldwide."
            ),
            "SWARM_4_LOOPS_ORCHESTRATION.md": (
                "Complementing the agentic systems analysis, this report dives deeper into the specific "
                "orchestration patterns — agent loops, durable execution, event sourcing, and self-improving "
                "systems — that enable reliable multi-agent coordination at production scale."
            ),
            "SWARM_5_QUANTUM_COMPUTING.md": (
                "This report examines the intersection of quantum computing and AI — a domain that offers "
                "one immediately actionable capability (post-quantum cryptography) while optimization and "
                "ML capabilities remain 3–7 years from practical deployment for informal economy applications."
            ),
            "SWARM_6_AGI_EMERGING.md": (
                "Shifting from specific technologies to the broader landscape, this report analyzes the AGI race "
                "and emerging AI systems. The period from February to July 2026 represents the most consequential "
                "six months in AI development history, with implications for Angavu's strategic positioning."
            ),
            "SWARM_7_EMERGING_SYSTEMS.md": (
                "This report examines the structural shifts — new architectures, on-device AI, inference economy — "
                "that create the technical feasibility for Angavu's mission. The convergence of MoE architectures, "
                "collapsing inference costs, and capable on-device models creates a once-in-a-decade window."
            ),
            "SWARM_8_HUMANITY_ETHICS_LANGUAGE.md": (
                "Moving from technology to ethics and language, this report presents parallel tracks: "
                "the documented pattern of Big Tech ethical failures that validates Angavu's positioning, "
                "and the technical pipeline for training African language models on live worker data."
            ),
            "SWARM_9_MISSING_UNITS.md": (
                "The final research report identifies the knowledge gaps between Valentine's BSc Economics "
                "& Statistics degree and the skills required to build Angavu Intelligence. This analysis "
                "provides a prioritized learning roadmap that bridges academic training with startup execution."
            ),
        }

        if filename in transitions:
            story.append(Paragraph(f"<i>{transitions[filename]}</i>", S['quote']))
            story.append(Spacer(1, 8))

        # Content
        flowables = md_to_flowables(filepath)
        story.extend(flowables)
        story.append(PageBreak())

    # ── Section 10: Degree Units Mapping ──
    print("  Processing Degree Units Mapping...")
    story.append(Paragraph("Section 10: Degree Units to Angavu Functions Mapping", S['h1']))
    story.append(HRule())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>This section maps all 42 Economics & Statistics degree units from Valentine Owuor's "
        "BSc program to specific functions across Angavu Intelligence's four product lines: "
        "Soko Pulse (Market Intelligence), Biashara Pulse (Business Intelligence), "
        "Alama Score (Credit Scoring), and Jamii Insights (Community Data).</i>", S['quote']
    ))
    story.append(Spacer(1, 8))

    mapping_path = os.path.join(RESEARCH_DIR, "DEGREE_UNITS_TO_FUNCTIONS_MAPPING.md")
    if os.path.exists(mapping_path):
        flowables = md_to_flowables(mapping_path)
        story.extend(flowables)
    story.append(PageBreak())

    # ── Section 11: Missing Degree Units ──
    print("  Processing Missing Degree Units Analysis...")
    story.append(Paragraph("Section 11: Missing Degree Units — Detailed Analysis", S['h1']))
    story.append(HRule())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>This section provides a comprehensive analysis of 68 degree units from 6 disciplines "
        "that are critical for building Angavu Intelligence but were not part of Valentine's "
        "BSc Economics & Statistics curriculum. Units are ranked by priority and mapped to "
        "specific product functions.</i>", S['quote']
    ))
    story.append(Spacer(1, 8))

    # Since we already included Swarm 9 content, add a summary table here
    story.append(Paragraph("Summary: Priority Distribution of Missing Units", S['h2']))

    priority_data = [
        ["Priority", "Count", "Examples"],
        ["Critical (must learn)", "12", "Machine Learning, Data Structures & Algorithms, "
         "Database Systems, Software Engineering, Spatial Statistics, Bayesian Statistics, NLP"],
        ["High priority", "18", "Graph Theory, Categorical Data Analysis, Survey Sampling, "
         "Operations Research, Big Data Analytics, Strategic Management, Gender Studies"],
        ["Medium priority", "22", "Financial Statistics, Biostatistics, Cybersecurity, "
         "Accounting, Environmental Economics, Health Economics, Political Economy"],
        ["Low priority (nice to have)", "16", "Topology, Functional Analysis, Dynamical Systems, "
         "Queuing Theory, Environmental Statistics"],
    ]

    t = make_table(priority_data[0], priority_data[1:],
                   [3.5*cm, 1.5*cm, CONTENT_W - 5*cm])
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recommended Learning Path (24 months)", S['h2']))

    path_data = [
        ["Phase", "Timeline", "Focus Areas", "Deliverable"],
        ["1: Foundation", "Months 1–6", "Programming, CS Foundations, ML, Data Viz",
         "Working MVP prototypes for Soko Pulse and Alama Score"],
        ["2: Specialization", "Months 7–12", "NLP, Spatial Stats, Bayesian, Cloud",
         "Differentiated products with NLP, spatial, Bayesian capabilities"],
        ["3: Business", "Months 13–18", "Entrepreneurship, Marketing, Domain Knowledge",
         "Fundable business with clear strategy and market understanding"],
        ["4: Advanced", "Months 19–24", "Deep Learning, Distributed Systems, Security",
         "Enterprise-grade platform with advanced analytics"],
    ]

    t = make_table(path_data[0], path_data[1:],
                   [2.5*cm, 2.5*cm, 5*cm, CONTENT_W - 10*cm])
    story.append(t)
    story.append(PageBreak())

    # ── Appendix A: Citation Index ──
    print("  Building citation index...")
    story.append(Paragraph("Appendix A: Complete Citation Index", S['h1']))
    story.append(HRule())
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "The following citations are compiled and deduplicated from all nine research reports. "
        "Sources are organized by category and sorted alphabetically within each category.", S['body']
    ))
    story.append(Spacer(1, 8))

    citation_categories = {
        "Primary AI Research Sources": [
            "OpenAI. 'Advancing voice intelligence with new models in the API.' May 7, 2026.",
            "OpenAI. 'Introducing GPT-5.5.' April 23, 2026.",
            "OpenAI. 'Introducing GPT-5.4 mini and nano.' March 17, 2026.",
            "OpenAI. 'Previewing GPT-5.6 Sol.' June 26, 2026.",
            "OpenAI. 'OpenAI and Broadcom unveil LLM-optimized inference chip.' June 24, 2026.",
            "Anthropic. 'Introducing Claude Opus 4.8.' May 28, 2026.",
            "Anthropic. 'Introducing Claude Sonnet 5.' June 30, 2026.",
            "Anthropic. 'Agents for Financial Services.' May 5, 2026.",
            "Anthropic. 'Scaling Managed Agents: Decoupling Brain from Hands.' April 8, 2026.",
            "Google DeepMind. 'Introducing Gemini Omni.' May 2026.",
            "Google DeepMind. 'Gemini Robotics ER 1.6.' April 14, 2026.",
            "Zhipu AI. 'GLM-5.2.' June 2026.",
            "DeepSeek. 'DeepSeek-V4 Preview Release.' April 24, 2026.",
            "Liquid AI. 'LFM2.5-1.2B-Thinking: On-Device Reasoning Under 1GB.' Jan 20, 2026.",
            "ElevenLabs. '$500M Series D at $11B valuation.' Feb 4, 2026.",
            "Microsoft Research. 'Paza: ASR benchmarks for low resource languages.' Feb 4, 2026.",
        ],
        "Industry Reports & Market Data": [
            "MarketsandMarkets. 'AI Agents Market Report.' 2025–2026.",
            "Market.us. 'Voice AI Agents Market Size, Share.' 2025.",
            "Mordor Intelligence. 'Voice Recognition Market Growing at 22.38% CAGR.' Jan 2026.",
            "Fortune Business Insights. 'Conversational AI Market.' 2026.",
            "World Economic Forum. 'Future of Jobs Report 2025.' Jan 2025.",
            "WEF. 'How Technology Can Help Bank Africa's Informal Economy.' Feb 2026.",
            "BCG. 'Beyond Payments: Unlocking Africa's Second FinTech Wave.' Mar 2026.",
            "GSMA. 'The Mobile Economy Africa 2026.'",
            "Gartner. 'Conversational AI will reduce contact center labor costs by $80B.' 2022.",
            "Goldman Sachs. 'How Will AI Affect the US Labor Market?' Mar 2026.",
            "IMF. 'AI Will Transform the Global Economy.' Jan 2024.",
        ],
        "Academic Papers": [
            "Adimulam, Gupta, Kumar. 'The Orchestration of Multi-Agent Systems.' arXiv:2601.13671, Jan 2026.",
            "Zhang, Kraska, Khattab. 'Recursive Language Models.' arXiv:2512.24601v3, May 2026.",
            "Lee et al. 'Meta-Harness: End-to-End Optimization of Model Harnesses.' arXiv:2603.28052, Mar 2026.",
            "Cheng, Cheng, Siu. 'Three-Pillar Model for Safe AI Agents.' arXiv:2601.06223, Jan 2026.",
            "Shinn et al. 'Reflexion: Language Agents with Verbal RL.' arXiv:2303.11366, 2023.",
            "arXiv. 'Low-Bit Quantization for Reasoning Models.' Jun 2026.",
            "Moslem, Wassie, Abebe. 'AfriNLLB: Efficient Translation for African Languages.' AfricaNLP 2026.",
            "Geng et al. 'MobileFineTuner: Fine-Tuning LLMs on Mobile Phones.' arXiv:2512.08211, 2025.",
            "Lahoti et al. 'Mamba-3: Improved Sequence Modeling using SSM.' arXiv:2603.15569, Mar 2026.",
        ],
        "Infrastructure & Hardware": [
            "IBM. '$10 billion five-year quantum computing investment.' Jun 2, 2026.",
            "NVIDIA. 'Blackwell Ultra: 50x better throughput per megawatt.' Feb 2026.",
            "NVIDIA. 'Nemotron 3 Super: Open Hybrid Mamba-Transformer MoE.' Mar 2026.",
            "Hashrate Index. 'NVIDIA acquired Groq for $20 billion.' Dec 2025.",
            "Hashrate Index. 'Cerebras IPO at ~$56 billion.' May 2026.",
            "Qualcomm. 'Investor Day 2026: AI computing vision.' Jun 25, 2026.",
            "Temporal. 'Replay 2026: Workflow Streams, Serverless Workers.' May 2026.",
        ],
        "Governance & Ethics": [
            "White House. 'Executive Order 14412: Post-Quantum Cryptography.' Jun 22, 2026.",
            "EU AI Act. 'High-risk system rules take effect August 2, 2026.'",
            "NSA. 'Security Design Considerations for AI-Driven Automation (MCP).' May 2026.",
            "African Union. 'Continental Artificial Intelligence Strategy.' Aug 2024.",
            "TIME. 'OpenAI Used Kenyan Workers on Less Than $2 Per Hour.' Jan 2023.",
            "AI Now Institute. 'The AGI Mythology.' Jun 2025.",
            "UNESCO. 'Recommendation on the Ethics of AI.' 2021, updated 2025.",
        ],
        "Africa & Informal Economy": [
            "World Bank. 'Future Jobs: Robots, AI, and Digital Platforms.' Jun 2025.",
            "Brookings. 'Africa's growing gig economy.' Jul 2025.",
            "Brookings. 'Reimagining the future of data and AI labor in Global South.' Oct 2025.",
            "Jumo World. 'Can AI solve financial inclusion in Africa?' Jun 2024.",
            "CGAP. 'Innovation for Inclusion: Roadmap for Inclusive Finance Policy.' May 2026.",
            "Springer. 'Economic impact of AI in agriculture.' Mar 2026.",
            "Future Market Insights. 'AI in Agriculture Market.' May 2026.",
        ],
    }

    for cat_name, citations in citation_categories.items():
        story.append(Paragraph(escape_para(cat_name), S['h2']))
        for cit in citations:
            story.append(Paragraph(f"• {escape_para(cit)}", S['bullet']))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ── Appendix B: Statistical Tables ──
    print("  Building statistical tables...")
    story.append(Paragraph("Appendix B: Statistical Tables & Benchmark Data", S['h1']))
    story.append(HRule())
    story.append(Spacer(1, 12))

    # Table 1: Voice AI Market
    story.append(Paragraph("Table B.1: Voice AI Market Size and Projections", S['h2']))
    voice_market = [
        ["Segment", "2024/2025 Value", "Projected Value", "CAGR"],
        ["Voice AI Agents", "$2.4B (2024)", "$47.5B (2034)", "34.8%"],
        ["Conversational AI", "$17.97B (2026)", "$82.46B (2034)", "—"],
        ["Voice Recognition", "$22.49B (2026)", "$61.71B (2031)", "22.38%"],
        ["AI Voice Generators", "$4.16B (2025)", "$20.71B (2031)", "30.7%"],
        ["Voice Assistant", "$7.08B (2024)", "$59.9B (2033)", "26.80%"],
        ["Voicebot", "$8.69B (2025)", "$54.64B (2034)", "22.51%"],
    ]
    story.append(make_table(voice_market[0], voice_market[1:],
                           [3.5*cm, 3*cm, 3*cm, 2*cm]))
    story.append(Spacer(1, 12))

    # Table 2: Frontier Model Benchmarks
    story.append(Paragraph("Table B.2: Frontier Model Benchmarks (June 2026)", S['h2']))
    frontier = [
        ["Benchmark", "GPT-5.5", "Claude Opus 4.8", "Gemini 3.1 Pro", "DeepSeek V4 Pro"],
        ["SWE-Bench Verified", "88.6%", "~85%", "~82%", "~80%"],
        ["GPQA Diamond", "~93%", "~92%", "~91%", "~88%"],
        ["ARC-AGI-1", "~90%", "~88%", "~85%", "~82%"],
        ["ARC-AGI-2", "~55%", "~50%", "~48%", "~42%"],
        ["Terminal-Bench 2.0", "82.7%", "69.4%", "68.5%", "~65%"],
        ["GDPval (win/tie)", "84.9%", "80.3%", "67.3%", "~60%"],
        ["LMArena Elo", "~1,500", "~1,510", "~1,490", "~1,450"],
    ]
    story.append(make_table(frontier[0], frontier[1:],
                           [3*cm, 2.2*cm, 2.8*cm, 2.5*cm, 2.5*cm]))
    story.append(Spacer(1, 12))

    # Table 3: Small Model Benchmarks
    story.append(Paragraph("Table B.3: Small Model Benchmarks (January 2026)", S['h2']))
    small_models = [
        ["Benchmark", "LFM2.5-1.2B-Thinking", "Qwen3-1.7B", "Granite-4.0-H-1B", "Llama 3.2 1B"],
        ["GPQA Diamond", "37.86%", "36.93%", "24.34%", "16.57%"],
        ["MATH-500", "87.96%", "81.92%", "47.20%", "23.40%"],
        ["IFEval", "88.42%", "71.65%", "80.08%", "52.37%"],
        ["Tool Use (BFCLv3)", "56.97%", "55.41%", "50.69%", "21.44%"],
    ]
    story.append(make_table(small_models[0], small_models[1:],
                           [3*cm, 3*cm, 2.5*cm, 2.5*cm, 2*cm]))
    story.append(Spacer(1, 12))

    # Table 4: Cost Efficiency
    story.append(Paragraph("Table B.4: Cloud Reasoning Cost Efficiency (June 2026)", S['h2']))
    cost_data = [
        ["Model", "Input $/1M", "Output $/1M", "GPQA Diamond", "Value Rating"],
        ["GPT-5.4 nano", "$0.20", "$1.25", "82.8%", "Best value"],
        ["DeepSeek V4 Flash", "~$0.20", "~$1.00", "~85%", "Best value (open)"],
        ["GPT-5.4 mini", "$0.75", "$4.50", "88.0%", "Excellent"],
        ["Claude Haiku 4.5", "$1.00", "$5.00", "~85%", "Good"],
        ["Claude Sonnet 5", "$3.00", "$15.00", "~90%", "Moderate"],
        ["GPT-5.4", "~$5.00", "~$15.00", "93.0%", "Premium"],
        ["Claude Opus 4.8", "$5.00", "$25.00", "~92%", "Premium"],
    ]
    story.append(make_table(cost_data[0], cost_data[1:],
                           [3*cm, 2*cm, 2*cm, 2.5*cm, 3*cm]))
    story.append(Spacer(1, 12))

    # Table 5: On-Device Performance
    story.append(Paragraph("Table B.5: On-Device Model Performance (July 2026)", S['h2']))
    device_data = [
        ["Model", "Parameters", "Memory", "Performance", "Use Case"],
        ["LFM2.5-1.2B", "1.2B", "<1GB (4-bit)", "Best-in-class at 1B", "General assistant"],
        ["Gemma 4 E2B", "2B", "1–1.5GB (4-bit)", "20–35 tok/s mobile", "Basic multimodal"],
        ["Gemma 4 E4B", "4B", "2–3GB (4-bit)", "12–20 tok/s mobile", "Complex multimodal"],
        ["Qwen3.5-0.8B", "0.8B", "~0.5GB (4-bit)", "Mobile-optimized", "Simple tasks"],
        ["Qwen3.5-2B", "2B", "~1.2GB (4-bit)", "Mobile-optimized", "Edge deployment"],
        ["Qwen3.5-9B", "9B", "~5.5GB (4-bit)", "50+ tok/s Mac", "Consumer assistant"],
        ["Phi-4-mini", "3.8B", "~2.3GB (4-bit)", "128K context", "Resource-constrained"],
    ]
    story.append(make_table(device_data[0], device_data[1:],
                           [2.5*cm, 2*cm, 2.5*cm, 3*cm, 3*cm]))
    story.append(Spacer(1, 12))

    # Table 6: AI Agents Market
    story.append(Paragraph("Table B.6: AI Agents Market Adoption (2026)", S['h2']))
    agent_market = [
        ["Metric", "Value", "Source"],
        ["AI Agents Market (2025)", "$7.84 billion", "MarketsandMarkets"],
        ["AI Agents Market (2030 projected)", "$52.62 billion", "MarketsandMarkets"],
        ["CAGR", "46.3%", "MarketsandMarkets"],
        ["Organizations using AI agents", "96%", "OutSystems, Apr 2026"],
        ["Organizations with agents in production", ">40%", "Mayfield, 2026"],
        ["Enterprise leaders planning expansion", "96%", "Multimodal.dev"],
        ["Organizations expecting ROI >100%", "62%", "Multimodal.dev"],
        ["Organizations with mature AI governance", "20%", "Deloitte, 2026"],
    ]
    story.append(make_table(agent_market[0], agent_market[1:],
                           [5.5*cm, 3*cm, 4*cm]))
    story.append(Spacer(1, 12))

    # Table 7: Africa Data Points
    story.append(Paragraph("Table B.7: Africa — Key Data Points for Angavu", S['h2']))
    africa_data = [
        ["Metric", "Value", "Source"],
        ["Informal employment in Sub-Saharan Africa", "85.8%", "ILO, 2024"],
        ["Africa's population (2024)", "1.4 billion", "UN DESA"],
        ["Africa's population (2050 projected)", "2.5 billion", "UN DESA"],
        ["Mobile money accounts in Sub-Saharan Africa", "835 million", "GSMA, 2024"],
        ["Adults with financial accounts (SSA)", "~55%", "World Bank Findex, 2025"],
        ["M-Pesa users", "51M+", "Safaricom, 2025"],
        ["Smartphone penetration (SSA)", "~50% (2025)", "GSMA"],
        ["Projected smartphone penetration (SSA, 2028)", "65%", "GSMA"],
    ]
    story.append(make_table(africa_data[0], africa_data[1:],
                           [6*cm, 3*cm, 3.5*cm]))
    story.append(Spacer(1, 12))

    # Table 8: Quantum Computing Investment
    story.append(Paragraph("Table B.8: Quantum Computing Investment Landscape (2026)", S['h2']))
    quantum_data = [
        ["Entity", "Investment/Event", "Date"],
        ["IBM", "$10 billion 5-year commitment", "Jun 2026"],
        ["Keyfactor", "$1B+ growth investment (PQC)", "Jul 2026"],
        ["Quantinuum", "$270M convertible round", "2026"],
        ["D-Wave", "$33.4M record quarterly bookings", "Q1 2026"],
        ["D-Wave", "$588M cash position", "Q1 2026"],
        ["White House EO 14412", "Federal PQC migration by 2030", "Jun 22, 2026"],
        ["Quantum tech total funding (2002–2025)", "$5.7 billion", "Quantum Insider"],
    ]
    story.append(make_table(quantum_data[0], quantum_data[1:],
                           [4*cm, 5.5*cm, 3*cm]))

    story.append(PageBreak())

    # ── Final Page ──
    story.append(Spacer(1, 100))
    story.append(Paragraph("— End of Research Compendium —", S['h1']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This document was compiled from nine specialized research reports covering the period "
        "February–July 2026, plus a comprehensive degree-units mapping exercise. It represents "
        "the analytical foundation for Angavu Intelligence's development as a thesis-grade "
        "reference for serving Africa's 600 million-plus informal workers.",
        S['body']
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Prepared by Valentine Owuor — BSc Economics & Statistics<br/>"
        "Masinde Muliro University of Science and Technology<br/>"
        "July 2026",
        ParagraphStyle('FinalNote', parent=S['body'], alignment=TA_CENTER, fontSize=11)
    ))

    # ── Build ──
    print("  Generating PDF...")
    doc.build(story, onFirstPage=draw_cover_page, onLaterPages=header_footer)
    print(f"  ✓ PDF generated: {OUTPUT_PATH}")

    # Report size
    size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"  ✓ File size: {size_mb:.1f} MB")
    return OUTPUT_PATH


if __name__ == '__main__':
    build_pdf()
