from tkinter import *

window = Tk()
window.title("Sports Merchandise Application")
window.geometry('350x200')
btn = Button(window, text="Click me")
btn.grid(column=1, row=0)

def add_game():
