# Network Traffic Monitoring and Logging System

A comprehensive Python application for real-time network traffic monitoring and logging using Wireshark family tools (pyshark and tshark). This project demonstrates network analysis automation and extensive use of Python's `os` and `sys` modules.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Requirements Compliance](#project-requirements-compliance)

## ✨ Features

- **Real-time Network Monitoring**: Capture and analyze network traffic in real-time
- **Bandwidth Calculation**: Calculate bandwidth usage in Kbps for each connection
- **Protocol Detection**: Identify TCP, UDP, ICMP, and other protocols
- **Hostname Resolution**: Resolve IP addresses to hostnames with special handling for private networks
- **Two Monitoring Modes**: Basic (1-second intervals) and Detailed (sliding window analysis)
- **Packet Logging**: Save captured packets to log files
- **Cross-platform Support**: Works on Linux and can be adapted for Windows

## 🔧 Requirements

### System Requirements

#### Linux
- Python 3.6 or higher
- Wireshark/tshark installed
- libpcap library
- Root/administrator privileges for packet capture
- Standard Unix tools: `ping`, `curl`, `wget` (for testing)

#### Windows (if adapted)
- Python 3.6 or higher
- Npcap (WinPcap API-compatible mode)
- Wireshark/tshark installed
- Administrator privileges

### Python Dependencies

Install Python dependencies using:
```bash
pip install -r requirements.txt
```

See [requirements.txt](requirements.txt) for the complete list.

## 📦 Installation

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install wireshark tshark python3-pip
sudo apt-get install libpcap-dev
```

#### Fedora/RHEL
```bash
sudo dnf install wireshark tshark python3-pip
sudo dnf install libpcap-devel
```

#### macOS
```bash
brew install wireshark python3
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Permissions

For Linux, you may need to add your user to the wireshark group:
```bash
sudo usermod -aG wireshark $USER
# Log out and log back in for changes to take effect
```

Alternatively, run scripts with `sudo`:
```bash
sudo python3 network_bandwidth2.py -i eth0
```

## 🚀 Usage

### Network Bandwidth Monitor

#### Basic Mode
Monitor network traffic with 1-second interval updates:
```bash
python3 network_bandwidth2.py -i eth0
```

#### Detailed Mode (Sliding Window)
Monitor with sliding window analysis:
```bash
python3 network_bandwidth2.py -i eth0 --detailed
```

#### Custom Time Window
Set a custom time window for detailed mode:
```bash
python3 network_bandwidth2.py -i eth0 --detailed -w 5.0
```

**Command-line Arguments:**
- `-i, --interface`: Network interface name (required)
- `--detailed`: Enable sliding-window detailed mode
- `-w, --window`: Time window in seconds (default: 1.0)

**Example Output:**
```
Monitoring traffic on interface: eth0
Press CTRL+C to stop.

--- Traffic Breakdown (last 1s) ---
127.0.0.1 (Localhost) → 127.0.0.1 (Localhost) (TCP): 0.61 Kbps
90.130.70.73 (No-DNS) → 172.21.83.232 (Private Network) (TCP): 3668.58 Kbps
172.21.80.1 (Private Network) → 224.0.0.251 (Multicast) (UDP): 1.60 Kbps
```

### Network Logger

Capture packets and save to log file:
```bash
python3 network_logger_test2.py
```

The script will:
1. List available network interfaces
2. Prompt for interface selection
3. Start capturing packets
4. Save to `capture_log.txt` when stopped (press ENTER)

**Output Format:**
- Frame number
- Source IP address
- Destination IP address
- Frame length (bytes)

### Generate Test Traffic

Run the test script to generate network traffic for testing:
```bash
chmod +x traffic_test.sh
./traffic_test.sh
```

This script runs:
- Ping test to google.com (20 packets)
- HTTP request to example.com
- File download from speedtest.tele2.net

All tests run concurrently in the background.

## 📁 Project Structure

```
.
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── network_bandwidth2.py     # Real-time bandwidth monitor
├── network_logger_test2.py   # Packet capture logger
└── traffic_test.sh           # Test traffic generator
```

## 🔍 Modules

### network_bandwidth2.py

Real-time network bandwidth monitoring tool using pyshark.

**Key Functions:**
- `resolve_hostname(ip)`: Resolves IP addresses to hostnames with special handling for private, loopback, multicast, and reserved addresses
- `monitor_basic(interface)`: Basic monitoring mode showing traffic breakdown every second
- `monitor_detailed(interface, window)`: Detailed mode with sliding window analysis
- `main()`: Command-line interface using argparse

**Features:**
- Real-time packet capture
- Bandwidth calculation (Kbps)
- Protocol identification
- Hostname resolution
- Traffic statistics aggregation

