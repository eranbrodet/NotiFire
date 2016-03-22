# -*- coding: utf-8 -*-
from distutils.version import StrictVersion
from functools import partial
from platform import system as which_system
from Tkinter import Tk, Frame, Label, Entry, StringVar, Button  # Elements
from Tkinter import TOP, BOTH, YES, FLAT, SUNKEN  # Properties
from logger import logger
from notiFireDb import NotiFireDb
from screenSplasher import splash

#TODO add systray icon


class FlatButton(Button, object):
    def __init__(self, master, no_bg=False, **kwargs):
        if (not no_bg) and 'bg' not in kwargs:
            kwargs['bg'] = "#ccc"
        kwargs['relief'] = FLAT
        Button.__init__(self, master, **kwargs)


class DraggableFrame(Frame, object):
    """
        Adapted from http://stackoverflow.com/a/7457825/2134702
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.bind('<ButtonPress-1>', self.start_move)
        self.bind('<ButtonRelease-1>', self.stop_move)
        self.bind('<B1-Motion>', self.on_motion)
        self.x = self.y = 0

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        x = (event.x_root - self.x - self.winfo_rootx() + self.winfo_rootx())
        y = (event.y_root - self.y - self.winfo_rooty() + self.winfo_rooty())
        self.master.geometry("+%s+%s" % (x, y))


class UI(object):
    def __init__(self):
        self._root = Tk()
        self._root.title("^ NotiFire ^")
        self._name = StringVar()
        self._is_osx = which_system() == 'Darwin'
        self._version = None

    ##########################################################################
    ####                       Public methods                            #####
    ##########################################################################
    def get_name(self):
        frame = DraggableFrame(self._root)
        frame.pack(side=TOP, fill=BOTH, expand=YES)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(4, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(4, weight=1)

        w = self._set_frame_geo(frame, 0.3, 0.3)[2]
        self._set_x_button(frame, w, self._close_get_name)
        Label(frame, text="Name:").grid(column=1, row=1)
        entry_style = SUNKEN if self._is_osx else FLAT
        entry = Entry(frame, exportselection=0, relief=entry_style, textvariable=self._name)
        entry.grid(column=2, row=1)
        entry.focus_set()
        error_label = Label(frame, fg='red')
        error_label.grid(column=1, row=2, columnspan=3)

        ok_cmd = partial(self._validate_name, error_label)
        FlatButton(frame, text='OK', width=20, font=("calibri", 15),
                   command=ok_cmd).grid(column=1, row=3, columnspan=3)

        self._root.bind('<Return>', ok_cmd)
        self._root.bind('<Escape>', self._close_get_name)
        self._run()
        return self._name.get() if self._name else self._name

    def main_window(self, name, ping_callback):
        self._name.set(name)
        self._ping_callback = ping_callback

        # Create Frame
        self.frame = DraggableFrame(self._root)
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)

        w = self._set_frame_geo(self.frame, 0.5, 0.6)[2]

        self._set_x_button(self.frame, w, self._root.destroy)
        Label(self.frame, text="Name:").place(x=10, y=15)
        Label(self.frame, text=self._name.get(), fg='blue').place(x=80, y=15)
        self._version_label = Label(self.frame, text="Newer version detected, please restart the app", fg='#a00', font=("calibri", 25))

        FlatButton(self.frame, text="Test", width=26, command=self._test_action).place(x=10, y=50)
        FlatButton(self.frame, text='Refresh', width=26, command=self._generate_ping_buttons).place(x=10, y=90)
        self.ping_buttons = []
        self._auto_refresh()
        self._check_version()
        self._run()

    ##########################################################################
    ####                       Private methods                           #####
    ##########################################################################
    def _run(self):
        # Set transparency
        self._root.wait_visibility(self._root)
        self._root.attributes('-alpha', 0.95)
        self._root.lift()
        # Run Event loop
        self._root.mainloop()

    def _close_get_name(self, event=None):
        self._name = None
        self._root.destroy()

    def _set_frame_geo(self, frame, wf, hf):
        # Set frame size and position
        screen_width = frame.master.winfo_screenwidth()
        screen_heigh = frame.master.winfo_screenheight()
        w = screen_width * wf
        h = screen_heigh * hf
        # Center the window
        x = (screen_width/2) - (w/2)
        y = (screen_heigh/2) - (h/2)
        frame.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        if not self._is_osx:
            frame.master.overrideredirect(True)  # Set no border or title
        return x, y, w, h

    def _set_x_button(self, frame, w, callback):
        x_button_x_coordinate = w-30 if self._is_osx else w-20
        FlatButton(frame, text='×', no_bg=True, width=1, font=("calibri", 15), command=callback).place(x=x_button_x_coordinate, y=-10)

    def _validate_name(self, error_label, event=None):
        name = self._name.get()
        if not 0 < len(name) < 25:
            error_label.config(text="Name must be 1-25 chars long")
            logger.error("Invalid name: %s" % (name))
        elif not all(ord(c) < 128 for c in name):
            error_label.config(text="Name must be ascii")
            logger.error("Invalid Name: %s" % (name))
        else:
            self._root.destroy()

    def _test_action(self):
        self._ping_someone(self._name.get())

    def _ping_someone(self, name):
        ret = self._ping_callback(name)
        if not ret:
            self._generate_ping_buttons()
            splash.error(name + ' is no longer available')

    def _generate_ping_buttons(self):
        logger.info("generating buttons")
        #TODO put in a frame with a scrollbar
        for button in self.ping_buttons:
            button.destroy()
        self.ping_buttons = []
        next_y = 10
        for name in sorted(NotiFireDb.get_all_names()):
            if self._name.get() == name:
                continue
            cmd = partial(self._ping_someone, name)
            button = FlatButton(self.frame, text="Ping " + name, width=20, command=cmd)
            self.ping_buttons.append(button)
            button.place(x=300, y=next_y)
            next_y += 40

    def _auto_refresh(self):
        self._generate_ping_buttons()
        self._root.after(600000, self._auto_refresh)  # Run again in 10 mintues

    def _check_version(self):
        with open("version.txt") as f:
            latest = StrictVersion(f.read())
        if self._version is None:
            self._version = latest
        elif self._version < latest:
            self._version_label.place(x=80, y=255)
            return
        self._root.after(86400000, self._check_version)  # Run again in 1 day


def unit_test():
    from sys import stdout
    name = UI().get_name()
    UI().main_window(name, lambda x:stdout.write('ping ' + x + '\n'))


if __name__ == '__main__':
    unit_test()
