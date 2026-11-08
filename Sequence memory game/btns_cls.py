import tkinter

# Global list for the configuration buttons
btns = []


class btn_start():
    '''A class function for a start button'''
    def __init__(self, board, txt, g, notxt, link):
        '''Self method'''
        self.b = board
        self.t = txt
        self.g = g
        self.no = notxt
        self.l = link
        # Create the start button
        self.btn = tkinter.Button(self.b, text=self.t, height = 2, command=self.c)
        self.btn.pack()
    
    def c(self):
        '''The command function'''
        # Destroy itself, the linked text widget and buttons from the list
        self.no.destroy()
        self.btn.destroy()
        if len(self.l) != 0:
            for btn in self.l:
                btn.destroy()
        # Create the configuration buttons
        self.b1 = btn_level(self.b, "2x2", 2, self.g)
        self.b2 = btn_level(self.b, "3x3", 3, self.g)
        self.b3 = btn_level(self.b, "4x4", 4, self.g)
        self.b4 = btn_level(self.b, "5x5", 5, self.g)
        self.b5 = btn_level(self.b, "6x6", 6, self.g)

        btns.extend([self.b1, self.b2, self.b3, self.b4, self.b5])

class btn_level():
    '''A class function for the configuration buttons'''
    def __init__(self, board, txt, n, g):
        '''Self method'''
        self.b = board
        self.n = n
        self.g = g
        # Create a variable for if the button is clicked
        self.click = False
        # Create the confuguration button
        self.btn = tkinter.Button(self.b, text=txt, height=5, width=30, bg = "#FEF6F7", font=('Times', '12'), command=self.c)
        self.btn.pack()
    
    def destroy(self):
        '''The destroy function to destroy the button itself'''
        self.btn.destroy()

    def c(self):
        '''The command function'''
        # The button is clicked, destroy the button itself
        self.click = True
        self.destroy()
        # Delete the other configuration buttons in the global list
        for btn in btns:
            if not btn.clicked():
                btn.destroy()
        # Initiate the game to start with the configuration of the button
        self.g(self.b, self.n).start()
    
    def clicked(self):
        return self.click