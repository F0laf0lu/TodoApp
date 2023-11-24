import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3


#DB Settings
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY, date TEXT, task TEXT, status REAL)''')
conn.commit()

today = datetime.now().strftime("%d/%m/%y")
i = 0
task_id = 0


# Clear Screen
def clear_screen():
    task_ent.delete(0, tk.END)

# Add tasks
def add_task():
    global i
    task_text = task_ent.get()
    if task_text == "":
        messagebox.showerror("TODOApp", "Invalid Entry")
    else:
        # insert into DB

        task_frm = tk.Frame(master=body_frm,  width=320, height=50, background="#ffffff")
        task_frm.place(x=10, y=70 + i * 65)

        task_lbl = ttk.Label(task_frm, text=task_text, font=("Helvetica", 15), background="white")
        task_lbl.place(x=15, y=15)

        delete_btn = tk.Button(task_frm, image=delete_icon, border=0, cursor="hand2", background="white", command= lambda: delete_task(delete_btn, task_id))
        delete_btn.place(x=280, y=15)

        mark_btn = tk.Button(task_frm, image=mark_icon, borderwidth=0, cursor="hand2", background="white", border=0, command= lambda: mark_task(mark_btn))
        mark_btn.place(x=220, y=15)

        # Keep track of tasks created
        task = {'frm': task_frm,'delete_btn': delete_btn, 'task_lbl': task_lbl, 'mark_btn': mark_btn}

        index.append(task)
        clear_screen()
        i += 1

        cursor.execute("INSERT INTO employees (date, task, status) VALUES (?, ?, ?)", (today, task_lbl['text'], 0))
        conn.commit()
        
        task_id = cursor.lastrowid

# Delete Tasks
def delete_task(delete_btn, task_id):
    global i
    for task in index:
        if task['delete_btn'] == delete_btn:
            task['frm'].destroy()
            task['delete_btn'].destroy()
            task['task_lbl'].destroy()
            task['mark_btn'].destroy()

            key = index.index(task)
            del index[key]

            # Update positions of the remaining tasks after the deleted one
            for j, remaining_task in enumerate(index):
                remaining_task['frm'].place(x=10, y=70 + j * 65)
                remaining_task['delete_btn'].place(x=280, y=15)
                remaining_task['task_lbl'].place(x=15, y=15)
                remaining_task['mark_btn'].place(x=220, y=15)

            i -= 1  # Decrement i as a task is removed

            cursor.execute("DELETE FROM employees WHERE id = ?", (task_id,))
            conn.commit()

            break  # Break out of the loop once the task is found

# Mark a task as donw with strikethrough
def mark_task(mark_btn):
    for task in index:
        if task['mark_btn'] == mark_btn:
            task['task_lbl'].config(font=("Helvetica", 15, "overstrike"))

            text = task['task_lbl']['text']

            cursor.execute("UPDATE employees SET status = ? WHERE task = ?", (1,text))
            conn.commit()



# Tkinter Window
window = tk.Tk()
window.geometry("360x450-30+10")
window.title("TODO APP")
window.resizable(False, False)

top_frm = tk.Frame(master=window, width=360, height=50, background="#333333")
top_frm.pack()

body_frm = tk.Frame(master=window,  width=360, height=400, background="#cccccc")
body_frm.pack()

date_lbl = ttk.Label(master=top_frm, text=today, font=("Georgia", 20, "bold"), foreground="white", background="#333333")
date_lbl.place(x=120, y=10)

task_ent = ttk.Entry(master=body_frm, font=("Helvetica", 15))
task_ent.place(x=10, y=20, height=39, width=290)


# Add task Button
image = Image.open("todoapp\\add.png")
add_image_resize = image.resize((30, 34))
add_icon = ImageTk.PhotoImage(add_image_resize)
add_btn = tk.Button(master=body_frm, image=add_icon, command=add_task, borderwidth=1, cursor="hand2")
add_btn.place(x=315, y=20)

# Delete Button
delete_image = Image.open("todoapp\delete.png")
delete_image_resize = delete_image.resize((25, 25))
delete_icon = ImageTk.PhotoImage(delete_image_resize)

# Mark Button
mark_image = Image.open("todoapp\mark.png")
mark_image_resize = mark_image.resize((25, 25))
mark_icon = ImageTk.PhotoImage(mark_image_resize)

index = []
window.mainloop()