"""Render the supplied news digest as a deterministic 1024 × 1024 PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FONTS = Path('/usr/share/fonts/truetype/dejavu')
STORIES = (
    ('DIPLOMACY', 'Trump heads to Shenzhen summit',
     "US President Donald Trump flew to China for a trilateral meeting in Shenzhen with China's Xi Jinping and Russia's Vladimir Putin, the three leaders' first three-way summit.", '#6D929B'),
    ('HEALTH', 'US loses measles-free status',
     'The Pan American Health Organization declared measles no longer eliminated in the United States after more than a year of spread. Over 5,400 cases were reported in 2026, the worst outbreak in over three decades.', '#9383A5'),
    ('RUSSIA', '19 killed in Siberia plane crash',
     'A Russian An-12 military transport plane crashed near Kemerovo in western Siberia, killing all 19 people on board. Officials suspect an equipment failure, and investigators are at the site.', '#A7806C'),
    ('MIDDLE EAST', 'Opposition wins Knesset speaker vote',
     "Israel's parliament elected Matan Kahana, an ally of Gadi Eisenkot, as speaker by 66 votes to 52, ousting an ally of caretaker prime minister Benjamin Netanyahu. Eisenkot has been tasked with forming a new government.", '#758C71'),
    ('ASIA-PACIFIC', 'Quad leaders meet in Manila',
     'The leaders of India, the United States, Japan and Australia met in Manila and announced a new maritime exercise, along with joint initiatives on AI and cybersecurity.', '#A48D58'),
)


def font(size, bold=False):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(draw, text, face, width):
    lines = []
    line = ''
    for word in text.split():
        candidate = f'{line} {word}' if line else word
        if draw.textlength(candidate, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def main():
    image = Image.new('RGB', (1024, 1024), '#F5F3EF')
    draw = ImageDraw.Draw(image)
    title_font = font(43, bold=True)
    tag_font = font(18, bold=True)
    headline_font = font(29, bold=True)
    body_font = font(22)
    footer_font = font(18)

    draw.rectangle((0, 0, 1023, 125), fill='#152739')
    title = 'WEDNESDAY 18 NOVEMBER 2026'
    assert draw.textlength(title, font=title_font) <= 944
    draw.text((40, 43), title, font=title_font, fill='white', anchor='lt')

    for index, (tag, headline, body, accent) in enumerate(STORIES):
        top = 146 + index * 163
        draw.rectangle((36, top, 41, top + 141), fill=accent)
        draw.text((60, top), tag, font=tag_font, fill=accent, anchor='lt')
        assert draw.textlength(headline, font=headline_font) <= 924
        draw.text((60, top + 27), headline, font=headline_font,
                  fill='#182A3B', anchor='lt')
        lines = wrap(draw, body, body_font, 924)
        assert len(lines) <= 3, f'Story body exceeds its block: {tag}'
        for line_index, line in enumerate(lines):
            draw.text((60, top + 67 + line_index * 27), line,
                      font=body_font, fill='#35424D', anchor='lt')
        if index < len(STORIES) - 1:
            draw.line((60, top + 151, 984, top + 151), fill='#DFDFDA')

    draw.line((36, 974, 988, 974), fill='#D7D9D8')
    draw.text((40, 989), 'Events of 18 November 2026, as reported.',
              font=footer_font, fill='#737A80', anchor='lt')
    image.save(ROOT / 'entry.png', format='PNG', optimize=False,
               compress_level=9)


if __name__ == '__main__':
    main()
