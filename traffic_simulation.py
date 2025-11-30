"""
SUMO Traffic Simulation with Fuzzy Logic Controller
"""

import os
import sys
import traci
import numpy as np
from fuzzy_traffic_controller import FuzzyTrafficController


class TrafficSimulation:
    def __init__(self, sumo_cfg_file, use_gui=True):
        self.sumo_cfg = sumo_cfg_file
        self.use_gui = use_gui
        self.fuzzy_controller = FuzzyTrafficController()
        self.tl_id = "0"
        
        self.phases = {
            'NS_green': 0,
            'NS_yellow': 1,
            'EW_green': 2,
            'EW_yellow': 3
        }
        
        self.current_phase = 'NS_green'
        self.phase_start_time = 0
        self.yellow_time = 3
        
        self.stats = {
            'total_waiting_time': 0,
            'total_vehicles': 0,
            'phase_changes': 0,
            'avg_queue_lengths': [],
            'avg_waiting_times': []
        }
        
        self.lanes = {
            'NS': ['N2C_0', 'N2C_1', 'S2C_0', 'S2C_1'],
            'EW': ['E2C_0', 'E2C_1', 'W2C_0', 'W2C_1']
        }

    def start_sumo(self):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("Please declare environment variable 'SUMO_HOME'")

        if self.use_gui:
            sumo_binary = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo-gui')
        else:
            sumo_binary = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo')

        sumo_cmd = [sumo_binary, "-c", self.sumo_cfg]
        traci.start(sumo_cmd)

    def get_lane_metrics(self, lanes):
        total_queue = 0
        total_waiting = 0
        vehicle_count = 0

        for lane in lanes:
            halting = traci.lane.getLastStepHaltingNumber(lane)
            total_queue += halting

            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for veh in vehicles:
                waiting_time = traci.vehicle.getWaitingTime(veh)
                total_waiting += waiting_time
                vehicle_count += 1

        avg_waiting = total_waiting / vehicle_count if vehicle_count > 0 else 0
        return total_queue, avg_waiting

    def compute_optimal_green_time(self, direction):
        lanes = self.lanes[direction]
        queue_length, waiting_time = self.get_lane_metrics(lanes)
        green_time = self.fuzzy_controller.compute_green_time(queue_length, waiting_time)
        
        self.stats['avg_queue_lengths'].append(queue_length)
        self.stats['avg_waiting_times'].append(waiting_time)
        
        return green_time

    def set_traffic_light_phase(self, phase_name):
        phase_index = self.phases[phase_name]
        traci.trafficlight.setPhase(self.tl_id, phase_index)
        self.current_phase = phase_name
        self.phase_start_time = traci.simulation.getTime()

    def run_simulation(self, duration=3600):
        self.start_sumo()
        step = 0
        current_green_time = 30
        
        print("Starting Traffic Simulation with Fuzzy Logic Controller")
        print("=" * 70)

        try:
            while step < duration:
                traci.simulationStep()
                current_time = traci.simulation.getTime()
                elapsed = current_time - self.phase_start_time

                if self.current_phase == 'NS_green':
                    if elapsed >= current_green_time:
                        self.set_traffic_light_phase('NS_yellow')
                        self.stats['phase_changes'] += 1
                        print(f"Time {current_time:.0f}s: NS Yellow (3s)")

                elif self.current_phase == 'NS_yellow':
                    if elapsed >= self.yellow_time:
                        current_green_time = self.compute_optimal_green_time('EW')
                        self.set_traffic_light_phase('EW_green')
                        print(f"Time {current_time:.0f}s: EW Green ({current_green_time:.1f}s)")

                elif self.current_phase == 'EW_green':
                    if elapsed >= current_green_time:
                        self.set_traffic_light_phase('EW_yellow')
                        self.stats['phase_changes'] += 1
                        print(f"Time {current_time:.0f}s: EW Yellow (3s)")

                elif self.current_phase == 'EW_yellow':
                    if elapsed >= self.yellow_time:
                        current_green_time = self.compute_optimal_green_time('NS')
                        self.set_traffic_light_phase('NS_green')
                        print(f"Time {current_time:.0f}s: NS Green ({current_green_time:.1f}s)")

                vehicles = traci.vehicle.getIDList()
                self.stats['total_vehicles'] = len(vehicles)
                
                for veh in vehicles:
                    self.stats['total_waiting_time'] += traci.vehicle.getWaitingTime(veh)

                step += 1

        except traci.exceptions.FatalTraCIError as e:
            print(f"SUMO simulation error: {e}")
        finally:
            traci.close()
            self.print_statistics()

    def print_statistics(self):
        print("\n" + "=" * 70)
        print("SIMULATION STATISTICS")
        print("=" * 70)
        print(f"Total Phase Changes: {self.stats['phase_changes']}")
        print(f"Total Vehicles Processed: {self.stats['total_vehicles']}")
        
        if self.stats['avg_queue_lengths']:
            avg_queue = np.mean(self.stats['avg_queue_lengths'])
            print(f"Average Queue Length: {avg_queue:.2f} vehicles")
        
        if self.stats['avg_waiting_times']:
            avg_wait = np.mean(self.stats['avg_waiting_times'])
            print(f"Average Waiting Time: {avg_wait:.2f} seconds")
        
        print("=" * 70)


if __name__ == "__main__":
    sumo_config = "sumo_files/intersection.sumocfg"
    
    if 'SUMO_HOME' not in os.environ:
        print("ERROR: SUMO_HOME environment variable not set!")
        print("Please set SUMO_HOME to your SUMO installation directory")
        sys.exit(1)
    
    sim = TrafficSimulation(sumo_config, use_gui=True)
    sim.run_simulation(duration=3600)
