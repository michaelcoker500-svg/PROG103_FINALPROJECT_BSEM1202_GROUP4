

import tkinter as tk                    # main GUI library — creates windows, buttons, labels
from tkinter import ttk, messagebox     # ttk = styled table/tabs, messagebox = pop-up alerts
from datetime import datetime  # reads date and time from the computer clock
import matplotlib.pyplot as plt
from collections import Counter


# USER ACCOUNTS — admin and three doctors can log in


USERS = {
    "admin":     {"password": "admin123", "role": "admin",  "name": "System Administrator"},
    "drkoroma":  {"password": "doc123",   "role": "doctor", "name": "Dr. Koroma"},
    "drjohnson": {"password": "doc456",   "role": "doctor", "name": "Dr. Johnson"},
    "drbangura": {"password": "doc789",   "role": "doctor", "name": "Dr. Bangura"},
}


# CONSTANTS — values that never change while the program runs


MIN_AGE = 1      # youngest age allowed to register
MAX_AGE = 160    # oldest age allowed to register

# All 16 districts of Sierra Leone — used in the district dropdown
DISTRICTS = [
    "Western Area Urban (Freetown)", "Western Area Rural (Freetown)",
    "Bo", "Bombali", "Bonthe", "Falaba", "Kailahun", "Kambia",
    "Karene", "Kenema", "Koinadugu", "Kono", "Moyamba",
    "Port Loko", "Pujehun", "Tonkolili"
]

# Common diagnoses in Sierra Leone — used in the diagnosis dropdown
DIAGNOSES = [
    "Malaria", "Typhoid Fever", "Cholera", "Tuberculosis (TB)",
    "HIV / AIDS", "Hypertension", "Diabetes", "Respiratory Infection",
    "Diarrhea / Dysentery", "Malnutrition", "Anaemia", "Skin Infection",
    "Maternal Health Issue", "Injury / Trauma", "Other"
]

# Treatment status options — "About to Start" is new in this version
STATUSES    = ["Under Treatment", "About to Start", "Recovered", "Referred to Hospital"]

# Doctors available for assignment
DOCTORS     = ["Dr. Koroma", "Dr. Johnson", "Dr. Bangura", "Unassigned"]

# Risk level options for the filter dropdown
RISK_LEVELS = ["High Risk", "Medium Risk", "Low Risk"]


# CURRENT USER — stores who is logged in right now


current_user = {"name": "", "role": "", "username": ""}


# DATA STORES — all patient and appointment data lives here


records      = []   # list — each item is a patient dictionary
appointments = []   # list — each item is an appointment dictionary


# DUMMY PATIENTS — 100 pre-loaded sample records
# These load automatically so the system is not empty on startup


import random
from datetime import datetime, timedelta

PATIENT_NAMES = [
    "Aminata Kamara","Mohamed Sesay","Fatmata Conteh","Ibrahim Bangura",
    "Mariama Koroma","Alpha Jalloh","Isatu Fofana","Sorie Turay",
    "Adama Kargbo","Brima Tarawalie","Hawa Mansaray","Lamin Kamara",
    "Tenneh Koroma","Abdul Barrie","Kadiatu Bah","Josephine Kamara",
    "Musa Conteh","Bintu Kallon","Alusine Sesay","Mariatu Turay",
    "Mohamed Kamara","Finda Koroma","Yayah Bangura","Aisha Kargbo",
    "Amadu Jalloh","Hassan Conteh","Sia Fofanah","Kumba Koroma",
    "Abubakarr Kamara","Martha Sesay"
]

DISTRICTS = [
    "Bo","Kenema","Kono","Bombali","Port Loko",
    "Western Area Urban (Freetown)",
    "Western Area Rural (Freetown)",
    "Kailahun","Kambia","Pujehun",
    "Tonkolili","Moyamba"
]

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
    "Maternal Health Issue"
]

OTHER_DIAGNOSES = [
    "Sickle Cell Anaemia",
    "Asthma",
    "Arthritis",
    "Migraine",
    "Eye Infection",
    "Heart Disease"
]

STATUS = [
    "About to Start",
    "Under Treatment",
    "Recovered",
    "Referred to Hospital"
]

DOCTORS = [
    "Dr. Koroma",
    "Dr. Johnson",
    "Dr. Bangura",
    "Dr. Kamara",
    "Dr. Sesay"
]

DUMMY_PATIENTS = []

for i in range(1, 101):

    diagnosis = random.choice(DIAGNOSES)

    other = ""

    if random.randint(1, 10) == 1:
        diagnosis = "Other"
        other = random.choice(OTHER_DIAGNOSES)

    patient = {
        "name": random.choice(PATIENT_NAMES) + f" {i}",
        "age": random.randint(1, 85),
        "gender": random.choice(["Male", "Female"]),
        "district": random.choice(DISTRICTS),
        "diagnosis": diagnosis,
        "other": other,
        "status": random.choice(STATUS),
        "doctor": random.choice(DOCTORS)
    }

    DUMMY_PATIENTS.append(patient)

DUMMY_APPOINTMENTS = []


# GLOBAL GUI REFERENCES
# These are assigned inside launch_main() and used by all functions


root                = None   # the main application window
counter_num         = None   # the big patient count in the header
card_total          = None   # "TOTAL PATIENTS" stat card
card_male           = None   # "MALE PATIENTS" stat card
card_female         = None   # "FEMALE PATIENTS" stat card
card_risk           = None   # "HIGH RISK" stat card
entry_name          = None   # Full Name input box
entry_age           = None   # Age input box
entry_other         = None   # hidden "Other" diagnosis text box
other_frame         = None   # the frame that wraps the Other text box
gender_var          = None   # StringVar holding gender dropdown value
district_var        = None   # StringVar holding district dropdown value
diagnosis_var       = None   # StringVar holding diagnosis dropdown value
status_var          = None   # StringVar holding treatment status value
doctor_var          = None   # StringVar holding assigned doctor value
table               = None   # the main records Treeview table
notebook            = None   # the tab bar (Records / Statistics / Filter)
stats_box           = None   # the text area in the Statistics tab
dots_btn            = None   # the 3-dot vertical button in the header
filter_gender_var   = None   # filter dropdown — gender
filter_district_var = None   # filter dropdown — district
filter_diag_var     = None   # filter dropdown — diagnosis
filter_status_var   = None   # filter dropdown — treatment status
filter_risk_var     = None   # filter dropdown — risk level
filter_name_var     = None   # StringVar for the name search box
filter_result_label = None   # label that shows filter result message
logout_flag         = False  # set to True when user clicks logout (not when closing with X)


# FUNCTION 1 — get_age_group
# Takes an age number and returns which group the patient is in


def get_age_group(age):
    if age >= 0 and age <= 12:       # 0 to 12 is a Child
        return "Child"
    elif age >= 13 and age <= 17:    # 13 to 17 is a Teenager
        return "Teenager"
    elif age >= 18 and age <= 59:    # 18 to 59 is an Adult
        return "Adult"
    else:                            # 60 and above is a Senior
        return "Senior"


# FUNCTION 2 — get_risk_level
# Takes an age and returns the health risk classification

def get_risk_level(age):
    if age <= 12 or age >= 60:       # young children and seniors = High Risk
        return "High Risk"
    elif age >= 13 and age <= 17:    # teenagers = Medium Risk
        return "Medium Risk"
    else:                            # adults = Low Risk
        return "Low Risk"


# FUNCTION 3 — process_record
# Calls both classification functions and returns both results


def process_record(age):
    age_group  = get_age_group(age)   # call function 1
    risk_level = get_risk_level(age)  # call function 2
    return age_group, risk_level      # return both at once


