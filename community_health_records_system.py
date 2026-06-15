
# SIERRA LEONE COMMUNITY HEALTH RECORDS SYSTEM
# Framework  : tkinter + ttk (Python Built-in)
# SDG        : SDG 3 - Good Health and Well-being


# tkinter    → creates the window, buttons, labels, entries
# ttk        → gives us the professional table and tabs
# messagebox → creates the pop-up alert boxes
# datetime   → reads the current date and time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# CONSTANTS


MIN_AGE = 1
MAX_AGE = 160

# All 16 districts of Sierra Leone
DISTRICTS = [
    "Western Area Urban (Freetown)",
    "Western Area Rural (Freetown)",
    "Bo",
    "Bombali",
    "Bonthe",
    "Falaba",
    "Kailahun",
    "Kambia",
    "Karene",
    "Kenema",
    "Koinadugu",
    "Kono",
    "Moyamba",
    "Port Loko",
    "Pujehun",
    "Tonkolili"
]

# Common health diagnoses in Sierra Leone
DIAGNOSES = [
    "Malaria",
    "Typhoid Fever",
    "Cholera",
    "Tuberculosis (TB)",
    "HIV / AIDS",
    "Hypertension",
    "Diabetes",
    "Respiratory Infection",
    "Diarrhea / Dysentery",
    "Malnutrition",
    "Anaemia",
    "Skin Infection",
    "Maternal Health Issue",
    "Injury / Trauma",
    "Other"
]


# RECORDS LIST

records = []


# FUNCTIONS


# FUNCTION 1: Get age group
def get_age_group(age):
    if age >= 0 and age <= 12:
        return "Child"
    elif age >= 13 and age <= 17:
        return "Teenager"
    elif age >= 18 and age <= 59:
        return "Adult"
    else:
        return "Senior"

# ---- FUNCTION 2: Get health risk level ----
def get_risk_level(age):
    if age <= 12 or age >= 60:
        return "High Risk"
    elif age >= 13 and age <= 17:
        return "Medium Risk"
    else:
        return "Low Risk"

# FUNCTION 3: Process and return both values
def process_record(age):
    age_group  = get_age_group(age)
    risk_level = get_risk_level(age)
    return age_group, risk_level

# FUNCTION 4: Update all live counters on screen
def update_dashboard():
    total  = len(records)
    male   = 0
    female = 0
    for r in records:
        if r["gender"] == "Male":
            male += 1
        else:
            female += 1
    high_risk = 0
    for r in records:
        if r["risk_level"] == "High Risk":
            high_risk += 1

    # Update the big number in the header
    counter_num.config(text=str(total))

    # Update each of the 4 stat cards
    card_total.config(text=str(total))
    card_male.config(text=str(male))
    card_female.config(text=str(female))
    card_risk.config(text=str(high_risk))

#FUNCTION 5: Refresh the records table
def refresh_table():
    # Remove every existing row
    for row in table.get_children():
        table.delete(row)

    # Re-add every record from the list
    for record in records:
        table.insert(
            "",
            tk.END,
            values=(
                f"#{record['number']}",
                record["name"],
                record["age"],
                record["gender"],
                record["district"],
                record["diagnosis"],
                record["status"],
                record["risk_level"],
                record["date"]
            )
        )

#FUNCTION 6: Add a new patient
def add_patient():
    name      = entry_name.get().strip()
    age_text  = entry_age.get().strip()
    gender    = gender_var.get()
    district  = district_var.get()
    diagnosis = diagnosis_var.get()
    status    = status_var.get()

    if not name:
        messagebox.showerror("Missing Information", "Please enter the patient's full name")
        return
    if not age_text:
        messagebox.showerror("Missing Information", "Please enter the patient's age")
        return
    if district == "-- Select District --":
        messagebox.showerror("Missing Information", "Please select the patient's district")
        return
    if diagnosis == "-- Select Diagnosis --":
        messagebox.showerror("Missing Information", "Please select a diagnosis")
        return

    try:
        age = int(age_text)
    except:
        messagebox.showerror("Invalid Input", "Age must be a number only")
        return

    if age < MIN_AGE or age > MAX_AGE:
        messagebox.showerror("Invalid Input", f"Age must be between {MIN_AGE} and {MAX_AGE}")
        return

    age_group, risk_level = process_record(age)
    record_number = len(records) + 1
    current_date  = datetime.now().strftime("%d/%m/%Y  %H:%M")

    record = {
        "number"    : record_number,
        "name"      : name,
        "age"       : age,
        "age_group" : age_group,
        "gender"    : gender,
        "district"  : district,
        "diagnosis" : diagnosis,
        "status"    : status,
        "risk_level": risk_level,
        "date"      : current_date
    }

    records.append(record)
    refresh_table()
    update_dashboard()

    messagebox.showinfo(
        "Registered Successfully",
        f"Patient '{name}' has been registered.\nRecord No: #{record_number}"
    )
    clear_form()

