"""
Fuzzy Logic Traffic Light Controller
This module implements a fuzzy logic system to control traffic lights based on
vehicle queue length and waiting time.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyTrafficController:
    """
    Fuzzy Logic Controller for adaptive traffic light management.

    Inputs:
    - queue_length: Number of vehicles waiting at the intersection
    - waiting_time: Average waiting time of vehicles

    Output:
    - green_time: Duration of green light phase (in seconds)
    """

    def __init__(self):
        self.setup_fuzzy_system()

    def setup_fuzzy_system(self):
        """Initialize fuzzy logic system with membership functions and rules."""

        # Input variables
        self.queue_length = ctrl.Antecedent(np.arange(0, 51, 1), 'queue_length')
        self.waiting_time = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_time')
        
        # Output variable
        self.green_time = ctrl.Consequent(np.arange(10, 91, 1), 'green_time')

        # Define membership functions for queue_length
        self.queue_length['low'] = fuzz.trimf(self.queue_length.universe, [0, 0, 15])
        self.queue_length['medium'] = fuzz.trimf(self.queue_length.universe, [10, 25, 40])
        self.queue_length['high'] = fuzz.trimf(self.queue_length.universe, [35, 50, 50])

        # Define membership functions for waiting_time
        self.waiting_time['short'] = fuzz.trimf(self.waiting_time.universe, [0, 0, 100])
        self.waiting_time['medium'] = fuzz.trimf(self.waiting_time.universe, [60, 150, 240])
        self.waiting_time['long'] = fuzz.trimf(self.waiting_time.universe, [200, 300, 300])

        # Define membership functions for green_time
        self.green_time['short'] = fuzz.trimf(self.green_time.universe, [10, 10, 30])
        self.green_time['medium'] = fuzz.trimf(self.green_time.universe, [25, 50, 75])
        self.green_time['long'] = fuzz.trimf(self.green_time.universe, [60, 90, 90])

        self.create_rules()
        self.control_system = ctrl.ControlSystem(self.rules)
        self.controller = ctrl.ControlSystemSimulation(self.control_system)

    def create_rules(self):
        """Define fuzzy rules for traffic light control."""
        self.rules = [
            ctrl.Rule(self.queue_length['low'] & self.waiting_time['short'],
                     self.green_time['short']),
            ctrl.Rule(self.queue_length['low'] & self.waiting_time['medium'],
                     self.green_time['short']),
            ctrl.Rule(self.queue_length['low'] & self.waiting_time['long'],
                     self.green_time['medium']),
            ctrl.Rule(self.queue_length['medium'] & self.waiting_time['short'],
                     self.green_time['medium']),
            ctrl.Rule(self.queue_length['medium'] & self.waiting_time['medium'],
                     self.green_time['medium']),
            ctrl.Rule(self.queue_length['medium'] & self.waiting_time['long'],
                     self.green_time['long']),
            ctrl.Rule(self.queue_length['high'] & self.waiting_time['short'],
                     self.green_time['medium']),
            ctrl.Rule(self.queue_length['high'] & self.waiting_time['medium'],
                     self.green_time['long']),
            ctrl.Rule(self.queue_length['high'] & self.waiting_time['long'],
                     self.green_time['long']),
        ]

    def compute_green_time(self, queue_len, wait_time):
        """
        Calculate optimal green time based on queue length and waiting time.

        Args:
            queue_len (int): Number of vehicles in queue
            wait_time (float): Average waiting time in seconds

        Returns:
            float: Recommended green light duration in seconds
        """
        queue_len = max(0, min(50, queue_len))
        wait_time = max(0, min(300, wait_time))

        self.controller.input['queue_length'] = queue_len
        self.controller.input['waiting_time'] = wait_time
        self.controller.compute()

        return self.controller.output['green_time']


if __name__ == "__main__":
    controller = FuzzyTrafficController()

    test_cases = [
        (5, 30),
        (25, 150),
        (45, 250),
        (10, 200),
        (40, 50),
    ]

    print("Fuzzy Traffic Light Controller - Test Results")
    print("=" * 60)
    print(f"{'Queue Length':<15} {'Waiting Time':<15} {'Green Time':<15}")
    print("-" * 60)

    for queue, wait in test_cases:
        green_time = controller.compute_green_time(queue, wait)
        print(f"{queue:<15} {wait:<15} {green_time:<15.2f}")

    print("=" * 60)