# FUNCTION 4 — load_dummy_data
# Fills records and appointments with the pre-defined sample data


def load_dummy_data():
    for i, p in enumerate(DUMMY_PATIENTS):  # loop through each dummy patient
        ag, rl     = process_record(p["age"])  # get age group and risk level
        # if diagnosis is "Other", show the custom text instead
        disp_diag  = p["other"] if p["diagnosis"] == "Other" and p["other"] else p["diagnosis"]
        records.append({               # add this patient as a dictionary to the list
            "number"         : i + 1,
            "name"           : p["name"],
            "age"            : p["age"],
            "age_group"      : ag,
            "gender"         : p["gender"],
            "district"       : p["district"],
            "diagnosis"      : p["diagnosis"],
            "other_diagnosis": p["other"],
            "display_diag"   : disp_diag,  # the text shown in the table
            "status"         : p["status"],
            "risk_level"     : rl,
            "doctor"         : p["doctor"],
            "date"           : "13/06/2026"
        })
    for appt in DUMMY_APPOINTMENTS:    # loop and add each dummy appointment
        appointments.append(dict(appt))  # dict() makes a copy so original is not changed


# FUNCTION 5 — update_dashboard
# Recalculates all 4 stat cards and the header counter
# Called every time a patient is added or deleted


def update_dashboard():
    total    = len(records)                                       # count all records
    male     = sum(1 for r in records if r["gender"] == "Male")  # count males
    female   = sum(1 for r in records if r["gender"] == "Female")# count females
    high     = sum(1 for r in records if r["risk_level"] == "High Risk")  # count high risk
    counter_num.config(text=str(total))   # update big number in header
    card_total.config(text=str(total))    # update total card
    card_male.config(text=str(male))      # update male card
    card_female.config(text=str(female))  # update female card
    card_risk.config(text=str(high))      # update high risk card


# FUNCTION 6 — refresh_table
# Clears the table and redraws records
# If data is given, it shows only those records (used for filtering)


def refresh_table(data=None):
    if data is None:                      # if no specific data given, show all
        data = records
    for row in table.get_children():      # remove every existing row from table
        table.delete(row)
    for rec in data:                      # loop through each record and add it
        disp = rec.get("display_diag", rec["diagnosis"])  # get the display version
        table.insert("", tk.END, values=(
            f"#{rec['number']}", rec["name"], rec["age"],
            rec["gender"],       rec["district"], disp,
            rec["status"],       rec["risk_level"], rec["date"]
        ))


# FUNCTION 7 — on_diagnosis_change
# Watches the diagnosis dropdown — when "Other" is selected,
# it shows an extra text box for the patient to specify


def on_diagnosis_change(*args):           # *args is required by tkinter trace
    if diagnosis_var.get() == "Other":    # if the user chose "Other"
        other_frame.pack(fill="x", pady=(4, 0))  # show the extra text field
    else:
        other_frame.pack_forget()         # hide the extra text field


# FUNCTION 8 — add_patient
# Reads the form, validates every field, then saves the new patient


def add_patient():
    name      = entry_name.get().strip()   # read name and remove extra spaces
    age_text  = entry_age.get().strip()    # read age as text first
    gender    = gender_var.get()           # read selected gender
    district  = district_var.get()        # read selected district
    diagnosis = diagnosis_var.get()        # read selected diagnosis
    other     = entry_other.get().strip() if diagnosis == "Other" else ""  # read Other field only if needed
    status    = status_var.get()           # read treatment status
    doctor    = doctor_var.get()           # read assigned doctor

    # ---- VALIDATION — same pattern as your terminal code ----
    if not name:
        messagebox.showerror("Missing", "Please enter the patient's full name")
        return   # stop the function here, same as continue in your terminal loop
    if not age_text:
        messagebox.showerror("Missing", "Please enter the patient's age")
        return
    if district == "-- Select District --":
        messagebox.showerror("Missing", "Please select the patient's district")
        return
    if diagnosis == "-- Select Diagnosis --":
        messagebox.showerror("Missing", "Please select a diagnosis")
        return
    if diagnosis == "Other" and not other:
        messagebox.showerror("Missing", "Please specify the diagnosis in the text field below")
        return

    try:                         # try to convert age text to a whole number
        age = int(age_text)
    except:
        messagebox.showerror("Invalid", "Age must be a number only (example: 35)")
        return

    if age < MIN_AGE or age > MAX_AGE:   # check age is in valid range
        messagebox.showerror("Invalid", f"Age must be between {MIN_AGE} and {MAX_AGE}")
        return

    #PROCESSING
    ag, rl        = process_record(age)   # get age group and risk level
    rec_num       = len(records) + 1      # next record number
    today         = datetime.now().strftime("%d/%m/%Y")   # today's date
    display_diag  = other if diagnosis == "Other" and other else diagnosis  # what to show in table

    records.append({               # save the patient as a dictionary
        "number"         : rec_num,
        "name"           : name,
        "age"            : age,
        "age_group"      : ag,
        "gender"         : gender,
        "district"       : district,
        "diagnosis"      : diagnosis,
        "other_diagnosis": other,
        "display_diag"   : display_diag,
        "status"         : status,
        "risk_level"     : rl,
        "doctor"         : doctor,
        "date"           : today
    })

    refresh_table()    # redraw the table with the new record included
    update_dashboard() # update all 4 stat cards
    messagebox.showinfo("Registered", f"Patient '{name}' registered as Record #{rec_num}.")
    clear_form()       # reset form for the next patient


# FUNCTION 9 — clear_form
# Resets every input field back to its default empty/starting value


def clear_form():
    entry_name.delete(0, tk.END)     # delete(0, tk.END) clears from start to end
    entry_age.delete(0, tk.END)
    entry_other.delete(0, tk.END)
    gender_var.set("Male")                           # reset dropdown to default
    district_var.set("-- Select District --")
    diagnosis_var.set("-- Select Diagnosis --")
    status_var.set("Under Treatment")
    doctor_var.set("Unassigned")
    other_frame.pack_forget()   # always hide the Other field when clearing

# FUNCTION 10 — delete_patient
# Removes the selected table row after asking for confirmation


def delete_patient():
    sel = table.selection()    # get the currently selected row
    if not sel:
        messagebox.showwarning("None Selected", "Please click on a patient row in the table first.")
        return
    item     = table.item(sel[0])                         # read the row data
    rec_lbl  = str(item["values"][0])                     # e.g. "#5"
    rec_num  = int(rec_lbl.replace("#", ""))              # extract 5 as a number
    pat_name = item["values"][1]                          # patient name column

    if messagebox.askyesno("Confirm Delete", f"Permanently delete record for {pat_name}?\nThis cannot be undone."):
        records[:] = [r for r in records if r["number"] != rec_num]  # remove from list
        for i, r in enumerate(records):   # renumber remaining records
            r["number"] = i + 1
        refresh_table()    # redraw the table
        update_dashboard() # update counters
        messagebox.showinfo("Deleted", f"Record for '{pat_name}' has been deleted.")


# FUNCTION 11 — open_edit_window
# Opens a popup form when a row is double-clicked
# Pre-fills all fields with the current values so user can edit them


