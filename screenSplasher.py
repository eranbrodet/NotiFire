from Tkinter import Tk, Frame, Label  # Elements
from Tkinter import TOP, BOTH, YES, CENTER  # Properties
from logger import logger

class splash(object):
    DEFAULT_TIMEOUT = 1500

    @classmethod
    def success(cls, text, timeout_ms=DEFAULT_TIMEOUT):
        logger.debug("Success splash: " + text)
        cls.show(text, background="#0a0", timeout_ms=timeout_ms, font_size=50)

    @classmethod
    def info(cls, text, timeout_ms=DEFAULT_TIMEOUT):
        logger.debug("Info splash: " + text)
        cls.show(text, background="#5bf", timeout_ms=timeout_ms)

    @classmethod
    def warning(cls, text, timeout_ms=DEFAULT_TIMEOUT):
        logger.debug("Warning splash: " + text)
        cls.show(text, background="#aa0", timeout_ms=timeout_ms, font_size=50)

    @classmethod
    def error(cls, text, timeout_ms=DEFAULT_TIMEOUT):
        logger.debug("Error splash: " + text)
        cls.show(text, background="#a00", timeout_ms=timeout_ms, font_size=50)

    @staticmethod
    def show(text, background="#fff", timeout_ms=DEFAULT_TIMEOUT, font_size=100):
        root = Tk()
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
        label = Label(frame, text=text, wraplength=screen_width * 0.8)
        label.pack(side=TOP, expand=YES)
        label.config(bg=background, justify=CENTER, font=("calibri", font_size))
        # Set transparency
        root.wait_visibility(root)  # Needed for linux (and must come after overrideredirect)
        root.attributes('-alpha', 0.6)
        # Run Event loop
        root.mainloop()


def unit_test():
    from random import randint
    rand_hex = "#%06x" % randint(0, 0xFFFFFF)
    logger.debug("Trying out " + rand_hex)
    splash.show("Your name here", rand_hex)
    splash.success("success")
    splash.info("info")
    splash.warning("warning")
    splash.error("error")


if __name__ == '__main__':
    unit_test()
