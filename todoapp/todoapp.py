#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import sys
import pynotify

import settings
from tododb import *

# Tries to create a conf file. The function will return control if it finds the file existing already
settings.create_conf()
TODO_TXT_LOCATION = ''

if settings.is_todo_existing():
    TODO_TXT_LOCATION = settings.get_location()
else:
    settings.select_todofile()
    TODO_TXT_LOCATION = settings.get_location()
    
print TODO_TXT_LOCATION

TODO = Tododb(TODO_TXT_LOCATION)

def sort_keys(todo_dict):
    func = lambda item : todo_dict[item][0][0]
    return sorted(todo_dict, key=func, reverse=True)
    
    
class TodoApplet:

    def mark_done(self, widget, data=None):
        TODO.mark_read_task(data)
        # Write to the file
        TODO.write_to_file()
        
    def quit(self, widget, data=None):
        gtk.main_quit()
        
    def change_filename(self, widget, data=None):
        """ Change the settings file """
        settings.select_todofile()
        notify = pynotify.Notification("The new location of todo.txt has been set","Please restart the application to load the new task list")
        notify.show()
        gtk.main_quit()
        
    
    def __init__ (self, todo_dict):
        self.ind = appindicator.Indicator("todo-menu", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon("distributor-logo")
        
        # Main menu
        self.menu = gtk.Menu()
        
        # Sort the todo list items according to their proirity
        sorted_keys = sort_keys(todo_dict)
        sorted_values = []
        for key in sorted_keys:
            sorted_values.append(todo_dict[key][0])
        
        # Add the values in sorted_values list to the manu
        # As a gtk.CheckMenuItem
        
        for i in range(len(sorted_values)):
            check = gtk.CheckMenuItem( sorted_values[i] )
            check.set_active(False)
            
            if todo_dict[ sorted_keys[i] ][1]:
                check.set_active(True)
            else:
                check.set_active(False)
            check.connect("activate", self.mark_done, sorted_keys[i])
            
            check.show()  
            # Check whether the task is already read or not and hence toggle the tick-mark
            # The read status is the second element in the tuple which is the value in the todo_dict
            
            self.menu.append(check)
        
        sep = gtk.SeparatorMenuItem()
        sep.show()
        self.menu.append(sep)
        
        select_item = gtk.MenuItem("Select the todo.txt file...")
        select_item.connect("activate", self.change_filename)
        select_item.show()
        self.menu.append(select_item)
        
        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        quit.connect("activate", self.quit)
        quit.show()
        self.menu.append(quit)
        
        self.menu.show()
        self.ind.set_menu(self.menu)
        
    def main(self):
        gtk.main()
        

write_dict = TODO.get_write_dict() 
t = TodoApplet(write_dict)
t.main()
            
        
        
        
        
        