def open_edit_window(event=None):   # event=None because tkinter passes a click event
    sel = table.selection()
    if not sel:
        return
    item    = table.item(sel[0])
    rec_num = int(str(item["values"][0]).replace("#", ""))
    target  = next((r for r in records if r["number"] == rec_num), None)  # find the record
    if not target:
        return

    # Create the edit window
    win = tk.Toplevel(root)              # Toplevel creates a child window above root
    win.title(f"Edit Record  —  {target['name']}")
    win.geometry("440x660")
    win.resizable(False, False)
    win.grab_set()   # grab_set() locks focus to this window — user must close it first

    # Black title bar at the top of the edit window
    hbar = tk.Frame(win, bg="black", height=48)
    hbar.place(x=0, y=0, relwidth=1)     # place stretches it across the full width
    tk.Label(hbar, text="     Edit Patient Record",
             font=("Arial", 12, "bold"), fg="white", bg="black").place(x=0, y=10, relwidth=1)

    body = tk.Frame(win, padx=20, pady=10)
    body.pack(fill="both", expand=True, pady=(48, 0))  # 48 padding pushes below the black bar

    # Helper functions for the edit form
    def lbl(text):   # creates a small bold label
        tk.Label(body, text=text, font=("Arial", 9, "bold"), anchor="w").pack(fill="x", pady=(7, 1))

    def ent(default=""):   # creates a pre-filled text entry
        e = tk.Entry(body, font=("Arial", 11), relief="solid", bd=1)
        e.insert(0, str(default))   # insert(0, text) puts text at position 0
        e.pack(fill="x", ipady=4)
        return e

    def drp(var, options):   # creates a dropdown
        d = tk.OptionMenu(body, var, *options)
        d.config(font=("Arial", 10), relief="solid", bd=1)
        d["menu"].config(font=("Arial", 10))
        d.pack(fill="x", ipady=3)

    # Build the edit form pre-filled with current values
    lbl("Full Name")
    e_name   = ent(target["name"])
    lbl("Age")
    e_age    = ent(target["age"])
    lbl("Gender")
    e_gender = tk.StringVar(value=target["gender"])
    drp(e_gender, ["Male", "Female"])
    lbl("District")
    e_dist   = tk.StringVar(value=target["district"])
    drp(e_dist, DISTRICTS)
    lbl("Diagnosis")
    e_diag   = tk.StringVar(value=target["diagnosis"])
    drp(e_diag, DIAGNOSES)
    lbl("Specify if Other was selected")
    e_other  = ent(target.get("other_diagnosis", ""))
    lbl("Treatment Status")
    e_status = tk.StringVar(value=target["status"])
    drp(e_status, STATUSES)
    lbl("Assigned Doctor")
    e_doc    = tk.StringVar(value=target.get("doctor", "Unassigned"))
    drp(e_doc, DOCTORS)

    #  Save function — validates and updates the record in-place
    def save_edit():
        new_name  = e_name.get().strip()
        new_age_t = e_age.get().strip()
        new_diag  = e_diag.get()
        new_other = e_other.get().strip()

        if not new_name:
            messagebox.showerror("Error", "Name cannot be empty", parent=win)
            return
        try:
            new_age = int(new_age_t)
        except:
            messagebox.showerror("Error", "Age must be a number", parent=win)
            return
        if new_age < MIN_AGE or new_age > MAX_AGE:
            messagebox.showerror("Error", f"Age must be between {MIN_AGE} and {MAX_AGE}", parent=win)
            return
        if new_diag == "Other" and not new_other:
            messagebox.showerror("Error", "Please specify the diagnosis", parent=win)
            return

        new_ag, new_rl = process_record(new_age)   # recalculate with new age
        disp = new_other if new_diag == "Other" and new_other else new_diag

        target.update({              # update() changes multiple dictionary values at once
            "name"           : new_name,
            "age"            : new_age,
            "age_group"      : new_ag,
            "gender"         : e_gender.get(),
            "district"       : e_dist.get(),
            "diagnosis"      : new_diag,
            "other_diagnosis": new_other,
            "display_diag"   : disp,
            "status"         : e_status.get(),
            "risk_level"     : new_rl,
            "doctor"         : e_doc.get()
        })

        refresh_table()    # redraw the updated record in the table
        update_dashboard() # update the stat cards
        messagebox.showinfo("Updated", f"Record for '{new_name}' updated successfully.", parent=win)
        win.destroy()      # close the edit window

    tk.Button(body, text=" Save Changes", command=save_edit,
              font=("Arial", 11, "bold"), relief="raised", bd=2, pady=9).pack(fill="x", pady=(14, 5))
    tk.Button(body, text="Cancel", command=win.destroy,
              font=("Arial", 10), relief="raised", bd=2, pady=6).pack(fill="x")


# FUNCTION 12 — apply_filter
# Filters the records table based on whichever dropdowns were set
# Records that don't match are hidden — they are NOT deleted


def apply_filter():
    g    = filter_gender_var.get()      # read each filter dropdown
    dist = filter_district_var.get()
    diag = filter_diag_var.get()
    stat = filter_status_var.get()
    risk = filter_risk_var.get()
    name = filter_name_var.get().strip().lower()   # lowercase for case-insensitive match

    filtered = records[:]   # start with all records ([:] makes a copy)

    if g    != "All":   # if not "All", keep only records that match
        filtered = [r for r in filtered if r["gender"] == g]
    if dist != "All":
        filtered = [r for r in filtered if r["district"] == dist]
    if diag != "All":
        filtered = [r for r in filtered if r["diagnosis"] == diag or r.get("display_diag") == diag]
    if stat != "All":
        filtered = [r for r in filtered if r["status"] == stat]
    if risk != "All":
        filtered = [r for r in filtered if r["risk_level"] == risk]
    if name:            # if the user typed a name, filter by it too
        filtered = [r for r in filtered if name in r["name"].lower()]

    if not filtered:
        filter_result_label.config(text=" No patients found matching these filters.")
    else:
        filter_result_label.config(text=f"  Showing {len(filtered)} matching patient(s).")

    notebook.select(0)       # switch to the Records tab to show results
    refresh_table(filtered)  # draw only the matching records


# FUNCTION 13 — search_patient
# Searches for a patient by name and shows "not found" if missing


def search_patient():
    query = filter_name_var.get().strip()   # read what the user typed
    if not query:
        messagebox.showwarning("Empty Search", "Please type a patient name to search for.")
        return

    results = [r for r in records if query.lower() in r["name"].lower()]  # case-insensitive

    if not results:   # if nothing was found
        filter_result_label.config(text=f" Patient not found: '{query}'")
        messagebox.showinfo(
            "Patient Not Found",
            f"No patient was found with the name '{query}'.\n\nPlease check the spelling and try again."
        )
    else:
        filter_result_label.config(text=f"  Found {len(results)} patient(s) matching '{query}'.")
        notebook.select(0)      # go to the Records tab
        refresh_table(results)  # show only the search results


# FUNCTION 14 — clear_filter
# Resets all filter dropdowns and shows all records again


def clear_filter():
    filter_gender_var.set("All")       # reset each filter back to "All"
    filter_district_var.set("All")
    filter_diag_var.set("All")
    filter_status_var.set("All")
    filter_risk_var.set("All")
    filter_name_var.set("")            # clear the name search box
    filter_result_label.config(text="")  # clear the result message
    refresh_table()   # show all records again


# FUNCTION 15 — show_statistics
# Counts data from all records and builds the statistics report


