import argparse
from .parser import translate, ParseError
import time
import os


def main():
    parser = argparse.ArgumentParser(description='Config -> XML translator')
    parser.add_argument('-i', '--input', required=True, help='Input .conf file')
    parser.add_argument('-o', '--output', required=True, help='Output .xml file')
    parser.add_argument('--watch', action='store_true', help='Watch input file and regenerate on change')
    args = parser.parse_args()
    try:
        def do_run():
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
            out = translate(text)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(out)
            print('Wrote - cli.py:20', args.output)
            print('\n XML output - cli.py:21')
            print(out)

        if args.watch:
            print(f'Watching {args.input} for changes. Press Ctrl+C to stop. - cli.py:25')
            last = None
            try:
                while True:
                    try:
                        m = os.path.getmtime(args.input)
                    except OSError:
                        m = None
                    if m != last:
                        last = m
                        try:
                            do_run()
                        except ParseError as e:
                            print('Syntax error: - cli.py:38', e)
                    time.sleep(1)
            except KeyboardInterrupt:
                print('\nStopped watching. - cli.py:41')
        else:
            do_run()
    except ParseError as e:
        print('Syntax error: - cli.py:45', e)
        raise SystemExit(2)
    except FileNotFoundError as e:
        print('File error: - cli.py:48', e)
        raise SystemExit(3)

if __name__ == '__main__':
    main()
