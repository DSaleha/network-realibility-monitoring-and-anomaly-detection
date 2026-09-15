# Network Reliability Monitoring & Anomaly Detection (End-to-End Project)
<img width="747" height="445" alt="Rpi 4" src="https://github.com/user-attachments/assets/cb71fb85-252b-4da4-8b61-b9503a87cea9" />


## 1. Problem
Building management needs to distinguish ISP-related connectivity issues from internal network problems.

## 2. Role
Designed the monitoring algorithm and data collection system, performed exploratory data analysis, and developed anomaly detection approaches.

## 3. Tech
### 3.1 Software
- **IDE:** VS Code, Thonny IDE
- **Programming Language:** Python 3
- **Libraries:** Ping3, Speedtest-CLI, Tkinter, SQLite3, Pandas, Matplotlib

### 3.2 Hardware
- Raspberry Pi 4 Model B (with kit)
- LCD 5"
- LAN cable

## 4. Approach

### 4.1 Logic Architecture Design

#### 4.1.1 Network Topology

#### 4.1.2 Measurement Indicators
- **Connectivity indicator:** real-time PING test every 5 seconds
- **Bandwidth indicator:** SPEEDTEST every 5-minute interval

#### 4.1.3 Algorithm (Flowchart)
The program runs sequentially (waterfall logic), switching the IP target node by node — from internal to external — using boolean checks. A speedtest is only triggered once the final status is confirmed online.

<img width="1538" height="2500" alt="flowchart" src="https://github.com/user-attachments/assets/8c9e4920-74a0-41a2-b3e7-a3746d5a5677" />



#### 4.1.4 Folder Structure
Multi-folder layout, split by function/module:

```
ISP_Monitoring/
├── venv/
├── logs/
│   ├── backend.log
│   └── history.sqlite
├── cache/
│   ├── last_result.json
│   └── last_result.json.bak
│
├── config.py
├── utils.py           #helper functions: JSON cache, time formatting, Pi status
├── db_logger.py       #sQLite save logic & database initialization
├── ping_check.py
├── speed_check.py
│
├── main.py             #backend
├── gui_display.py      #frontend
└── launcher.sh
```

### 4.2 Data Handling
Due to SD card storage limitations, logs are capped at 1000 rows — once the limit is reached, the oldest entry is overwritten. Ping history is only written to the database when the connectivity status changes.

### 4.3 User Interface
Since the display is a 5" LCD, the UI is kept minimal — color-coded status is the primary signal so anyone walking by can instantly tell whether the network is healthy or degraded. Alongside the color indicator, real-time ping/speedtest numbers and a short interpretation of each condition are shown to help staff decide on next steps.

<img width="887" height="554" alt="final_ui" src="https://github.com/user-attachments/assets/77d43e82-9145-47c1-bce8-c24afe908abf" />

### 4.4 Troubleshooting Matrix
A standard troubleshooting table is included so anyone on-site can follow a consistent process when an issue occurs.

![Troubleshooting matrix](path/to/troubleshooting_matrix.png)

## 5 Debugging
Since the hardware is mounted permanently on the wall, debugging is done remotely via VNC Viewer.

## 6 Data Analysis Cycle (1-Month Trial — Linknet Monitoring)
An end-to-end data analysis of Linknet ISP performance and network stability during a 1-month trial period (April 24, 2026 – May 25, 2026). 
The analysis combines event logs (monitoring_logs.csv) and system telemetry logs (backend.csv).

The goal of this project is to analyze network disruption logs, identify patterns, filter out system noise, and provide actionable engineering recommendations.

### 6.1 Data Analysis Folder Structure
```
EDA_ISP_Monitoring/
├── dataset/
│   ├── monitoring_logs.csv
│   └── backend.csv
└── analisis_internet_monitoring.ipynb
```

### 6.2 Executive Summary
Total Processed Logs: 476,567 telemetry records (backend.csv) and 1,000 main event logs (monitoring_logs.csv).
Total Network Incidents: 142 events (14.2% of total event logs), consolidating into 89 unique disturbance episodes using a 30-minute time-gap threshold.
Peak Disruption Window: Disruptions peak between 07:00–08:00 AM, with the failure rate reaching 26.8% of total recorded traffic at 07:00 AM.
Incident Type Breakdown:

* Disrupted External Internet Access — 50.0% (71 events)
* Internal Router Issue — 36.6% (52 events)
* Building ISP Issue — 13.4% (19 events)

<img width="1189" height="489" alt="image" src="https://github.com/user-attachments/assets/a6b88f1e-82ed-4d12-aa10-bf22280944eb" />

### 6.3 Data Analysis Cycle
This project follows the data analysis lifecycle end-to-end, from raw logs to actionable recommendations:

