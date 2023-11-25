import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import sqlite3

#DB Settings
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY, date TEXT, task TEXT, status REAL)''')
conn.commit()

# Global Vars
today = datetime.now().strftime("%d/%m/%y")
i = 0

# List all tasks
def list_tasks(date):
    # Clear existing tasks
    for task in index:
        task['frm'].destroy()
        task['delete_btn'].destroy()
        task['task_lbl'].destroy()
        task['mark_btn'].destroy()
    index.clear()
    
    cursor.execute("SELECT id, date, task, status FROM employees WHERE date = ?", (date,))
    rows = cursor.fetchall()
    k = 0
    for row in rows:
        task_id = row[0]
        task_frm = tk.Frame(master=frame, width=375, height=40, background="#444444")
        task_frm.grid(row=k, column=0, pady=(10, 0))

        if row[3] == 0:
            task_lbl = ttk.Label(task_frm, text=row[2], font=("Helvetica", 15), background="#444444", foreground="white")
            task_lbl.place(x=15, y=10)
        else:
            task_lbl = ttk.Label(task_frm, text=row[2], font=("Helvetica", 15, "overstrike"), background="#444444", foreground="white")
            task_lbl.place(x=15, y=10)

        delete_btn = tk.Button(task_frm, image=delete_icon, border=0, cursor="hand2", background="#444444", command=lambda id=task_id: delete_task(id))
        delete_btn.place(x=280, y=10)

        mark_btn = tk.Button(task_frm, image=mark_icon, borderwidth=0, cursor="hand2", background="#444444", border=0, command=lambda id=task_id: mark_task(id))
        mark_btn.place(x=220, y=10)

        # The tasks listed from the database are kept of tracked in the task dictionary whoch are then appended to the index list (similar to the add task function, where we are keeping track of tasks created), which is used to delete or mark task

        task = {'frm': task_frm, 'delete_btn': delete_btn, 'task_lbl': task_lbl, 'mark_btn': mark_btn, 'id':task_id}
        index.append(task)
        k += 1

# Task Functions
# Clear Screen
def clear_screen():
    task_ent.delete(0, tk.END)


# Change date function
def change_date(delta):
    date_format = "%d/%m/%y"
    current_date = datetime.strptime(date_lbl['text'], date_format)
    new_date = current_date + timedelta(days=delta)
    date_lbl['text'] = new_date.strftime(date_format)
    list_tasks(date_lbl['text'])

def prev_date():
    change_date(-1)

def next_date():
    change_date(1)

# Add tasks
def add_task():
    global i, task_id
    avail_tasks=len(index)

    if avail_tasks > 0:
        i = avail_tasks+1
    task_text = task_ent.get()
    if task_text == "":
        messagebox.showerror("TODOApp", "Invalid Entry")
    else:
        task_frm = tk.Frame(master=frame,  width=375, height=40, background="#444444")
        task_frm.grid(row=i, column=0, pady=(10, 0))

        task_lbl = ttk.Label(task_frm, text=task_text, font=("Helvetica", 15), background="#444444", foreground="white")
        task_lbl.place(x=15, y=10)

        delete_btn = tk.Button(task_frm, image=delete_icon, border=0, cursor="hand2", background="#444444", command= lambda: delete_task(task_id))
        delete_btn.place(x=280, y=10)

        mark_btn = tk.Button(task_frm, image=mark_icon, borderwidth=0, cursor="hand2", background="#444444", border=0, command= lambda: mark_task(mark_btn))
        mark_btn.place(x=220, y=10)

        cursor.execute("INSERT INTO employees (date, task, status) VALUES (?, ?, ?)", (date_lbl["text"], task_lbl['text'], 0))
        conn.commit()
        
        task_id = cursor.lastrowid
        
        # Keep track of tasks created
        task = {'frm': task_frm,'delete_btn': delete_btn, 'task_lbl': task_lbl, 'mark_btn': mark_btn, 'id':task_id}
        index.append(task)
        i += 1
        clear_screen()


# Delete Tasks
def delete_task(task_id):
    global i
    for task in index:
        if task['id'] == task_id:
            # Remove the task from the index list

            key = index.index(task)
            del index[key]

            # Hide the Tkinter widgets associated with the task
            task['frm'].grid_forget()
            task['delete_btn'].place_forget()
            task['task_lbl'].place_forget()
            task['mark_btn'].place_forget()

            # Update positions of the remaining tasks after the deleted one
            for j, remaining_task in enumerate(index):
                remaining_task['frm'].grid(row=j, column=0,  pady=(10,0))
                remaining_task['delete_btn'].place(x=280, y=10)
                remaining_task['task_lbl'].place(x=15, y=10)
                remaining_task['mark_btn'].place(x=220, y=10)

            i -= 1  # Decrement i as a task is removed

            if i < 0:
                i = 0

            cursor.execute("DELETE FROM employees WHERE id = ?", (task_id,))
            conn.commit()
            
            # Re-list tasks after deleting one
            list_tasks(date_lbl['text'])


# Mark a task as done with strikethrough
def mark_task(task_id):
    for task in index:
        if task['id'] == task_id:
            task['task_lbl'].config(font=("Helvetica", 15, "overstrike"))

            text = task['task_lbl']['text']

            cursor.execute("UPDATE employees SET status = ? WHERE task = ?", (1,text))
            conn.commit()

# frame configure
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

# Tkinter Window
window = tk.Tk()
window.geometry("375x450-30+10")
window.title("TODO APP")
window.resizable(False, False)

# ScrollBar
#------Scrollbars are only activated on Text, Canvas and Listbox widgets-------
canvas = tk.Canvas(window, borderwidth=0, background="#ffffff")  #create a canva
frame = tk.Frame(canvas, background="#ffffff") #Put a frame in the canvas

#create sb widget
vsb = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set) #Configure sb on canvas widget

vsb.pack(side="right", fill="y") #postion sb
canvas.pack(side="left", fill="both", pady=(108,0), expand=True) #position canvas
canvas.create_window((4,4), window=frame, anchor="nw") 
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas)) 

# All Frames
top_frm = tk.Frame(master=window, width=375, height=50, background="#333333")
top_frm.place(x=0, y=0)

ent_frm = tk.Frame(master=window, width=375, height=60, background="white")
ent_frm.place(x=0, y=50)

task_ent = ttk.Entry(master=ent_frm, font=("Helvetica", 15))
task_ent.place(x=10, y=15, height=39, width=290)

# Date Label
date_lbl = ttk.Label(master=top_frm, text=today, font=("Georgia", 20, "bold"), foreground="white", background="#333333")
date_lbl.place(x=120, y=10)


# Change date
# image = Image.open("todoapp\\add.png")
# add_image_resize = image.resize((30, 34))
# add_icon = ImageTk.PhotoImage(add_image_resize)
next_date_btn = tk.Button(master=top_frm, command=next_date,background="black",borderwidth=1, cursor="hand2")
next_date_btn.place(x=260, y=20)

prev_date_btn = tk.Button(master=top_frm,command=prev_date, background="black",borderwidth=1, cursor="hand2")
prev_date_btn.place(x=100, y=20)

# Buttons
# Add task 
image = Image.open("todoapp\images\\add.png")
add_image_resize = image.resize((30, 34))
add_icon = ImageTk.PhotoImage(add_image_resize)
add_btn = tk.Button(master=ent_frm, image=add_icon, command=add_task, borderwidth=1, cursor="hand2")
add_btn.place(x=315, y=15)

# Delete task
delete_image = Image.open("todoapp\images\delete.png")
delete_image_resize = delete_image.resize((25, 25))
delete_icon = ImageTk.PhotoImage(delete_image_resize)

# # Mark task
mark_image = Image.open("todoapp\images\mark.png")
mark_image_resize = mark_image.resize((25, 25))
mark_icon = ImageTk.PhotoImage(mark_image_resize)
index = []

list_tasks(today)

window.mainloop()