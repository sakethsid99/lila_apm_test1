# LILA BLACK Visualization: Journey Nexus
# Link for working tool: https://lilablack.streamlit.app/

Journey Nexus is a powerful, interactive visualization tool designed to analyze player movement, combat, and looting patterns in the LILA BLACK game world. It transforms raw Parquet event data into actionable heatmaps and playback animations. 

Target User : Level Designer
Name: Sid, Level Designer at LILA Games

Objective: To create maps that feel balanced, exciting, and free of "frustrating" deaths.

Core Need: Sid needs to know if the physical landmarks he placed (bridges, towers, loot rooms) are actually being used by players or if they are becoming "dead zones."

The Pain Points
Data Blindness: Sid has thousands of telemetry rows but cannot "see" the flow of a match. He is guessing where bottlenecks occur.
The "Bot Noise" Problem: Raw data mixes human and bot movement. Sid needs to know how real players behave, as bots often follow predictable paths that don't reflect true player sentiment.

Static vs. Dynamic Flow: He can see where people died, but he doesn't know when or why. Was it a fair fight, or did the "Storm" trap them because of poor terrain design?

🛠️ How This Tool Solves Them
This visualization tool transforms raw Parquet files into an interactive diagnostic dashboard:
Match Reconstruction: Instead of viewing isolated journeys, the tool aggregates all files by match_id. Sid can watch an entire 50-player session unfold in real-time using the Timeline Playback.
Human-Centric Filtering: With a single toggle, Sid can filter out bots to analyze authentic human "Hotdrop" behavior and rotation patterns.
Lethality Heatmaps: The tool overlays a density heatmap of Kill and KilledByStorm events. This instantly highlights "Meat Grinders" where the map geometry might be giving one side an unfair advantage.
Spatial Context: By mapping world coordinates precisely to the 1024x1024 minimap, Sid sees exactly which rock, building, or bridge is the source of the friction.

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
