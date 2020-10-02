import tkinter as tk
from tkinter.ttk import *
#from PIL import ImageTK,Image


#tkinter stuff
menu = tk.Tk()
menu.title("Going the Distance")
menu.geometry("800x500")

#background stuff
backgroundIMG = tk.PhotoImage(file = "Menu Art.png")
Lbackground = tk.Label(menu, image = backgroundIMG)
Lbackground.place(x=0, y=0, relwidth = 1, relheight=1)

#events
def close_program():
    menu.destroy()

def controls_window():
    Controls = tk.Toplevel(menu)
    Controls.title("Controls")
    Controls.geometry("500x500")
    ControlsIMG = tk.PhotoImage(file = "Control Scheme.png")
    LControls = tk.Label(Controls, image = ControlsIMG)
    LControls.place(x=0, y=0, relwidth = 1, relheight=1)
    Controls.mainloop()

def Start_Game():
    Main()#game loop thing

#Buttons
Bstart_game = tk.Button(menu, text = "Start Game", width = 25 , height = 5, command = Start_Game)
Bstart_game.grid(row = 0, column = 1, padx = 10, pady = 10)

Bcontrols = tk.Button(menu, text = "Controls", width = 25, height = 5, command = controls_window)
Bcontrols.grid(row = 1, column = 1, padx = 10, pady = 10)

Bleaderboard = tk.Button(menu, text = "Leaderboard", width = 25, height = 5)
Bleaderboard.grid(row = 2, column = 1, padx = 10, pady = 10)

Bquit = tk.Button(menu, text = "Quit", width = 25, height = 5, command = close_program)
Bquit.grid(row = 3, column = 1, padx = 10, pady = 10)

menu.mainloop()
