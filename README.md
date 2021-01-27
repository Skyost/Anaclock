# Anaclock

Displays hour and date on a Raspberry Pi connected to a 4x64 LED Matrix
(from [AZ-Delivery](https://www.amazon.fr/gp/product/B079HVW652/)).

## Features

* Only needs a mouse.
* Displays hour with a little Pac-Man animation on mouse move / scroll / left click.
* Displays date on right click.
* Handle left click for more than 5 seconds to turn off the device (means no need to have a shutdown button).

## Installation

You need to install :

* [Pynput](https://pypi.org/project/pynput/).
* [Luma LED Matrix](https://luma-led-matrix.readthedocs.io/en/latest/install.html).
* [Luma Emulator](https://luma-emulator.readthedocs.io/en/latest/install.html).

## Usage

Run `python anaclock.py --debug=True or False --test=True or False` with :

* `debug = True` if you want to launch it via Pygame (needs Pygame and its dependencies to be installed),
  pass `False` or nothing if you want to launch it using the 4x64 LED Matrix.
* `test = True` if you want to run the `Test` module,
  pass `False` or nothing if you don't want to.

Therefore, if you want to run it in production, you'll must likely want to run `python anaclock.py`.