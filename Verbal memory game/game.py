# Import Module
import tkinter as tk
from tkinter import ttk
from gamefunc import *
from widget_class import *
import sys
import random

# create root window
root = tk.Tk()

# root window title and dimension
root.title("Verbal memory game")
# Set geometry (widthxheight)
root.geometry('900x900')
# Set window to be un-resizable
root.resizable(False, False)

# Global variables
language = tk.Label(root, text="Language setting", font=("Arial", 16, "bold italic"))
# language checkboxes
en = tk.IntVar()
fr= tk.IntVar()
es = tk.IntVar()

en_check = tk.Checkbutton(root, text="English", variable=en, onvalue=1, offvalue=0)
fr_check = tk.Checkbutton(root, text="French", variable=fr, onvalue=1, offvalue=0)
es_check = tk.Checkbutton(root, text="Spanish", variable=es, onvalue=1, offvalue=0)

mode = tk.Label(root, text="Game mode", font=("Arial", 16, "bold italic"))
w_number = tk.IntVar()
word_count = tk.Label(root, text="Number of words")
w_slider = tk.Scale(root, from_=1, to=6, orient=tk.HORIZONTAL, showvalue=1, variable=w_number, resolution=1)
r_number = tk.IntVar()
round_count = tk.Label(root, text="Number of rounds")
r_slider = tk.Scale(root, from_=1, to=6, orient=tk.HORIZONTAL, showvalue=1, variable=r_number, resolution=1)
difficulty = tk.Label(root, text="Difficulty mode", font=("Arial", 16, "bold italic"))
diffvar = tk.StringVar()
diff1 = tk.Radiobutton(root, text="Easy", variable=diffvar, value="Easy")
diff2 = tk.Radiobutton(root, text="Medium", variable=diffvar, value="Medium")
diff3 = tk.Radiobutton(root, text="Hard", variable=diffvar, value="Hard")

# start button
def start_game():
    w_number = w_slider.get()
    r_number = r_slider.get()
    if (en.get()+fr.get()+es.get() == 0):
        print("Choose at least one language")
    else:
        # get rid of labels
        language.place_forget()
        en_check.place_forget()
        fr_check.place_forget()
        es_check.place_forget()
        mode.place_forget()
        word_count.place_forget()
        w_slider.place_forget()
        round_count.place_forget()
        r_slider.place_forget()
        difficulty.place_forget()
        diff1.place_forget()
        diff2.place_forget()
        diff3.place_forget()

        start_btn.place_forget()
        # start game
        g = game(root, en, fr, es, w_number, r_number, diffvar)
        g.start()

start_btn = tk.Button(root, text="Start game", command=start_game)


def main_page():
    # main page display 
    # language setting
    language.place(relx = 0.1, rely = 0.3)

    en_check.place(relx = 0.1, rely = 0.35)
    en_check.select() # default selection
    fr_check.place(relx = 0.1, rely = 0.40)
    es_check.place(relx = 0.1, rely = 0.45)

    # game setting
    mode.place(relx = 0.42, rely = 0.3)

    word_count.place(relx=.42, rely = 0.35)
    w_slider.place(relx=0.42, rely=0.4)

    round_count.place(relx=.42, rely = 0.45)
    r_slider.place(relx=0.42, rely=0.5)

    difficulty.place(relx =0.7, rely=0.3 )
    diff1.place(relx=0.7, rely=0.35)
    diff2.place(relx=0.7, rely=0.4)
    diff3.place(relx=0.7, rely=0.45)
    diffvar.set("Easy")

    start_btn.place(relx=0.45, rely=0.7)

