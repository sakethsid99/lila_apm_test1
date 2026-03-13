# Architecture Documentation: LILA BLACK Visualization Tool

## Tech Stack Choices
The tool is built using the following stack:
*   **Streamlit**: Chosen for its ability to rapidly create data-centric web interfaces. It bridges the gap between a Python script and a usable dashboard without the overhead of a full React/Django stack.
*   **Pandas**: The industry standard for data manipulation in Python, essential for handling and filtering the large Parquet datasets efficiently.
*   **Plotly**: Provides high-performance interactive visualizations. It allows for layered "Scatter" and "Heatmap" plots on top of custom background images (the minimaps).
*   **Pillow (PIL)**: Used for robust loading and handling of minimap assets in various formats (PNG/JPG).

## Data Flow
1.  **Raw Ingestion**: Data is read from `.nakama-0` Parquet files. During loading, the `event` column is decoded from bytes to strings, and a `user_type` column is dynamically generated (Human vs Bot) based on the UUID format of the `user_id`.
2.  **Aggregation**: Multiple files belonging to the same `match_id` are concatenated to provide a holistic view of the match.
3.  **Transform**: Game coordinates (`x`, `z`) are converted into minimap pixel coordinates (`pixel_x`, `pixel_y`) using map-specific scale and origin constants.
4.  **Interactive Rendering**: The application filters the data based on the user's selected date, map, and time (playback). Only relevant events are passed to Plotly for rendering on the static minimap background.

## Coordinate Mapping Approach
This was the most critical technical challenge. Game coordinates $(X, Z)$ use a localized world space, while the minimaps are fixed $1024 \times 1024$ pixel images.
*   **Formula**: $pixel = (world - origin) * scale$
*   **Y-Axis Flip**: Screen space coordinates $(0,0)$ are at the top-left, while match coordinates often follow a bottom-up or standard Cartesian system. The formula `1024 - (v * 1024)` was applied to correctly align the movement with the visual landmarks on the map.
*   **Normalization**: Coordinates are clamped to the 0-1024 range to ensure all points stay within the minimap boundaries.

## Assumptions & Ambiguities
*   **Bot Identity**: Some bots appear only in combat events (`BotKill`) but lack associated movement data files. We assumed these are transient NPCs spawned near human players.
*   **Map Constants**: We assumed the provided scale and origin values in the `player_data/README.md` were accurate and used them as our baseline for conversion.
*   **Event Categorization**: Since there are many raw event types, we grouped them into broader categories (Movement, Combat, Item, Environment) to simplify the UI and legend.

## Trade-offs
| Consideration | Final Decision | Rationale |
| :--- | :--- | :--- |
| **Real-time Pathing vs. Snapshot** | Snapshot (Latest Position) | Showing every single movement point for every player simultaneously overwhelmed the map. We show the "current" location + a historical heatmap instead. |
| **Global Data Loading** | Caching (st.cache_data) | Loading hundreds of Parquet files on every interaction was too slow. Caching by date/match makes the UI feel "instant". |
| **Full Video Player** | Custom Scrubber | Building a custom loop with `time.sleep` and `st.rerun` allowed us to keep the logic entirely in Python while providing Play/Pause/Seek functionality. |

## Future Potential
With more time, we would implement:
*   **Individual Player Toggle**: Selecting specific players to highlight their unique paths.
*   **Kill Feed Sidebar**: A vertical list of combat events synced to the timeline.
*   **Web-Optimized Assets**: Converting high-res minimaps to WebP for faster initial load.