def show_statistics():
    total = len(records)
    if total == 0:
        messagebox.showinfo("No Data", "No patients registered yet.")
        return

    male      = sum(1 for r in records if r["gender"] == "Male")
    female    = sum(1 for r in records if r["gender"] == "Female")
    high      = sum(1 for r in records if r["risk_level"] == "High Risk")
    medium    = sum(1 for r in records if r["risk_level"] == "Medium Risk")
    low       = sum(1 for r in records if r["risk_level"] == "Low Risk")
    under     = sum(1 for r in records if r["status"] == "Under Treatment")
    about_to  = sum(1 for r in records if r["status"] == "About to Start")
    recovered = sum(1 for r in records if r["status"] == "Recovered")
    referred  = sum(1 for r in records if r["status"] == "Referred to Hospital")
    avg_age   = sum(r["age"] for r in records) / total   # total age divided by count

    # Count most common diagnosis using a dictionary
    diag_count = {}
    for r in records:
        d = r.get("display_diag", r["diagnosis"])
        diag_count[d] = diag_count.get(d, 0) + 1   # get(d, 0) returns 0 if key not found yet
    top_diag = max(diag_count, key=diag_count.get)  # find the key with the highest count

    # Count most affected district
    dist_count = {}
    for r in records:
        dist_count[r["district"]] = dist_count.get(r["district"], 0) + 1
    top_dist = max(dist_count, key=dist_count.get)

    # Build the report text — \n means go to the next line
    report  = "\n"
    report += "        COMMUNITY HEALTH STATISTICS REPORT\n"
    report += "        \n"
    report += "        \n\n"
    report += f"  Generated On           : {datetime.now().strftime('%d/%m/%Y  %H:%M')}\n"
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
    report += f"  ├─ About to Start              :  {about_to}\n"
    report += f"  ├─ Under Treatment             :  {under}\n"
    report += f"  ├─ Recovered                   :  {recovered}\n"
    report += f"  └─ Referred to Hospital        :  {referred}\n\n"
    report += f"  MOST COMMON DIAGNOSIS          :  {top_diag}\n"
    report += f"  MOST AFFECTED DISTRICT         :  {top_dist}\n\n"
    report += f"  {'─' * 50}\n"

    notebook.select(1)   # switch to the Statistics tab (index 1)
    stats_box.config(state="normal")     # unlock so we can write
    stats_box.delete(1.0, tk.END)        # clear existing text
    stats_box.insert(tk.END, report)     # write the report
    stats_box.config(state="disabled")   # lock again so user cannot type


# FUNCTION 16 — show_dots_menu
# Shows a dropdown menu when the 3-dot (⋮) button is clicked


def show_dots_menu():
    menu = tk.Menu(root, tearoff=0, font=("Arial", 10))    # tearoff=0 removes the dotted line
    menu.add_command(label="    Doctor's Dashboard", command=open_doctors_dashboard)
    menu.add_separator()                                    # draws a dividing line
    menu.add_command(label="    Logout",               command=logout)
    x = dots_btn.winfo_rootx()                             # get button's X position on screen
    y = dots_btn.winfo_rooty() + dots_btn.winfo_height()   # position menu just below the button
    menu.post(x, y)   # post() shows the menu at the given screen coordinates


# FUNCTION 17 — logout
# Asks for confirmation, then closes the main window and ends program


def logout():
    global logout_flag
    if messagebox.askyesno("Logout", f"Are you sure you want to logout, {current_user['name']}?"):
        logout_flag = True    # mark that this was a logout — not just the X button
        root.quit()           # quit() exits mainloop safely without destroying window yet


# FUNCTION 18  open_doctors_dashboard
# Opens a separate appointments window for doctors or admin


