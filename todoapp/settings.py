#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import os,sys

import ConfigParser

# We are going to use the COnfigParser module to read the file .todoappconf in /home/$USER

def create_conf():
    """ Create the .todoappconf file if it does not exist """
    # Check if the conf file exists or not first
    # If it exists, then return out of the function
    config = ConfigParser.ConfigParser()
    loc = os.getenv('HOME')+"/.todoappconf"
    if os.path.isfile(loc):
        # The conf file already exists
        return
    else:
        # it does not exit, time to create it
        fo = open(loc,'w')
        config.add_section("todofile")
        # The default location of the todo.txt file is /home/$USER/todo.txt
        todo_loc = os.getenv('HOME')+"/todo.txt"
        config.set("todofile","location", todo_loc)
        config.write(fo)
        fo.close()
        
def get_location():
    """ reads the .todoappconf file and returns the location of the todo.txt file """
    config = ConfigParser.ConfigParser()
    loc = os.getenv('HOME')+"/.todoappconf"
    try:
        config.read(loc)
    except:
        sys.exit(0)
        
    todo_loc = config.get("todofile","location")
    return todo_loc
    
def set_location(location):
    """ sets the location variable in the .todoappconf file """
    config = ConfigParser.ConfigParser()
    loc = os.getenv('HOME')+"/.todoappconf"
    try:
        config.read(loc)
    except:
        sys.exit(0)
    fo = open(loc,'w')
    
    config.set("todofile","location",location)
    config.write(fo)
    fo.close()
       
    
def select_todofile():
    """ Opens a gtk file chooser dialog and ask the user for the todo.txt file """
    dialog = gtk.FileChooserDialog(
            title = 'Please select the todofile',
            action = gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons = (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN,gtk.RESPONSE_OK)
            )
    dialog.set_default_response(gtk.RESPONSE_OK)
    filename = ''
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename(),'selected'
    dialog.destroy()
    todo_loc = filename[0]
    set_location(todo_loc)
    return
        
def is_location_set():
    """ Checks if the conf file has the location of the todofile set or not """
    config = ConfigParser.ConfigParser()
    loc = os.getenv('HOME')+"/.todoappconf"
    try:
        config.read(loc)
    except:
        sys.exit(0)
    
    if 'todofile' in config.sections():
        if 'location' in config.options('todofile'):
            try:
                test = config.get('todofile','location')
                if test != '':
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False
    else:
        return False
        
def is_todo_existing():
    """ Checks if the location of the todo.txt file is correct """
    config = ConfigParser.ConfigParser()
    loc = os.getenv('HOME')+"/.todoappconf"
    try:
        config.read(loc)
    except:
        sys.exit(0)
    location = config.get('todofile','location')
    if os.path.isfile(location):
        return True
    else:
        return False      
                
        




# Change this
# TODO: make a flexible way to change the TODO_TXT_LOCATION from time to time
# TODO_TXT_LOCATION = '/home/rishi/todo.txt'

