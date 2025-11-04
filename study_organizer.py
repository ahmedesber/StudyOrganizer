#imports
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import os

# using a simple .txt file
data_file = "study_data.txt"   


# load previously saved study tasks (if any)
def load_tasks():
    tasks_list = []
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            for line in f:
                bits = line.strip().split(" | ")
                # expected order: subject | task | date | priority | status
                if len(bits) == 5:
                    sub, task, dt, pr, stat = bits
                    tasks_list.append({
                        "sub": sub,
                        "task": task,
                        "date": dt,
                        "prio": pr,
                        "status": stat
                    })
    return tasks_list


# save tasks
def save_tasks():
    with open(data_file, "w") as f:
        for t in tasks:
            f.write(f"{t['sub']} | {t['task']} | {t['date']} | {t['prio']} | {t['status']}\n")
    print("saved data")  


# add task
def add_task():
    s = simpledialog.askstring("Add", "Subject:")
    tsk = simpledialog.askstring("Add", "Task:")
    if not s or not tsk:
        messagebox.showerror("Error", "Subject and Task required")
        return

    while True:
        d = simpledialog.askstring("Add", "Deadline (YYYY-MM-DD)")
        try:
            datetime.datetime.strptime(d, "%Y-%m-%d")
            break
        except:
            messagebox.showerror("Invalid", "Date format is wrong!")

    pr = simpledialog.askstring("Add", "Priority (High/Medium/Low)")
    if pr:
        pr = pr.capitalize()
    if pr not in ["High", "Medium", "Low"]:
        pr = "Medium"

    tasks.append({"sub": s, "task": tsk, "date": d,
                  "prio": pr, "status": "Pending"})
    refresh()
    save_tasks()
    print("added task:", tsk)


# delete task
def delete_task():
    sel = table.selection()
    if not sel:
        messagebox.showerror("Error", "Select a task first")
        return

    idx = int(table.index(sel[0]))
    t = tasks.pop(idx)
    refresh()
    save_tasks()
    messagebox.showinfo("Deleted", t['task'])
    print("deleted", t['task'])


# mark done
def mark_done():
    sel = table.selection()
    if not sel:
        messagebox.showerror("Error", "Pick task first")
        return

    idx = int(table.index(sel[0]))
    tasks[idx]["status"] = "Done"
    refresh()
    save_tasks()
    print("marked done:", tasks[idx]['task'])


# show today's tasks
def today_tasks():
    today = str(datetime.date.today())
    msg = ""
    for t in tasks:
        if t['date'] == today and t['status'] == "Pending":
            msg += f"{t['sub']}: {t['task']} ({t['prio']})\n"
    if not msg:
        msg = "No pending tasks today :)"
    messagebox.showinfo("Today", msg)


# refresh table
def refresh():
    for row in table.get_children():
        table.delete(row)
    for i, t in enumerate(tasks):
        table.insert("", "end", iid=i, values=(
            t['date'], t['sub'], t['task'], t['prio'], t['status']))


# main window
tasks = load_tasks()
print("tasks loaded:", len(tasks))

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
