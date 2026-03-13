# Game Design Insights: LILA BLACK Visualization

Using the Journey Nexus visualization tool, we analyzed player behavior across multiple maps and match types. Here are the three most significant insights gathered from the data.

---

## 1. POI Dominance & "Peripheral Vacuum"
**What caught our eye:**
In the **GrandRift** map, the heatmap shows an overwhelming concentration of player activity in the central **"MINE PIT"** area. Conversely, large sections of the map, such as the "Labour Quarters," are completely devoid of player movement throughout the match lifespan.

**Actionable Insight:**
*   **Metric Affected**: Map Utilization % and Encounter Variety.
*   **Actionable Item**: The level design currently funnels players too aggressively into one central node. Designers should consider placing high-value Loot or unique interactive objects (e.g., jump pads or portals) in the peripheral quarters to reward exploration and distribute the combat density.

**Why a Level Designer should care:**
A map where 70% of the space is unused is inefficient for asset budgets and leads to predictable, repetitive gameplay. Distributing the "heat" creates more diverse combat scenarios.

---

## 2. The "Ghost Bot" Phenomenon (Transient NPCs)
**What caught our eye:**
We discovered matches (e.g., in **AmbroseValley**) where the "Total Kills" statistic was high (e.g., 2-3 kills) while the "Unique Bots" count remained at 0. Analyzing the raw data revealed that these "Ghost Bots" generate `BotKill` events but never survive long enough to record movement (`Position`) files.

**Actionable Insight:**
*   **Metric Affected**: Server Performance & Player Engagement.
*   **Actionable Item**: This confirms that the game successfully uses "on-demand" NPC spawning for combat flavor. Designers can increase the frequency of these transient encounters to make the world feel "busy" without the performance overhead of full-session bot AI tracking.

**Why a Level Designer should care:**
Knowing that players can engage with non-persistent entities allows for "hot-dropping" flavor NPCs into specific zones to create artificial tension without needing complex global pathing networks.

---

## 3. High Attrition & Early-Game Lethality
**What caught our eye:**
In **Lockdown** matches with high bot counts, we observed a 100% mortality rate within the first 5 minutes. The "Total Deaths" metric frequently matched the total number of starting entities. There was almost no "late-game" data, suggesting that encounters are so lethal and cover is so sparse that matches end prematurely.

**Actionable Insight:**
*   **Metric Affected**: Match Duration and Player Lifetime Value (PLV).
*   **Actionable Item**: Review the "Sightlines" and "Time-to-Kill" (TTK) in the Lockdown map. The data suggests that players (and bots) are unable to disengage once a fight starts. Adding more LOS (Line of Sight) blockers or "safe zones" would extend match duration.

**Why a Level Designer should care:**
If players are dying too quickly, they have less time to interact with the game's mechanics or monetization loops. Longer survival times generally correlate with higher player satisfaction in the battle royale genre.
