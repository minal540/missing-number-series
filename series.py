# Minal code-----------------------
import tkinter as tk
from tkinter import messagebox

def detect_arithmetic(series):
    diffs = []
    for i in range(1, len(series)):
        if series[i] is not None and series[i - 1] is not None:
            diffs.append(series[i] - series[i - 1])
    if len(set(diffs)) == 1:
        return ("Arithmetic", diffs[0])
    return None

def detect_geometric(series):
    ratios = []
    for i in range(1, len(series)):
        if series[i] is not None and series[i - 1] not in (0, None):
            ratios.append(series[i] / series[i - 1])
    if len(set(ratios)) == 1:
        return ("Geometric", ratios[0])
    return None

def detect_fibonacci(series):
    for i in range(2, len(series)):
        if None not in (series[i-2], series[i-1], series[i]):
            if series[i] != series[i-1] + series[i-2]:
                return None
    return "Fibonacci"

def detect_alternating(series):
    even_diffs = []
    odd_diffs = []
    for i in range(2, len(series)):
        if i % 2 == 0 and series[i] is not None and series[i-2] is not None:
            even_diffs.append(series[i] - series[i-2])
        elif i % 2 == 1 and series[i] is not None and series[i-2] is not None:
            odd_diffs.append(series[i] - series[i-2])
    if even_diffs and odd_diffs and len(set(even_diffs)) == 1 and len(set(odd_diffs)) == 1:
        return ("Alternating", even_diffs[0], odd_diffs[0])
    return None

def detect_custom_cube_plus_one(series):
    cubes = [11, 9, 7, 5, 3, 1]
    try:
        base = series[0]
        for i in range(1, len(series)):
            if series[i] is not None:
                expected = base + cubes[i - 1]**3 + 1
                if expected != series[i]:
                    return None
                base = series[i]
            else:
                return f"Pattern: + (cube + 1) with descending cubes\nMissing Value: {base + cubes[i - 1]**3 + 1}"
    except:
        return None
    return None

def detect_linear_increase(series):
    # Check if the difference is increasing linearly (e.g., +2, +4, +6...)
    diffs = []
    for i in range(1, len(series)):
        if series[i] is not None and series[i - 1] is not None:
            diffs.append(series[i] - series[i - 1])
    diff_diffs = []
    for i in range(1, len(diffs)):
        diff_diffs.append(diffs[i] - diffs[i - 1])
    if len(set(diff_diffs)) == 1:
        idx = series.index(None)
        if idx >= 2:
            prev1 = series[idx - 1] - series[idx - 2]
            step = diff_diffs[0]
            return f"Pattern: Increasing Difference (+{step})\nMissing Value: {series[idx - 1] + prev1 + step}"
    return None

def solve_series(series):
    if series.count(None) != 1:
        return "Only one missing value supported."

    missing_index = series.index(None)

    arith = detect_arithmetic(series)
    if arith:
        pattern, diff = arith
        if missing_index > 0:
            return f"Pattern: Arithmetic (+{diff})\nMissing Value: {series[missing_index - 1] + diff}"
        else:
            return f"Pattern: Arithmetic (+{diff})\nMissing Value: {series[1] - diff}"

    geo = detect_geometric(series)
    if geo:
        pattern, ratio = geo
        if missing_index > 0:
            return f"Pattern: Geometric (\u00d7{ratio})\nMissing Value: {series[missing_index - 1] * ratio}"
        else:
            return f"Pattern: Geometric (\u00d7{ratio})\nMissing Value: {series[1] / ratio}"

    if detect_fibonacci(series):
        if missing_index >= 2:
            return f"Pattern: Fibonacci\nMissing Value: {series[missing_index-1] + series[missing_index-2]}"
        else:
            return "Pattern: Fibonacci\nMissing value is at the beginning, not enough data."

    alt = detect_alternating(series)
    if alt:
        _, even_diff, odd_diff = alt
        if missing_index % 2 == 0:
            return f"Pattern: Alternating\nMissing Value: {series[missing_index - 2] + even_diff}"
        else:
            return f"Pattern: Alternating\nMissing Value: {series[missing_index - 2] + odd_diff}"

    custom = detect_custom_cube_plus_one(series)
    if custom:
        return custom

    linear_increase = detect_linear_increase(series)
    if linear_increase:
        return linear_increase

    return "Pattern not recognized. Try manual check."

def run_solver():
    raw_input = entry.get()
    try:
        parts = raw_input.split(',')
        series = [int(x.strip()) if x.strip() != '?' else None for x in parts]
        result = solve_series(series)
        messagebox.showinfo("Result", result)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# GUI
root = tk.Tk()
root.title("Missing Number Series Solver")

label = tk.Label(root, text="Enter number series (use ? for missing number):")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

btn = tk.Button(root, text="Solve", command=run_solver)
btn.pack(pady=10)

root.mainloop()