**Technologies Used:**
- `pyshark`: Packet capture and parsing
- `socket`: Hostname resolution
- `ipaddress`: IP address classification
- `argparse`: Command-line argument parsing
- `collections.defaultdict`: Efficient statistics aggregation

### network_logger_test2.py

Network packet logger using tshark via subprocess.

**Key Features:**
- Interface selection using tshark
- Subprocess execution for tshark
- Threading for non-blocking keyboard input
- File I/O operations
- Error handling with proper exit codes

**Technologies Used:**
- `os`: File path operations (`os.path.abspath()`)
- `sys`: Standard input handling (`sys.stdin.fileno()`, `sys.stdin.read()`), exit codes (`sys.exit()`)
- `subprocess`: Execute tshark command-line tool
- `threading`: Background keyboard input monitoring
- `termios`/`tty`: Raw terminal input (Linux)

**Demonstrates:**
- Extensive use of `os` module for file operations
- Extensive use of `sys` module for I/O and program control
- Integration with external tools (tshark)
- Cross-platform considerations

### traffic_test.sh

Bash script to generate test network traffic.

**Features:**
- Concurrent network operations
- Multiple traffic types (ICMP, HTTP, file transfer)
- Background execution

## 🧪 Testing

### Test Scenario 1: Basic Monitoring
1. Start the monitor:
   ```bash
   python3 network_bandwidth2.py -i eth0
   ```
2. In another terminal, generate traffic:
   ```bash
   ./traffic_test.sh
   ```
3. Observe real-time traffic breakdown in the monitor

### Test Scenario 2: Detailed Mode
1. Start detailed monitoring:
   ```bash
   python3 network_bandwidth2.py -i eth0 --detailed -w 5.0
   ```
2. Generate traffic and observe sliding window analysis

### Test Scenario 3: Packet Logging
1. Start the logger:
   ```bash
   python3 network_logger_test2.py
   ```
2. Select interface and let it capture packets
3. Press ENTER to stop
4. Check `capture_log.txt` for captured packets

## 🔧 Troubleshooting

### "Permission denied" or "No packets captured"
**Solution:** Run with sudo/administrator privileges:
```bash
sudo python3 network_bandwidth2.py -i eth0
```

### "pyshark not found" or ImportError
**Solution:** Install pyshark:
```bash
pip install pyshark
```

### "tshark not found" or FileNotFoundError
**Solution:** Install Wireshark/tshark:
```bash
# Ubuntu/Debian
sudo apt-get install wireshark tshark

# Fedora/RHEL
sudo dnf install wireshark tshark

# macOS
brew install wireshark
```

### "No interfaces found"
**Solution:** 
1. List interfaces manually:
   ```bash
   tshark -D
   ```
2. Check interface is up:
   ```bash
   ip link show
   # or
   ifconfig
   ```

### Interface name issues
**Solution:** Use the exact interface name from `tshark -D` output. Common names:
- `eth0`, `eth1` (Ethernet)
- `wlan0`, `wlan1` (Wireless)
- `lo` (Loopback)

### termios module not available (Windows)
**Solution:** The `network_logger_test2.py` uses Linux-specific modules. For Windows, you would need to adapt the keyboard input handling using `msvcrt` or other Windows-compatible methods.

## ✅ Project Requirements Compliance

This project fulfills all requirements for the Final Project Exam:

- ✅ **Wireshark Family Tools**: Uses both `pyshark` and `tshark`
- ✅ **Python os Module**: Extensively used in `network_logger_test2.py`:
  - `os.path.abspath()` for file paths
  - File I/O operations
- ✅ **Python sys Module**: Extensively used in `network_logger_test2.py`:
  - `sys.stdin.fileno()` for file descriptor access
  - `sys.stdin.read()` for input handling
  - `sys.exit()` for program termination
- ✅ **Network Analysis**: Real-time traffic monitoring, protocol detection, bandwidth calculation
- ✅ **Automation**: Automated packet capture, statistics calculation, and logging
- ✅ **Network Logging Tool**: Complete packet logging functionality

## 📝 Notes

- The bandwidth monitor (`network_bandwidth2.py`) primarily uses pyshark for packet capture
- The network logger (`network_logger_test2.py`) demonstrates extensive use of `os` and `sys` modules
- Both tools work together to provide comprehensive network monitoring capabilities
- The test script helps validate the monitoring tools with realistic traffic patterns

## 📄 License

This project is created for educational purposes as part of a Final Project Exam.

## 👤 Author

- Muhammad Javier - 24/546674/PA/23210
- Khrisna Dwi Haryanto - 24/546482/PA/23198
- Aufa Sultan Majid Syach Putra Yuliyanto - 24/532890/PA/22550
- Yusuf Imantaka Bastari -  24/532731/PA/22530

---

**Note:** Always ensure you have proper authorization before monitoring network traffic. Unauthorized network monitoring may violate privacy laws and organizational policies.