########################## GAME ##########################
class game():
    BG = "#8a9cbd"
    FONT = ('')

    MEMO = 0
    PLAY = 1

    def __init__(self, board, en, fr, es, word, round, diff):
        # Basics
        self.BOARD = board
        self.en = en
        self.fr = fr
        self.es = es
        self.word = word
        self.round = round
        self.diff = diff
        self.lang = self.en.get()+self.fr.get()+self.es.get()

        # Widgets
        self.gamestart = tk.Label(self.BOARD, text="Round 1", font=("Arial", 16, "bold italic"))
        self.congratulations = tk.Label(self.BOARD, text="Congratulations!", font=("Arial", 16, "bold italic"))
        self.memorize  = tk.Label(self.BOARD, text="-Memorize-", font=("Arial", 16, "bold"))
        self.lg = tk.Button(self.BOARD, text="Leave game", command=self.on_quit)
        self.pa = tk.Button(self.BOARD, text="Play again", command=self.play_again)
        self.nr = tk.Button(self.BOARD, text="Next round", command=self.new_game)
        self.ok = tk.Button(self.BOARD, text="Ok", command=self.okd)

        # Grid for words
        if self.word >= 3:
            if self.word == 4:
                self.COLUMNS = 2
            else:
                self.COLUMNS = 3
        else:
            self.COLUMNS = self.word

        if self.word > 3:
            self.ROWS = 2
        else:
            self.ROWS = 1

        self.WIDTH = 200*self.COLUMNS
        self.HEIGHT = 35*(self.lang)*self.ROWS

        self.PIXELS_BY_HEIGHT = (self.HEIGHT//self.ROWS)
        self.PIXELS_BY_WIDTH = (self.WIDTH//self.COLUMNS)
        
        # Other 
        self.IDS = {}
        
    def start(self):
        # Game title
        self.gamestart.pack(side="top", pady=20)
        self.round_count = 0

        # Game board
        self.canva = tk.Canvas(self.BOARD, width=self.WIDTH, height=self.HEIGHT, highlightthickness=3, highlightbackground=self.BG)
        self.canva.place(relx=0.5, rely=0.5, anchor="center")
        # Rectangles and mini-rectangles
        self.rectangles_classes = []
        self.rectangles_words = []
        self.rectangles_words_bounds = {}
        if self.word != 5:
            for row in range(self.ROWS):
                for col in range(self.COLUMNS):
                    x = col * self.PIXELS_BY_WIDTH
                    y = row * self.PIXELS_BY_HEIGHT
                    idr = self.canva.create_rectangle(x+1, y+1, x+self.PIXELS_BY_WIDTH-1, y+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
                    self.rectangles_classes.append(idr)
                    if self.lang > 1:
                        for mini_row in range(self.lang):
                            d = mini_row * 35
                            idrw = self.canva.create_rectangle(x+11, y+d+5, x+self.PIXELS_BY_WIDTH-10, y+d+35-5)
                            self.rectangles_words.append(idrw)
                            self.rectangles_words_bounds[idrw] = (x+11, y+d+5, x+self.PIXELS_BY_WIDTH-10, y+d+35-5)
                    else:
                        self.rectangles_words.append(idr)
                        self.rectangles_words_bounds[idr] = (x+1, y+1, x+self.PIXELS_BY_WIDTH-1, y+self.PIXELS_BY_HEIGHT-1)
        else:
            def create_mini(idr, x,y):
                if self.lang > 1:
                    for mini_row in range(self.lang):
                        d = mini_row * 35
                        idrw = self.canva.create_rectangle(x+11, y+d+5,x+self.PIXELS_BY_WIDTH-10, y+d+35-5)
                        self.rectangles_words.append(idrw)
                        self.rectangles_words_bounds[idrw] = (x+11, y+d+5, x+self.PIXELS_BY_WIDTH-10, y+d+35-5)
                else:
                    self.rectangles_words.append(idr)
                    self.rectangles_words_bounds[idr] = (x, y, x-1+self.PIXELS_BY_WIDTH-1, y-1+self.PIXELS_BY_HEIGHT-1)
            idr1 = self.canva.create_rectangle(1, 1, 0+self.PIXELS_BY_WIDTH-1, 0+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
            self.rectangles_classes.append(idr1)
            create_mini(idr1, 1, 1)
            idr2 = self.canva.create_rectangle(201, 1, 200+self.PIXELS_BY_WIDTH-1, 0+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
            self.rectangles_classes.append(idr2)
            create_mini(idr2, 201, 1)
            idr3 = self.canva.create_rectangle(401, 1, 400+self.PIXELS_BY_WIDTH-1, 0+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
            self.rectangles_classes.append(idr3)
            create_mini(idr3, 401,1)
            idr4 = self.canva.create_rectangle(100, (35*self.lang)+1, 100+self.PIXELS_BY_WIDTH-1, (35*self.lang)+1+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
            self.rectangles_classes.append(idr4)
            create_mini(idr4, 100,(35*self.lang)+1)
            idr5 = self.canva.create_rectangle(301, (35*self.lang)+1, 301+self.PIXELS_BY_WIDTH-1, (35*self.lang)+1+self.PIXELS_BY_HEIGHT-1, outline="#a8bce0")
            self.rectangles_classes.append(idr5)
            create_mini(idr5, 301,(35*self.lang)+1)

        self.new_game()
        
    def new_game(self):
        self.nr.pack_forget()
        self.state = self.MEMO
        self.round_count += 1
        self.gamestart.config(text="Round "+str(self.round_count))

        # Generate word lists
        if len(self.IDS) != 0:
            for i in self.IDS:
                self.canva.itemconfig(i, state=tk.HIDDEN)
        self.IDS = {}
        self.word_list = generate_problem(self.word, self.en, self.fr, self.es)
        self.word_display(self.word_list, self.rectangles_words_bounds)
        print(self.word_list)
        self.memo()

    def memo(self):
        time_given = memo_time(self.word_list)
        self.memorize.pack(side="bottom", anchor="center", pady=30)
        self.memorize.config(text="-Memorize-")
        '''
        # Memorization-time bar
        self.time_bar = ttk.Progressbar(self.BOARD, orient=tk.HORIZONTAL, length=100, mode="determinate")
        self.time_bar.pack(side="bottom", anchor="center", pady=10)
        # Animate it
        x = 0
        while (x<time_given):
            time.sleep(0.5)
            self.time_bar['value'] += 100/(time_given*2)
            x += 0.5
            self.time_bar.update_idletasks()
        '''
        self.BOARD.after(time_given*1000, self.level_choose)
    
    def word_display(self, words, rectangles):
        # Display words on canva
        flat_words = [item for sublist in words for item in sublist]
        count = 0
        for bounds in rectangles.values():
            x = round((bounds[0] + bounds[2]) / 2)
            y = round((bounds[1] + bounds[3]) / 2)
            id = self.canva.create_text(x, y, text=flat_words[count])
            # Save into dictionary, Key = ID of the number text, Value = Number
            self.IDS[id] = flat_words[count]
            count += 1

    def level_choose(self):
        if self.diff.get() == "Easy":
            self.play_easy()
        elif self.diff.get() == "Medium":
            self.play_easy()
        elif self.diff.get() == "Hard":
            self.play_hard()

    def play_easy(self):
        self.state = self.PLAY
        self.memorize.config(text="-Submit answer-")
        for i in self.IDS:
            self.canva.itemconfig(i, state=tk.HIDDEN)
            self.canva.update()

        # Choices
        flat_choices = [item for sublist in self.word_list for item in sublist]
        if self.diff.get() == "Medium":
            larger_lst = random_add(flat_choices, self.en, self.fr, self.es)
            flat_choices = larger_lst

        print(flat_choices)
        random.shuffle(flat_choices)

        self.CHOICES = {}
        count = 0
        for choice in flat_choices:
            choice_id = tk.Label(self.BOARD, text=choice, height=1)
            index_num = count
            add_x = index_num // 6
            add_y = index_num  % 6
            choice_id.place(relx=0.23+(0.1*add_x), rely=0.1+(0.03*add_y))

            canva_x_top_left = self.canva.winfo_x()
            canva_y_top_left = self.canva.winfo_y()
            canva_x_bottom_right = canva_x_top_left + self.WIDTH
            canva_y_bottom_right = canva_y_top_left + self.HEIGHT

            dragw = drag_widget(choice_id, (0.23+(0.1*add_x), 0.1+(0.03*add_y)), canva_x_top_left, canva_y_top_left, canva_x_bottom_right, canva_y_bottom_right, self.rectangles_words_bounds)
            self.CHOICES[choice_id] = (0.23+(0.1*add_x), 0.1+(0.03*add_y))
            count += 1
        
        self.submit = tk.Button(self.BOARD, text="Submit", command=self.check_ans)
        self.submit.pack(side='bottom',  pady=100)
    
    def play_hard(self):
        self.state = self.PLAY
        self.memorize.config(text="-Submit answer-")
        for i in self.IDS:
            self.canva.itemconfig(i, state=tk.HIDDEN)
            self.canva.update()
        # self.time_bar.destroy()

        self.ENTRIES = {}
        for coord in self.rectangles_words_bounds.values():
            var = tk.StringVar()
            entry = tk.Entry(self.BOARD, textvariable = var, justify='center')
            x = round((coord[0] + coord[2]) / 2)
            y = round((coord[1] + coord[3]) / 2)
            wind = self.canva.create_window(x, y, window=entry)
            self.ENTRIES[wind] = [var, (x, y)]

        self.submit = tk.Button(self.BOARD, text="Submit", command=self.check_ans)
        self.submit.pack(side='bottom', anchor='center', pady=100)

    def check_ans(self):
        self.submit.pack_forget()

        valid = True
        count = 0
        flat_answers = [item for sublist in self.word_list for item in sublist]
        verify = [False] * len(flat_answers)

        if (self.diff.get() == "Easy") or (self.diff.get() == "Medium"):
            for input in self.CHOICES:
                x_input = input.winfo_x()
                y_input = input.winfo_y()
                input_text = input.cget("text")
                input.place_forget()
                right_text = ""
                index = 0
                for i,rectangle in enumerate(self.rectangles_words_bounds):
                    bound = self.rectangles_words_bounds[rectangle]
                    if (x_input<= self.canva.winfo_x()+bound[2]) and (self.canva.winfo_x()+bound[0]<=x_input) and (y_input<=self.canva.winfo_y()+bound[3]) and (self.canva.winfo_y()+bound[1]<=y_input):
                        right_text = flat_answers[i]
                        index = i
                if input_text != right_text:
                    if (input_text in flat_answers):
                        valid = False
                else:
                    verify[index] = True

        elif self.diff.get() == "Hard":
            for input in self.ENTRIES:
                self.canva.itemconfig(input, state=tk.HIDDEN)
                if self.ENTRIES[input][0].get() != flat_answers[count]:
                    valid = False
                    verify[count] = (False)
                else:
                    verify[count] = (True)
                count += 1

        if valid:
            if (self.round_count < self.round):
                self.new_game()
            else:
                self.canva.place_forget()
                self.gamestart.pack_forget()
                self.memorize.pack_forget()
                self.congratulations.pack(side="top", pady=20)
                self.pa.place(relx = 0.5, rely=0.45, anchor="center")
                self.lg.place(relx=0.5, rely=0.55, anchor="center")
        else:
            count = 0
            for i in self.IDS:
                if verify[count]:
                    self.canva.itemconfig(i, state=tk.NORMAL, fill="#a2fa3c")
                else:
                    self.canva.itemconfig(i, state=tk.NORMAL, fill="#313331")
                self.canva.update()
                count += 1
            if (self.round_count < self.round):
                self.nr.pack(side='bottom', anchor='center', pady=100)
            else:
                self.ok.pack(side='bottom', anchor='center', pady=100)
                
    def okd(self):
        self.canva.place_forget()
        self.gamestart.pack_forget()
        self.memorize.pack_forget()
        self.ok.pack_forget()
        self.pa.place(relx = 0.5, rely=0.45, anchor="center")
        self.lg.place(relx=0.5, rely=0.55, anchor="center")

    def play_again(self):
        self.congratulations.pack_forget()
        self.pa.place_forget()
        self.lg.place_forget()
        main_page()

    def on_quit(self):
        sys.exit()
        
########################## GAME ##########################

# Execute Tkinter
main_page()
root.mainloop()
