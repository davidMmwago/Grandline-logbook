"""Assembles the self-contained index.html from src/template.html, the data file and the assets.

    python data/build_data.py   # only needed after changing data/raw/*
    python build.py
"""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
p = lambda *a: os.path.join(HERE, *a)
b64 = lambda f: base64.b64encode(open(p('src', 'assets', f), 'rb').read()).decode()

page = open(p('src', 'template.html'), encoding='utf-8').read()
for key, value in {
    '__DATA__': open(p('data', 'one-piece.json'), encoding='utf-8').read(),
    '__FONT__': b64('one-piece-font.ttf'),
    '__PAPER__': b64('paper.jpg'),
    '__MERRY__': b64('going-merry.webp'),
    '__SUNNY__': b64('thousand-sunny.webp'),
    '__LOGPOSE__': b64('log-pose.webp'),
}.items():
    assert key in page, f'{key} missing from template'
    page = page.replace(key, value)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);'
        'padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}'
        'img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
with open(p('index.html'), 'w', encoding='utf-8') as f:
    f.write(head + page + '\n</body>\n</html>\n')
print(f'Wrote index.html ({os.path.getsize(p("index.html")) // 1024} KB)')