def open_doctors_dashboard():
    role  = current_user["role"]    # "admin" or "doctor"
    uname = current_user["name"]    # e.g. "Dr. Koroma"

    dash = tk.Toplevel(root)        # Toplevel creates a second window above root
    dash.title("Doctor's Dashboard")
    dash.geometry("980x640")
    dash.resizable(True, True)

    #  Dashboard Header
    hdr = tk.Frame(dash, bg="black", height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)   # keep height fixed
    tk.Label(hdr, text=f"   Doctor's Dashboard   |   {uname}",
             font=("Arial", 13, "bold"), fg="white", bg="black", anchor="w").pack(side="left", pady=12, padx=12)
    tk.Button(hdr, text="✕  Close", command=dash.destroy,
              font=("Arial", 9, "bold"), fg="white", bg="grey30",
              relief="flat", padx=8, pady=4, cursor="hand2").pack(side="right", padx=12, pady=10)

    # Decide which appointments to show
    def get_visible():
        if role == "doctor":                                  # doctors see only their own
            return [a for a in appointments if a["doctor"] == uname]
        return appointments[:]                                # admin sees everyone's

    #  Stat Cards Row
    card_bar = tk.Frame(dash)
    card_bar.pack(fill="x", padx=10, pady=(6, 0))

    def refresh_cards():   # rebuilds the stat cards with current counts
        for w in card_bar.winfo_children():
            w.destroy()   # clear old cards first
        vis = get_visible()
        for title, count, col in [
            ("TOTAL",       len(vis),                                                "#1A3C5A"),
            ("SCHEDULED",   sum(1 for a in vis if a["status"] == "Scheduled"),       "#2D6A4F"),
            ("COMPLETED",   sum(1 for a in vis if a["status"] == "Completed"),       "#1E8449"),
            ("CANCELLED",   sum(1 for a in vis if "Cancel" in a["status"]),          "#C0392B"),
            ("RESCHEDULED", sum(1 for a in vis if "Reschedul" in a["status"]),       "#CA6F1E"),
        ]:
            f = tk.Frame(card_bar, bg=col, padx=12, pady=9)
            f.pack(side="left", padx=4, fill="y")
            tk.Label(f, text=title, font=("Arial", 8, "bold"), fg="white", bg=col).pack(anchor="w")
            tk.Label(f, text=str(count), font=("Arial", 20, "bold"), fg="white", bg=col).pack(anchor="w")

    refresh_cards()

    #  Button Bar above table
    bbar = tk.Frame(dash)
    bbar.pack(fill="x", padx=10, pady=5)

    # Appointments Treeview Table
    tbl_frame = tk.Frame(dash)
    tbl_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

    acols = ("Patient", "Doctor", "Date", "Time", "Reason", "Status")
    atbl  = ttk.Treeview(tbl_frame, columns=acols, show="headings", height=13)
    as_   = ttk.Style()
    as_.configure("Treeview",         font=("Arial", 10), rowheight=27)
    as_.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    for col in acols:
        atbl.heading(col, text=col)
    atbl.column("Patient", width=175, anchor="w")
    atbl.column("Doctor",  width=135, anchor="w")
    atbl.column("Date",    width=100, anchor="center")
    atbl.column("Time",    width=90,  anchor="center")
    atbl.column("Reason",  width=220, anchor="w")
    atbl.column("Status",  width=150, anchor="center")

    av = ttk.Scrollbar(tbl_frame, orient="vertical",   command=atbl.yview)
    ah = ttk.Scrollbar(tbl_frame, orient="horizontal", command=atbl.xview)
    atbl.configure(yscrollcommand=av.set, xscrollcommand=ah.set)
    av.pack(side="right",  fill="y")
    ah.pack(side="bottom", fill="x")
    atbl.pack(fill="both", expand=True)

    def load_atbl():   # reloads the appointments table from the list
        for r in atbl.get_children():
            atbl.delete(r)
        for a in get_visible():
            atbl.insert("", tk.END, values=(
                a["patient_name"], a["doctor"],
                a["date"], a["time"], a["reason"], a["status"]
            ))

    load_atbl()   # fill table when dashboard first opens

    def get_sel():   # returns the appointment dict for the selected row
        sel = atbl.selection()
        if not sel:
            messagebox.showwarning("None Selected", "Please click on an appointment row first.", parent=dash)
            return None
        vals = atbl.item(sel[0])["values"]
        # match by patient name, date and time to find the correct appointment
        for a in appointments:
            if a["patient_name"] == vals[0] and a["date"] == vals[2] and a["time"] == vals[3]:
                return a
        return None

    # Action: Mark Complete
    def mark_complete():
        a = get_sel()
        if a:
            a["status"] = "Completed"
            load_atbl()
            refresh_cards()
            messagebox.showinfo("Updated", "Appointment marked as Completed.", parent=dash)

    # Action: Cancel Appointment
    def cancel_appt():
        a = get_sel()
        if a and messagebox.askyesno("Cancel", f"Cancel appointment for {a['patient_name']}?", parent=dash):
            a["status"] = "Cancelled"
            load_atbl()
            refresh_cards()

    # Action: Reschedule Appointment
    def reschedule_appt():
        a = get_sel()
        if not a:
            return

        rw = tk.Toplevel(dash)   # a small popup window for reschedule details
        rw.title("Reschedule Appointment")
        rw.geometry("360x300")
        rw.resizable(False, False)
        rw.grab_set()   # lock focus to this popup

        tk.Label(rw, text=f"Rescheduling: {a['patient_name']}",
                 font=("Arial", 11, "bold")).pack(pady=12)
        tk.Label(rw, text="New Date (DD/MM/YYYY):", font=("Arial", 10)).pack()
        d_e = tk.Entry(rw, font=("Arial", 11), width=24)
        d_e.insert(0, a["date"])   # pre-fill with current date
        d_e.pack(pady=(2, 8))
        tk.Label(rw, text="New Time (e.g. 10:00 AM):", font=("Arial", 10)).pack()
        t_e = tk.Entry(rw, font=("Arial", 11), width=24)
        t_e.insert(0, a["time"])   # pre-fill with current time
        t_e.pack(pady=(2, 8))
        tk.Label(rw, text="Reason for Rescheduling:", font=("Arial", 10)).pack()
        r_e = tk.Entry(rw, font=("Arial", 11), width=24)
        r_e.pack(pady=(2, 10))

        def save_rs():
            nd = d_e.get().strip()
            nt = t_e.get().strip()
            nr = r_e.get().strip()
            if not nd or not nt:
                messagebox.showerror("Error", "Date and time are required.", parent=rw)
                return
            a["date"]   = nd
            a["time"]   = nt
            a["status"] = "Rescheduled" + (f" — {nr}" if nr else "")
            load_atbl()
            refresh_cards()
            rw.destroy()
            messagebox.showinfo("Done", f"Appointment rescheduled to {nd} at {nt}.", parent=dash)

        tk.Button(rw, text="Save Reschedule", command=save_rs,
                  font=("Arial", 10, "bold"), relief="raised", bd=2, pady=7).pack(padx=20, fill="x")

    # Action: Add New Appointment
    def add_new_appt():
        aw = tk.Toplevel(dash)
        aw.title("New Appointment")
        aw.geometry("380x430")
        aw.resizable(False, False)
        aw.grab_set()

        tk.Label(aw, text="New Appointment", font=("Arial", 13, "bold")).pack(pady=12)
        ab = tk.Frame(aw, padx=22)
        ab.pack(fill="both", expand=True)

        def al(text):
            tk.Label(ab, text=text, font=("Arial", 9, "bold"), anchor="w").pack(fill="x", pady=(7, 1))

        al("Select Patient")
        pnames = [r["name"] for r in records] if records else ["No patients registered"]
        p_var  = tk.StringVar(value=pnames[0])
        pm = tk.OptionMenu(ab, p_var, *pnames)
        pm.config(font=("Arial", 10), relief="solid", bd=1)
        pm["menu"].config(font=("Arial", 10))
        pm.pack(fill="x", ipady=3)

        al("Assign Doctor")
        doc_list = [d for d in DOCTORS if d != "Unassigned"]
        doc_var  = tk.StringVar(value=uname if role == "doctor" else doc_list[0])
        dm = tk.OptionMenu(ab, doc_var, *doc_list)
        dm.config(font=("Arial", 10), relief="solid", bd=1)
        dm["menu"].config(font=("Arial", 10))
        dm.pack(fill="x", ipady=3)

        al("Date (DD/MM/YYYY)")
        date_e = tk.Entry(ab, font=("Arial", 11), relief="solid", bd=1)
        date_e.insert(0, datetime.now().strftime("%d/%m/%Y"))
        date_e.pack(fill="x", ipady=4)

        al("Time (e.g. 09:00 AM)")
        time_e = tk.Entry(ab, font=("Arial", 11), relief="solid", bd=1)
        time_e.pack(fill="x", ipady=4)

        al("Reason for Appointment")
        reason_e = tk.Entry(ab, font=("Arial", 11), relief="solid", bd=1)
        reason_e.pack(fill="x", ipady=4)

        def save_appt():
            pat    = p_var.get()
            doc    = doc_var.get()
            date   = date_e.get().strip()
            time   = time_e.get().strip()
            reason = reason_e.get().strip()
            if not date or not time or not reason:
                messagebox.showerror("Missing", "Please fill in all fields.", parent=aw)
                return
            rec_num = next((r["number"] for r in records if r["name"] == pat), 0)
            appointments.append({
                "patient_name": pat, "patient_num": rec_num,
                "doctor"      : doc, "date"       : date,
                "time"        : time, "reason"    : reason,
                "status"      : "Scheduled"
            })
            load_atbl()
            refresh_cards()
            messagebox.showinfo("Saved", f"Appointment for {pat} on {date} at {time} saved.", parent=aw)
            aw.destroy()

        tk.Button(ab, text=" Save Appointment", command=save_appt,
                  font=("Arial", 11, "bold"), relief="raised", bd=2, pady=8).pack(fill="x", pady=(14, 0))

    # Place the action buttons in the button bar
    for txt, cmd in [
        ("+ New Appointment", add_new_appt),
        (" Mark Complete",  mark_complete),
        (" Reschedule",     reschedule_appt),
        ("  Cancel",         cancel_appt),
    ]:
        tk.Button(bbar, text=txt, command=cmd,
                  font=("Arial", 10, "bold"), relief="raised", bd=2,
                  padx=10, pady=5, cursor="hand2").pack(side="left", padx=(0, 6))


# LOGIN WINDOW


