from tkinter import *
root = Tk()
root.title('Hover Test')
root.geometry('400x400')

def button_hover(event, text):
    status_label.config(text=text)
def button_leave(event,text):
    status_label.config(text=text)  # Clear the status label when the mouse leaves the button


my_button = Button(root, text='Button', font=('Arial', 14), bg='lightblue', fg='black')
my_button.pack(pady=20)
status_label = Label(root, text='', bd=1, relief=SUNKEN, anchor=E)
status_label.pack(side=BOTTOM, fill=X, pady=5)
my_button.bind("<Enter>", lambda event: button_hover(event,'Button Hovered!'))
my_button.bind("<Leave>", lambda event: button_leave(event,'Button Left!'))

my_button2 = Button(root, text='Button', font=('Arial', 14), bg='lightblue', fg='black')
my_button2.pack(pady=20)
my_button2.bind("<Enter>", lambda event: button_hover(event,'Button2 Hovered!'))
my_button2.bind("<Leave>", lambda event: button_leave(event,'Button2 Left!'))

root.mainloop()

