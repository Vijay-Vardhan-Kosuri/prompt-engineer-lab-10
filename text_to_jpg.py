#!/usr/bin/env python3
"""Convert experiment text outputs into clean JPG images."""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def create_text_image(text: str, output_path: str, title: str = "", width: int = 900):
    # Use a monospace-friendly font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        title_font = font
        header_font = font

    # Prepare lines
    lines = []
    if title:
        lines.append(title)
        lines.append("")
    
    for line in text.splitlines():
        # Wrap long lines
        if len(line) > 95:
            wrapped = textwrap.wrap(line, width=95)
            lines.extend(wrapped)
        else:
            lines.append(line)

    line_height = 20
    padding = 30
    img_height = padding * 2 + len(lines) * line_height + 20
    img_width = width

    # Create image with light background
    img = Image.new("RGB", (img_width, img_height), color=(248, 249, 250))
    draw = ImageDraw.Draw(img)

    # Draw a subtle header bar
    draw.rectangle([0, 0, img_width, 50], fill=(30, 64, 175))  # Indigo

    y = padding
    for i, line in enumerate(lines):
        if i == 0 and title:
            # Title already drawn in header conceptually
            draw.text((padding, 12), title, font=title_font, fill=(255, 255, 255))
            y = 60
            continue

        # Color coding for sections
        if line.startswith("===") or line.startswith("PROBLEM") or line.startswith("Expected"):
            color = (30, 64, 175)  # Blue
            use_font = header_font
        elif "Correct? YES" in line:
            color = (22, 163, 74)  # Green
            use_font = font
        elif "Correct? NO" in line:
            color = (220, 38, 38)  # Red
            use_font = font
        elif line.startswith("LLM Response") or line.startswith("Parsed") or "→" in line or "Final answer" in line:
            color = (15, 23, 42)
            use_font = font
        else:
            color = (51, 65, 85)
            use_font = font

        draw.text((padding, y), line, font=use_font, fill=color)
        y += line_height

    # Footer
    draw.rectangle([0, img_height - 25, img_width, img_height], fill=(226, 232, 240))
    draw.text((padding, img_height - 20), "CoT Prompting Experiment • Simulated LLM Outputs", 
              font=font, fill=(100, 116, 139))

    img.save(output_path, "JPEG", quality=95)
    print(f"Saved: {output_path}")


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    scenarios = [
        ("correct", "Output 1: Direct Prompt Correct (by chance)"),
        ("wrong_add_only", "Output 2: Direct Prompt Incorrect (forgot to sell half)"),
        ("wrong_half_first", "Output 3: Direct Prompt Incorrect (alternate error)"),
    ]

    for scenario, title in scenarios:
        txt_path = os.path.join(out_dir, f"experiment_{scenario}.txt")
        if not os.path.exists(txt_path):
            print(f"Missing {txt_path}, skipping")
            continue
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Clean a bit for image (remove the "Running..." and file save lines)
        content_lines = []
        for line in content.splitlines():
            if line.startswith("Running CoT") or line.startswith("[Text output"):
                continue
            content_lines.append(line)
        clean_content = "\n".join(content_lines).strip()

        jpg_path = os.path.join(out_dir, f"experiment_output_{scenario}.jpg")
        create_text_image(clean_content, jpg_path, title=title)


if __name__ == "__main__":
    main()
