import tkinter as tk

class drag_widget():
    def __init__(self, widget, og_pos, c_tlx, c_tly, c_brx, c_bry, rect_bounds):
        self.widget = widget
        self.og_pos = og_pos
        self.startx = 0
        self.starty = 0
        self.widget.bind("<Button-1>", func=lambda event: self.drag_start(event))
        self.widget.bind("<B1-Motion>", func=lambda event: self.drag(event))
        self.widget.bind("<B1-ButtonRelease>", func=lambda event: self.drag_stop(event, self.og_pos, c_tlx, c_tly, c_brx, c_bry, rect_bounds))
        self.widget.configure(cursor="hand1")
    
    def drag_start(self, event):
        self.startx = event.x
        self.starty = event.y

    def drag(self, event):
        x = self.widget.winfo_x() + event.x - self.startx
        y = self.widget.winfo_y() + event.y - self.startx
        self.widget.place(relx=x/900, rely=y/900)

    def drag_stop(self, event, pos, c_tlx, c_tly, c_brx, c_bry, rect_bounds):
        x = self.widget.winfo_x() + event.x - self.startx
        y = self.widget.winfo_y() + event.y - self.startx
        if (c_tlx <= x) and (x<=c_brx) and (c_tly <= y) and (y<=c_bry):
            found = False
            for bounds in rect_bounds.values():
                if (c_tlx+bounds[0]-1 <= x) and (x<=c_tlx+bounds[2]+1) and (c_tly+bounds[1]-2 <= y) and (y<=c_tly+bounds[3]+2):
                    newx = round((c_tlx+bounds[0] + c_tlx+bounds[2]) / 2)
                    newy = round((c_tly+bounds[1] + c_tly+bounds[3]) / 2)
                    found = True
                    self.widget.place(relx=newx/900, rely=newy/900, anchor="center")
            if not found:
                self.widget.place(relx=pos[0], rely=pos[1])
        else:
            self.widget.place(relx=pos[0], rely=pos[1])

'''
try_window = tk.Tk()
label = tk.Label(try_window, bg="blue")
label.place(x=0,y=0)
drag_label = drag_widget(label, (0,0), 0,0,0,0,None)
button = tk.Button(try_window)
button.pack()

try_window.mainloop()
'''