from abc import ABC, abstractmethod
from threading import Thread
import random
import time
import logging
import sys
import os


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='')

is_run_generator = True


class Event(ABC):

    @abstractmethod
    def change_plane_roll(self, tilt, rate_of_correction):
        pass


class Turbulence(Event):
    def __init__(self, current_turbulence):
        self.current_turbulence = current_turbulence

    def change_plane_roll(self, tilt, rate_of_correction=0):
        self.current_turbulence = random.gauss(0, 5)
        tilt += self.current_turbulence
        return tilt


class Correction(Event):
    def __init__(self, current_correction):
        self.current_correction = current_correction

    def change_plane_roll(self, tilt, rate_of_correction):
        self.current_correction = -tilt * rate_of_correction
        tilt += self.current_correction
        return tilt


class Plane:
    def __init__(self, roll):
        self.roll = roll
        self.correction = Correction(0)

    def correct_flight_trajectory(self):
        time.sleep(0.5)
        self.roll = self.correction.change_plane_roll(self.roll, random.random())


class Environment:
    def __init__(self, plane, turbulence):
        self.plane = plane
        self.turbulence = turbulence

    def generate_turbulence(self):
        global is_run_generator
        while is_run_generator:
            self.plane.roll = \
                self.turbulence.change_plane_roll(self.plane.roll)
            yield self.turbulence.current_turbulence


def clear_terminal():
    clear_command = {'posix': 'clear', 'nt': 'cls'}
    os.system(clear_command.get(os.name, ' '))


def get_formatted_num(num):
    if num >= 0:
        return f"+{num}"
    else:
        return f"{num}"


airplane = Plane(0)
environment = Environment(airplane, Turbulence(0))


def flight_loop(plane):
    initial_plane_roll = plane.roll
    for turbulence in environment.generate_turbulence():
        logging.info(f"Initial plane roll: {initial_plane_roll}\n"
                     f"Turbulence: {get_formatted_num(turbulence)}\n"
                     f"Plane roll: {plane.roll}")
        plane.correct_flight_trajectory()
        logging.info(f"Correction: {get_formatted_num(plane.correction.current_correction)}\n"
                     f"Final plane roll: {plane.roll}\n"
                     f"Press Enter to catapult\n")
        time.sleep(1.5)
        initial_plane_roll = plane.roll
        clear_terminal()


if __name__ == '__main__':
    flight_thread = Thread(target=flight_loop, args=(airplane,))
    user_thread = Thread(target=input)
    flight_thread.start()

    user_thread.start()
    user_thread.join()
    is_run_generator = False
    flight_thread.join()
    logging.info("You catapulted from the plane")
