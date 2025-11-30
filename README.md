# Traffic Light Controller Using Fuzzy Logic

A smart traffic light control system that uses fuzzy logic to adjust traffic signal timings based on real-time traffic conditions. The system is integrated with SUMO (Simulation of Urban MObility) for realistic traffic simulation.

## Project Overview

This project implements an adaptive traffic light controller that:
- Uses fuzzy logic to make intelligent decisions about traffic light timings
- Monitors queue lengths and waiting times at intersections
- Dynamically adjusts green light durations to optimize traffic flow
- Reduces average waiting times and congestion

## Features

- **Fuzzy Logic Controller**: Implements a Mamdani-type fuzzy inference system with:
  - Input variables: Queue length (0-50 vehicles), Waiting time (0-300 seconds)
  - Output variable: Green light duration (10-90 seconds)
  - 9 fuzzy rules for intelligent decision-making

- **SUMO Integration**: 
  - 4-way intersection simulation with realistic traffic patterns
  - Multiple vehicle routes and flows
  - Real-time traffic data collection via TraCI

- **Adaptive Control**:
  - Monitors traffic conditions in real-time
  - Adjusts signal timings based on current traffic demand
  - Yellow light transitions for safe phase changes

## Project Structure

```
NNFL_Project/
├── fuzzy_traffic_controller.py    # Fuzzy logic controller implementation
├── traffic_simulation.py           # SUMO-Python integration
├── run_simulation.py              # Main simulation runner
├── build_network.py               # Network generation script
├── requirements.txt               # Python dependencies
├── sumo_files/                    # SUMO configuration files
│   ├── intersection.nod.xml       # Network nodes
│   ├── intersection.edg.xml       # Network edges
│   ├── intersection.con.xml       # Lane connections
│   ├── intersection.rou.xml       # Vehicle routes and flows
│   ├── intersection.sumocfg       # SUMO configuration
│   └── intersection.net.xml       # Generated network (after build)
└── README.md                     
```

## Prerequisites

### 1. Install SUMO
- Download SUMO from: https://www.eclipse.org/sumo/


### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Installation & Setup

1. **Clone or download this project**

2. **Set SUMO_HOME environment variable** 

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the SUMO network:**
   ```bash
   python build_network.py
   ```
   This generates `sumo_files/intersection.net.xml` from the network definition files.

## Running the Simulation

### Basic Usage

```bash
python run_simulation.py
```

The script will prompt you to choose between GUI or headless mode:
- **GUI mode**: Visual simulation with SUMO's graphical interface
- **Headless mode**: Faster simulation without graphics

### Direct Execution

Run with GUI:
```bash
python traffic_simulation.py
```

## How It Works

### 1. Fuzzy Logic Controller

The fuzzy controller uses three membership functions for each variable:

**Input: Queue Length (vehicles)**
- Low: 0-15 vehicles
- Medium: 10-40 vehicles
- High: 35-50 vehicles

**Input: Waiting Time (seconds)**
- Short: 0-100 seconds
- Medium: 60-240 seconds
- Long: 200-300 seconds

**Output: Green Time (seconds)**
- Short: 10-30 seconds
- Medium: 25-75 seconds
- Long: 60-90 seconds

**Fuzzy Rules:**
1. IF queue is LOW AND wait is SHORT → green time is SHORT
2. IF queue is LOW AND wait is MEDIUM → green time is SHORT
3. IF queue is LOW AND wait is LONG → green time is MEDIUM
4. IF queue is MEDIUM AND wait is SHORT → green time is MEDIUM
5. IF queue is MEDIUM AND wait is MEDIUM → green time is MEDIUM
6. IF queue is MEDIUM AND wait is LONG → green time is LONG
7. IF queue is HIGH AND wait is SHORT → green time is MEDIUM
8. IF queue is HIGH AND wait is MEDIUM → green time is LONG
9. IF queue is HIGH AND wait is LONG → green time is LONG

### 2. Traffic Simulation

The SUMO simulation creates a 4-way intersection with:
- 2 lanes per approach (North, South, East, West)
- Vehicle flows with varying probabilities
- Traffic light phases:
  - Phase 0: North-South green
  - Phase 1: North-South yellow
  - Phase 2: East-West green
  - Phase 3: East-West yellow

### 3. Control Loop

1. Monitor current phase and elapsed time
2. When green phase completes:
   - Switch to yellow phase (3 seconds)
   - Calculate next direction's traffic metrics
   - Use fuzzy controller to determine optimal green time
3. Switch to next green phase with calculated duration
4. Repeat

## Testing the Fuzzy Controller

Test the fuzzy logic independently:

```bash
python fuzzy_traffic_controller.py
```

This will run test cases and display the fuzzy outputs for different traffic scenarios.

## Customization

### Adjust Fuzzy Logic Parameters

Edit `fuzzy_traffic_controller.py`:
- Modify membership function ranges
- Add/remove fuzzy rules
- Change input/output variable universes

### Modify Traffic Patterns

Edit `sumo_files/intersection.rou.xml`:
- Change vehicle flow probabilities
- Add new routes
- Adjust vehicle types and speeds

### Change Intersection Layout

Edit SUMO network files:
- `intersection.nod.xml`: Node positions
- `intersection.edg.xml`: Road parameters
- `intersection.con.xml`: Lane connections

After changes, rebuild the network:
```bash
python build_network.py
```

## Performance Metrics

The simulation tracks:
- Total phase changes
- Total vehicles processed
- Average queue length
- Average waiting time

Statistics are displayed at the end of each simulation run.


## References

- SUMO Documentation: https://sumo.dlr.de/docs/
- Scikit-Fuzzy: https://pythonhosted.org/scikit-fuzzy/
- Fuzzy Logic in Traffic Control: Various research papers on adaptive traffic signal control

## License

This project is built as part of Neural Network & Fuzzy Logic (NNFL) coursework.

