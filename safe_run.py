import sys
import traceback
from config_tool.parser import translate, ParseError

def main():
    if len(sys.argv) < 3:
        print('Usage: python  <input.conf> <output.xml> - safe_run.py:7')
        return 2
    inp = sys.argv[1]
    outp = sys.argv[2]
    try:
        with open(inp, 'r', encoding='utf-8') as f:
            text = f.read()
        out = translate(text)
        with open(outp, 'w', encoding='utf-8') as f:
            f.write(out)
        print('Wrote - safe_run.py:17', outp)
        return 0
    except ParseError as e:
        msg = f'ParseError: {e}'
        print(msg)
        with open('error.log', 'a', encoding='utf-8') as log:
            log.write(msg + '\n')
        return 3
    except Exception as e:
        tb = traceback.format_exc()
        print('Error: see error.log - safe_run.py:27')
        with open('error.log', 'a', encoding='utf-8') as log:
            log.write(tb + '\n')
        return 1       

if __name__ == '__main__':
    sys.exit(main())
