# app.py
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import storage, planner, export_utils



TZ = ZoneInfo("Europe/Tallinn")

st.set_page_config(page_title="Badminton Match Planner", layout="wide")

st.title("🏸 Badminton Match Planner")

now = datetime.now(TZ)
week_data, week_fp = storage.read_week(now)

# --- Ensure that if week is locked but schedule missing, generate it automatically ---
if week_data.get("locked") and not week_data.get("matches"):
    players = week_data.get("players", [])
    if len(players) == 12:
        st.info("Generating schedule for locked week...")
        all_matches = planner.generate_full_schedule(players)
        week_data["matches"] = all_matches
        storage.save_week(week_data, now)
        import export_utils
        export_utils.save_schedule_excel(all_matches, week_data["week"])
        export_utils.save_schedule_png(all_matches, week_data["week"])
        st.success("✅ Schedule generated automatically!")


st.sidebar.markdown(f"**Week:** {week_data['week']}")
st.sidebar.markdown(f"**Now:** {now.strftime('%Y-%m-%d %H:%M %Z')}")

# Create the week's JSON if missing (also called on app start)
storage.create_week_if_missing(now)

locked = week_data.get("locked", False)

# Show entry status
st.header("Player Entries (Mon — Thu)")

if locked:
    st.info("This week's entries are LOCKED. You cannot add players.")
else:
    st.success("Entries are OPEN. You can add players until Thu 23:59 or until 12 players join.")

players = week_data.get("players", [])

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Current players")
    for i, p in enumerate(players, start=1):
        st.write(f"{i}. {p}")

with col2:
    if not locked and storage.is_entry_window_open(now):
        new_name = st.text_input("Add player name", key="player_name")
        if st.button("Add player"):
            new_name = new_name.strip()
            if new_name == "":
                st.warning("Enter a non-empty name.")
            elif new_name in players:
                st.warning("Player already in list.")
            elif len(players) >= 12:
                st.warning("Already 12 players.")
            else:
                players.append(new_name)
                week_data["players"] = players
                storage.save_week(week_data, now)
                st.experimental_rerun()
    else:
        st.info("Entry window is closed (Mon–Thu only) or week is locked.")

# Auto-lock conditions
if not locked:
    # If 12 players reached -> lock and generate
    if len(players) >= 12 or storage.now_is_past_thursday_end(now):
        st.warning("Locking week (12 players reached or Thursday passed). Generating schedule...")
        week_data = storage.lock_week(now)
        locked = True
        # generate schedule
        all_matches = planner.generate_full_schedule(players)
        week_data["matches"] = all_matches
        storage.save_week(week_data, now)
        # export
        excel_path = export_utils.save_schedule_excel(all_matches, week_data["week"])
        png_path = export_utils.save_schedule_png(all_matches, week_data["week"])
        st.success(f"Schedule generated and saved: {excel_path} and {png_path}")
        # refresh
        st.experimental_rerun()

# If locked, show schedule
if locked:
    st.header("This Week's Schedule")
    matches = week_data.get("matches", [])
    if not matches:
        st.info("No schedule generated yet.")
    else:
        for m in matches:
            st.subheader(f"Match {m['match_id']}")
            for c in m["courts"]:
                st.markdown(f"**Court {c['court_id']}** — Team A: {', '.join(c['team_a'])}  vs  Team B: {', '.join(c['team_b'])}")
        # show schedule image if available
        img_path = Path("schedule") / f"{week_data['week']} - schedule.png"
        if img_path.exists():
            st.image(str(img_path))