def show_login():
    logged_in = [False]   # list so the nested function can change it

    lw = tk.Tk()
    lw.title("Login  Sierra Leone Community Health Records")
    lw.geometry("420x500")
    lw.resizable(False, False)

    # Black header
    hdr = tk.Frame(lw, bg="black", height=88)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(hdr, text=" Community Health Records System",
             font=("Georgia", 14, "bold"), fg="white", bg="black").pack(pady=(18, 3))
    tk.Label(hdr, text="",
             font=("Arial", 9), fg="grey60", bg="black").pack()

    body = tk.Frame(lw, padx=45, pady=28)
    body.pack(fill="both", expand=True)

    tk.Label(body, text="Sign In", font=("Arial", 17, "bold"), anchor="w").pack(fill="x", pady=(0, 18))

    tk.Label(body, text="Username", font=("Arial", 10, "bold"), anchor="w").pack(fill="x", pady=(0, 2))
    usr = tk.Entry(body, font=("Arial", 12), relief="solid", bd=1)
    usr.pack(fill="x", ipady=7, pady=(0, 10))

    tk.Label(body, text="Password", font=("Arial", 10, "bold"), anchor="w").pack(fill="x", pady=(0, 2))
    pwd = tk.Entry(body, font=("Arial", 12), relief="solid", bd=1, show="●")  # show="●" hides characters
    pwd.pack(fill="x", ipady=7)

    err = tk.Label(body, text="", font=("Arial", 9), fg="red", anchor="w")
    err.pack(fill="x", pady=(6, 0))

    def do_login(event=None):   # event=None so it works both from button and Enter key
        username = usr.get().strip().lower()
        password = pwd.get().strip()
        if username not in USERS:
            err.config(text=" Username not found")
            return
        if USERS[username]["password"] != password:
            err.config(text=" Incorrect password. Please try again.")
            return
        current_user["name"]     = USERS[username]["name"]
        current_user["role"]     = USERS[username]["role"]
        current_user["username"] = username
        logged_in[0] = True
        lw.quit()   # quit() exits mainloop safely without destroying the window yet

    lw.bind("<Return>", do_login)   # pressing Enter key also triggers login

    tk.Button(body, text="Login  →", command=do_login,
              font=("Arial", 12, "bold"), relief="raised", bd=2, pady=10, cursor="hand2").pack(fill="x", pady=(14, 0))

    # Credentials hint at the bottom
    hint = tk.Frame(lw, bg="#F0F0F0", padx=18, pady=9)
    hint.pack(fill="x")
    tk.Label(hint, text="Demo Credentials:", font=("Arial", 8, "bold"), bg="#F0F0F0", anchor="w").pack(anchor="w")
    tk.Label(hint, text="Admin  →  admin / admin123",
             font=("Arial", 8), fg="grey40", bg="#F0F0F0", anchor="w").pack(anchor="w")
    tk.Label(hint, text="Doctors  →  drkoroma / doc123   |   drjohnson / doc456   |   drbangura / doc789",
             font=("Arial", 8), fg="grey40", bg="#F0F0F0", anchor="w", wraplength=360).pack(anchor="w")

    lw.protocol("WM_DELETE_WINDOW", lw.quit)   # X button also exits mainloop
    usr.focus()         # put cursor in username box automatically
    lw.mainloop()       # run the login window
    lw.destroy()        # cleanup after mainloop exits
    return logged_in[0] # return True if login was successful

# ANALYTICS FUNCTIONS


def gender_chart():
    genders = [p["gender"] for p in records]

    data = Counter(genders)

    plt.figure(figsize=(6, 6))
    plt.pie(
        data.values(),
        labels=data.keys(),
        autopct="%1.1f%%"
    )
    plt.title("Gender Distribution")
    plt.show()


def age_group_chart():

    groups = {
        "Children (0-12)": 0,
        "Teenagers (13-17)": 0,
        "Adults (18-59)": 0,
        "Seniors (60+)": 0
    }

    for p in records:
        age = int(p["age"])

        if age <= 12:
            groups["Children (0-12)"] += 1
        elif age <= 17:
            groups["Teenagers (13-17)"] += 1
        elif age <= 59:
            groups["Adults (18-59)"] += 1
        else:
            groups["Seniors (60+)"] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(groups.keys(), groups.values())
    plt.title("Age Group Distribution")
    plt.ylabel("Patients")
    plt.xticks(rotation=15)
    plt.show()


def treatment_status_chart():

    statuses = [p["status"] for p in records]

    data = Counter(statuses)

    plt.figure(figsize=(6, 6))
    plt.pie(
        data.values(),
        labels=data.keys(),
        autopct="%1.1f%%"
    )
    plt.title("Treatment Status Distribution")
    plt.show()


def district_chart():

    districts = [p["district"] for p in records]

    data = Counter(districts)

    plt.figure(figsize=(10, 5))
    plt.bar(data.keys(), data.values())
    plt.title("Patients by District")
    plt.ylabel("Patients")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def diagnosis_chart():

    diagnoses = [p["diagnosis"] for p in records]

    data = Counter(diagnoses)

    plt.figure(figsize=(10, 5))
    plt.bar(data.keys(), data.values())
    plt.title("Patients by Diagnosis")
    plt.ylabel("Cases")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




def doctor_workload_chart():

    doctors = [p["doctor"] for p in records]

    data = Counter(doctors)

    plt.figure(figsize=(8, 5))
    plt.bar(data.keys(), data.values())
    plt.title("Doctor Workload")
    plt.ylabel("Assigned Patients")
    plt.xticks(rotation=20)
    plt.show()


def registration_trend_chart():

    months = []

    for p in records:

        try:
            date_str = p["date_registered"]

            dt = datetime.strptime(date_str, "%d/%m/%Y")

            months.append(dt.strftime("%b"))

        except:
            continue

    data = Counter(months)

    order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    values = [data.get(m, 0) for m in order]

    plt.figure(figsize=(10, 5))
    plt.plot(order, values, marker="o")
    plt.title("Monthly Registration Trend")
    plt.ylabel("Registrations")
    plt.grid(True)
    plt.show()



# MAIN WINDOW BUILDER

