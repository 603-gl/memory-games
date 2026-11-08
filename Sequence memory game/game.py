import tkinter
import random
import time
import sys

from btns_cls import *

class game():
    HEIGHT = 750
    WIDTH = 750
    BG = "#fffee0"
    FONT = ('Times', '50', 'bold')

    MEMO = 0
    PLAY = 1

    DELAY = 500

    def __init__(self, board, n):
        '''Initialize the constants with board and columns/rows'''
        self.BOARD = board
        self.ROWS = n
        self.COLUMNS = n
        self.PIXELS_BY_SQUARE = (self.HEIGHT//self.ROWS)
    
    def start(self):
        '''Start the game'''
        # Create the canva and button
        self.canva = tkinter.Canvas(self.BOARD, width = self.WIDTH, height = self.HEIGHT, bg = self.BG)
        self.canva.pack()

        self.quit = tkinter.Button(self.BOARD, text="Quit", command=self.on_quit)
        self.quit.pack()

        # Create hint button
        self.hint = tkinter.Button(self.BOARD, text="Hints (3)", command=self.hints)
        self.hint.pack()
        self.hint_counts = 0

        self.canva.bind("<Button-1>", func=lambda event: self.on_click(event))

        # Create a list of each rectangle ID
        self.rectangles = []
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                x = col * self.PIXELS_BY_SQUARE
                y = row * self.PIXELS_BY_SQUARE
                idr = self.canva.create_rectangle(x+1, y+1, x+self.PIXELS_BY_SQUARE-1, y+self.PIXELS_BY_SQUARE-1, fill = self.BG)
                self.rectangles.append(idr)
        
        # Create a dictionary associating each square with it's coordinate bounds
        self.rect_bounds = {}
        for i in range(1, (self.ROWS * self.COLUMNS) +1):
            self.rect_bounds[i] = self.square(i)

        # Start the timer handler.
        self.auto = self.BOARD.after(self.DELAY, self.on_timer) 
        self.counter = 0

        self.state = self.MEMO
        self.new_game()

    def square(self, sqr):
        '''Convert a square position to it's canva coordinates'''
        # Create a list matrix, containing lists of rows
        self.ROWS_LST = []
        row = 0 # None
        col = 0 # None
        count = 0
        temp_lst = []
        for i in range(1, (self.ROWS * self.COLUMNS)+1):
            count += 1
            if count != self.COLUMNS:
                temp_lst.append(i)
            else:
                temp_lst.append(i)
                self.ROWS_LST.append(temp_lst)
                temp_lst = []
                count = 0
        # Get the row and column of the respective square
        for i in self.ROWS_LST:
            if sqr in i:
                row = self.ROWS_LST.index(i) + 1
                col = i.index(sqr) + 1
        # Convert the square into bound coordinates on the canva
        n = (self.HEIGHT // self.ROWS)
        x = (n*(col-1), n*col)
        y = (n*(row-1), n*row)
        return x, y
    
    def new_game(self):
        '''Initialize a new game with level 1 values'''
        self.state = self.MEMO
        # Number Sequence to Memorize
        self.NUMBER_SEQUENCE = [1]
        # Index to keep track of the correct clicks
        self.INDEX = 0
        # Initialize the board title
        self.BOARD.title('LEVEL:' + str(len(self.NUMBER_SEQUENCE)))
        # Clean the Square IDs and Pattern memory
        self.IDS = {}
        self.PATTERN = {}
        # Begin memorization
        self.memo()

    def memo(self):
        '''Initialize memorization board'''
        self.state = self.MEMO
        squares = self.ROWS * self.COLUMNS
        self.associate = {}
        # For each number in the number sequence, associate it with a random square on the board
        for i in self.NUMBER_SEQUENCE:
            r = random.randint(1, squares)
            while r in self.associate.values():
                r = random.randint(1, squares)
            # Key = number, Value = Square position
            self.associate[i] = r
        # Convert each number, square pair to show the number on the board
        for key in self.associate:
            self.num_to_pixel(key, self.associate[key])

    def num_to_pixel(self, num, sqr):
        '''Show each number of the number sequence on the canva board, according to their randomized square position'''
        # Get the bound coordinates of the square
        bounds = self.rect_bounds[sqr]
        # Get the center coordinates of the square
        x = round((bounds[0][0] + bounds[0][1]) / 2)
        y = round((bounds[1][0] + bounds[1][1]) / 2)
        # Create the text number on the screen
        id = self.canva.create_text(x, y, text=str(num), font=self.FONT)
        # Save into dictionary, Key = ID of the number text, Value = Number
        self.IDS[id] = num
        # Save into dictionary, Key = Number, Value = Square bound coordinates
        self.PATTERN[num] = bounds


    def on_click(self, event):
        '''Handle a left-click of the mouse'''
        self.state = self.PLAY
        self.counter = 0
        # For every ID of number saved, hide it from the user
        for i in self.IDS:
            self.canva.itemconfig(i, state=tkinter.HIDDEN)
            self.canva.update()
        # Get the coordinates of the mouse-click of the user
        x = self.canva.canvasx(event.x)
        y = self.canva.canvasy(event.y)

        # Check if the click is within the canva
        valid = False
        temp_ind = 0 # None
        i_num = 0 # None
        if x in range(0, 751) and y in range(0, 751):
            # If it clicked in one of the squares in the pattern
            for sqrs in self.PATTERN.values(): 
                # Get the square bounds and the number that it clicked
                if x in range(sqrs[0][0], sqrs[0][1]+1) and y in range(sqrs[1][0], sqrs[1][1]+1): 
                    temp_ind = list(self.PATTERN.values()).index(sqrs) 
                    i_num = list(self.PATTERN.keys())[temp_ind] 
                    valid = True
            # If it didn't click one of the squares in the pattern
            if not valid: 
                self.red_flash(x,y)
                print("YOU LOSE")
                # Delete any create number text
                if len(self.IDS) != 0:
                    for i in self.IDS:
                        self.canva.delete(i) 
                self.new_game()
        # It it clicked outside of the canva
        if not valid: 
            return
        # If the number associated is the right number to the pattern
        if self.NUMBER_SEQUENCE[self.INDEX] == i_num: 
                self.green_flash(i_num)
                # Add to the count of correct clicks
                self.INDEX += 1 
                # If the length of the number sequence is equal to the number of correct clicks
                if len(self.NUMBER_SEQUENCE) == self.INDEX: 
                    # If length is total number of squares
                    if len(self.NUMBER_SEQUENCE) == (self.ROWS * self.COLUMNS): 
                        # The game is finished, they won
                        self.BOARD.title("MEMORY GAME")
                        self.canva.destroy()
                        self.quit.destroy()
                        self.hint.destroy()
                        # Create tkinter note
                        note = tkinter.Text(self.BOARD, bg = "#fffee0", height = 9, width = 30, font=('Times', '15'))
                        note.tag_configure("center", justify="center")
                        note.insert("1.0",'''Congratulations, you won!''')
                        note.tag_add("center", "1.0", "end")
                        note.pack()
                        leave = tkinter.Button(self.BOARD, text="Leave Game", height=2, command=self.on_quit)
                        leave.pack()
                        again = btn_start(self.BOARD, "Play Again", game, note, [leave])

                    # Continue onto the next level
                    else:
                        # Delete the old pattern
                        if len(self.IDS) != 0:
                            for i in self.IDS:
                                self.canva.delete(i) 
                        # Initialize new level
                        self.INDEX = 0 
                        # Add the consecutive number to the number sequence
                        recall_num = self.NUMBER_SEQUENCE[-1] 
                        self.NUMBER_SEQUENCE.append(recall_num + 1) 
                        self.BOARD.title('LEVEL:' + str(len(self.NUMBER_SEQUENCE))) 
                        self.IDS = {}
                        self.PATTERN = {}
                        self.memo()
        # They clicked a number in the pattern, but not the right one
        else:
            self.red_flash(x,y)
            print("YOU LOSE")
            if len(self.IDS) != 0:
                for i in self.IDS:
                    self.canva.delete(i)
            self.new_game()
    
    def green_flash(self, num):
        '''Green flash on good click'''
        sqr = self.associate[num]
        rec_id = self.rectangles[sqr-1]
        self.canva.itemconfig(rec_id, fill = "#e6f8d1")
        self.canva.update()
        time.sleep(0.1)
        # Revert to the standard color.
        self.canva.itemconfig(rec_id, fill = self.BG)
        self.canva.update()
    
    def red_flash(self, x_c, y_c):
        '''Red flash on wrong click'''
        ind = 0 # None
        for bound in self.rect_bounds.values():
            if (x_c in range(bound[0][0], bound[0][1] +1)) and (y_c in range(bound[1][0], bound[1][1] +1)):
                ind = list(self.rect_bounds.values()).index(bound)
        sqr = list(self.rect_bounds.keys())[ind]
        rec_id = self.rectangles[sqr-1]
        self.canva.itemconfig(rec_id, fill = "#febdb9")
        self.canva.update()
        time.sleep(0.1)
        # Revert to the standard color.
        self.canva.itemconfig(rec_id, fill = self.BG)
        self.canva.update()
    
    
    def hints(self):
        '''Provide hints to the user'''
        if self.state == self.PLAY:
            self.hint_counts += 1
            if self.hint_counts + 1 <= 3:
                string = "Hints (" + str(3-self.hint_counts) + ')'
                self.hint.config(text=string)
                for i in self.IDS:
                    self.canva.itemconfig(i, state=tkinter.NORMAL)
                    self.canva.update()
                time.sleep(0.3)
                for i in self.IDS:
                    self.canva.itemconfig(i, state=tkinter.HIDDEN)
                    self.canva.update()
            else:
                self.hint.config(state="disabled")
                self.hint.config(text="Hints (0)")
                for i in self.IDS:
                    self.canva.itemconfig(i, state=tkinter.NORMAL)
                    self.canva.update()
                time.sleep(0.3)
                for i in self.IDS:
                    self.canva.itemconfig(i, state=tkinter.HIDDEN)
                    self.canva.update()     

    def on_timer(self):
        '''This method is used to handle a timer event. It counts up to 10 seconds for the memorization.'''
        if self.counter == 20:
            self.counter = 0
            # self.PLAY state, as if the user left-clicked
            self.state = self.PLAY
            # For every ID of number saved, hide it from the user
            for i in self.IDS:
                self.canva.itemconfig(i, state=tkinter.HIDDEN)
                self.canva.update()

        elif self.state == self.MEMO:
            self.counter += 1 # add one to the count of every half-seconds
        
        self.auto = self.BOARD.after(self.DELAY, self.on_timer)

    def on_quit(self): 
        '''Handle a right click from the mouse.'''
        sys.exit()