#### 6.3.1 Data Collection & Preparation
* Datasets: Ingested two main datasets — monitoring_logs.csv (1,000 rows of main event logs) and backend.csv (476,567 rows of system telemetry data).
* Parsing: Used Regex to extract timestamps, statuses, latency (ms), and router temperature (°C) from raw text logs in the backend data.

#### 6.3.2 Data Cleaning & Preprocessing
* Datetime Transformation: Converted string timestamps into pandas datetime objects and extracted the hour feature for time-series analysis.
* Filtering: Excluded SPEEDTEST and Normal statuses to isolate the 142 rows of actual disruption data.
* Outlier Detection: Found a latency outlier of 899.47 ms still labeled INTERNET NORMAL, revealing a logical flaw in the monitoring system.

#### 6.3.3 Exploratory Data Analysis (EDA) & Visualization
* Proportion Analysis: Grouped disruptions by type — External Internet Disruption accounts for 50.0% of issues, followed by Internal Router Issue (36.6%) and Building ISP Issue (13.4%).
* Hourly Trend Mapping: Calculated the percentage of disruptions per hour against the total logs for that hour. Finding: 07:00–08:00 AM is the most vulnerable window, with up to a 26.8% failure rate.
* Data Visualization: Built pie charts and stacked bar charts with matplotlib to visualize the breakdown of disruption types across different hours.
  
<img width="1358" height="515" alt="download" src="https://github.com/user-attachments/assets/76654112-6d7e-429b-9ceb-dd8474ce8171" />

#### 6.3.4 Advanced Analysis & Feature Engineering (Noise Filtering)
* Thresholding & Episode Grouping: Solved a "system blind spot" where back-to-back logs created the illusion of a single 4-hour outage. Engineered a new rule: a gap of >30 minutes defines a new episode.
* Duration Calculation: Grouped the 142 logs into 89 unique episodes and classified each by duration:
  * Noise / False Positive (< 1 min): 60 episodes
  * Needs Monitoring (1–5 mins): 11 episodes
  * Genuine Outage (> 5 mins): 18 episodes
* Data Merging: Used pd.merge_asof (2-minute tolerance) to safely join event logs with backend telemetry data on the nearest timestamp.

#### 6.3.5 Insights & Business Recommendations
* Temperature Correlation: Router temperature averaged 45.35°C (range: 39.9°C–53.6°C, median 45.3°C).
  Temperature is not the root cause of disruptions — most outages occurred within normal temperature ranges.
<img width="1256" height="472" alt="image" src="https://github.com/user-attachments/assets/128903f2-e58e-4f5a-a396-743a608a725e" />
  
* System Logic Evaluation: The latency_ms metric measures different endpoints depending on status (NORMAL = Google DNS, DEGRADED = Building Gateway, DOWN = Internal Router), making cross-status latency comparisons invalid.
  
## 7 Key Insights

### 7.1 Time of Day Pattern
Disruptions correlate strongly with office start hours:
| Time | Failure Rate | Logs |
| :--- | :---: | :--- |
| 07:00 AM | **26.8%** | 19 of 71 |
| 08:00 AM | 22.0% | 13 of 59 |
| 11:00 AM | 20.4% | 11 of 54 |

Interpretation: Concurrent connection spikes during morning office hours strain both external bandwidth and internal routing devices.

### 7.2 Incident Classification & Noise Filtering
Episodes are categorized by duration to separate genuine downtime from temporary network noise:
| Episode Category | Duration | Count | Status & Action |
| :--- | :--- | :---: | :--- |
| **Noise / Intermittent** | < 1 min | **60** | Momentary ping drops / transient spikes |
| **Needs Monitoring** | 1–5 mins | **11** | Short micro-outages requiring observation |
| **Genuine Incident** | > 5 mins | **18** | Valid outages requiring technical intervention |

Note: All Building ISP Issue episodes lasted under 5 minutes. Longer outages (20–60+ minutes) were dominated by Disrupted External Internet Access.

### 7.3 Monitoring System Blind Spot
The system currently relies only on packet loss (ping return).
High latency (e.g., 899.47 ms) still registers as INTERNET NORMAL because the ping eventually returns — there is no high-latency alert threshold.

## 8 Evaluation
* Add secondary fallback targets.
* Run the PING test 3 times per node.
* Modify the backend logic to eliminate the blind spot.
* Schedule Preventive Maintenance, including physical inspection and bandwidth checks.

## 9 Documentation
<img width="1572" height="1060" alt="image" src="https://github.com/user-attachments/assets/0259d7c8-73fc-40bf-8d89-6d70104e2a65" />


---
# THANK YOU (Dede Saleha - 2026)
