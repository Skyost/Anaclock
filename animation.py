from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.emulator.device import pygame
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from PIL import ImageFont
import time


class Animation(object):

    def __init__(self, debug=False):
        self.debug = debug

    def run(self):
        self.animate()
        self.finish_animation()

    def create_device(self):
        if self.debug:
            return pygame(width=32, height=8)
        else:
            serial = spi(gpio=noop())
            return max7219(serial, cascaded=4, block_orientation=-90, contrast=0)

    @staticmethod
    def create_font():
        return ImageFont.truetype('fonts/pixelsix10.ttf', 8)

    def animate(self):
        pass

    def finish_animation(self):
        if self.debug:
            from pygame import quit
            quit()


class HourAnimation(Animation):

    def __init__(self, debug=False):
        super(HourAnimation, self).__init__(debug=debug)

    def animate(self):
        device = self.create_device()
        current_time = time.strftime('%H:%M')
        font = HourAnimation.create_font()
        HourAnimation.pacman_animation(device, current_time, font, -8, device.width + 1, 1)
        time.sleep(1)
        HourAnimation.pacman_animation(device, current_time, font, device.width, -9, -1)

    @staticmethod
    def pacman_animation(device, current_time, font, start, stop, step):
        reverse = step < 0
        phantom_gap = 10
        stop_with_gap = stop if not reverse else (stop - phantom_gap)
        for x in range(start, stop_with_gap, step):
            with canvas(device) as draw:
                text_width, text_height = draw.textsize(current_time, font=font)
                text_x, text_y = (device.width - text_width) / 2, (device.height - text_height) / 2
                if x >= text_x:
                    draw.text(
                        (text_x, text_y),
                        current_time,
                        fill='white',
                        font=font,
                        spacing=1,
                    )
                    draw.rectangle([(x, 0), (device.width, device.height)], fill='black')
                HourAnimation.draw_pacman(draw, x, reverse)
                if reverse and x <= device.width - phantom_gap:
                    HourAnimation.draw_phantom(draw, x + phantom_gap)
                time.sleep(0.05)

    @staticmethod
    def draw_pacman(draw, x, reverse=False):
        for y in [0, 7]:
            draw.line([(x + 2, y), (x + 5, y)], fill='white')
        for y in [1, 6]:
            draw.line([(x + 1, y), (x + 6, y)], fill='white')
        for y in [2, 3, 4, 5]:
            draw.line([(x, y), (x + 7, y)], fill='white')
        if x % 2 == 0:
            draw.rectangle([(x + (3 if reverse else 4), 3), (x + (0 if reverse else 7), 4)], fill='black')
            if x % 4 == 2:
                draw.point((x + (0 if reverse else 7), 5), fill='black')
                draw.point((x + (0 if reverse else 7), 2), fill='black')
                draw.point((x + (1 if reverse else 6), 5), fill='black')
                draw.point((x + (1 if reverse else 6), 2), fill='black')

    @staticmethod
    def draw_phantom(draw, x):
        draw.line([(x + 1, 0), (x + 5, 0)], fill='white')
        for y in [1, 4, 5, 6]:
            draw.line([(x, y), (x + 6, y)], fill='white')
        if x % 3 == 1:
            draw.line([(x, 7), (x + 6, 7)], fill='white')
            draw.line([(x, 3), (x + 6, 3)], fill='white')
        else:
            for offset in [0, 2, 4, 6]:
                draw.point((x + offset, 7), fill='white')
            for offset in [1, 4]:
                draw.point((x + offset + x % 2, 3), fill='white')
        for y in [2, 3]:
            for offset in [0, 3, 6]:
                draw.point((x + offset, y), fill='white')


class TextAnimation(Animation):

    def __init__(self, text, debug=False):
        super(TextAnimation, self).__init__(debug=debug)
        self.text = text

    def animate(self):
        device = self.create_device()
        font = DateAnimation.create_font()
        virtual = viewport(device, width=len(self.text) * 8 + 2 * device.width, height=device.height)
        with canvas(virtual) as draw:
            draw.text((device.width, 0), self.text, fill="white", font=font)
            text_width = draw.textsize(self.text, font=font)[0]
        for offset in range(device.width + text_width + 1):
            virtual.set_position((offset, 0))
            time.sleep(0.05)


class DateAnimation(TextAnimation):

    def __init__(self, debug=False):
        super(DateAnimation, self).__init__(time.strftime('%a %d %b %Y'), debug=debug)