def launch_main():
    global root, counter_num, card_total, card_male, card_female, card_risk
    global entry_name, entry_age, entry_other, other_frame
    global gender_var, district_var, diagnosis_var, status_var, doctor_var
    global table, notebook, stats_box, dots_btn
    global filter_gender_var, filter_district_var, filter_diag_var
    global filter_status_var, filter_risk_var, filter_name_var, filter_result_label

    root = tk.Tk()    # create the main window
    root.title("Sierra Leone Community Health Records System")
    root.geometry("1200x820")
    root.minsize(1000, 700)   # window cannot be made smaller than this


    # HEADER  black bar across the top


    header = tk.Frame(root, bg="black", height=90)
    header.pack(fill="x")
    header.pack_propagate(False)   # keeps height at exactly 90 pixels

    lhdr = tk.Frame(header, bg="black")
    lhdr.pack(side="left", padx=20, pady=8)
    tk.Label(lhdr, text="  SIERRA LEONE COMMUNITY HEALTH RECORDS",
             font=("Georgia", 17, "bold"), fg="white", bg="black", anchor="w").pack(anchor="w")
    tk.Label(lhdr, text="Ministry of Health  ·  SDG 3: Good Health & Well-being",
             font=("Tahoma", 10), fg="white", bg="black", anchor="w").pack(anchor="w", pady=(4, 2))
    tk.Label(lhdr, text=f"Logged in as: {current_user['name']}   ({current_user['role'].title()})",
             font=("Arial", 8, "italic"), fg="grey60", bg="black", anchor="w").pack(anchor="w")

    # Right side — patient counter and 3-dot menu button
    rhdr = tk.Frame(header, bg="black")
    rhdr.pack(side="right", padx=10)

    # ⋮ is the 3-dot vertical icon — clicking shows a dropdown menu
    dots_btn = tk.Button(rhdr, text="⋮", font=("Arial", 22, "bold"),
                         fg="white", bg="black", relief="flat", bd=0,
                         cursor="hand2", command=show_dots_menu,
                         activebackground="grey20", activeforeground="white")
    dots_btn.pack(side="right", padx=12, pady=18)

    cnt = tk.Frame(rhdr, bg="black")
    cnt.pack(side="right", padx=15)
    tk.Label(cnt, text="PATIENTS REGISTERED", font=("Arial", 8, "bold"),
             fg="white", bg="black").pack()
    counter_num = tk.Label(cnt, text="0", font=("Arial", 34, "bold"), fg="white", bg="black")
    counter_num.pack()


    # MAIN CONTENT — left column (form) + right column (dashboard)


    main_area = tk.Frame(root)
    main_area.pack(fill="both", expand=True, padx=12, pady=10)

    #  LEFT COLUMN: Registration Form

    left_col = tk.Frame(main_area, width=315)
    left_col.pack(side="left", fill="y", padx=(0, 10))
    left_col.pack_propagate(False)   # keep width fixed at 315

    form_card = tk.Frame(left_col, bd=1, relief="solid")
    form_card.pack(fill="both", expand=True)

    fbar = tk.Frame(form_card, bg="black")   # black title bar for the form
    fbar.pack(fill="x")
    tk.Label(fbar, text="   PATIENT REGISTRATION FORM",
             font=("Arial", 11, "bold"), fg="white", bg="black", anchor="w").pack(fill="x", pady=9, padx=5)

    # Scrollable canvas for the form — so all fields fit on any screen size
    fc = tk.Canvas(form_card, highlightthickness=0)
    fs = tk.Scrollbar(form_card, orient="vertical", command=fc.yview)
    form_body = tk.Frame(fc, padx=15, pady=5)
    form_body.bind("<Configure>",
                   lambda e: fc.configure(scrollregion=fc.bbox("all")))  # update scroll area when form changes size
    fwin = fc.create_window((0, 0), window=form_body, anchor="nw")        # place form_body inside canvas
    fc.bind("<Configure>", lambda e: fc.itemconfig(fwin, width=e.width))  # make form fill canvas width
    fc.configure(yscrollcommand=fs.set)
    fs.pack(side="right", fill="y")
    fc.pack(side="left", fill="both", expand=True)

    # Enable mousewheel scrolling on the form
    def scroll_form(evt):
        fc.yview_scroll(int(-1 * (evt.delta / 120)), "units")
    fc.bind("<Enter>", lambda e: fc.bind_all("<MouseWheel>", scroll_form))
    fc.bind("<Leave>", lambda e: fc.unbind_all("<MouseWheel>"))

    # Helpers to create each form element consistently
    def flbl(text):   # bold label above a field
        tk.Label(form_body, text=text, font=("Arial", 9, "bold"), anchor="w").pack(fill="x", pady=(8, 1))

    def fent():   # plain text entry box
        e = tk.Entry(form_body, font=("Arial", 11), relief="solid", bd=1)
        e.pack(fill="x", ipady=5)
        return e

    def fdrp(var, options):   # dropdown menu (OptionMenu)
        d = tk.OptionMenu(form_body, var, *options)
        d.config(font=("Arial", 10), relief="solid", bd=1)
        d["menu"].config(font=("Arial", 10))
        d.pack(fill="x", ipady=3)
        return d

    # Build each form field
    flbl("Full Name")
    entry_name = fent()

    flbl("Age")
    entry_age = fent()

    flbl("Gender")
    gender_var = tk.StringVar(value="Male")
    fdrp(gender_var, ["Male", "Female"])

    flbl("District")
    district_var = tk.StringVar(value="-- Select District --")
    fdrp(district_var, DISTRICTS)

    flbl("What Are You Diagnosed With?")
    diagnosis_var = tk.StringVar(value="-- Select Diagnosis --")
    fdrp(diagnosis_var, DIAGNOSES)
    diagnosis_var.trace("w", on_diagnosis_change)   # watch for "Other" being selected

    # Hidden "Other" frame — only visible when "Other" diagnosis is selected
    other_frame = tk.Frame(form_body)
    tk.Label(other_frame, text="Please specify your diagnosis:",
             font=("Arial", 9, "bold"), anchor="w").pack(fill="x", pady=(4, 1))
    entry_other = tk.Entry(other_frame, font=("Arial", 11), relief="solid", bd=1)
    entry_other.pack(fill="x", ipady=4)

    flbl("Treatment Status")
    status_var = tk.StringVar(value="Under Treatment")
    fdrp(status_var, STATUSES)   # includes the new "About to Start" option

    flbl("Assigned Doctor")
    doctor_var = tk.StringVar(value="Unassigned")
    fdrp(doctor_var, DOCTORS)

    fb2 = tk.Frame(form_card, padx=15, pady=12)
    fb2.pack(fill="x")
    tk.Button(fb2, text="  Register Patient", command=add_patient,
              font=("Arial", 11, "bold"), relief="raised", bd=2, pady=9, cursor="hand2").pack(fill="x", pady=(0, 6))
    tk.Button(fb2, text="  Clear Form", command=clear_form,
              font=("Arial", 10), relief="raised", bd=2, pady=7, cursor="hand2").pack(fill="x")

    #  RIGHT COLUMN: Dashboard

    right_col = tk.Frame(main_area)
    right_col.pack(side="right", fill="both", expand=True)

    # 4 live stat cards
    cards_row = tk.Frame(right_col)
    cards_row.pack(fill="x", pady=(0, 10))

    def make_card(parent, title):
        c = tk.Frame(parent, relief="groove", bd=2, padx=15, pady=10)
        c.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(c, text=title, font=("Arial", 9, "bold"), anchor="w").pack(anchor="w")
        v = tk.Label(c, text="0", font=("Arial", 26, "bold"))
        v.pack(anchor="w")
        return v   # return so update_dashboard() can change the number

    card_total  = make_card(cards_row, "TOTAL PATIENTS")
    card_male   = make_card(cards_row, "MALE PATIENTS")
    card_female = make_card(cards_row, "FEMALE PATIENTS")
    card_risk   = make_card(cards_row, "HIGH RISK")

    # Tab bar — Records, Statistics, Filter
    tab_style = ttk.Style()
    tab_style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[14, 6])
    notebook = ttk.Notebook(right_col)
    notebook.pack(fill="both", expand=True)

    #  TAB 1: Patient Records Table

    records_tab = tk.Frame(notebook)
    notebook.add(records_tab, text="   Patient Records  ")

    ibar = tk.Frame(records_tab, padx=10, pady=7)
    ibar.pack(fill="x")
    tk.Label(ibar, text="💡  Click a row to select  |  Double-click to Edit  |  Select then click Delete to remove",
             font=("Arial", 9, "italic")).pack(side="left")
    tk.Button(ibar, text="🗑  Delete Selected", command=delete_patient,
              font=("Arial", 10, "bold"), relief="raised", bd=2, padx=10, pady=4, cursor="hand2").pack(side="right", padx=5)

    tbl_frame = tk.Frame(records_tab)
    tbl_frame.pack(fill="both", expand=True, padx=5, pady=5)

    COLS = ("No.", "Full Name", "Age", "Gender", "District",
            "Diagnosed With", "Status", "Risk Level", "Date Registered")
    table = ttk.Treeview(tbl_frame, columns=COLS, show="headings", height=10)

    ts = ttk.Style()
    ts.configure("Treeview",         font=("Arial", 10), rowheight=28)
    ts.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    WS = {"No.": 45, "Full Name": 155, "Age": 45, "Gender": 70, "District": 185,
          "Diagnosed With": 145, "Status": 140, "Risk Level": 90, "Date Registered": 135}
    for col in COLS:
        table.heading(col, text=col)
        table.column(col, width=WS[col], anchor="center", minwidth=40)
    table.column("Full Name",      anchor="w")   # left-align text columns
    table.column("District",       anchor="w")
    table.column("Diagnosed With", anchor="w")
    table.column("Status",         anchor="w")
    table.bind("<Double-1>", open_edit_window)   # double-click opens edit window

    vs = ttk.Scrollbar(tbl_frame, orient="vertical",   command=table.yview)
    hs = ttk.Scrollbar(tbl_frame, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
    vs.pack(side="right",  fill="y")
    hs.pack(side="bottom", fill="x")
    table.pack(fill="both", expand=True)

    #  TAB 2: Statistics

    stats_tab_frame = tk.Frame(notebook)
    notebook.add(stats_tab_frame, text="   Statistics  ")

    sb_bar = tk.Frame(stats_tab_frame, padx=10, pady=8)
    sb_bar.pack(fill="x")
    tk.Button(sb_bar, text=" Generate Statistics Report", command=show_statistics,
              font=("Arial", 10, "bold"), relief="raised", bd=2, padx=14, pady=6, cursor="hand2").pack(side="left")

    stats_box = tk.Text(stats_tab_frame, font=("Courier", 11), relief="flat",
                        padx=15, pady=10, state="disabled")
    stats_box.pack(fill="both", expand=True)
    stats_box.config(state="normal")
    stats_box.insert(tk.END, "\n\n  Click 'Generate Statistics Report' to view the full community health data.")
    stats_box.config(state="disabled")


    # TAB 3 : ANALYTICS DASHBOARD


    analytics_tab = tk.Frame(notebook)
    notebook.add(analytics_tab, text="   Analytics Dashboard  ")

    title = tk.Label(
        analytics_tab,
        text="Community Health Analytics Dashboard",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=15)

    btn_frame = tk.Frame(analytics_tab)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="‍⚕ Gender Distribution",
        width=30,
        command=gender_chart
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text=" Age Group Analysis",
        width=30,
        command=age_group_chart
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text=" Treatment Status",
        width=30,
        command=treatment_status_chart
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text=" Patients by District",
        width=30,
        command=district_chart
    ).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text=" Diagnosis Analysis",
        width=30,
        command=diagnosis_chart
    ).grid(row=2, column=0, padx=10, pady=10)


    tk.Button(
        btn_frame,
        text="⚕ Doctor Workload",
        width=30,
        command=doctor_workload_chart
    ).grid(row=3, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text=" Registration Trend",
        width=30,
        command=registration_trend_chart
    ).grid(row=3, column=1, padx=10, pady=10)

    # TAB 3: Filter & Search

    filter_tab_frame = tk.Frame(notebook)
    notebook.add(filter_tab_frame, text="    Filter & Search  ")

    # Initialise all filter StringVars
    filter_gender_var   = tk.StringVar(value="All")
    filter_district_var = tk.StringVar(value="All")
    filter_diag_var     = tk.StringVar(value="All")
    filter_status_var   = tk.StringVar(value="All")
    filter_risk_var     = tk.StringVar(value="All")
    filter_name_var     = tk.StringVar()

    # Scrollable canvas for the filter page
    flt_c = tk.Canvas(filter_tab_frame, highlightthickness=0)
    flt_s = tk.Scrollbar(filter_tab_frame, orient="vertical", command=flt_c.yview)
    flt_i = tk.Frame(flt_c, padx=22, pady=15)
    flt_i.bind("<Configure>", lambda e: flt_c.configure(scrollregion=flt_c.bbox("all")))
    fwi   = flt_c.create_window((0, 0), window=flt_i, anchor="nw")
    flt_c.bind("<Configure>", lambda e: flt_c.itemconfig(fwi, width=e.width))
    flt_c.configure(yscrollcommand=flt_s.set)
    flt_s.pack(side="right", fill="y")
    flt_c.pack(side="left", fill="both", expand=True)

    def scroll_flt(evt):
        flt_c.yview_scroll(int(-1 * (evt.delta / 120)), "units")
    flt_c.bind("<Enter>", lambda e: flt_c.bind_all("<MouseWheel>", scroll_flt))
    flt_c.bind("<Leave>", lambda e: flt_c.unbind_all("<MouseWheel>"))

    def ftlbl(text):
        tk.Label(flt_i, text=text, font=("Arial", 10, "bold"), anchor="w").pack(fill="x", pady=(10, 2))

    def ftdrp(var, options):
        d = tk.OptionMenu(flt_i, var, *options)
        d.config(font=("Arial", 10), relief="solid", bd=1)
        d["menu"].config(font=("Arial", 10))
        d.pack(fill="x", ipady=4)

    tk.Label(flt_i, text=" Filter & Search Patients",
             font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(0, 4))
    tk.Label(flt_i,
             text="Select filter values and click Apply. Leave 'All' to ignore that field. Use Search to find by name.",
             font=("Arial", 9), fg="grey40", anchor="w", wraplength=560).pack(fill="x", pady=(0, 8))

    # Name search row  entry + search button side by side
    ftlbl("Search by Patient Name")
    srow = tk.Frame(flt_i)
    srow.pack(fill="x")
    tk.Entry(srow, textvariable=filter_name_var, font=("Arial", 11),
             relief="solid", bd=1).pack(side="left", fill="x", expand=True, ipady=5)
    tk.Button(srow, text="Search", command=search_patient,
              font=("Arial", 10, "bold"), relief="raised", bd=2, padx=10, pady=4).pack(side="left", padx=(6, 0))

    # Filter dropdowns  one per column
    ftlbl("Filter by Gender")
    ftdrp(filter_gender_var, ["All", "Male", "Female"])
    ftlbl("Filter by District")
    ftdrp(filter_district_var, ["All"] + DISTRICTS)
    ftlbl("Filter by Diagnosis")
    ftdrp(filter_diag_var, ["All"] + DIAGNOSES)
    ftlbl("Filter by Treatment Status")
    ftdrp(filter_status_var, ["All"] + STATUSES)
    ftlbl("Filter by Risk Level")
    ftdrp(filter_risk_var, ["All"] + RISK_LEVELS)

    filter_result_label = tk.Label(flt_i, text="", font=("Arial", 10, "bold"), anchor="w")
    filter_result_label.pack(fill="x", pady=(10, 4))

    brow = tk.Frame(flt_i)
    brow.pack(fill="x", pady=(4, 20))
    tk.Button(brow, text=" Apply Filter", command=apply_filter,
              font=("Arial", 11, "bold"), relief="raised", bd=2, padx=14, pady=8).pack(side="left", padx=(0, 8))
    tk.Button(brow, text="  Clear Filter", command=clear_filter,
              font=("Arial", 10), relief="raised", bd=2, padx=14, pady=8).pack(side="left")


    # STATUS BAR  black bar at the very bottom


    sbar = tk.Frame(root, bg="black", height=26)
    sbar.pack(fill="x", side="bottom")
    sbar.pack_propagate(False)
    tk.Label(sbar,
             text=f"    Sierra Leone Community Health Records  ·  SDG 3  ·  PROG103  ·  {current_user['name']}",
             font=("Arial", 8), fg="white", bg="black", anchor="w").pack(side="left", pady=4)
    tk.Label(sbar, text=f"v3.0  ·  {datetime.now().strftime('%d/%m/%Y')}  ",
             font=("Arial", 8), fg="white", bg="black", anchor="e").pack(side="right", pady=4)


    # LOAD DATA AND START


    load_dummy_data()    # fill records and appointments with 15 patients + 6 appointments
    refresh_table()      # draw all records in the table
    update_dashboard()   # set all 4 stat cards to the correct starting values

    root.mainloop()      # keep the window open — blocks here until quit() or destroy()
    root.destroy()       # clean up the window after mainloop exits
    return logout_flag   # return True if user clicked Logout, False if they closed with X


# ENTRY POINT — while loop so logout always goes back to login


while True:

    # Show the login window — blocks here until user logs in or closes it
    login_success = show_login()

    if not login_success:
        # User closed the login window without logging in — end the program
        break

    # Reset the logout flag before every new session
    logout_flag = False

    # Launch the main system — blocks here until logout or window close
    user_logged_out = launch_main()

    if not user_logged_out:
        # User closed the main window with the X button — end the program
        break

    # If we reach here, the user clicked Logout
    # Clear all session data so the next login starts completely fresh
    records.clear()
    appointments.clear()
    current_user["name"]     = ""
    current_user["role"]     = ""
    current_user["username"] = ""
    # The while loop continues — show_login() runs again automatically