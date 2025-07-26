# Cowrie Honeypot Log Analyzer & Visualizer 🍯

This project provides a set of Python scripts to parse, analyze, and visualize log data from a [Cowrie](https://github.com/cowrie/cowrie) SSH/Telnet honeypot. It extracts key attack metrics, identifies attacker IPs, and generates an interactive world map to show the geographic location of the attackers.

-----

## ✨ Features

  * **Log Parsing**: Automatically parses Cowrie's plaintext log file (`cowrie.log`).
  * **Attack Analytics**: Extracts valuable information, including:
      * Top 10 most frequent attacker IP addresses.
      * Top 10 most common commands executed by attackers.
      * A list of all IPs that achieved a successful login.
      * Total number of connections and commands.
  * **JSON Report**: Generates a clean, structured `attack_report.json` file summarizing the analysis.
  * **Geolocation Tracking** 🌍: Uses the [ip-api.com](http://ip-api.com/) service to find the geographic location of each unique attacker IP.
  * **Interactive Visualization** 📊: Creates a `visual_report.html` file with an interactive world map plotting the location of attackers, built with Plotly.

-----

## 🚀 Getting Started

### 1. Setup Cowrie Honeypot
Follow the guide on Cowrie GitHub or use:
```
git clone https://github.com/cowrie/cowrie.git
cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt
cp etc/cowrie.cfg.dist etc/cowrie.cfg
```
Edit etc/cowrie.cfg to set ports, logging paths, etc.

Start Cowrie:
```bash
bin/cowrie start
```
### 2. Run the Dashboard

```bash
python app.py
```

Then visit http://localhost:5000

-----

## ⚙️ How It Works

The process is handled by two main scripts:

1.  **`cowrie-log-parser.py`**: This script reads the `cowrie.log` file. It uses regular expressions to find and count connection attempts, successful logins, and commands executed by attackers. It then saves this summary data to `output/attack_report.json`.

2.  **`visual_report.py`**: After the log parsing is complete, the first script calls this one. It takes the list of unique attacker IPs, queries a geolocation API for each one, and then uses Plotly and Pandas to generate an interactive HTML map visualizing the data.

The data flows as follows:
`cowrie.log` → `cowrie-log-parser.py` → `attack_report.json` → `visual_report.py` → `visual_report.html`

-----

## ✔️ Prerequisites

Before you begin, ensure you have the following set up:

1.  **A Running Cowrie Honeypot**: This tool analyzes logs from Cowrie. You must have Cowrie installed and running. If you need to set it up, please follow the [Official Cowrie Installation Guide](https://www.google.com/search?q=https://cowrie.readthedocs.io/en/latest/installation.html).
2.  **Python 3**: The scripts are written in Python 3. You can check your version with `python3 --version`.
3.  **Pip**: Python's package installer is required to install dependencies.

-----

## 🚀 Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Elite-Tadano/Cowrie_Honeypot_Deployment.git
    cd Cowrie_Honeypot_Deployment
    ```

2.  **Install Python dependencies:**
    It's recommended to create a `requirements.txt` file with the following content:

    ```
    pandas
    plotly
    requests
    ```

    Then, install the packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the Log Path:**
    Open the `cowrie-log-parser.py` file and **update the `LOG_PATH` variable** to point to your `cowrie.log` file.

    ```python
    # cowrie-log-parser.py

    # ❗ IMPORTANT: Change this path to match your Cowrie installation
    LOG_PATH = "/home/cowrie/cowrie/var/log/cowrie/cowrie.log" 
    ```

    The exact path can vary depending on your setup.

-----

## ▶️ Usage

After installation and configuration, running the analysis is simple. Just execute the main parser script:

```bash
python3 cowrie-log-parser.py
```

You will see the following output as it runs:

```
[*] Parsing plaintext Cowrie log...
[+] Parsed successfully. Generating visualization...
```

Once finished, the output files will be available in the `output/` directory.

-----

## 📄 Output Files

The script will create an `output` directory containing the following files:

1.  **`attack_report.json`**: A JSON file containing the summarized attack data.

    ```json
    {
      "top_ips": [["192.168.1.100", 50]],
      "successful_logins": ["192.168.1.100"],
      "top_commands": [["ls -la", 20], ["whoami", 15]],
      "total_commands": 150,
      "total_sessions": 75,
      "generated_at": "2025-07-26T12:00:00.000000"
    }
    ```

2.  **`visual_report.html`**: An interactive HTML map. **Open this file in your web browser** to see the geolocation of attacker IPs. You can hover over points to see IP and country details.

3.  **`ip_geolocation.json`**: A JSON array containing the raw geolocation data fetched from the API for each IP address.

-----

## ⚖️ License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