# ---- FUNCTION 7: Clear the registration form ----
def clear_form():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    gender_var.set("Male")
    district_var.set("-- Select District --")
    diagnosis_var.set("-- Select Diagnosis --")
    status_var.set("Under Treatment")

# ---- FUNCTION 8: Delete the selected patient ----
def delete_patient():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Row Selected",
            "Please click on a patient row in the table first."
        )
        return

    item         = table.item(selected[0])
    record_label = str(item["values"][0])
    record_num   = int(record_label.replace("#", ""))
    patient_name = item["values"][1]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to permanently delete this record?\n\n"
        f"Patient : {patient_name}\n"
        f"Record  : {record_label}"
    )

    if confirm:
        records[:] = [r for r in records if r["number"] != record_num]
        for i, r in enumerate(records):
            r["number"] = i + 1
        refresh_table()
        update_dashboard()
        messagebox.showinfo("Deleted", f"Record for '{patient_name}' has been deleted.")

#FUNCTION 9: Show statistics report
def show_statistics():
    total = len(records)

    if total == 0:
        messagebox.showinfo("No Data", "No patients registered yet.")
        return

    male   = 0
    female = 0
    for r in records:
        if r["gender"] == "Male":
            male += 1
        else:
            female += 1

    high   = 0
    medium = 0
    low    = 0
    for r in records:
        if r["risk_level"] == "High Risk":
            high += 1
        elif r["risk_level"] == "Medium Risk":
            medium += 1
        else:
            low += 1

    under     = 0
    recovered = 0
    referred  = 0
    for r in records:
        if r["status"] == "Under Treatment":
            under += 1
        elif r["status"] == "Recovered":
            recovered += 1
        else:
            referred += 1

    total_age = 0
    for r in records:
        total_age += r["age"]
    avg_age = total_age / total

    diag_count = {}
    for r in records:
        d = r["diagnosis"]
        if d in diag_count:
            diag_count[d] += 1
        else:
            diag_count[d] = 1
    top_diagnosis = max(diag_count, key=diag_count.get)

    dist_count = {}
    for r in records:
        d = r["district"]
        if d in dist_count:
            dist_count[d] += 1
        else:
            dist_count[d] = 1
    top_district = max(dist_count, key=dist_count.get)

    report  = f"\n"
    report += f"  \n"
    report += f"        COMMUNITY HEALTH STATISTICS REPORT         \n"
    report += f"        SDG 3 — Good Health and Well-being            \n"
    report += f"       Sierra Leone Community Health Records          \n"
    report += f"  \n\n"
    report += f"  Generated On       : {datetime.now().strftime('%d/%m/%Y  %H:%M')}\n"
    report += f"  {'─' * 50}\n\n"
    report += f"  TOTAL REGISTERED PATIENTS     :  {total}\n\n"
    report += f"  GENDER BREAKDOWN\n"
    report += f"  ├─ Male Patients               :  {male}\n"
    report += f"  └─ Female Patients             :  {female}\n\n"
    report += f"  AVERAGE PATIENT AGE            :  {avg_age:.1f} years\n\n"
    report += f"  RISK LEVELS\n"
    report += f"  ├─ High Risk                   :  {high}\n"
    report += f"  ├─ Medium Risk                 :  {medium}\n"
    report += f"  └─ Low Risk                    :  {low}\n\n"
    report += f"  TREATMENT STATUS\n"
    report += f"  ├─ Under Treatment             :  {under}\n"
    report += f"  ├─ Recovered                   :  {recovered}\n"
    report += f"  └─ Referred to Hospital        :  {referred}\n\n"
    report += f"  MOST COMMON DIAGNOSIS          :  {top_diagnosis}\n"
    report += f"  MOST AFFECTED DISTRICT         :  {top_district}\n\n"
    report += f"  {'─' * 50}\n"

    # Switch to the Statistics tab and show the report
    notebook.select(1)
    stats_box.config(state="normal")
    stats_box.delete(1.0, tk.END)
    stats_box.insert(tk.END, report)
    stats_box.config(state="disabled")

#
# BUILD THE WINDOW
#

root = tk.Tk()
root.title("Sierra Leone Community Health Records System")
root.geometry("1200x820")
root.minsize(1000, 700)

#
# HEADER — Black background, white text
#

# Header frame — bg="black" replaces the old navy blue
header = tk.Frame(root, bg="black", height=90)
header.pack(fill="x")
header.pack_propagate(False)

# Left side of header — must set bg="black" to match the frame
left_hdr = tk.Frame(header, bg="black")
left_hdr.pack(side="left", padx=20, pady=8)

