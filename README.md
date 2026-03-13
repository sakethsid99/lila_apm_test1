# LILA BLACK Visualization: Journey Nexus

Journey Nexus is a powerful, interactive visualization tool designed to analyze player movement, combat, and looting patterns in the LILA BLACK game world. It transforms raw Parquet event data into actionable heatmaps and playback animations.

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.8 or higher.
*   The `player_data` folder should be in the root directory (containing date folders and `minimaps`).

### 2. Installation
Clone the repository and install the required dependencies:
```bash
# In the project root
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
*   **Core**: Python
*   **Interface**: Streamlit
*   **Data Analysis**: Pandas, Pyarrow
*   **Visualization**: Plotly Express, Plotly Graph Objects
*   **Image Processing**: Pillow (PIL)

## 🗺️ Key Features
*   **Match Statistics**: Real-time counters for Kills, Deaths, and Loots per match.
*   **Multilayered Visualization**: Toggle between Individual Paths (scatter), Density Heatmaps, or both.
*   **Smart Playback**: Play, Pause, Rewind, and Forward buttons with a synchronized time scrubber.
*   **Coordinate Mapping**: Automated conversion from world coordinates to minimap pixels for all three maps (AmbroseValley, GrandRift, Lockdown).

## 📄 Documentation
*   [ARCHITECTURE.md](ARCHITECTURE.md): Technical deep-dive into coordinate mapping and data flow.
*   [INSIGHTS.md](INSIGHTS.md): Analysis of three key game-design patterns discovered using this tool.
