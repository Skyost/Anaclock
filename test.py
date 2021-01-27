from animation import HourAnimation, DateAnimation


class Test(object):

    def __init__(self, debug=False):
        self.hour_animation = HourAnimation(debug=debug)
        self.date_animation = DateAnimation(debug=debug)

    def run(self):
        self.hour_animation.run()
        self.date_animation.run()
