import time

from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from luma.core.device import device
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.emulator.device import pygame
from luma.led_matrix.device import max7219


class Animation(object):

    def __init__(self, debug: bool = False):
        self.debug = debug

    def run(self):
        self.animate()
        self.finish_animation()

    def create_device(self) -> device:
        if self.debug:
            return pygame(width=32, height=8)
        else:
            serial = spi(gpio=noop())
            return max7219(serial, cascaded=4, block_orientation=-90, contrast=0)

    @staticmethod
    def create_font() -> ImageFont:
        return ImageFont.truetype('fonts/pixelsix10.ttf', 8)

    def animate(self):
        pass

    def finish_animation(self):
        if self.debug:
            from pygame import quit
            quit()


class HourAnimation(Animation):

    def __init__(self, debug: bool = False):
        super(HourAnimation, self).__init__(debug)

    def animate(self):
        luma_device = self.create_device()
        current_time = time.strftime('%H:%M')
        font = HourAnimation.create_font()
        HourAnimation.pacman_animation(luma_device, current_time, font, -8, luma_device.width + 1, 1)
        time.sleep(1)
        HourAnimation.pacman_animation(luma_device, current_time, font, luma_device.width, -9, -1)

    @staticmethod
    def pacman_animation(
            luma_device: device,
            current_time: str,
            font: ImageFont,
            start: int,
            stop: int,
            step: int
    ):
        reverse = step < 0
        phantom_gap = 10
        stop_with_gap = stop if not reverse else (stop - phantom_gap)
        for x in range(start, stop_with_gap, step):
            with canvas(luma_device) as draw:
                text_width, text_height = draw.textsize(current_time, font)
                text_x, text_y = (luma_device.width - text_width) / 2, (luma_device.height - text_height) / 2
                if x >= text_x:
                    draw.text(
                        (text_x, text_y),
                        current_time,
                        fill='white',
                        font=font,
                        spacing=1,
                    )
                    draw.rectangle([(x, 0), (luma_device.width, luma_device.height)], fill='black')
                HourAnimation.draw_pacman(draw, x, reverse)
                if reverse and x <= luma_device.width - phantom_gap:
                    HourAnimation.draw_phantom(draw, x + phantom_gap)
                time.sleep(0.05)

    @staticmethod
    def draw_pacman(draw: ImageDraw, x: int, reverse: bool = False):
        step = x % 8
        for y in [0, 7]:
            draw.line([(x + 2, y), (x + 5, y)], fill='white')
        for y in [1, 6]:
            draw.line([(x + 1, y), (x + 6, y)], fill='white')
        for y in [2, 3, 4, 5]:
            draw.line([(x, y), (x + 7, y)], fill='white')
        if 2 <= step <= 7:
            draw.rectangle([(x + (3 if reverse else 4), 3), (x + (0 if reverse else 7), 4)], fill='black')
            if 4 <= step <= 5:
                draw.point((x + (0 if reverse else 7), 5), fill='black')
                draw.point((x + (0 if reverse else 7), 2), fill='black')
                draw.point((x + (1 if reverse else 6), 5), fill='black')
                draw.point((x + (1 if reverse else 6), 2), fill='black')

    @staticmethod
    def draw_phantom(draw: ImageDraw, x: int):
        eyes_step = x % 5
        feet_step = x % 2
        draw.line([(x + 1, 0), (x + 5, 0)], fill='white')
        for y in [1, 3, 4, 5, 6]:
            draw.line([(x, y), (x + 6, y)], fill='white')
        for y in [2, 3]:
            for offset in [0, 3, 6]:
                draw.point((x + offset, y), fill='white')
        if feet_step == 1:
            for offset in [0, 2, 4, 6]:
                draw.point((x + offset, 7), fill='white')
        else:
            draw.line([(x, 7), (x + 6, 7)], fill='white')
            draw.line([(x, 3), (x + 6, 3)], fill='white')
        if eyes_step <= 3:
            eyes_offset = 1 if 0 <= eyes_step <= 1 else 0
            for offset in [1, 4]:
                draw.point((x + offset + eyes_offset, 3), fill='black')


class TextAnimation(Animation):

    def __init__(self, text: str, debug: bool = False):
        super(TextAnimation, self).__init__(debug)
        self.text = text

    def create_text(self):
        return self.text

    def animate(self):
        luma_device = self.create_device()
        text = self.create_text()
        font = DateAnimation.create_font()
        virtual = viewport(luma_device, width=len(text) * 8 + 2 * luma_device.width, height=luma_device.height)
        with canvas(virtual) as draw:
            draw.text((luma_device.width, 0), text, fill='white', font=font)
            text_width = draw.textsize(text, font=font)[0]
        for offset in range(luma_device.width + text_width + 1):
            virtual.set_position((offset, 0))
            time.sleep(0.05)


class DateAnimation(TextAnimation):

    def __init__(self, debug=False):
        super(DateAnimation, self).__init__('%a %d %b %Y', debug)

    def create_text(self):
        return time.strftime(self.text)
