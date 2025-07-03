#!/usr/bin/env python3
"""
Printer Exerciser Script
Generates a PDF with four vertical CMYK bars at a random position and sends it to a printer via CUPS.
"""
import argparse
import random
import tempfile
import os
import sys
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
import subprocess

PAGE_SIZES = {
    'A4': A4,
    'letter': letter
}

CMYK_COLORS = [
    CMYKColor(1, 0, 0, 0),  # Cyan
    CMYKColor(0, 1, 0, 0),  # Magenta
    CMYKColor(0, 0, 1, 0),  # Yellow
    CMYKColor(0, 0, 0, 1),  # Black
]


def generate_pdf(filename, page_size, bar_width_mm, bar_height_mm):
    c = canvas.Canvas(filename, pagesize=page_size)
    page_width, page_height = page_size
    
    # Convert mm to points (1 mm = 2.83465 points)
    mm = 2.83465
    bar_width = bar_width_mm * mm
    bar_height = bar_height_mm * mm
    group_width = 4 * bar_width
    group_height = bar_height

    # Random position (all bars inside page)
    max_x = page_width - group_width
    max_y = page_height - group_height
    x = random.uniform(0, max_x)
    y = random.uniform(0, max_y)

    for i, color in enumerate(CMYK_COLORS):
        c.setFillColor(color)
        c.rect(x + i * bar_width, y, bar_width, bar_height, fill=1, stroke=0)

    c.showPage()
    c.save()
    return filename


def print_pdf(filename, printer_name):
    try:
        subprocess.run([
            'lp',
            '-d', printer_name,
            filename
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error printing file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate and print a CMYK nozzle exerciser page.")
    parser.add_argument('--printer', required=True, help='Printer name (as known to CUPS)')
    parser.add_argument('--page-size', default='A4', choices=PAGE_SIZES.keys(), help='Page size (default: A4)')
    parser.add_argument('--bar-width', type=float, default=7, help='Bar width in mm (default: 7)')
    parser.add_argument('--bar-height', type=float, default=40, help='Bar height in mm (default: 40)')
    parser.add_argument('--debug', action='store_true', help='Debug mode: only generate and save the PDF, do not print or delete')
    parser.add_argument('--output', default=None, help='Output PDF filename (default: temp file)')
    args = parser.parse_args()

    page_size = PAGE_SIZES[args.page_size]
    output_file = args.output or tempfile.mktemp(suffix='.pdf')

    generate_pdf(output_file, page_size, args.bar_width, args.bar_height)
    print(f"Generated test page: {output_file}")

    if args.debug:
        print("Debug mode: not printing or deleting the file.")
        return

    print_pdf(output_file, args.printer)
    print(f"Sent to printer: {args.printer}")

    if not args.output:
        os.remove(output_file)
        print("Temporary file removed.")

if __name__ == '__main__':
    main()
