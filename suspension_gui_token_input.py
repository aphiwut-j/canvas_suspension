import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

#YOUR TOKEN
import token_canvas 

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL = "YOUR DOMAIN"

HEADERS = {}

# -----------------------------
# PROMPT FOR TOKEN
# -----------------------------
def prompt_for_token():
    """
    1. Try default token first
    2. If invalid, prompt user
    """

    # --- Try default token ---
    default_headers = validate_token(token_canvas.TOKEN_KEY)
    if default_headers:
        return default_headers

    # --- Default failed → prompt user ---
    token = simpledialog.askstring(
        "Canvas Access Token Required",
        "Default token is invalid or expired.\n\n"
        "Please enter your Canvas Access Token:",
        show="*"
    )

    # User cancelled
    if token is None:
        messagebox.showinfo("Cancelled", "Operation cancelled by user.")
        return None

    token = token.strip()
    if not token:
        messagebox.showerror("Invalid Token", "No token entered.")
        return None

    user_headers = validate_token(token)
    if not user_headers:
        messagebox.showerror("Invalid Token", "Token validation failed.")
        return None

    return user_headers


# -----------------------------
# CANVAS: SUSPEND USER
# -----------------------------
def suspend_user(sis_user_id, headers):
    url = f"{BASE_URL}/api/v1/users/sis_user_id:{sis_user_id}"
    payload = {"user[event]": "suspend"}
    r = requests.put(url, headers=headers, data=payload)
    r.raise_for_status()

# -----------------------------
# CANVAS: Un-SUSPEND USER
# -----------------------------
def unsuspend_user(sis_user_id, headers):
    url = f"{BASE_URL}/api/v1/users/sis_user_id:{sis_user_id}"
    payload = {"user[event]": "unsuspend"}
    r = requests.put(url, headers=headers, data=payload)
    r.raise_for_status()

# -----------------------------
# RUN Un-SUSPENSION
# -----------------------------
def run_unsuspension(students, headers):
    success = 0
    failed = []

    for sis_id in students:
        try:
            unsuspend_user(int(sis_id.strip()), headers)
            success += 1
        except Exception as e:
            failed.append(f"{sis_id}: {e}")

    result = f"Unsuspended: {success}"

    if failed:
        result += f"\nFailed: {len(failed)}\n\n"
        result += "\n".join(failed[:10])

    messagebox.showinfo("Completed", result)

# -----------------------------
# LOAD FILE
# -----------------------------
def load_file():
    file_path = filedialog.askopenfilename(
        title="Select CSV or Excel file",
        filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls")
        ]
    )

    if not file_path:
        return

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
        return

    if "Student No" not in df.columns:
        messagebox.showerror("Missing Column", 'Column "Student No" not found.')
        return

    students = (
        df["Student No"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    headers = prompt_for_token()
    if not headers:
        return

    preview_and_confirm(students, headers)

# -----------------------------
# CHOOSE ACTION
# -----------------------------
def choose_action(students):
    action_window = tk.Toplevel()
    action_window.title("Choose Action")
    action_window.geometry("420x260")
    action_window.grab_set()  # make modal

    preview_text = (
        f"Students selected: {len(students)}\n\n"
        "First 10 SIS IDs:\n" +
        "\n".join(students[:10])
    )

    label = tk.Label(
        action_window,
        text=preview_text,
        justify="left",
        wraplength=380
    )
    label.pack(pady=15)

    chosen_action = {"value": None}

    def select(action):
        chosen_action["value"] = action
        action_window.destroy()

    btn_frame = tk.Frame(action_window)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="Suspend",
        width=12,
        command=lambda: select("suspend")
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        btn_frame,
        text="Un-suspend",
        width=12,
        command=lambda: select("unsuspend")
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        btn_frame,
        text="Cancel",
        width=12,
        command=lambda: select(None)
    ).grid(row=0, column=2, padx=5)

    action_window.wait_window()
    return chosen_action["value"]

# -----------------------------
# VALIDATE TOKEN
# -----------------------------\
def validate_token(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(
            f"{BASE_URL}/api/v1/users/self",
            headers=headers,
            timeout=10
        )
        r.raise_for_status()
        return headers
    except Exception:
        return None

# -----------------------------
# PROCESSING PROMPT
# -----------------------------
def show_processing_dialog(parent):
    dialog = tk.Toplevel(parent)
    dialog.title("Processing")
    dialog.geometry("300x120")
    dialog.grab_set()          # modal
    dialog.resizable(False, False)

    tk.Label(
        dialog,
        text="Processing, please wait...",
        font=("Arial", 11)
    ).pack(pady=30)

    # Disable closing
    dialog.protocol("WM_DELETE_WINDOW", lambda: None)

    return dialog

# -----------------------------
# CONFIRMATION PROMPT
# -----------------------------
def preview_and_confirm(students, headers):
    action = choose_action(students)

    if not action:
        return

    processing_dialog = show_processing_dialog(root)
    root.update_idletasks()

    try:
        if action == "suspend":
            run_suspension(students, headers)
        elif action == "unsuspend":
            run_unsuspension(students, headers)
    finally:
        processing_dialog.destroy()


# -----------------------------
# RUN SUSPENSION
# -----------------------------
def run_suspension(students, headers):
    success = 0
    failed = []

    for sis_id in students:
        try:
            suspend_user(int(sis_id.strip()), headers)
            success += 1
        except Exception as e:
            failed.append(f"{sis_id}: {e}")

    result = f"Suspended: {success}"

    if failed:
        result += f"\nFailed: {len(failed)}\n\n"
        result += "\n".join(failed[:10])

    messagebox.showinfo("Completed", result)

# -----------------------------
# GUI SETUP
# -----------------------------
root = tk.Tk()
root.title("Canvas – Suspend / Unsuspend Users")
root.geometry("420x180")

label = tk.Label(
    root,
    text="Suspend Canvas accounts from CSV / Excel",
    font=("Arial", 11)
)
label.pack(pady=20)

button = tk.Button(
    root,
    text="Select File",
    width=20,
    command=load_file
)
button.pack(pady=10)

root.mainloop()
