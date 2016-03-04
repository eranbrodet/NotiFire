from Tkinter import Tk, Frame, Label  # Elements
from Tkinter import TOP, BOTH, YES, CENTER  # Properties


class splash(object):
    @staticmethod
    def show(text, background="#fff", timeout_ms=1500):
        root = Tk()
        # Set transparency
        root.wait_visibility(root)  # Needed for linux
        root.attributes('-alpha', 0.5)
        root.attributes("-topmost", True)
        # Set Timeout
        root.after(timeout_ms, root.destroy)
        # Create Frame
        frame = Frame(root)
        frame.pack(side=TOP, fill=BOTH, expand=YES)
        # Set frame size and position
        screen_width = frame.master.winfo_screenwidth()
        screen_heigh = frame.master.winfo_screenheight()
        w = screen_width * 0.8
        h = screen_heigh * 0.6
        # Center the window
        x = (screen_width/2) - (w/2)
        y = (screen_heigh/2) - (h/2)
        frame.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Adjust frame properties
        frame.master.overrideredirect(True)  # Set no border or title
        frame.config(bg=background)
        # Create text label
        label = Label(frame, text=text)
        label.pack(side=TOP, expand=YES)
        label.config(bg=background, justify=CENTER, font=("calibri", 100))
        # Run Event loop
        root.mainloop()


def unit_test():
    from random import randint
    splash.show("Your name here", "#%06x" % randint(0, 0xFFFFFF))

if __name__ == '__main__':
    unit_test()
