from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import subprocess
import tkinter as tk
import sys
 
 
# create an instance for window
window = Tk()
window.geometry("500x750+200+100")

#set icon
window.iconbitmap('startipy.ico')

# set title for window
window.title("StartiPy")

# create and configure menu
menu = Menu(window)
window.config(menu=menu)

# create editor window for writing code 
editor = ScrolledText(window, font=("Ebrima 13"), wrap=None, undo=True, autoseparators=True, fg="black", bg="#ecedee")
editor.pack(fill=BOTH, expand=1)
editor.focus()
file_path = ""
code = ""

# temporary container for code comparison
codeTemp = ""

# default theme
theme = "light"

# function to create new file
def new_file(event=None):
    global codeTemp, file_path
    if len(editor.get('1.0', END))==1:
        try:
            path = asksaveasfilename(filetypes=[('Python Files', '*.py')], defaultextension = '.py') 
            open(path, 'w')
            file_path = path
            editor.delete('1.0', END)
            codeTemp = editor.get('1.0', END)
        except:
            return
    if editor.get('1.0', END)!=codeTemp:
        if file_path == '':
            saveMsg = messagebox.askyesno(title="File has been edited.", message="Save file?")
            if int(saveMsg) == 1:
                save_file()
    try:
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')], defaultextension = '.py') 
        open(path, 'w')
        file_path = path
        editor.delete('1.0', END)
        codeTemp = editor.get('1.0', END)
    except:
        return
window.bind("<Control-n>", new_file)

# function to open files
def open_file(event=None):
    global code, file_path, codeTemp
    open_path = askopenfilename(filetypes=[("Python File", "*.py")])
    file_path = open_path
    with open(open_path, "r") as file:
        code = file.read()
        editor.delete(1.0, END)
        editor.insert(1.0, code)
        codeTemp = editor.get('1.0', END)
window.bind("<Control-o>", open_file)

# function to save files
def save_file(event=None):
    global code, file_path, codeTemp
    if file_path == '':
        save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py")])
        file_path = save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)
        codeTemp = editor.get('1.0', END)
        return
window.bind("<Control-s>", save_file)

# function to save files as specific name 
def save_as(event=None):
    global code, file_path, codeTemp
    save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py")])
    file_path = save_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code)
        codeTemp = editor.get('1.0', END)
        return
window.bind("<Control-S>", save_as)

# clear the previous text from
# output_windows
def clearCode(event=None):
    output_window.delete(1.0, END)
    
# function to execute the code and
# display its output
def run(event=None):
    global code, file_path, codeTemp
    cmd = f"python {file_path}"
    if len(editor.get('1.0', END))==1:
        messagebox.showinfo(title="StartiPy", message="File is Empty.")
        return      
    if file_path == '' or (editor.get('1.0', END)!=codeTemp):
        saveMsg = messagebox.askokcancel(title="Please save the file first.", message="Save file?")
        if int(saveMsg) == 1:
            codeTemp = editor.get('1.0', END)
            save_file()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    output, error =  process.communicate()
    
    # delete the previous text from
    # output_windows
    #output_window.delete(1.0, END)
    
    # insert the new output text in
    # output_windows
    output_window.insert(1.0, output)
    
    # insert the error text in output_windows
    # if there is error
    if len(error)>3:
        output_window.config(fg="red")
    else:
        exec(str(theme)+"()")
    output_window.insert(1.0, error)
window.bind("<F5>", run)

# function to close IDE window
def close(event=None):
    window.destroy()
window.bind("<Control-q>", close)
# define function to cut 
# the selected text

def cut_text(event=None):
        editor.event_generate(("<<Cut>>"))
        
# define function to copy 
# the selected text
def copy_text(event=None):
        editor.event_generate(("<<Copy>>"))
        
# define function to paste 
# the previously copied text
def paste_text(event=None):
        editor.event_generate(("<<Paste>>"))
     
# create menus
file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
view_menu = Menu(menu, tearoff=0)
theme_menu = Menu(menu, tearoff=0)
feature_menu = Menu(menu, tearoff=0)

# add menu labels
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label ="View", menu=view_menu)
menu.add_cascade(label ="Theme", menu=theme_menu)
menu.add_cascade(label ="FEATURES", font=("helvetica 12 bold"), menu=feature_menu)

# add commands in file menu
file_menu.add_command(label='New File', accelerator="Ctrl+N", command = new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)

# add commands in edit menu
edit_menu.add_command(label="Cut", command=cut_text) 
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
run_menu.add_command(label="Run", accelerator="F5", command=run)

#for calling out code block from code
def callBlocks(name):
    blocks = ""
    with open(name+'.txt') as f:
        blocks = f.read()
    editor.insert(1.0, blocks)

# functions for code snippets and blocks
def cSnippets():
    #primary window for snippets
    sWindow = Toplevel(window)
    sWindow.title("Code Snippets")
    sWindow.iconbitmap('startipy.ico')
    sWindow.geometry("300x600+250+150")
    return

def cBlocks():
    #primary window for blocks
    bWindow = Toplevel(window)
    bWindow.title("Code Blocks")
    bWindow.iconbitmap('startipy.ico')
    bWindow.geometry("300x600+250+150")
    #blockBtn = Button(bWindow, text="smetsjlk", command=lambda: callBlocks("blocks"))
    #blockBtn.pack()
    return

# add commands in feature menu
feature_menu.add_command(label="Code Snippets", font=("helvetica 10 bold"), command=cSnippets) 
feature_menu.add_command(label="Code Blocks", font=("helvetica 10 bold"), command=cBlocks)

# function to display and hide status bar
show_status_bar = BooleanVar()
show_status_bar.set(True)
def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar = False 
    else :
        status_bars.pack(side=BOTTOM)
        show_status_bar = True
        
view_menu.add_checkbutton(label = "Status Bar" , onvalue = True, offvalue = 0,variable = show_status_bar , command = hide_statusbar)

# create a label for status bar
status_bars = ttk.Label(window,text = "lines: 0")
status_bars.pack(side = BOTTOM, anchor=E)

# function to display count and word characters
text_change = False
def change_word(event = None):
    global text_change
    if editor.edit_modified():
        text_change = True
        lines = int(editor.index('end').split('.')[0])-1
        status_bars.config(text = f"lines: {lines}")
    editor.edit_modified(False)
editor.bind("<<Modified>>",change_word)

# function for light mode window
def light():
    global theme
    theme = "light"
    editor.config(fg="black", bg="#ecedee")
    output_window.config(fg="black", bg="white")
    
# function for dark mode window
def dark():
    global theme
    theme = "dark"
    editor.config(fg="white", bg="#192734")
    output_window.config(fg="white", bg="#15202b")
    
# add commands to change themes
theme_menu.add_command(label="light", command=light)
theme_menu.add_command(label="dark", command=dark)

# run button
run_btn = Button(window, text="Run", height=1,relief=RIDGE, bd=0, bg="green", fg="white", activebackground="light green", activeforeground="black", font="Helvetica", command=run)
run_btn.pack(fill=BOTH, expand=0)

# clear button
clr_btn = Button(window, text="Clear", height=1,relief=RIDGE, bd=0, bg="yellow", fg="black", activebackground="light green", activeforeground="black", font="Helvetica", command=clearCode)
clr_btn.pack(fill=BOTH, expand=0)

# create output window to display output of written code
output_window = ScrolledText(window, font="12", height=10, fg="black", bg="white")
output_window.pack(fill=BOTH, expand=1)
window.mainloop()
