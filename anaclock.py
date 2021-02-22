import argparse
import os
from datetime import datetime

from pynput.mouse import Button, Listener

from display import Display
from test import Test


class Anaclock(object):

    def __init__(self, debug: bool = False):
        self.display = Display(debug)
        self.left_click_time = None

    def listen(self):
        with Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll
        ) as listener:
            listener.join()

    def on_move(self, x: int, y: int):
        self.display.display_hour()

    def on_click(self, x: int, y: int, button: Button, pressed: bool):
        if button == Button.left:
            if pressed:
                self.left_click_time = datetime.now()
            if not pressed and self.left_click_time is not None:
                delta = datetime.now() - self.left_click_time
                if delta.seconds >= 5:
                    self.display.display_text('Bye !').join(10)
                    os.system('sudo shutdown -h now')
                    return False
                self.left_click_time = None
        if not pressed:
            if button == Button.left:
                self.display.display_hour()
            elif button == Button.right:
                self.display.display_date()

    def on_scroll(self, x: int, y: int, dx: int, dy: int):
        self.display.display_hour()


def main(debug: bool, test: bool):
    try:
        if test:
            Test(debug).run()
        else:
            Anaclock(debug).listen()
    except KeyboardInterrupt:
        print('Interrupted via keyboard.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Anaclock arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--debug', type=bool, default=False, help='Whether to run the script using an emulator.')
    parser.add_argument('--test', type=bool, default=False, help='Whether to run the tests.')
    args = parser.parse_args()
    main(args.debug, args.test)
