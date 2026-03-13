import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime
import time
from PIL import Image
from utils.data_loader import load_parquet_file
from utils.mapping import get_pixel_coords

# Define configuration
DATA_DIR = "player_data"
DATE_FOLDERS = ["February_10", "February_11", "February_12", "February_13", "February_14"]
MAP_IDS = ["AmbroseValley", "GrandRift", "Lockdown"]

st.set_page_config(page_title="LILA Visualization App", layout="wide")

# Hide Streamlit header, deploy button, and reduce top padding
st.markdown("""
    <style>
        /* Hide the header and menu explicitly */
        header[data-testid="stHeader"] {display: none !important;}
        .stAppHeader {display: none !important;}
        #MainMenu {visibility: hidden;}
        /* Reduce the massive default top margin */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data(folder_path: str) -> pd.DataFrame:
    """Loads and concatenates all parquet files within the selected date folder."""
    frames = []
    if not os.path.exists(folder_path):
        return pd.DataFrame()
        
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.nakama-0'):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Need to use the custom load_parquet_file to decode events & add user_type
                df = load_parquet_file(file_path)
                frames.append(df)
            except Exception as e:
                st.warning(f"Error loading {file_name}: {e}")
                
    if not frames:
        return pd.DataFrame()
        
    return pd.concat(frames, ignore_index=True)

@st.cache_data
def get_match_data_with_coords(df_day: pd.DataFrame, selected_map: str, selected_match: str) -> pd.DataFrame:
    """Filters date-level data to a specific match and computes minimap coordinates once."""
    df_map = df_day[df_day['map_id'] == selected_map]
    df_match = df_map[df_map['match_id'] == selected_match].copy()
    df_match = df_match.sort_values(by='ts')
    
    # Pre-calculate coordinates for the whole match
    coords = df_match.apply(
        lambda row: get_pixel_coords(row['x'], row['z'], row['map_id']), 
        axis=1, result_type='expand'
    )
    if not coords.empty:
        df_match['pixel_x'] = coords[0]
        df_match['pixel_y'] = coords[1]
    else:
        df_match['pixel_x'] = []
        df_match['pixel_y'] = []
        
    return df_match

# Application UI - Main body
st.markdown("### 🌌 Journey Nexus <span style='font-size:14px; color:gray; font-weight:normal;'>LILA Player Visualization</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    selected_day = st.date_input(
        "Select Date", 
        datetime.date(2026, 2, 10), 
        min_value=datetime.date(2026, 2, 10), 
        max_value=datetime.date(2026, 2, 14)
    )
    selected_date = selected_day.strftime("%B_%d")

with col2:
    selected_map = st.selectbox("Select Map", MAP_IDS)

# Load data based on date
folder_path = os.path.join(DATA_DIR, selected_date)

with st.spinner(f"Loading data for {selected_date}..."):
    df_day = load_all_data(folder_path)

if df_day.empty:
    st.error(f"No data found in {folder_path}.")
    st.stop()

# Filter Controls - New horizontal row
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    show_humans = st.checkbox("Show Humans", value=True)
with col_f2:
    show_bots = st.checkbox("Show Bots", value=True)
with col_f3:
    display_mode = st.radio("Display Mode", ["Individual Paths", "Heatmap", "Both"], horizontal=True)

# Filter data to only include the selected map
df_map = df_day[df_day['map_id'] == selected_map].copy()

if df_map.empty:
    st.warning(f"No match events found for {selected_map} on {selected_date}.")
else:
    # Match ID filtering
    unique_matches = sorted(df_map['match_id'].dropna().unique().tolist())
    if not unique_matches:
        st.warning("No valid match IDs found in the data.")
        st.stop()
        
    st.divider()
    
    # Sub-header for Match and Playback
    col_sub1, col_sub2 = st.columns([1, 2])
    with col_sub1:
        selected_match = st.selectbox("Select Match ID", unique_matches)
    
    # Filter to selected match, sort globally, and map coordinates (Cached!)
    with st.spinner(f"Preparing match {selected_match}..."):
        df_match = get_match_data_with_coords(df_day, selected_map, selected_match)
        
    # Timeline playback video player
    min_ts = df_match['ts'].min()
    max_ts = df_match['ts'].max()
    
    if pd.isna(min_ts) or pd.isna(max_ts) or min_ts == max_ts:
        selected_ts = max_ts
        st.info("Match has only one timestamp.")
        st.session_state.is_playing = False
    else:
        min_dt = min_ts.to_pydatetime()
        max_dt = max_ts.to_pydatetime()
        
        # Initialize session state for this specific match
        if 'match_id' not in st.session_state or st.session_state.match_id != selected_match:
            st.session_state.match_id = selected_match
            st.session_state.current_time = min_dt
            st.session_state.is_playing = False
        
        with col_sub2:
            st.write(f"**Playback Controls** (Current: {st.session_state.current_time.strftime('%H:%M:%S')})")
            cp1, cp2, cp3, cp4 = st.columns([1, 1, 1, 4])
            with cp1:
                if st.button("⏪"):
                    st.session_state.current_time = max(min_dt, st.session_state.current_time - datetime.timedelta(seconds=5))
                    st.session_state.is_playing = False
            with cp2:
                if st.session_state.is_playing:
                    if st.button("⏸️"):
                        st.session_state.is_playing = False
                        st.rerun()
                else:
                    if st.button("▶️"):
                        st.session_state.is_playing = True
                        st.rerun()
            with cp3:
                if st.button("⏩"):
                    st.session_state.current_time = min(max_dt, st.session_state.current_time + datetime.timedelta(seconds=5))
                    st.session_state.is_playing = False
            with cp4:
                st.session_state.current_time = st.slider(
                    "Scrub", min_value=min_dt, max_value=max_dt, 
                    value=st.session_state.current_time, format="HH:mm:ss",
                    label_visibility="collapsed"
                )
        
        selected_ts = pd.to_datetime(st.session_state.current_time)
        
    # Filter events at or before the current playback time
    df_history = df_match[df_match['ts'] <= selected_ts].copy()

    # Filter for official events and add category first before splitting
    official_events = {
        'Position': 'Movement',
        'BotPosition': 'Movement',
        'Kill': 'Combat',
        'Killed': 'Combat',
        'BotKill': 'Combat',
        'BotKilled': 'Combat',
        'KilledByStorm': 'Environment',
        'Loot': 'Item'
    }
    df_history = df_history[df_history['event'].isin(official_events.keys())].copy()
    df_history['category'] = df_history['event'].map(official_events)
    
    # Apply Human/Bot Filter
    allowed_types = []
    if show_humans: allowed_types.append('Human')
    if show_bots: allowed_types.append('Bot')
    df_history = df_history[df_history['user_type'].isin(allowed_types)]
    
    # To prevent visual clutter, we show ALL discrete events (Kills, Deaths, Loot)
    # But for 'Movement', we only show the LATEST known position for each user
    is_movement = df_history['category'] == 'Movement'
    
    df_discrete = df_history[~is_movement]
    df_movement = df_history[is_movement]
    
    if not df_movement.empty:
        # Get the latest position for each unique user at this point in time
        df_latest_movement = df_movement.groupby('user_id').last().reset_index()
    else:
        df_latest_movement = pd.DataFrame()
        
    # Recombine for rendering
    if not df_history.empty:
        df_render = pd.concat([df_discrete, df_latest_movement], ignore_index=True)
    else:
        df_render = df_history
    # Visualization setup
    
    # Map from Map ID to minimap image filename
    image_ext = "jpg" if selected_map == "Lockdown" else "png"
    img_path = os.path.join(DATA_DIR, "minimaps", f"{selected_map}_Minimap.{image_ext}")
    
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        st.error(f"Minimap image not found at {img_path}")
        st.stop()
        
    import plotly.graph_objects as go
    fig = go.Figure()

    # Define a symbol map for better control and consistency
    symbol_map = {
        'Position': 'circle', 'BotPosition': 'circle-open',
        'Kill': 'star', 'Killed': 'star-open',
        'BotKill': 'diamond', 'BotKilled': 'diamond-open',
        'KilledByStorm': 'x',
        'Loot': 'square'
    }
    
    # Add Heatmap if selected
    if display_mode in ["Heatmap", "Both"] and not df_history.empty:
        fig.add_trace(go.Histogram2dContour(
            x=df_history['pixel_x'],
            y=df_history['pixel_y'],
            name="Density",
            colorscale='Hot',
            reversescale=True,
            showscale=False,
            ncontours=20,
            opacity=0.6,
            line=dict(width=0)
        ))

    # Map colors to categories explicitly to ensure stability
    color_map = {
        'Movement': '#1f77b4',  # blue
        'Combat': '#d62728',    # red
        'Environment': '#2ca02c', # green
        'Item': '#ff7f0e'       # orange
    }

    # Add Scatter Points if selected
    if display_mode in ["Individual Paths", "Both"] and not df_render.empty:
        # We reuse the px.scatter logic but add to fig
        scatter_fig = px.scatter(
            df_render, 
            x='pixel_x', 
            y='pixel_y',
            color='category',
            color_discrete_map=color_map,
            symbol='event',
            symbol_map=symbol_map,
            hover_data=['user_type', 'user_id', 'match_id', 'ts', 'x', 'z']
        )
        for trace in scatter_fig.data:
            fig.add_trace(trace)
    
    # Configure grid overlay for readability
    fig.update_layout(
        images=[
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=0,          # Plotly draws downward from (x,y)
                sizex=1024,
                sizey=1024,
                sizing="stretch",
                opacity=0.7,
                layer="below"
            )
        ],
        xaxis=dict(
            range=[0, 1024],
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        yaxis=dict(
            range=[1024, 0], # Reversed Y-axis
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        width=800,
        height=800,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        # Set legend positioning out of the way
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )
    
    # Display the plot
    st.plotly_chart(fig, width="stretch")

    # Match Statistics Section (at the bottom)
    st.divider()
    st.markdown("### 📊 Match Summary")
    
    # Calculate global stats for this match (not just current history)
    # Filter for official events
    df_match_filtered = df_match[df_match['event'].isin(official_events.keys())].copy()
    df_match_filtered['category'] = df_match_filtered['event'].map(official_events)
    
    # Calculate metrics
    num_humans = df_match_filtered[df_match_filtered['user_type'] == 'Human']['user_id'].nunique()
    num_bots = df_match_filtered[df_match_filtered['user_type'] == 'Bot']['user_id'].nunique()
    
    total_kills = len(df_match_filtered[df_match_filtered['event'].isin(['Kill', 'BotKill'])])
    total_deaths = len(df_match_filtered[df_match_filtered['event'].isin(['Killed', 'BotKilled', 'KilledByStorm'])])
    total_loots = len(df_match_filtered[df_match_filtered['event'] == 'Loot'])
    
    # Display metrics in columns
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    m_col1.metric("Players (Human)", num_humans)
    m_col2.metric("Bots", num_bots)
    m_col3.metric("Total Kills", total_kills)
    m_col4.metric("Total Deaths", total_deaths)
    m_col5.metric("Total Loots", total_loots)

    # If currently playing, progress time and rerun
    if 'is_playing' in st.session_state and st.session_state.is_playing:
        if st.session_state.current_time < max_dt:
            # Advance playback by 1 realtime second per tick
            st.session_state.current_time = min(max_dt, st.session_state.current_time + datetime.timedelta(seconds=1))
            time.sleep(0.5) # Emulate playback speed (2x realtime)
            st.rerun()
        else:
            # Reached end of match
            st.session_state.is_playing = False
            st.rerun()
