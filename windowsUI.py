# -*- coding: utf-8 -*-
from functools import partial
from Tkinter import Tk, Frame, Label, Entry, StringVar, Button  # Elements
from Tkinter import TOP, BOTH, YES, FLAT  # Properties
from notiFireDb import NotiFireDb
from screenSplasher import splash

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


class MainWindow(object):
    def __init__(self, port, name, register_callback, ping_callback):
        self._root = Tk()
        self._port = StringVar()
        self._port.set(port)
        self._name = StringVar()
        self._name.set(name)
        self._register_callback = register_callback
        self._ping_callback = ping_callback

    def show(self):
        # Set transparency
        #self.root.wait_visibility(self.root)  # Needed for linux ?
        self._root.attributes('-alpha', 0.95)

        # Create Frame
        self.frame = DraggableFrame(self._root)
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)
        # Set frame size and position
        screen_width = self.frame.master.winfo_screenwidth()
        screen_heigh = self.frame.master.winfo_screenheight()
        w = screen_width * 0.5
        h = screen_heigh * 0.6
        # Center the window
        x = (screen_width/2) - (w/2)
        y = (screen_heigh/2) - (h/2)
        self.frame.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Adjust frame properties
        self.frame.master.overrideredirect(True)  # Set no border or title

        FlatButton(self.frame, text='×', no_bg=True, width=1, font=("calibri", 15), command=self._root.destroy).place(x=w-20, y=-10)

        Label(self.frame, text="Port").place(x=10, y=15)
        Entry(self.frame, exportselection=0, relief=FLAT, textvariable=self._port).place(x=80, y=15)

        Label(self.frame, text="Name").place(x=10, y=55)
        Entry(self.frame, exportselection=0, relief=FLAT, textvariable=self._name).place(x=80, y=55)

        FlatButton(self.frame, text="Update", width=26, command=self._update_action).place(x=10, y=90)

        #TODO put in a frame with a scrollbar

        self.buttons = []
        self._generate_ping_buttons()

        # Run Event loop
        self._root.mainloop()

    def _update_action(self):
        self._register_callback(self._name.get(), self._port.get())

    def _ping_smoeone(self, name):
        ret = self._ping_callback(name)
        if not ret:
            self._generate_ping_buttons()
            splash.error(name + ' is no longer available')

    def _generate_ping_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        next_y = 10
        for name in sorted(NotiFireDb.get_all_names()):
            #TODO filter out yourself (maybe unless in some debug mode)
            cmd = partial(self._ping_smoeone, name)
            button = FlatButton(self.frame, text="Ping " + name, width=20, command=cmd)
            self.buttons.append(button)
            button.place(x=300, y=next_y)
            next_y += 40

def unit_test():
    from sys import stdout
    MainWindow("12345", "Eran", lambda x,y:stdout.write('Register ' + x + ', ' + y + '\n'),
               lambda x:stdout.write('ping ' + x + '\n')).show()


if __name__ == '__main__':
    unit_test()
