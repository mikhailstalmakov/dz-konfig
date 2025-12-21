from config_tool.parser import translate
import os

examples = [
    'examples/server.conf',
    'examples/physics.conf',
]

for conf in examples:
    if not os.path.exists(conf):
        print('Not found:', conf)
        continue
    text = open(conf, 'r', encoding='utf-8').read()
    out = translate(text)
    outpath = os.path.splitext(conf)[0] + '.xml'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(out)
    print('Wrote', outpath)
