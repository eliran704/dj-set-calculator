import streamlit as st
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    """
    Convert a time string to total seconds.
    Supports MM:SS or HH:MM:SS formats.
    """
    try:
        parts = time_str.split(":")
        if len(parts) == 2:  # MM:SS format
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS format
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            return None
    except ValueError:
        return None

def seconds_to_hms(seconds):
    """Convert seconds to a formatted HH:MM:SS string."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# App title
st.title("🎵 DJ Set Time Calculator")

st.write("""
Welcome to the DJ Set Time Calculator! Input start and end times for each track in MM:SS or HH:MM:SS format. 
The app will calculate each track's duration and the total set time.
""")

# Initialize session state for tracks
if "tracks" not in st.session_state:
    st.session_state.tracks = []

# Track input section
st.subheader("Add Your Tracks")
with st.form(key="track_form", clear_on_submit=True):  # Automatically clear inputs after submission
    start_time = st.text_input("Enter Start Time (MM:SS or HH:MM:SS):", key="start_time_input")
    end_time = st.text_input("Enter End Time (MM:SS or HH:MM:SS):", key="end_time_input")

    if st.form_submit_button("Add Track"):
        start_seconds = time_to_seconds(start_time.strip())
        end_seconds = time_to_seconds(end_time.strip())

        if start_seconds is None or end_seconds is None:
            st.error("Invalid time format. Please enter times in MM:SS or HH:MM:SS format.")
        elif end_seconds < start_seconds:
            # Handle crossing midnight
            end_seconds += 24 * 3600
            duration = end_seconds - start_seconds
            st.session_state.tracks.append((start_time, end_time, duration))
            st.success(f"Track added successfully (Duration: {seconds_to_hms(duration)})")
        else:
            duration = end_seconds - start_seconds
            st.session_state.tracks.append((start_time, end_time, duration))
            st.success(f"Track added successfully (Duration: {seconds_to_hms(duration)})")

# Display added tracks
if st.session_state.tracks:
    st.subheader("Your Tracks")
    track_durations = []
    total_set_time = 0

    for i, (start, end, duration) in enumerate(st.session_state.tracks, start=1):  # Start numbering from 1
        total_set_time += duration
        track_durations.append(
            {"Track": f"Track {i}", "Start Time": start, "End Time": end, "Duration": seconds_to_hms(duration)}
        )

    # Display track durations in a table
    st.table(track_durations)

    # Show total duration
    st.subheader("Total DJ Set Duration")
    st.success(f"🎶 {seconds_to_hms(total_set_time)}")

# Reset button
if st.button("Reset Tracks"):
    st.session_state.tracks = []
    st.success("Track list cleared.")
