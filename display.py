from threading import Thread

from animation import Animation, HourAnimation, DateAnimation, TextAnimation


class Display(object):

    def __init__(self, debug: bool = False):
        self.current_thread = None
        self.hour_animation = HourAnimation(debug)
        self.date_animation = DateAnimation(debug)
        self.create_text_animation = lambda text: TextAnimation(text, debug)

    def display_hour(self) -> Thread:
        return self.animate_if_possible(self.hour_animation)

    def display_date(self) -> Thread:
        return self.animate_if_possible(self.date_animation)

    def display_text(self, text: str) -> Thread:
        return self.animate_if_possible(self.create_text_animation(text))

    def animate_if_possible(self, animation: Animation) -> Thread:
        if self.current_thread is not None and self.current_thread.is_alive():
            return self.current_thread
        self.current_thread = Thread(target=self.run_animation, args=[animation])
        self.current_thread.start()
        return self.current_thread

    def run_animation(self, animation: Animation):
        animation.run()
        self.current_thread = None
