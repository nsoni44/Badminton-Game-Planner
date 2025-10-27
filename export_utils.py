# export_utils.py
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.table import Table

OUT_DIR = Path("schedule")
OUT_DIR.mkdir(exist_ok=True)

def save_schedule_excel(all_matches, week_name):
    rows = []
    for m in all_matches:
        for c in m["courts"]:
            rows.append({
                "Match": m["match_id"],
                "Court": c["court_id"],
                "Team A": ", ".join(c["team_a"]),
                "Team B": ", ".join(c["team_b"])
            })
    df = pd.DataFrame(rows)
    out = Path(f"{week_name} - schedule.xlsx")
    df.to_excel(out, index=False)
    return out

def save_schedule_png(all_matches, week_name):
    # Create a simple table image using matplotlib
    rows = []
    for m in all_matches:
        for c in m["courts"]:
            rows.append([m["match_id"], c["court_id"], " & ".join(c["team_a"]), " & ".join(c["team_b"])])
    columns = ["Match", "Court", "Team A", "Team B"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_axis_off()
    table = Table(ax, bbox=[0,0,1,1])
    n_rows = len(rows)+1
    n_cols = len(columns)
    cell_h = 1.0 / max(n_rows, 1)
    cell_w = 1.0 / n_cols

    # header
    for j, col in enumerate(columns):
        table.add_cell(0, j, cell_w, cell_h, text=col, loc='center', facecolor='lightgrey')
    # data
    for i, row in enumerate(rows, start=1):
        for j, cell in enumerate(row):
            table.add_cell(i, j, cell_w, cell_h, text=str(cell), loc='center')
    ax.add_table(table)
    fname = OUT_DIR / f"{week_name} - schedule.png"
    plt.savefig(fname, bbox_inches='tight')
    plt.close(fig)
    return fname
