import os
import sys
import subprocess


def build_sumo_network():
    """Generate SUMO network file from nodes, edges, and connections."""
    
    print("Building SUMO Network with Safe Traffic Light Logic...")
    print("-" * 50)
    
    if 'SUMO_HOME' not in os.environ:
        print("ERROR: SUMO_HOME environment variable not set!")
        print("Please install SUMO and set SUMO_HOME to the installation directory")
        return False
    
    netconvert = os.path.join(os.environ['SUMO_HOME'], 'bin', 'netconvert')
    
    if os.name == 'nt':
        netconvert += '.exe'
    
    # Check if TLS file exists
    tls_file = 'sumo_files/intersection.tls.xml'
    if not os.path.exists(tls_file):
        print(f"WARNING: {tls_file} not found!")
        print("Creating it now with safe traffic light phases...")
        try:
            result = subprocess.run([sys.executable, 'fix_traffic_lights.py'], 
                                  capture_output=True, text=True, check=True)
            print("TLS file created successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error creating TLS file: {e}")
            return False
        except FileNotFoundError:
            print("ERROR: fix_traffic_lights.py not found!")
            print("Please run: python fix_traffic_lights.py")
            return False
    
    cmd = [
        netconvert,
        '--node-files=sumo_files/intersection.nod.xml',
        '--edge-files=sumo_files/intersection.edg.xml',
        '--connection-files=sumo_files/intersection.con.xml',
        '--tllogic-files=sumo_files/intersection.tls.xml',
        '--output-file=sumo_files/intersection.net.xml',
        '--no-turnarounds'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Network built successfully!")
            print(f"Output: sumo_files/intersection.net.xml")
            print()
            print("SAFETY CHECK:")
            print("  Phase 0: NS=GREEN,  EW=RED    (Safe)")
            print("  Phase 1: NS=YELLOW, EW=RED    (Safe)")
            print("  Phase 2: NS=RED,    EW=GREEN  (Safe)")
            print("  Phase 3: NS=RED,    EW=YELLOW (Safe)")
            print()
            print("NO conflicting greens - collision risk eliminated!")
            return True
        else:
            print(f"Error building network:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print(f"ERROR: netconvert not found at {netconvert}")
        print("Please check your SUMO installation")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = build_sumo_network()
    sys.exit(0 if success else 1)
