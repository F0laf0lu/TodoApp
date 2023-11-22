import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk

i = 0

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
        task_lbl = ttk.Label(body_frm, text=task_text, font=("Helvetica", 15), background="white")
        task_lbl.place(x=15, y=95 + i * 50)

        delete_btn = tk.Button(body_frm, image=delete_icon, border=0, cursor="hand2", background="white", command= lambda: delete_task(delete_btn))
        delete_btn.place(x=320, y=95 + i * 50)

        mark_btn = tk.Button(body_frm, image=mark_icon, borderwidth=0, cursor="hand2", background="white", border=0, command= lambda: mark_task(mark_btn))
        mark_btn.place(x=270, y=95 + i * 50)

        # Keep track of tasks created and iterator (i)
        task = {'delete_btn': delete_btn, 'task_lbl': task_lbl, 'mark_btn': mark_btn}
        i += 1
        index.append(task)
        clear_screen()


# Delete Tasks
def delete_task(delete_btn):
    global i
    for task in index:
        if task['delete_btn'] == delete_btn:
            task['delete_btn'].destroy()
            task['task_lbl'].destroy()
            task['mark_btn'].destroy()
            key = index.index(task)
            del index[key]

            # Update positions of the remaining tasks after the deleted one
            for j, remaining_task in enumerate(index):
                remaining_task['delete_btn'].place(x=320, y=95 + j * 50)
                remaining_task['task_lbl'].place(x=15, y=95 + j * 50)
                remaining_task['mark_btn'].place(x=270, y=95 + j * 50)

            i -= 1  # Decrement i as a task is removed

            break  # Break out of the loop once the task is found


# Mark a task as donw with strikethrough
def mark_task(mark_btn):
    for task in index:
        if task['mark_btn'] == mark_btn:
            task['task_lbl'].config(font=("Helvetica", 15, "overstrike"))



# Tkinter Window

window = tk.Tk()
window.geometry("360x450-30+10")
window.title("TODO APP")
window.resizable(False, False)

top_frm = tk.Frame(master=window, width=360, height=50, bg="black")
top_frm.pack()

body_frm = tk.Frame(master=window, width=360, height=400, background="white")
body_frm.pack()

date_lbl = ttk.Label(master=top_frm, text="Date", font=("Helvetica", 15, "bold"))
date_lbl.pack()

task_ent = ttk.Entry(master=body_frm, font=("Helvetica", 15))
task_ent.place(x=15, y=20, height=39, width=290)


# Add task Button
image = Image.open("todoapp\\add.png")
add_image_resize = image.resize((30, 34))
add_icon = ImageTk.PhotoImage(add_image_resize)
add_btn = tk.Button(master=body_frm, image=add_icon, command=add_task, borderwidth=1, cursor="hand2", background="yellow")
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