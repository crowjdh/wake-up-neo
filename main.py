import os
import sys
import time


def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

def main(target):
  ttys = f'/dev/{target}'

  does_target_exists = os.path.exists(ttys)
  is_target_writable = os.access(ttys, os.W_OK)
  is_condition_met = does_target_exists and is_target_writable

  if not is_condition_met:
    exit(1)
  with open(ttys, 'wb', buffering=0) as f, open('script.txt', 'rb') as script:
    f.write(b'\r' + b' ' * 50 + b'\r')
    while True:
      ch = script.read(1)
      if not ch:
        break
      ch = b'\r\n' if ch == b'\n' else ch
      f.write(ch)
      time.sleep(0.1 if ch != b'\r\n' else 1)
    while True:
      ch = getch()
      if ch == '`':
        break
  
      ch = '\r\n' if ch == '\r' else ch
      print(ch, end='', flush=True)
      f.write(ch.encode())


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Specify target.")
    exit()

  target = sys.argv[1]
  main(target)
