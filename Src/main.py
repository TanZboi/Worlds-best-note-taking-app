from tkinter import *
from tkinter.colorchooser import askcolor

import customtkinter
import customtkinter as ct
import psutil as psutil


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    STARTING_BGCOLOUR = 'white'

    def __init__(self):

        self.root = customtkinter.CTk()
        self.root.title('Paint')

        self.file_button = customtkinter.CTkButton(self.root, text='New Page', command=self.file)
        self.file_button.grid(row=0, column=0)

        self.pen_button = customtkinter.CTkButton(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=1)

        self.brush_button = customtkinter.CTkButton(self.root, text='Dark Mode', command=self.set_dark)
        self.brush_button.grid(row=0, column=2)

        self.brush_button = customtkinter.CTkButton(self.root, text='Light Mode', command=self.set_light)
        self.brush_button.grid(row=1, column=2)

        self.color_button = customtkinter.CTkButton(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=3)

        self.eraser_button = customtkinter.CTkButton(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=4)

        self.clear_button = customtkinter.CTkButton(self.root, text='Clear', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=5)

        #create label
        self.positionlabel = customtkinter.CTkLabel(self.root, text='MousePosition: ')
        self.positionlabel.grid(row=1, column=0)

        self.colourlabel = customtkinter.CTkLabel(self.root, text='Current Colour: ')
        self.colourlabel.grid(row=1, column=3)

        self.thicknesslabel = customtkinter.CTkLabel(self.root, text='Thickness: ')
        self.thicknesslabel.grid(row=1, column=1)

        self.choose_size_button = customtkinter.CTkSlider(self.root, from_=1, to=30)
        self.choose_size_button.grid(row=0, column=6)

        self.eraserstatuslabel = customtkinter.CTkLabel(self.root, text='Eraser: ')
        self.eraserstatuslabel.grid(row=1, column=4)

        self.numberofpointsdrawnlabel = customtkinter.CTkLabel(self.root, text='Number of points drawn: ')
        self.numberofpointsdrawnlabel.grid(row=1, column=5)

        self.numberofpointsdrawnlabel = customtkinter.CTkLabel(self.root, text='Number of points drawn: ')
        self.numberofpointsdrawnlabel.grid(row=1, column=5)

        self.ramusagelabel = customtkinter.CTkLabel(self.root, text='Ram Usage: ')
        self.ramusagelabel.grid(row=1, column=6)

        self.c = Canvas(self.root, bg='white', width=1280, height=720)
        self.c.grid(row=2, columnspan=7)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.stroke_num = 0
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.bgcolour = self.STARTING_BGCOLOUR
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        #set label to 'Nothing drawn yet'
        self.positionlabel.configure(text='Nothing drawn yet')

    def use_pen(self):
        self.color = 'black'
        self.eraser_on = False

    def set_dark(self):
        self.c.configure(bg='black')
        self.color = 'white'
        #redraw all lines in white
        for item in self.c.find_all():
            self.c.itemconfig(item, fill='white')

    def set_light(self):
        self.c.configure(bg='white')
        self.color = 'black'
        for item in self.c.find_all():
            self.c.itemconfig(item, fill='black')

    def file(self):
        if __name__ == '__main__':
            Paint()

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.eraserstatuslabel.configure(text='Eraser: On')
        self.eraser_on = True

    def erase(self, event):
        overlapping = self.c.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        for item in overlapping:
            tags = self.c.gettags(item)
            lines = self.c.find_all()
            for line in lines:
                if self.c.gettags(line)[0] == tags[0]:
                    self.c.delete(line)
                    

    def paint(self, event):
        if self.eraser_on:
            self.erase(event)
            return
        self.line_width = self.choose_size_button.get()
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36, tags=f"{self.stroke_num}")
        self.old_x = event.x
        self.old_y = event.y
        print(self.old_x, self.old_y)

        #set label to mouse position
        self.positionlabel.configure(text='MousePosition: ' + str(self.old_x) + ', ' + str(self.old_y))

        #set label to colour
        self.colourlabel.configure(text='Current Colour: ' + str(self.color))

        #set label to thickness
        self.thicknesslabel.configure(text='Thickness: ' + str(self.line_width) + "px")

        #set label to eraser status
        self.eraserstatuslabel.configure(text='Eraser: ' + 'On' if self.eraser_on else 'Off')

        #set label to number of points drawn
        self.numberofpointsdrawnlabel.configure(text='Number of points drawn: ' + str(len(self.c.find_all())))

        self.ramusagelabel.configure(text='Ram Usage: ' + str(psutil.virtual_memory().percent) + '% of ' + str((psutil.virtual_memory().total)/(1024*1024)) + 'MB')

    def clear_canvas(self):
        self.c.delete(ALL)
        #set label of number of points drawn to 0
        self.numberofpointsdrawnlabel.configure(text='Number of lines drawn: 0')

    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.stroke_num += 1


if __name__ == '__main__':
    Paint()
