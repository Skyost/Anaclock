from threading import Thread

from animation import HourAnimation, DateAnimation, TextAnimation


class Displayer(object):

    def __init__(self, debug=False):
        self.current_thread = None
        self.hour_animation = HourAnimation(debug=debug)
        self.date_animation = DateAnimation(debug=debug)
        self.create_text_animation = lambda text: TextAnimation(text, debug=debug)

    def display_hour(self):
        return self.animate_if_possible(self.hour_animation)

    def display_date(self):
        return self.animate_if_possible(self.date_animation)

    def display_text(self, text):
        return self.animate_if_possible(self.create_text_animation(text))

    def animate_if_possible(self, animation):
        if self.current_thread is not None and self.current_thread.is_alive():
            return
        self.current_thread = Thread(target=self.run_animation, args=[animation])
        self.current_thread.start()
        return self.current_thread

    def run_animation(self, animation):
        animation.run()
        self.current_thread = None
