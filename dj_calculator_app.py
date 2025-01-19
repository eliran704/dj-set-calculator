import streamlit as st
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    """Convert a time string to total seconds (MM:SS format)."""
    try:
        parts = time_str.split(":")
        if len(parts) == 2:  # MM:SS format
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        else:
            return None
    except ValueError:
        return None

def seconds_to_hms(seconds):
    """Convert seconds to a formatted MM:SS string."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

# Add custom CSS for mobile responsiveness
st.markdown("""
    <style>
    /* Mobile responsive CSS */
    @media screen and (max-width: 768px) {
        .css-ffhzg2 {
            padding: 10px;
            font-size: 14px;
        }
        .css-1v3fvcr {
            width: 100%;
        }
        .css-12oz5g7 {
            font-size: 16px;
        }
    }
    /* Styling for better spacing and layout */
    .css-1v3fvcr {
        display: flex;
        flex-wrap: wrap;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🎵 DJ Set Time Calculator")

st.write("""
Welcome to the DJ Set Time Calculator! Enter start and end times for each track using the input fields. 
The app will calculate each track's duration and the total set time.
""")

# Initialize session state for tracks
if "tracks" not in st.session_state:
    st.session_state.tracks = []

# Track input section
st.subheader("Add Your Tracks")
with st.form(key="track_form", clear_on_submit=True):  # Automatically clear inputs after submission
    st.markdown("### Start Time")
    col1, col2 = st.columns([1, 1])  # Equal-width columns for Minutes and Seconds
    with col1:
        start_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="start_minutes_input", label_visibility="collapsed", format="%d", help="Enter minutes")
    with col2:
        start_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="start_seconds_input", label_visibility="collapsed", format="%d", help="Enter seconds")

    st.markdown("### End Time")
    col3, col4 = st.columns([1, 1])  # Equal-width columns for Minutes and Seconds
    with col3:
        end_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="end_minutes_input", label_visibility="collapsed", format="%d", help="Enter minutes")
    with col4:
        end_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="end_seconds_input", label_visibility="collapsed", format="%d", help="Enter seconds")

    if st.form_submit_button("Add Track"):
        # Combine inputs into formatted time strings
        start_time = f"{start_minutes:02}:{start_seconds:02}"
        end_time = f"{end_minutes:02}:{end_seconds:02}"
        
        # Convert to seconds for calculation
        start_total_seconds = time_to_seconds(start_time)
        end_total_seconds = time_to_seconds(end_time)

        if start_total_seconds is None or end_total_seconds is None:
            st.error("Invalid time format. Please check your inputs.")
        elif end_total_seconds < start_total_seconds:
            # Handle crossing midnight
            end_total_seconds += 24 * 3600
            duration = end_total_seconds - start_total_seconds
            st.session_state.tracks.append((start_time, end_time, duration))
            st.success(f"Track added successfully (Duration: {seconds_to_hms(duration)})")
        else:
            duration = end_total_seconds - start_total_seconds
            st.session_state.tracks.append((start_time, end_time, duration))
            st.success(f"Track added successfully (Duration: {seconds_to_hms(duration)})")

# Display added tracks
if st.session_state.tracks:
    st.subheader("Your Tracks")
    total_set_time = 0
    track_durations = []

    for idx, (start, end, duration) in enumerate(st.session_state.tracks, 1):  # Start numbering from 1
        total_set_time += duration
        track_durations.append(
            {"Track Number": f"{idx}", "Start Time": start, "End Time": end, "Duration": seconds_to_hms(duration)}
        )

    # Display track durations with custom formatting
    st.dataframe(track_durations, use_container_width=True)

    # Show total duration
    st.subheader("Total DJ Set Duration")
    st.success(f"🎶 {seconds_to_hms(total_set_time)}")

# Reset button
if st.button("Reset Tracks"):
    st.session_state.tracks = []
    st.success("Track list cleared.")
