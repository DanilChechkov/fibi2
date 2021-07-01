import pickle
import gi
import os

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

path1 = os.getcwd() +'/'

def pdump(file,item):
    with open(path1 + str(file)+'.pkl','wb') as f: pickle.dump(item,f)
def pload(file):
    with open(path1 + str(file)+'.pkl','rb') as f: return pickle.load(f)

class Handler:
    def __init__(self):
        self.window_is_hidden = False

builder = Gtk.Builder()
builder.add_from_file(path1+'fibi.glade')
builder.connect_signals(Handler())

window = builder.get_object('window1')
window.connect('destroy',Gtk.main_quit)
window.show_all()
Gtk.main()