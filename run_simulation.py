import sys
import os
from traffic_simulation import TrafficSimulation

def main():
    """Main function to run the simulation."""
    
    print("=" * 70)
    print("FUZZY LOGIC TRAFFIC LIGHT CONTROLLER")
    print("Using SUMO Traffic Simulation")
    print("=" * 70)
    print()
    
    if 'SUMO_HOME' not in os.environ:
        print("ERROR: SUMO_HOME environment variable not set!")
        print()
        print("Please install SUMO and set the SUMO_HOME environment variable:")
        print("  Windows: set SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo")
        print("  Linux/Mac: export SUMO_HOME=/usr/share/sumo")
        print()
        return 1
    
    if not os.path.exists("sumo_files/intersection.net.xml"):
        print("ERROR: Network file not found!")
        print("Please run 'python build_network.py' first to generate the network")
        return 1
    
    sumo_config = "sumo_files/intersection.sumocfg"
    
    if not os.path.exists(sumo_config):
        print(f"ERROR: Configuration file not found: {sumo_config}")
        return 1
    
    print("Configuration:")
    print(f"  - SUMO Config: {sumo_config}")
    print(f"  - SUMO_HOME: {os.environ['SUMO_HOME']}")
    print(f"  - Simulation Duration: 3600 seconds (1 hour)")
    print()
    
    use_gui = input("Use SUMO GUI? (y/n, default=y): ").strip().lower()
    use_gui = use_gui != 'n'
    
    print()
    print("Starting simulation...")
    print()
    
    try:
        sim = TrafficSimulation(sumo_config, use_gui=use_gui)
        sim.run_simulation(duration=3600)
        
        print()
        print("Simulation completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        print()
        print("Simulation interrupted by user")
        return 1
    except Exception as e:
        print()
        print(f"ERROR: Simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())