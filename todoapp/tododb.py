#!/usr/bin/env python

import re, sys, os
import random
import pynotify
import settings

# Tododb is a python dict as a database for the todo tasks in todo.txt
# It reads from the todo.txt specified in the settings.TODO_TXT_LOCATION variable
# It renders each task line as per the syntax given in the README as follows:
# For example if the task line is:
# '* 2 This is a sample task for #todoapp', 
# Tododb reads it and creates a list : ['*','2','This is a simple task for #todoapp','#todoapp']
# where '*': due task ('x' marks done tasks)
#       '2': task priority for later sorting
#       'This is a...': task string
#       '#todoapp': hashtag for categorising the task
# A dictionary is then rendered with a key as an random but unique integer and the value as the list



            
def generate_random(current_list):
    """ Generate a number to serve as a key in the todo_dict """
    while True:
        number = random.randrange(1,10000)
        # Of course the random number must in fact be unique too
        if number not in current_list:
            return number
        else:
            continue

class EmptyFileException(Exception):
    """ Exception to be raised for an empty file so as to prevent errors further down the program"""
    def __init__(self, arg):
        self.args = args

class Tododb:
    """ The main class implementing the todo.txt file to a dictionary logic as per README """
    task_count = 0
    
    def __init__(self, filename):

        self.tasklist = [] 
        self.tododict = {}
        
        self.location = filename
        print "file:",filename         

        try:
            self.fo = open(filename, 'r')
        except IOError, args:
            notify = pynotify.Notification("ERROR finding todo.txt","Please check the settings")
            notify.show()
            sys.exit(0)
        else:
            try:
                file_size = os.path.getsize(self.location)
                if file_size == 0L:
                    raise EmptyFileException("The todo.txt is empty")
            except EmptyFileException, arg:
                notify = pynotify.Notification("Oops, There is some problem here...",arg)
                notify.show()
                sys.exit(0)              
        
                                    
        for line in self.fo:
            if line != '':
                if line.startswith('*') or line.startswith('x'):
                    key_list = []
                    search = re.search( r'(\d)(.+)\n', line)
                    importance = search.group(1)
                    string = search.group(2).strip()
                    
                    split = string.split()
                    # Get the hash tagged word
                    tag = ""
                    for word in split:
                        if word.startswith('#'):
                            tag += word
                        

                    if tag == '' : tag+='no#'
                    status = line[0]
                    
                                                    
                    key_list.append(status)
                    key_list.append(importance)
                    key_list.append(string)
                    key_list.append(tag)

                    id = generate_random(self.tododict.keys())
                    self.tododict[id] = key_list
                    Tododb.task_count += 1
                else:
                    notify = pynotify.Notification("ERROR READING SYNTAX","Please read the README for syntax help")
                    notify.show()
            else:
                continue
                
        self.fo.close()

    def write_to_file(self):
        fo = open(TODO_TXT_LOCATION,'w')
        for key in self.tododict:
            l = self.tododict[key]
            line = l[0] + ' ' + l[1] + ' ' + l[2] + '\n'
            fo.write(line)
        fo.close()
            
    def mark_read_task(self, data):
        """ changes the * to x for a task """
        if self.tododict[data][0] == '*':
            self.tododict[data][0] = 'x'
            # print 'Marking Read'
        elif self.tododict[data][0] == 'x':
            self.tododict[data][0] = '*'
            # print 'Marking Unread'
        

    def delete_task(self, task_id):
        """ Delete the entry pertaining to the id passed """
        del self.tododict[task_id]

    def get_write_dict(self):
        """ Returns the part of the entry in tododict which is to appear in the appindicator """
        # The task lists should also display the priority number
        return_dict = {}
        for item in self.tododict:
            value = self.tododict[item]
            line = value[1] + ' ' + value[2]
            
           
            read = False
            if value[0] == '*':
                read = False
            else:
                read = True
            
            return_dict[item] = (line, read)
        return return_dict
            


    def get_dict(self):
        return self.tododict

    def print_dict(self):
        for item in self.tododict:
            print item,'\t',self.tododict[item]
        print Tododb.task_count


  
                    
                   
            
        

    