tk.Label(
    left_hdr,
    text="🏥   SIERRA LEONE COMMUNITY HEALTH RECORDS",
    font=("Georgia", 17, "bold"),
    fg="white",      # white text on black background
    bg="black",
    anchor="w"
).pack(anchor="w")

tk.Label(
    left_hdr,
    text="Ministry of Health  ",
    font=("Tahoma", 12),
    fg="white",
    bg="black",
    anchor="w"
).pack(anchor="w", pady=(4, 2))

tk.Label(
    left_hdr,
    text="",
    font=("Arial", 8, "italic"),
    fg="white",
    bg="black",
    anchor="w"
).pack(anchor="w")

# Right side of header live patient counter
right_hdr = tk.Frame(header, bg="black")
right_hdr.pack(side="right", padx=35)

tk.Label(
    right_hdr,
    text="PATIENTS REGISTERED",
    font=("Arial", 8, "bold"),
    fg="white",
    bg="black"
).pack()

# This number updates live every time a patient is added or deleted
counter_num = tk.Label(
    right_hdr,
    text="0",
    font=("Arial", 34, "bold"),
    fg="white",
    bg="black"
)
counter_num.pack()

#
# MAIN CONTENT — Two columns
#

# No bg= set here — uses the default tkinter white/grey
main_area = tk.Frame(root)
main_area.pack(fill="both", expand=True, padx=12, pady=10)

#
# LEFT COLUMN — Registration Form
#

left_col = tk.Frame(main_area, width=315)
left_col.pack(side="left", fill="y", padx=(0, 10))
left_col.pack_propagate(False)

# Form card — thin solid border, no color
form_card = tk.Frame(left_col, bd=1, relief="solid")
form_card.pack(fill="both", expand=True)

# Black section bar at the top of the form card
form_bar = tk.Frame(form_card, bg="black")
form_bar.pack(fill="x")
tk.Label(
    form_bar,
    text="  📋   PATIENT REGISTRATION FORM",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="black",
    anchor="w"
).pack(fill="x", pady=9, padx=5)

# Form body — default background, no colors
form_body = tk.Frame(form_card, padx=18, pady=5)
form_body.pack(fill="both", expand=True)

# Helper functions — no colors, just fonts and layout

def field_label(text):
    # Bold label above each input field
    tk.Label(
        form_body,
        text=text,
        font=("Arial", 9, "bold"),
        anchor="w"
    ).pack(fill="x", pady=(8, 1))

def field_entry():
    # Plain input box with a solid border
    e = tk.Entry(
        form_body,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )
    e.pack(fill="x", ipady=5)
    return e

def field_dropdown(var, options):
    # Default dropdown — no custom colors
    d = tk.OptionMenu(form_body, var, *options)
    d.config(font=("Arial", 10), relief="solid", bd=1)
    d["menu"].config(font=("Arial", 10))
    d.pack(fill="x", ipady=3)

#  Form fields

field_label("Full Name")
entry_name = field_entry()

field_label("Age")
entry_age = field_entry()

field_label("Gender")
gender_var = tk.StringVar(value="Male")
field_dropdown(gender_var, ["Male", "Female"])

field_label("District")
district_var = tk.StringVar(value="-- Select District --")
field_dropdown(district_var, DISTRICTS)

field_label("What Are You Diagnosed With?")
diagnosis_var = tk.StringVar(value="-- Select Diagnosis --")
field_dropdown(diagnosis_var, DIAGNOSES)

field_label("Treatment Status")
status_var = tk.StringVar(value="Under Treatment")
field_dropdown(status_var, ["Under Treatment", "Recovered", "Referred to Hospital"])

# Buttons — default grey tkinter style

btn_area = tk.Frame(form_card, padx=18, pady=15)
btn_area.pack(fill="x")

# Register button  default grey, bold font, raised border
tk.Button(
    btn_area,
    text=" Register Patient",
    command=add_patient,
    font=("Arial", 11, "bold"),
    relief="raised",
    bd=2,
    pady=9,
    cursor="hand2"
).pack(fill="x", pady=(0, 7))

# Clear button — default grey
tk.Button(
    btn_area,
    text="  Clear Form",
    command=clear_form,
    font=("Arial", 10),
    relief="raised",
    bd=2,
    pady=7,
    cursor="hand2"
).pack(fill="x")

#
# RIGHT COLUMN — Dashboard
#

right_col = tk.Frame(main_area)
right_col.pack(side="right", fill="both", expand=True)

# 4 Stat Cards — groove border instead of colored backgrounds

cards_row = tk.Frame(right_col)
cards_row.pack(fill="x", pady=(0, 10))

def make_stat_card(parent, title):
    # groove relief creates a nice bordered box without needing colors
    card = tk.Frame(parent, relief="groove", bd=2, padx=15, pady=10)
    card.pack(side="left", fill="both", expand=True, padx=4)
    tk.Label(card, text=title, font=("Arial", 9, "bold"), anchor="w").pack(anchor="w")
    val = tk.Label(card, text="0", font=("Arial", 26, "bold"))
    val.pack(anchor="w")
    return val

