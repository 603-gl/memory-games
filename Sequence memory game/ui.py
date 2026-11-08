import tkinter

from game import *
from btns_cls import *

BOARD = tkinter.Tk()
BOARD.geometry("1000x1000")
BOARD["bg"] = "#fff49b"
BOARD.title("MEMORY GAME")

welcome = tkinter.Text(BOARD, bg = "#fffee0", height = 30, width = 90, font=('Times', '15', 'bold'))
welcome.tag_configure("center", justify="center")
welcome.insert("1.0", '''Welcome to the Memory Game!\n
Choose the game configuration that you want (2,3,4,5 or 6).\n
Memorize the number sequence pattern on the board.\n
When you're ready, click the numbers in order (the numbers will disapear as soon as your first click\n
or after 10 seconds).
               ''')
welcome.tag_add("center", "1.0", "end")
welcome.pack()

btn_start(BOARD, "Start Game", game, welcome, [])


BOARD.mainloop()