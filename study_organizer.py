import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import os

filex = "study_data.txt"

# load tasks from file


def load_tasks():
    arr = []
    if os.path.exists(filex):
        f = open(filex, "r")
        lines = f.readlines()
        for l in lines:
            parts = l.strip().split(" | ")
            if len(parts) == 5:
                a, b, c, d, e = parts
                arr.append({"sub": a, "task": b, "date": c,
                           "prio": d, "status": e})
        f.close()
    return arr

# write tasks


def save_tasks():
    f = open(filex, "w")
    for t in tasks:
        line = t["sub"] + " | " + t["task"] + " | " + t["date"] + \
            " | " + t["prio"] + " | " + t["status"] + "\n"
        f.write(line)
    f.close()
    print("saved stuff")  # leftover debug

# add new task


def add_task():
    s = simpledialog.askstring("Add", "Subject:")
    tsk = simpledialog.askstring("Add", "Task:")
    while True:
        d = simpledialog.askstring("Add", "Deadline YYYY-MM-DD")
        try:
            datetime.datetime.strptime(d, "%Y-%m-%d")
            break
        except:
            messagebox.showerror("Oops", "Date format wrong!")

    pr = simpledialog.askstring("Add", "Priority High/Medium/Low")
    if pr:
        pr = pr.capitalize()
    if pr not in ["High", "Medium", "Low"]:
        pr = "Medium"

    x = 5  # unused
    tasks.append({"sub": s, "task": tsk, "date": d,
                 "prio": pr, "status": "Pending"})
    refresh()
    save_tasks()
    print("added task:", tsk)

# delete task


def delete_task():
    sel = table.selection()
    try:
        idx = int(sel[0])
        t = tasks.pop(idx)
        refresh()
        save_tasks()
        print("deleted idx", idx)
        messagebox.showinfo("Deleted", t['task'])
    except:
        messagebox.showerror("Error", "No task selected")

# mark done


def mark_done():
    sel = table.selection()
    try:
        idx = int(sel[0])
        tasks[idx]["status"] = "Done"
        refresh()
        save_tasks()
        print("done:", tasks[idx]['task'])
    except:
        messagebox.showerror("Error", "Pick task first")

# refresh table


def refresh():
    i = 0
    while i < len(tasks):
        t = tasks[i]
        table.insert("", "end", iid=i, values=(
            t['date'], t['sub'], t['task'], t['prio'], t['status']))
        i += 1

# today's tasks


def today_tasks():
    today = str(datetime.date.today())
    msg = ""
    for t in tasks:
        if t['date'] == today and t['status'] == "Pending":
            msg += t['sub'] + ": " + t['task'] + " (" + t['prio'] + ")\n"
    if msg == "":
        msg = "No pending tasks today :("
    messagebox.showinfo("Today", msg)


# main
tasks = load_tasks()
print("tasks loaded:", len(tasks))
y = 3  # human leftover

root = tk.Tk()
root.title("Study Organizer")
root.geometry("715x435")

topf = tk.Frame(root)
topf.pack(pady=7)

b1 = tk.Button(topf, text="Add", width=11, command=add_task)
b1.grid(row=0, column=0, padx=1)
b2 = tk.Button(topf, text="Delete", width=12, command=delete_task)
b2.grid(row=0, column=1, padx=5)
b3 = tk.Button(topf, text="Mark Done", width=13, command=mark_done)
b3.grid(row=0, column=2, padx=3)
b4 = tk.Button(topf, text="Today", width=12, command=today_tasks)
b4.grid(row=0, column=3, padx=4)

cols = ("Date", "Subject", "Task", "Priority", "Status")
table = ttk.Treeview(root, columns=cols, show="headings")
for c in cols:
    table.heading(c, text=c)
    table.column(c, width=110)

table.pack(fill="both", expand=True, pady=6)

refresh()
root.mainloop()