card_total  = make_stat_card(cards_row, "TOTAL PATIENTS")
card_male   = make_stat_card(cards_row, "MALE PATIENTS")
card_female = make_stat_card(cards_row, "FEMALE PATIENTS")
card_risk   = make_stat_card(cards_row, "HIGH RISK")


# TABS Records Table + Statistics


# Tab style — just font and padding, no color changes
tab_style = ttk.Style()
tab_style.configure(
    "TNotebook.Tab",
    font=("Arial", 10, "bold"),
    padding=[14, 6]
)

notebook = ttk.Notebook(right_col)
notebook.pack(fill="both", expand=True)

# TAB 1: Patient Records

records_tab = tk.Frame(notebook)
notebook.add(records_tab, text="  Patient Records  ")

# Instruction bar — no custom background
info_bar = tk.Frame(records_tab, padx=10, pady=7)
info_bar.pack(fill="x")

tk.Label(
    info_bar,
    text="💡  Click any row to select it. Then click Delete to remove the record.",
    font=("Arial", 9, "italic")
).pack(side="left")

# Delete button — default grey style
tk.Button(
    info_bar,
    text="🗑   Delete Selected",
    command=delete_patient,
    font=("Arial", 10, "bold"),
    relief="raised",
    bd=2,
    padx=10,
    pady=4,
    cursor="hand2"
).pack(side="right", padx=5)

# The Treeview table
table_frame = tk.Frame(records_tab)
table_frame.pack(fill="both", expand=True, padx=5, pady=5)

COLUMNS = (
    "No.",
    "Full Name",
    "Age",
    "Gender",
    "District",
    "Diagnosed With",
    "Status",
    "Risk Level",
    "Date Registered"
)

table = ttk.Treeview(
    table_frame,
    columns=COLUMNS,
    show="headings",
    height=10
)

# Table style — font and row height only, no custom colors
tbl_style = ttk.Style()
tbl_style.configure("Treeview",         font=("Arial", 10), rowheight=28)
tbl_style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

WIDTHS = {
    "No."            : 45,
    "Full Name"      : 155,
    "Age"            : 45,
    "Gender"         : 70,
    "District"       : 185,
    "Diagnosed With" : 145,
    "Status"         : 140,
    "Risk Level"     : 90,
    "Date Registered": 135
}

for col in COLUMNS:
    table.heading(col, text=col)
    table.column(col, width=WIDTHS[col], anchor="center", minwidth=40)

# Left-align the text columns
table.column("Full Name",      anchor="w")
table.column("District",       anchor="w")
table.column("Diagnosed With", anchor="w")
table.column("Status",         anchor="w")

# Scrollbars
v_scroll = ttk.Scrollbar(table_frame, orient="vertical",   command=table.yview)
h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

v_scroll.pack(side="right",  fill="y")
h_scroll.pack(side="bottom", fill="x")
table.pack(fill="both", expand=True)

# TAB 2: Statistics

stats_tab = tk.Frame(notebook)
notebook.add(stats_tab, text="   Statistics  ")

stats_btn_bar = tk.Frame(stats_tab, padx=10, pady=8)
stats_btn_bar.pack(fill="x")

# Generate statistics button — default grey
tk.Button(
    stats_btn_bar,
    text="📊   Generate Statistics Report",
    command=show_statistics,
    font=("Arial", 10, "bold"),
    relief="raised",
    bd=2,
    padx=14,
    pady=6,
    cursor="hand2"
).pack(side="left")

# Statistics text area — default background
stats_box = tk.Text(
    stats_tab,
    font=("Courier", 11),
    relief="flat",
    padx=15,
    pady=10,
    state="disabled"
)
stats_box.pack(fill="both", expand=True)

stats_box.config(state="normal")
stats_box.insert(tk.END, "\n\n  Click 'Generate Statistics Report' to view the full community health data.")
stats_box.config(state="disabled")


# STATUS BAR — Black background, white text


# Status bar at the very bottom — black to match the header
status_bar = tk.Frame(root, bg="black", height=26)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

tk.Label(
    status_bar,
    text="  🔒  Sierra Leone Community Health Records System  ·  "
         "SDG 3 — Good Health & Well-being  ·  Limkokwing University — PROG103",
    font=("Arial", 8),
    fg="white",
    bg="black",
    anchor="w"
).pack(side="left", pady=4)

tk.Label(
    status_bar,
    text=f"v2.0  ·  {datetime.now().strftime('%d/%m/%Y')}  ",
    font=("Arial", 8),
    fg="white",
    bg="black",
    anchor="e"
).pack(side="right", pady=4)


# Keep the window open


root.mainloop()

