from pynput.mouse import Button, Listener
from datetime import datetime
from displayer import Displayer
from test import Test
import argparse
import os


class Anaclock(object):

    def __init__(self, debug=False):
        self.displayer = Displayer(debug=debug)
        self.left_click_time = None

    def listen(self):
        with Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll
        ) as listener:
            listener.join()

    def on_move(self, x, y):
        self.displayer.display_hour()

    def on_click(self, x, y, button, pressed):
        if button == Button.left:
            if pressed:
                self.left_click_time = datetime.now()
            if not pressed and self.left_click_time is not None:
                delta = datetime.now() - self.left_click_time
                if delta.seconds >= 5:
                    self.displayer.display_text('Bye !').join(timeout=10)
                    os.system('sudo shutdown -h now')
                    return False
                self.left_click_time = None
        if not pressed:
            if button == Button.left:
                self.displayer.display_hour()
            elif button == Button.right:
                self.displayer.display_date()

    def on_scroll(self, x, y, dx, dy):
        self.displayer.display_hour()


def main(debug, test):
    try:
        if test:
            Test(debug=debug).run()
        else:
            Anaclock(debug=debug).listen()
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
