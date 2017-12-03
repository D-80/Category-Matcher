import Queue 
from Queue import Empty
import threading
import time
try:
    from force import Jedi
except ImportError:
    print "Couldn't load force module"
try:
    import stopwatch
except ImportError:
    print "Couldn't load stopwatch module"
try:
    import re
except ImportError:
    print "Couldn't load regex module"
try:
    from Tkinter import * 
except ImportError: 
    from tkinter import *
except:
    print "Couldn't load tkinter module"


#DATABASE:
input_data = []
output_data = []

input_array = []
output_array = []
cat_array = []
key_array = []
categories = {} #categories[n] to get name of the row in sub_categories
sub_categories = [] #multidimensional array of sub_categories 
keys = {} #keys[category_name] to get category number from its name
syek = {} #syek[self.output_column[n]] to get category name from its number

#SOURCE FILES:
input_src = "src/input.txt"
output_src = "src/output.txt"
input_data_src = "src/input_data.txt"
output_data_src = "src/output_data.txt"
cat_src = "src/cat.txt"
key_src = "src/key.txt"
guidelines_src = "src/guidelines.txt"
anchor_src = "src/anchor.txt"



class JediThread(threading.Thread):
    def __init__(self, queue, jedi, index, w1 = None, w2 = None, w3 = None, threshold = 0):
        threading.Thread.__init__(self)
        self.queue = queue
        self.index = index
        self.jedi = jedi
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.threshold = threshold
    def run(self):
        self.jedi.compare_products(self.index, self.w1, self.w2, self.w3)
        self.queue.put(self.jedi.filter_products(self.threshold))


class GUI(Frame): #OUR MAIN CONTAINER WITH MOST EMBEDDED FUNCTIONS

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Excell")

        print "TURBO EXCELL 2000"
        print
        print "All your work shall be saved to output.txt after pressing the Home button."
        print "Be sure to do it often!"
        print
        print "HOTKEYS"
        print "Enter: Choose"
        print "Shift + Enter: Confirm in Regex Panel"
        print "BackSpace: Return"
        print "Shift + BackSpace: Return to the Categories Menu"
        print "Shift + N key: Jump to the next unclassified product"
        print "Shift + M key: Jump to the next unknown product"
        print "Shift + U key: Assign category Unknown" 
        print "S key: Select in the Regex Panel"
        print "D key: De-select in the Regex Panel"
        print "Home: Copy from the output_array into the output.txt file"
        print "F1: Open the Guidelines Window"
        print
        print

        #top menu
        prepare_database() 

        try:
            for index in range(len(output_array)):
                input_data.append(input_array[index])
                output_data.append(output_array[index])
        except:
            print "error maybe due to different sizes of files"

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu)
        file_menu.add_command(label="Load Input", command=lambda:self.load_input_window(self))
        file_menu.add_command(label="Load Output", command=lambda:self.load_output_window(self))
        file_menu.add_command(label="Save Output as", command=lambda:self.save_as_window(self))
        file_menu.add_command(label="Save Output as output.txt (Home)", command=lambda:self.save(self))
        file_menu.add_command(label="Merge Outputs", command=self.merge_outputs_window)
        file_menu.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file_menu)
        
        edit_menu = Menu(menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Normal Mode", command=self.normal_mode)
        edit_menu.add_command(label="Correction Mode", command=self.correct_mode)
        edit_menu.add_command(label="Super Lazy Mode", command=self.super_lazy_mode)
        menu.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menu)
        help_menu.add_command(label="Guidelines (F1)", command=self.guidelines)
        menu.add_cascade(label="Help", menu=help_menu)
        
        #categories
        index = 0
        for x in range(len(key_array)):
            
            if key_array[x]=='\n':
                categories[index] = cat_array[x][0:-1] 
                column = []
                sub_categories.append(column)
                index += 1

                #can't use this shit because there is no scrollbar for menus :P
                #self.sub_menu = Menu(self)
                #self.sub_menu.add_command(label="Exit", command=self.cat_menu.grab_release())
                #self.sub_menu.add_command(label="Add Category", command=self.add_sub_cat)
                #self.cat_menu.add_cascade(label=categories[-1], menu=self.sub_menu)
            else:
                sub_categories[index-1].append(cat_array[x][0:-1])
                keys[cat_array[x][0:-1]]=key_array[x]
                syek[key_array[x]]=cat_array[x][0:-1]
                #self.sub_menu.add_command(label=cat_array[x], command=self.fill_data)

        syek["?\n"] = "Unknown"
        syek["\n"] = "Empty"
        keys["Unknown"] = "?\n"
        keys["Empty"] = "\n"
     
        self.yoda = Jedi(input_array, output_array, input_data, output_data)
        
        self.normal_mode()

#GENERAL METHODS
################################################################################################
    def save_anchor(self):
        with open(anchor_src, 'w+') as file:
            file.write(self.anchor)
            file.seek(0)
            print "Anchor position saved to ", self.anchor
            print


    def load_anchor(self):
        with open(anchor_src, 'r') as file:
            self.anchor = file.read()
            print "Anchor position is ", self.anchor
            print


    def save_action(self):
        save_array_to_file()
        self.save_anchor()
        print("Progress Saved")


    def save(self, event):
        self.save_action()


    def save_as_window(self, event):
        self.file_name = StringVar()
        self.save_window = Toplevel(self.master)
        self.save_window.wm_title("Save as")
        self.save_instruct = Label(self.save_window, text="Save as:")
        self.save_name_entry = Entry(self.save_window, textvariable=self.file_name)
        self.save_instruct.pack()
        self.save_name_entry.pack()
        self.save_window.bind("<Return>", self.save_as)


    def save_as(self, event):
        f = open("output/"+self.file_name.get(), "w+")
        save_array_to_file(input_src, "output/"+self.file_name.get())
        f.close()
        print("Progress Saved")


    def load_input_window(self, event):
        self.name = StringVar()
        self.popup_window = Toplevel(self.master)
        self.popup_window.wm_title("Load Input")
        self.instruct = Label(self.popup_window, text="File name:")
        self.load_entry = Entry(self.popup_window, textvariable=self.name)
        self.instruct.pack()
        self.load_entry.pack()
        self.popup_window.bind("<Return>", self.load_input) 


    def load_output_window(self, event):
        self.name = StringVar()
        self.popup_window = Toplevel(self.master)
        self.popup_window.wm_title("Load Output")
        self.instruct = Label(self.popup_window, text="File name:")
        self.load_entry = Entry(self.popup_window, textvariable=self.name)
        self.instruct.pack()
        self.load_entry.pack()
        self.popup_window.bind("<Return>", self.load_output) 


    def load_output(self, event):
        loaded = False
        try:
            read_files(input_src,self.load_entry.get())
            loaded = True
        except IOError:
            print "I hate to say it, but it looks like the system you're searching for doesn't exist." 
            loaded = False
        if loaded == True:
            print "File ",self.load_entry.get()," successfully loaded"
            self.popup_window.destroy()
        
        self.update_output_array()


    def load_input(self, event):
        loaded = False
        try:
            read_files(self.load_entry.get())
            loaded = True
        except IOError:
            print "I hate to say it, but it looks like the system you're searching for doesn't exist." 
            loaded = False
        if loaded == True:
            print "File ",self.load_entry.get()," successfully loaded"
            self.popup_window.destroy()
        
        self.update_input_array()


    def update_output_array(self):#<---really it's update_output_column
            print "Updating output column"
            #print "old output column size = ", self.output_column.size()
            self.output_column.delete(0, self.output_column.size())
            for i in range(len(output_array)):
                self.output_column.insert(END, output_array[i])
            self.output_column.pack(side=RIGHT, fill=BOTH, expand=TRUE)
            #print "new output column size = ", self.output_column.size()
            
            self.categories_column.delete(0, self.categories_column.size())
            for i in range(len(output_array)):
                self.categories_column.insert(END, syek[output_array[i]])
            self.categories_column.pack(side=LEFT, fill=BOTH, expand=TRUE)
            
            self.count()
            #self.select_next_action()
            try:
                self.choose_cat_action()
            except:
                print "ERROR updating output array. Probably all items are done"


    def update_input_array(self):
        print "Updating output column"
       # print "old output column size = ", self.output_column.size()
        self.input_column.delete(0, self.input_column.size())
        for i in range(len(input_array)):
            self.input_column.insert(END, input_array[i])
        self.input_column.pack(side=LEFT, fill=BOTH, expand=TRUE)
       # print "new output column size = ", self.output_column.size() 
        self.count()


    def guidelines_hotkey(self, event):
        self.guidelines()


    def guidelines(self):
        with open(guidelines_src, 'r') as file:
            self.guide = file.read()
            guide_window = Toplevel(self.master)
            guide_window.wm_title("Guidelines")
            guide_window.geometry("600x800")
            guide_text = Text(guide_window, width=550, height=750)
            guide_text.pack()
            guide_text.insert(END, self.guide)


    def merge_outputs_window(self):
        self.merge_window = Toplevel(self.master)
        self.merge_window.wm_title("Merge Outputs")
        
        self.level1 = Frame(self.merge_window)
        self.level2 = Frame(self.merge_window)
        self.level3 = Frame(self.merge_window)
        
        self.name1 = StringVar()
        self.name2 = StringVar()
        self.name3 = StringVar()

        self.label1 = Label(self.level1, text="File name:")
        self.label2 = Label(self.level2, text="File name:")
        self.label3 = Label(self.level3, text="Final output file name:")

        self.var1 = IntVar()
        self.button1 = Checkbutton(self.level1, text="Remove \\r", variable=self.var1)
       
        self.var2 = IntVar()
        self.button2 = Checkbutton(self.level2, text="Remove \\r", variable=self.var2)
        
        self.load_entry1 = Entry(self.level1, textvariable=self.name1)
        self.load_entry2 = Entry(self.level2, textvariable=self.name2)
        self.save_entry = Entry(self.level3, textvariable=self.name3)

        self.confirm_button = Button(self.merge_window, text="Merge", command=self.merge_outputs)
        
        self.label1.pack(side=LEFT)
        self.button1.pack(side=RIGHT)
        self.load_entry1.pack(side=RIGHT)
        self.label2.pack(side=LEFT)
        self.button2.pack(side=RIGHT)
        self.load_entry2.pack(side=RIGHT)
        self.label3.pack(side=LEFT)
        self.save_entry.pack(side=RIGHT)

        self.level1.pack()
        self.level2.pack()
        self.level3.pack()
        self.confirm_button.pack()


    def merge_outputs(self):
        print "Merging outputs..."
 
        self.f1_array = []
        self.f2_array = []
        self.f3_array = []

        with open(self.name1.get(), 'r') as file:
            for line in file:
                self.f1_array.append(line)

        with open(self.name2.get(), 'r') as file:
            for line in file:
                self.f2_array.append(line)

        self.compare_files(0)#<--Essentially the same philosophy as in are_you_sure


    def compare_files(self, index):
        print "Comparing files at index ", index
        print "Windows format f1 = ",self.var1.get(), " f2 = ",self.var2.get()

        #general check

        self.misia = 0

        for x in range(index, len(self.f1_array)): 

            if len(self.f3_array) == len(self.f1_array): #OK 
                self.write_to()
                print "Merge finished"#+
                break
            elif len(self.f1_array) != len(self.f2_array): #OK
                print "ERROR: Sizes of files don't match"
                break
            else:
                #formating keys
                if self.var1.get() == 1: #IF WINDOWS FORMAT
                    self.key1 = syek[self.f1_array[x].rstrip()]#OK
                else:
                    self.key1 = syek[self.f1_array[x]] #OK
                if self.var2.get() == 1: #SAME FOR THE FILE2
                    self.key2 = syek[self.f2_array[x].rstrip()]#OK
                else:
                    self.key2 = syek[self.f2_array[x]] #OK
                print self.key1, self.key2 #ALL GOOD
   
                #comparing lines
                if self.key1 == self.key2: #TWO LINES ARE EQUALS
                    print self.key1
                    self.f3_array.append(keys[self.key1]) #OK
                    print "Line ",self.f1_array[x]," equals Line ",self.f2_array[x] #OK
                    
                    print
                    print x, ": Line ",self.key1," added to file" #OK
                    print
                    continue
                elif self.key1 == "Empty": #LINE 1 IS EMPTY
                    print self.key2
                    self.f3_array.append(keys[self.key2])#OK 
                    print "Line from file 1 is empty"

                    print
                    print index, ": Line ",self.key2," added to file"
                    print
                    continue
                elif self.key2 == "Empty": #LINE 2 IS EMPTY
                    print self.key1
                    self.f3_array.append(keys[self.key1])#OK
                    print "Line from file 2 is empty"

                    print
                    print index, ": Line ",self.key1,  "added to file"
                    print
                    continue
                else:
                    print 
                    print "Else... "
                    print
                    self.misia = x
                    break
        print "End of loop"
        self.choose_wisely(input_array[self.misia], self.key1, self.key2, self.misia)


    def choose_wisely(self, product, old_key, new_key, index): #NEW KEY = self.f1_array[], OLD KEY = self.f2_array[], index = x from compare_files
       
        if len(self.f3_array) == len(self.f1_array): #OK 
            self.write_to()
            print "Merge finished"#+
        else: 
            print "Choose wisely"
            print "Windows format f1 = ",self.var1.get(), " f2 = ",self.var2.get()
            
            print "Index = ",index

            self.key1 = 0#OK
            self.key2 = 0#OK

            #formating keys
            if self.var1.get() == 1: #IF WINDOWS FORMAT
                self.key1 = syek[old_key[:-2]+"\n"]#OK
            else:
                self.key1 = syek[old_key]#OK

            if self.var2.get() == 1:#SAME FOR THE FILE2
                self.key2 = syek[new_key[:-2]+"\n"]#OK
            else:
                self.key2 = syek[new_key]#OK
            print self.key1, self.key2 #ALL GOOD
            
            #comparing files

            print "Choose wisely"
            "choose_wisely"
            
            self.sure_window = Toplevel(self.master)
            self.sure_window.geometry("400x300")
            self.sure_window.wm_title(product)
            print repr(old_key), repr(new_key)

            
            quest = "Do you want to replace the category\n\n"+self.key1+"\n\nwith\n\n"+self.key2+"?"
            self.sure_label = Label(self.sure_window, text=quest)
            self.answ_panel = Frame(self.sure_window)
            self.yes = Button(self.answ_panel, text="Yes", command=lambda:self.red_pill(new_key, index))
            self.no = Button(self.answ_panel, text="No", command=lambda:self.blue_pill(old_key, index))
            
            self.sure_label.pack()
            self.answ_panel.pack(side=BOTTOM)
            self.yes.pack(side=LEFT)
            self.no.pack(side=RIGHT)


    def red_pill(self, new_key, index):
        print "yes"
        print new_key
        self.f3_array.insert(index,keys[new_key])
        self.sure_window.destroy()
        self.compare_files(index+1)

        print
        print index, ": line ",new_key, " added to file"
        print


    def blue_pill(self, old_key, index):
        print "no"
        self.f3_array.insert(index,keys[old_key])
        self.sure_window.destroy()
        self.compare_files(index+1)



#NORMAL_MODE METHODS
###########################################################################################
    def normal_mode(self):
        #LAYOUT
        #main_frame
        try:
            self.normal_mode_f.destroy()
        except:
            "There is no normal_mode instance yet"
        try:
            self.correct_mode_f.destroy()
        except:
            "There is no correct_mode instance yet"

        self.normal_mode_f = Frame(self.master)
        self.main_frame = Frame(self.normal_mode_f)
        
        print "You are now in the Normal Mode"

        scrollbar = Scrollbar(self.main_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.done_panel = Frame(self.main_frame)
        self.done_label = Label(self.done_panel, text="Done:")
        self.done_button = Button(self.done_panel, text="Update", command=lambda:self.count_done(self))
        self.anchor_label = Button(self.done_panel, text="Set anchor to: ", command=self.set_anchor)
        self.anchor = 0
        self.anchor_text = StringVar()
        self.anchor_entry = Entry(self.done_panel, text=self.anchor_text)
        self.auto = BooleanVar()
        self.auto.set(True)
        self.mode_button = Checkbutton(self.done_panel, text="Automatic Mode", variable=self.auto)
        self.complete_button = Button(self.done_panel, text="Complete", command=self.complete_auto)
        self.extent = StringVar()
        self.ext = Entry(self.done_panel, width=3, textvariable=self.extent)
        self.extent.set(0.0)

        self.ext.pack(side=RIGHT)
        self.complete_button.pack(side=RIGHT)
        self.mode_button.pack(side=RIGHT)
        self.anchor_entry.pack(side=RIGHT)
        self.anchor_label.pack(side=RIGHT)
        self.done_button.pack(side=RIGHT)
        self.done_label.pack(side=RIGHT)
        self.done_panel.pack(side=TOP)
        self.load_anchor()

        print "Automatic Mode = ", self.auto.get()

        #input/categories/output_column
        self.input_column = Listbox(self.main_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(input_array)):
            self.input_column.insert(END, str(i) + ":  " + input_array[i])
        self.input_column.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.categories_column = Listbox(self.main_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(output_array)):
            self.categories_column.insert(END, syek[output_array[i]])
        self.categories_column.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.output_column = Listbox(self.main_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(output_array)):
            self.output_column.insert(END, output_array[i])
        self.output_column.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        scrollbar.config(command=self.scroll)

        #pack
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        #results
        self.res_frame = Frame(self.normal_mode_f)
        self.res_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        self.normal_mode_f.pack(fill=BOTH, expand=TRUE)
        self.pack()

        """
        #category menu
        self.e = ''
        self.cat_menu = Menu(self.master)
        self.cat_menu.add_command(label="Exit", command=self.cat_menu.grab_release())
        self.cat_menu.add_command(label="Add Category", command=self.add_category)
        """
        self.count_done(self)
        self.main_frame.focus()
        self.input_column.focus()
        self.key_bindings()
        self.select_next_action()

    def double_click(self, event):
        self.choose_cat_action()


    def key_bindings(self):
        self.master.bind("<Return>", self.choose_cat)
        self.master.bind("<Home>", self.save)
        self.master.bind("<Shift-N>", self.select_next)
        self.master.bind("<Shift-M>", self.select_unknown)
        self.master.bind("<Shift-U>", self.unknown)
        self.master.bind("<Shift-BackSpace>", self.choose_cat)
        self.master.bind("<F1>", self.guidelines_hotkey)
        self.master.bind("<Tab>", self.tab_handler)
        self.master.bind("<Double-Button-1>", self.double_click)

    
    def unbind_all(self):

        self.master.unbind("<Down>")
        self.master.unbind("<Shift-Return>")
        self.master.unbind("<n>")
        self.master.unbind("<s>")
        self.master.unbind("<d>")


    def tab_handler(self, event):
        return 'break'

    def set_anchor(self):
        self.anchor = self.anchor_entry.get()
        print "Anchor set to: ", self.anchor

    
    def unknown(self,event):
        self.unknown_action()    


    def unknown_action(self):
        output_array.insert(self.input_column.curselection()[0],"?\n")
        output_array.pop(self.input_column.curselection()[0]+1)
        print "No category at index = ", self.input_column.curselection()[0]
        self.update_output_array()


    def select_next(self, event):
        self.select_next_action()


    def select_next_action(self):
        try:
            for x in range(int(self.anchor), len(input_array)):
                if self.input_column.get(x) != str(x)+":  " +"#N/A\n" and self.output_column.get(x) == "\n":
                                   
                    self.output_column.focus()

                    self.output_column.see(0)
                    self.output_column.select_clear(0, END)
                    self.output_column.activate(x)
                    self.output_column.select_set(x)
                    self.output_column.see(x)
                    
                    self.input_column.see(0)
                    self.input_column.select_clear(0, END)
                    self.input_column.activate(x)
                    self.input_column.select_set(x)
                    self.input_column.see(x)

                    self.categories_column.see(0)
                    self.categories_column.select_clear(0, END)
                    self.categories_column.activate(x)
                    self.categories_column.select_set(x)
                    self.categories_column.see(x)

                    break 
            self.choose_cat_action()
        except:
            print "Couldn't select_next, probably because all items are done."
            self.select_unknown_action()


    def select_unknown(self, event):
        self.select_unknown_action()


    def select_unknown_action(self):
        try:
            for x in range(int(self.anchor), len(input_array)):
                if self.output_column.get(x) == "?\n" and input_array[x] != "#N/A\n":
                                   
                    self.output_column.focus()

                    self.output_column.see(0)
                    self.output_column.select_clear(0, END)
                    self.output_column.activate(x)
                    self.output_column.select_set(x)
                    self.output_column.see(x)
                    
                    self.input_column.see(0)
                    self.input_column.select_clear(0, END)
                    self.input_column.activate(x)
                    self.input_column.select_set(x)
                    self.input_column.see(x)

                    self.categories_column.see(0)
                    self.categories_column.select_clear(0, END)
                    self.categories_column.activate(x)
                    self.categories_column.select_set(x)
                    self.categories_column.see(x)

                    break 
            self.choose_cat_action()
        except:
            print "Couldn't select_unknown, probably because all items are done."



    def scroll(self,*args):
        apply(self.input_column.yview, args)
        apply(self.output_column.yview, args)
        apply(self.categories_column.yview, args)


    def client_exit(self):
        self.save_action()
        exit()


    def choose_cat(self, event):
        self.choose_cat_action()


    def choose_cat_action(self):         
        self.product = input_array[self.input_column.curselection()[0]]

        for widget in self.res_frame.winfo_children():
            widget.destroy()

        self.master.clipboard_clear()
        self.master.clipboard_append(self.product)
        self.master.update()

        product_label = Label(self.res_frame, text=self.product)
        product_label.pack()

        self.search_box = Frame(self.res_frame)
        self.search_label = Label(self.search_box, text="Search: ")
        self.search_string = StringVar()
        self.search_entry = Entry(self.search_box, text=self.search_string)

        self.search_label.pack(side=LEFT)
        self.search_entry.pack(side=RIGHT)
        self.search_box.pack()

        self.unknown_button = Button(self.res_frame, text="Unknown", command=lambda:self.fill_data_unknown_gate(self))
        self.unknown_button.pack()

        self.match_box = Frame(self.res_frame)
        self.match_label = Button(self.match_box, text="Closest match: ", command=lambda:self.closest_match(self))
        self.mname = StringVar()
        self.msim = StringVar()
        self.mcat = StringVar()
        self.match_name = Label(self.match_box, textvariable=self.mname)
        self.match_sim = Label(self.match_box, textvariable=self.msim)
        self.match_cat = Button(self.match_box, textvariable=self.mcat, command=lambda:self.fill_data_closest_match_gate(self))
        self.mname.set(" Name ")
        self.msim.set( "Similarity ")
        self.mcat.set(" Category ") 
        self.match_label.pack(side=LEFT)
        self.match_name.pack(side=LEFT)
        self.match_sim.pack(side=LEFT)
        self.match_cat.pack(side=LEFT)
        self.match_box.pack(side=TOP)


        self.cat_weight_label = Label(self.res_frame, text="Weights")
        self.cat_weight_frame = Frame(self.res_frame)
        self.cat_w1_label = Label(self.cat_weight_frame, text="Words = ")
        self.cat_w2_label = Label(self.cat_weight_frame, text="Numbers = ")
        self.cat_w3_label = Label(self.cat_weight_frame, text="Units = ")
        self.cat_w1 = StringVar()
        self.cat_w2 = StringVar()
        self.cat_w3 = StringVar()
        #original weights:
        self.cat_w1.set(2)
        self.cat_w2.set(1)
        self.cat_w3.set(1)
        
        self.cat_w1_entry = Entry(self.cat_weight_frame, width=3, textvariable=self.cat_w1)
        self.cat_w2_entry = Entry(self.cat_weight_frame, width=3, textvariable=self.cat_w2)
        self.cat_w3_entry = Entry(self.cat_weight_frame, width=3, textvariable=self.cat_w3)
        self.cat_w1_label.pack(side=LEFT)
        self.cat_w1_entry.pack(side=LEFT)
        self.cat_w2_label.pack(side=LEFT)
        self.cat_w2_entry.pack(side=LEFT)
        self.cat_w3_label.pack(side=LEFT)
        self.cat_w3_entry.pack(side=LEFT)
        self.cat_weight_label.pack()
        self.cat_weight_frame.pack()

        scrollbar = Scrollbar(self.res_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.category_listbox = Listbox(self.res_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(categories)):
            self.category_listbox.insert(END, categories[i])

        self.category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.category_listbox.yview)

        self.category_listbox.selection_clear(0, END)
        self.category_listbox.selection_set(0)

        self.res_frame.focus()
        self.category_listbox.focus()

        self.unbind_all()
        self.key_bindings()

        self.master.bind("<Down>", self.focus_on_search)
        self.master.bind("<Up>", self.focus_on_search2)
        self.master.bind("<Return>", self.choose_cat2_gate1)
        self.master.bind("<Shift-Return>", self.search_cat)

        self.choose_cat2_gate2_bool = False

        self.search_box.focus()
        self.search_entry.focus()


    def fill_data_closest_match_gate(self, event):
        self.category_name = self.mcat.get()
        self.category_no = keys[self.mcat.get()]
        self.parent_cat_selection = ""
        self.fill_data()


    def choose_cat2_gate1(self, event): #if through choose_cat
        self.selection = self.category_listbox.curselection()[0]
        self.parent_cat2 = self.category_listbox.get(self.category_listbox.curselection()[0])
        self.choose_cat2()


    def search_cat(self, event):

        self.cats = []
        self.sub_cats = []
        self.parent_cat = {}

        for i in range(len(categories)):
            match_cat = re.search(self.search_string.get(), categories[i], flags=re.IGNORECASE)
            if match_cat:
                column = []
                column.append(categories[i])
                column.append(i)
                self.cats.append(column)
        
        for i in range(len(sub_categories)):
            for j in range(len(sub_categories[i])):
                match_cat = re.search(self.search_string.get(), sub_categories[i][j], flags=re.IGNORECASE)
                if match_cat:
                    column2 = []
                    column2.append(sub_categories[i][j])
                    #+"   ("+categories[i]+")")
                    column2.append(i)
                    column2.append(j)
                    self.sub_cats.append(column2)
                    self.parent_cat[sub_categories[i][j]] = categories[i] 

        self.category_listbox.delete(0, END)
       
        for i in range(len(self.cats)):
            self.category_listbox.insert(END, self.cats[i][0]) 
            self.category_listbox.itemconfig(END, {'bg':'skyblue'})

        for i in range(len(self.sub_cats)):
            self.category_listbox.insert(END, self.sub_cats[i][0]+"  ("+self.parent_cat[self.sub_cats[i][0]]+")")
            self.category_listbox.itemconfig(END, {'bg':'palegreen'})

        self.master.bind("<Return>", self.choose_cat2_gate2)


    def choose_cat2_gate2(self, event): #if through search_cat
        if self.category_listbox.curselection()[0] < len(self.cats):
            self.selection = self.cats[self.category_listbox.curselection()[0]][1]
            self.mika = self.cats[self.category_listbox.curselection()[0]][0]
            self.choose_cat2_gate2_bool = True
            self.choose_cat2()
        else:
            self.fill_data_gate2()


    def choose_cat2(self):
        #self.selection = self.category_listbox.curselection()[0] <-- we get this var either through choose_cat2_gate1 or gate2

        for widget in self.res_frame.winfo_children():
            widget.destroy()

        product_label = Label(self.res_frame, text=self.product)
        product_label.pack()

        scrollbar = Scrollbar(self.res_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.category_listbox2 = Listbox(self.res_frame, yscrollcommand=scrollbar.set, exportselection=False)

        for i in range(len(sub_categories[self.selection])):
            self.category_listbox2.insert(END, sub_categories[self.selection][i])

        self.category_listbox2.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.category_listbox2.yview)

        self.category_listbox2.selection_clear(0, END)
        self.category_listbox2.selection_set(0)

        self.res_frame.focus()
        self.category_listbox2.focus()

        self.master.unbind("<Up>")
        self.master.unbind("<Down>")
        self.master.bind("<Return>", self.fill_data_gate1)

    
    def fill_data_gate1(self, event): #if through search (but not when choosing sub_cat directly) or through choose_cat
        self.category_name = sub_categories[self.selection][self.category_listbox2.curselection()[0]]
        self.category_no = keys[self.category_name]
        
        if self.choose_cat2_gate2_bool == True:
            self.parent_cat_selection = self.mika
        else: self.parent_cat_selection = self.parent_cat2 
        
        self.choose_cat2_gate2_bool = False
        self.fill_data()


    def fill_data_gate2(self): #if through search (but only when choosing sub_cat directly)
        self.category_name = self.sub_cats[self.category_listbox.curselection()[0] - len(self.cats)][0] 
        self.category_no = keys[self.category_name]
        self.parent_cat_selection = self.parent_cat[self.category_name]
        self.fill_data()


    def fill_data_unknown_gate(self, event):
        self.category_name = "Unknown"
        self.category_no = "?\n"
        self.parent_cat_selection = ""
        self.fill_data()
        """
        output_array.insert(self.input_column.curselection()[0],"?\n")
        output_array.pop(self.input_column.curselection()[0]+1)
        print "No category at index = ", self.input_column.curselection()[0]
        self.update_output_array()
        """

    def fill_data(self):
        if self.auto.get() == True:
            self.fill_data_auto()
        else:
            self.fill_data_manual() 


    def copy(self, event):
        self.master.clipboard_clear()
        print self.outcomes_table.get(ACTIVE)
        self.master.clipboard_append(self.outcomes_table.get(ACTIVE))
        self.master.update()


    def fill_data_manual(self):
        for widget in self.res_frame.winfo_children():
            widget.destroy()

        product_label = Label(self.res_frame, text=self.product)
        serial_up_label = Label(self.res_frame, text=self.parent_cat_selection)
        serial_label = Label(self.res_frame, text=self.category_name)
        serial_number = Label(self.res_frame, text=self.category_no)

        self.regex = Label(self.res_frame, text="Search by pattern:")
        self.exp = StringVar()
        self.exp_entry = Entry(self.res_frame, textvariable=self.exp)

        self.outcomes_frame = Frame(self.res_frame)

        self.confirm_button = Button(self.res_frame, text="Confirm", command=lambda:self.confirm(self))

        product_label.pack()
        serial_up_label.pack()
        serial_label.pack()
        serial_number.pack()
        self.regex.pack()
        self.exp_entry.pack()
        self.exp_entry.focus()
        self.outcomes_frame.pack(expand=True, fill=BOTH)
        self.confirm_button.pack(side=BOTTOM)

        self.unbind_all()

        self.master.unbind("<BackSpace>")
        self.master.bind("<Shift-Return>", self.confirm)
        self.master.bind("<Return>", self.accept)
        self.master.bind("<q>", self.choose_cat2)


    def accept(self, event): 

        for widget in self.outcomes_frame.winfo_children():
            widget.destroy()

        reg_exp = self.exp_entry.get()

        #self.outcomes = {}
        #self.outcomes.clear()
            
        #can't use dict because of duplicates

        self.outcomes2 = [] #the 2-dim array containing [name, string] of every found entry (with regex)
        self.outcomes_table_ref = {}

        scrollbar = Scrollbar(self.outcomes_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.outcomes_table = Listbox(self.outcomes_frame, yscrollcommand=scrollbar.set, selectmode = MULTIPLE, exportselection=False)

        self.outcomes_table.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.outcomes_table.yview)

        for n in range(len(input_array)):

        	match_exp = re.search(reg_exp, input_array[n], flags=re.IGNORECASE)
                #raw_string = "%r"%input_array[n]
                raw_string = input_array[n]

		if match_exp:
                    if self.output_column.get(n) == self.category_no:
                        print input_array[n]," is already assigned to ",self.category_name
                    elif self.output_column.get(n) == "\n":
                        column = []
                        column.append(raw_string)
                        column.append(n)
                        self.outcomes2.append(column)
                        self.outcomes_table.insert(END, raw_string)
                    elif self.output_column.get(n) == "?\n":
                        column = []
                        column.append(raw_string)
                        column.append(n)
                        self.outcomes2.append(column)
                        
                        name_label = syek[self.output_column.get(n)] + ":   " + raw_string
                        self.outcomes_table.insert(END, name_label)
                       
                        #making future step-back reference:
                        self.outcomes_table_ref[self.outcomes_table.get(END)] = raw_string
                        self.outcomes_table.itemconfig(END, {'bg':'aliceblue'})
                    else:
                        column = []
                        column.append(raw_string)
                        column.append(n)
                        self.outcomes2.append(column)
                        
                        name_label = syek[self.output_column.get(n)] + ":   " + raw_string
                        self.outcomes_table.insert(END, name_label)
                       
                        #making future step-back reference:
                        self.outcomes_table_ref[self.outcomes_table.get(END)] = raw_string
                        self.outcomes_table.itemconfig(END, {'bg':'Rosy Brown'})
               
        self.master.bind("<Control-a>", self.select_all) 
        self.master.bind("<Control-d>", self.deselect_all)
        self.master.bind("<BackSpace>", self.focus_on_regex)
        self.master.bind("<Down>", self.focus_on_outcomes)
        self.master.bind("<Up>", self.focus_on_outcomes2)
        self.master.bind("<Shift-Return>", self.confirm)
        self.outcomes_table.bind('<s>', self.select)
        self.outcomes_table.bind('<d>', self.deselect)


    def select_all(self, event):
        self.outcomes_table.selection_set(0, END)


    def deselect_all(self, event):
        self.outcomes_table.selection_clear(0, END)


    def confirm(self, event): 
        print "Confirmed"
        selected = self.outcomes_table.curselection()
        self.indexes = []
        self.index_names = {}
        y = 0

        #iterating over the whole selection looking for index numbers
        for select in selected:
            
            for x in range(len(self.outcomes2)):
                
                outcome_uni = unicode(self.outcomes2[x][0], "utf-8")
                selected_uni = self.outcomes_table.get(select) #ALREADY UNICODE
                
                if self.outcomes_table.itemcget(select, 'bg') == 'Rosy Brown' or self.outcomes_table.itemcget(select, 'bg') ==  'aliceblue':
                    selected_uni = unicode(self.outcomes_table_ref[selected_uni], "utf-8")

                if outcome_uni == selected_uni:
                    self.indexes.append(self.outcomes2[x][1])
                    self.index_names[self.indexes[y]] = self.outcomes2[x][0]
                    y+=1

        print
        print "Chosen products: ", self.index_names
        print
        self.adding_changes()


    def adding_changes(self):
        #creating backup:
        self.undo_output_array = output_array[:]

        print
        print "Adding changes"
        for n, index in enumerate(self.indexes):
            if output_array[index] != "\n" and output_array[index] != "?\n" and str(self.category_no) != output_array[index]:
                print self.indexes
                self.are_you_sure(self.index_names[index],output_array[index],str(self.category_no), index)
                self.indexes.remove(index) 
                #self.adding_changes() <-- nested in are_you_sure
                break
            else:
                output_array.insert(index, str(self.category_no))
                output_array.pop(index+1)
                print "%r"%output_array[index], "at index = ", index
        self.update_output_array()
        
        try:
            self.select_next_action()
        except:
            print "Couldn't select_next()"
        try:
            self.select_unknown_action()
        except: 
            print "Couldn't select_unknown()"

        print


    def undo(self):
        global output_array
        output_array = self.undo_output_array[:]
        self.update_output_array()


    def are_you_sure(self, product, old_key, new_key, index):
        print
        print "Are you sure?"
        self.sure_window = Toplevel(self.master)
        self.sure_window.geometry("400x300")
        self.sure_window.wm_title(product)
        quest = "Do you want to replace the category\n\n"+syek[old_key]+"\n\nwith\n\n"+syek[new_key]+"?"
        self.sure_label = Label(self.sure_window, text=quest)
        self.answ_panel = Frame(self.sure_window)
        self.yes = Button(self.answ_panel, text="Yes", command=lambda:self.yes_i_am(new_key, index))
        self.no = Button(self.answ_panel, text="No", command=self.no_i_am_not)
        
        self.sure_label.pack()
        self.answ_panel.pack(side=BOTTOM)
        self.yes.pack(side=LEFT)
        self.no.pack(side=RIGHT)
        print

    
    def yes_i_am(self, new_key, index):
        print
        output_array.insert(index, str(self.category_no))
        output_array.pop(index+1)
        print "%r"%output_array[index], "at index = ", index
        self.update_output_array()
        self.sure_window.destroy()
        self.adding_changes()
        print


    def no_i_am_not(self):
        self.sure_window.destroy()
        self.adding_changes()


    def count_done(self, event):
        self.count()


    def count(self):
        count = 0
        total = 0
        for x in range(self.output_column.size()):
            if self.input_column.get(x)!=str(x)+":  " +"#N/A\n": 
                total+=1
            if self.output_column.get(x)!='\n':
                count+=1
        score = str(count) + " / " + str(total)
        self.done_label.configure(text="Done: "+score)


    def write_to(self):
        with open(self.name3.get(), 'w+') as file:
            for line in self.f3_array:
                file.write(line)


    def focus_on_search(self, event):
        try:
            self.res_frame.focus()
            self.category_listbox.focus()
        except:
            print "Can't focus_on_search()"


    def focus_on_search2(self, event):
        try:
            if self.category_listbox.curselection()[0] == 0:
                self.res_frame.focus()
                self.search_box.focus()
                self.search_entry.focus()
        except:
            print "Can't focus_on_search2()"


    def focus_on_outcomes(self, event):
        try:
            self.outcomes_frame.focus()
            self.outcomes_table.focus()
        except:
            print "Can't focus_on_outcomes()"


    def focus_on_outcomes2(self, event):
        if self.outcomes_table.index(ACTIVE) == 0:
            try: 
                self.outcomes_frame.focus()
                self.exp_entry.focus()
            except:
                print "Can't focus_on_outcomes2()"


    def focus_on_regex(self, event):
        if self.auto.get() == False:
            try:
                self.outcomes_frame.focus()
                self.exp_entry.focus()
            except:
                print "Can't focus_on_regex()"


    def select(self, event):
        self.outcomes_table.select_set(self.outcomes_table.index(ACTIVE))
        print(self.outcomes_table.get(ACTIVE))


    def deselect(self, event):
        self.outcomes_table.select_clear(self.outcomes_table.index(ACTIVE))


#AUTO_MODE METHODS
##########################################################################################
    
    def process_queue(self):
        try:
            self.result = self.queue.get(0)
        except Queue.Empty:
            self.master.after(100, self.process_queue)
    
    def closest_match(self, event):
        w1 = float(self.cat_w1.get())
        w2 = float(self.cat_w2.get())
        w3 = float(self.cat_w3.get())
    
        #MAKING JEDI IN A NEW THREAD:
        
        self.queue = Queue.Queue()
        JediThread(self.queue, self.yoda, self.input_column.curselection()[0],w1,w2,w3).start()
        self.master.after(100, self.process_queue)

        self.yoda.compare_products(self.input_column.curselection()[0], w1, w2, w3)
        similar_products = self.yoda.filter_products(0)
       
        
        similar_product = "None"

        for x in range(len(similar_products[0][1])): 
            key = output_data[similar_products[0][1][x][2]] 
            if key == '?\n' or key == '\n':
                continue
            else:
                similar_product = similar_products[0][1][x]
                break

        print
        print "Sliced product:"
        print similar_products[0][0][0], " index = ",
        print
        print "Closest match:"
        print similar_product
        print

        index = similar_product[2]

        self.mname.set(input_data[index])
        self.msim.set(similar_product[1])
        self.mcat.set(syek[output_data[index]])


    def complete_auto(self):#Function for assigning keys automatically
        #self.shrek.countdown(self.extent.get(), len(input_array))
       
        self.auto_count = 0

        for x in range(int(self.anchor), len(output_array)):
            if output_array[x] == "\n" or output_array[x] == "?\n" and input_array[x] != "#N/A\n":
                self.auto_count+=1

        for x in range(int(self.anchor), len(output_array)):
            if output_array[x] == "\n" or output_array[x] == "?\n" and input_array[x] != "#N/A\n":
                print x

                self.yoda.compare_products(x)
                simsarr = self.yoda.filter_products(0)

                #shrek = Jedi([input_array[x]], [output_array[x]], input_data, output_data)
                #simsarr = shrek.filter_products(float(self.extent.get()))
                print input_array[x], output_array[x]

                try:
                    for y in range(len(simsarr[0][1])):
                        if output_data[simsarr[0][1][y][2]] != "\n" and output_data[simsarr[0][1][y][2]] != "?\n": 
                            new_key = output_data[simsarr[0][1][y][2]]
                            p2 = simsarr[0][1][y][0]
                            sim = simsarr[0][1][y][1]
                            print simsarr[0][1][y]
                            break
                except UnboundLocalError:
                    print "There is no similar product in the following criterion"

                try:
                    self.select_next_action()
                except:
                    print "Couldn't select_next()"
                try:
                    self.select_unknown_action()
                except: 
                    print "Couldn't select_unknown()"

                self.would_you_kindly(input_array[x], output_array[x], new_key, x, sim, p2)
                break


    def super_lazy_mode(self):#Function for assigning keys super automatically 

        how_many = 0

        for x in range(self.input_column.index(ACTIVE),self.input_column.index(END)):
            if output_array[x] == "\n" or output_array[x] == "?\n" and input_array[x] != "#N/A\n":
                
                self.yoda.compare_products(x)
                simsarr = self.yoda.filter_products(float(self.extent.get()))
                
                self.new_key = "?\n"

                try:
                    for y in range(len(simsarr[0][1])):
                        """
                        print
                        print "n ?= ", output_data[simsarr[0][1][y][2]]
                        print "? ?= ", output_data[simsarr[0][1][y][2]] 
                        print "0.8 < ", simsarr[0][1][y][1]  
                        print
                        """
                        if output_data[simsarr[0][1][y][2]] != "\n" and output_data[simsarr[0][1][y][2]] != "?\n": #and simsarr[0][1][y][1] > 0.8:
                            self.new_key = output_data[simsarr[0][1][y][2]]
                            p2 = simsarr[0][1][y][0]
                            sim = simsarr[0][1][y][1]
                            print "MET CRITERION!"
                            print "Product index: ",x, ", Product: ",input_array[x]
                            print "Similar product: ", simsarr[0][1][y]
                            output_array.insert(x, self.new_key)
                            output_array.pop(x+1)
                            self.update_output_array()
                            how_many += 1
                            print how_many, " product(s) done"
                            break
                except UnboundLocalError:
                    print "There is no similar product in the following criterion"

                try:
                    self.select_next_action()
                except:
                    print "Couldn't select_next()"
                try:
                    self.select_unknown_action()
                except: 
                    print "Couldn't select_unknown()"

                #self.would_you_kindly(input_array[x], output_array[x], new_key, x, sim, p2)
        
        print "Super Lazy Mode finished"
        


    def would_you_kindly(self, product, old_key, new_key, index, sim, p2):
        print
        print "Would you kindly...?"
        self.would_window = Toplevel(self.master)
        self.would_window.geometry("600x400")
        self.would_window.title("Automatic Mode")
        self.would_window.wm_title(product)
        quest = "Would you kindly replace the category\n\n"+syek[old_key]+"\n\nwith\n\n"+syek[new_key]+"?"
        self.sure_label = Label(self.would_window, text=quest)
        self.product2_label = Label(self.would_window, text="Product = "+str(p2))
        self.sim_label = Label(self.would_window, text="Similarity = "+str(sim))
        self.answ_panel = Frame(self.would_window)
        self.products_left = Label(self.would_window, text=str(self.auto_count))
        self.yes = Button(self.answ_panel, text="Yes", command=lambda:self.yes_i_would(new_key, index))
        self.no = Button(self.answ_panel, text="No", command=self.no_i_would_not)
       
        self.sure_label.pack()
        self.product2_label.pack()
        self.sim_label.pack()
        self.answ_panel.pack(side=BOTTOM)
        self.yes.pack(side=LEFT)
        self.no.pack(side=RIGHT)
        self.products_left.pack(side=BOTTOM)
        print
               

    def yes_i_would(self, new_key, index):
        print
        print "%r"%new_key, "at index = ", index
        print
        
        output_array.insert(index, new_key)
        output_array.pop(index+1)
        self.update_output_array()
        self.would_window.destroy()
        self.complete_auto()


    def no_i_would_not(self):
        self.would_window.destroy()


    def fill_data_auto(self): 
     
        for widget in self.res_frame.winfo_children():
            widget.destroy()

        product_label = Label(self.res_frame, text=self.product)
        serial_up_label = Label(self.res_frame, text=self.parent_cat_selection)
        serial_label = Label(self.res_frame, text=self.category_name)
        serial_number = Label(self.res_frame, text=self.category_no)
       
        self.tresh_label = Label(self.res_frame, text="Probability Threshold Value")
        self.slider = Scale(self.res_frame, orient='horizontal', from_=0, to=100)
        self.slider.set(0)

        enter_button = Button(self.res_frame, text="Enter", command=lambda:self.accept_auto(self))
        self.outcomes_frame = Frame(self.res_frame)
        self.confirm_button = Button(self.res_frame, text="Confirm", command=lambda:self.confirm(self))

        self.fill_weight_label = Label(self.res_frame, text="Weights")
        self.fill_weight_frame = Frame(self.res_frame)
        self.fill_w1_label = Label(self.fill_weight_frame, text="Words = ")
        self.fill_w2_label = Label(self.fill_weight_frame, text="Numbers = ")
        self.fill_w3_label = Label(self.fill_weight_frame, text="Units = ")
        self.fill_w1 = StringVar()
        self.fill_w2 = StringVar()
        self.fill_w3 = StringVar()
        self.fill_w1_entry = Entry(self.fill_weight_frame, width=3, textvariable=self.fill_w1)
        self.fill_w2_entry = Entry(self.fill_weight_frame, width=3, textvariable=self.fill_w2)
        self.fill_w3_entry = Entry(self.fill_weight_frame, width=3, textvariable=self.fill_w3)
        self.fill_w1_label.pack(side=LEFT)
        self.fill_w1_entry.pack(side=LEFT)
        self.fill_w2_label.pack(side=LEFT)
        self.fill_w2_entry.pack(side=LEFT)
        self.fill_w3_label.pack(side=LEFT)
        self.fill_w3_entry.pack(side=LEFT)
        self.skip = BooleanVar()
        self.skip.set(True)
        self.skip_button = Checkbutton(self.res_frame, text="Skip Done", variable=self.skip)
        self.products_left = StringVar()
        self.products_left_label = Label(self.res_frame, textvariable = self.products_left)

        #original weights:
        self.fill_w1.set(2)
        self.fill_w2.set(1)
        self.fill_w3.set(1)
        
        product_label.pack()
        serial_up_label.pack()
        serial_label.pack()
        serial_number.pack()
        self.tresh_label.pack()
        self.slider.pack(fill=BOTH)
        self.fill_weight_label.pack()
        self.fill_weight_frame.pack()
        self.skip_button.pack()
        enter_button.pack()
        self.outcomes_frame.pack(expand=True, fill=BOTH)
        self.products_left_label.pack()
        self.confirm_button.pack(side=BOTTOM)

        self.unbind_all()

        self.master.unbind("<BackSpace>")

        self.master.bind("<Shift-Return>", self.confirm)
        self.master.bind("<Return>", self.accept_auto)
        self.master.bind("<q>", self.choose_cat2)
        self.master.bind("<Left>", self.shift_slider_left)
        self.master.bind("<Right>", self.shift_slider_right)


    def shift_slider_left(self, event):
        if self.slider.get() > 10:
            self.slider.set(self.slider.get()-10)
        else:
            self.slider.set(0)


    def shift_slider_right(self, event): 
        if self.slider.get() < 90:
            self.slider.set(self.slider.get()+10)
        else:
            self.slider.set(100)


    def accept_auto(self, event):
        print self.slider.get() 
        for widget in self.outcomes_frame.winfo_children():
            widget.destroy()

        if self.slider.get() != 100:
            threshold = float('0.'+str(self.slider.get()))
        else:
            threshold = 1.0

        y_w1 = float(self.fill_w1.get())
        y_w2 = float(self.fill_w2.get())
        y_w3 = float(self.fill_w3.get()) 

        self.yoda.compare_products(self.input_column.curselection()[0], y_w1, y_w2, y_w3, True)
        output = self.yoda.filter_products(threshold)
        
        #self.yadle = Jedi([input_array[self.input_column.curselection()[0]]], [output_array[self.input_column.curselection()[0]]], input_array, output_array, y_w1, y_w2, y_w3)
        #output = self.yadle.filter_products(threshold)

        print
        print "Closest product:"
        print output[0][1][0]
        print

        self.outcomes2 = [] #the 2-dim array containing [name, string] of every found entry (with auto)
        self.outcomes_table_ref = {}

        scrollbar = Scrollbar(self.outcomes_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.outcomes_table = Listbox(self.outcomes_frame, yscrollcommand=scrollbar.set, selectmode = MULTIPLE, exportselection=False)

        self.outcomes_table.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.outcomes_table.yview)

        """ TO-DO!!!
            elif self.output_column.get(index_no) == "#N/A\n" or self.output_column.get(index_no) == "#N/A\r\n":
                print "Line is empty"
        """
        for n in range(len(output[0][1])):
            index_no = output[0][1][n][2]

            if self.output_column.get(index_no) == self.category_no:
                print input_array[index_no], "is already assigned to ", self.category_name
            elif self.output_column.get(index_no) == "\n" and input_array[index_no] != "#N/A\n":
                column = []
                column.append(input_array[index_no])
                column.append(index_no)
                self.outcomes2.append(column)
                self.outcomes_table.insert(END, input_array[index_no])
            elif self.output_column.get(index_no) == "?\n" and input_array[index_no] != "#N/A\n":
                column = []
                column.append(input_array[index_no])
                column.append(index_no)
                self.outcomes2.append(column)
                
                name_label = syek[output_array[index_no]] + ":   " + input_array[index_no]
                self.outcomes_table.insert(END, name_label)
               
                self.outcomes_table_ref[self.outcomes_table.get(END)] = input_array[index_no]
                self.outcomes_table.itemconfig(END, {'bg':'aliceblue'})
            elif self.skip.get() != True:
                column = []
                column.append(input_array[index_no])
                column.append(index_no)
                self.outcomes2.append(column)

                name_label = syek[output_array[index_no]] + ":   " + input_array[index_no]
                self.outcomes_table.insert(END, name_label)

                self.outcomes_table_ref[self.outcomes_table.get(END)] = input_array[index_no]
                self.outcomes_table.itemconfig(END, {'bg':'Rosy Brown'})

        self.products_left.set(str(self.outcomes_table.index(END)) + " products")

        self.master.bind("<Control-a>", self.select_all) 
        self.master.bind("<Control-d>", self.deselect_all)
        self.master.bind("<BackSpace>", self.focus_on_regex)
        self.master.bind("<Down>", self.focus_on_outcomes)
        self.master.bind("<Up>", self.focus_on_outcomes2)
        self.master.bind("<Shift-Return>", self.confirm)
        self.outcomes_table.bind('<s>', self.select)
        self.outcomes_table.bind('<d>', self.deselect)
        self.master.bind("<Control-c>",self.copy)


#CORRECTION MODE METHODS
########################################################################################
#TO-DO:
#ADD BIND ON SPECIFIC LISTBOX

    def correct_mode(self):
        print
        print "You are now in the Correction Mode" 
        try:
            self.normal_mode_f.destroy()
        except:
            "There is no normal_mode instance yet"
        try:
            self.correct_mode_f.destroy()
        except:
            "There is no correct_mode instance yet"
        
        self.correct_mode_f = Frame(self.master)
    
        self.master.unbind("<Return>")    
        
        self.change_to_panel()
        self.change_from_panel()       

        self.master.bind("<Left>", self.left_panel)
        self.master.bind("<Right>", self.right_panel)
        print


    def change_from_panel(self):
        try:
            self.change_from.destroy()
        except:
            "There is no change_from instance yet"

        self.change_from = Frame(self.correct_mode_f)
        self.cf_label = Label(self.change_from, text="CHOOSE ITEMS FROM THE CATEGORY")

        self.cf_listbox = Frame(self.change_from)
        scrollbar = Scrollbar(self.cf_listbox)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.f_category_listbox = Listbox(self.cf_listbox, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(categories)):
            self.f_category_listbox.insert(END, categories[i])

        self.f_category_listbox.insert(0, "UNKNOWN")

        self.f_category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.f_category_listbox.yview)

        self.cf_label.pack()
        self.cf_listbox.pack(fill=BOTH, expand=True)
        self.change_from.pack(side=LEFT, fill=BOTH, expand=True)
        self.change_to.pack(side=RIGHT, fill=BOTH, expand=True)
        self.correct_mode_f.pack(fill=BOTH, expand=True)
        self.f_category_listbox.pack()

        self.change_from.focus()
        self.cf_listbox.focus()
        self.f_category_listbox.focus()
        
        self.f_category_listbox.bind("<Return>", self.f_choose_sub_cat)


    def change_to_panel(self):
        try:
            self.change_to.destroy()
        except:
            "There is no change_to instance yet"

        self.change_to = Frame(self.correct_mode_f)
        self.ct_label = Label(self.change_to, text="CHOOSE THEIR NEW CATEGORY")

        self.ct_listbox = Frame(self.change_to)
        scrollbar = Scrollbar(self.ct_listbox)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.t_category_listbox = Listbox(self.ct_listbox, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(categories)):
            self.t_category_listbox.insert(END, categories[i])

        self.t_category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.t_category_listbox.yview)

        self.ct_label.pack()
        self.ct_listbox.pack(fill=BOTH, expand=True)
        self.change_to.pack(side=LEFT, fill=BOTH, expand=True)
        self.correct_mode_f.pack(fill=BOTH, expand=True)
        self.t_category_listbox.pack()

        self.change_to.focus()
        self.ct_listbox.focus()
        self.t_category_listbox.focus()
        
        self.t_category_listbox.bind("<Return>", self.t_choose_sub_cat)
        

    def f_choose_sub_cat(self, event):        
        self.unknown_bool = False
        try:
            self.selection = self.f_category_listbox.curselection()[0]
        except:
            print "Variable self.selection is already set"

        if self.f_category_listbox.get(self.selection) == "UNKNOWN":
            self.unknown_bool = True
            self.f_fill_data()
        else:
            for widget in self.change_from.winfo_children():
                widget.destroy()

            self.cf_listbox = Frame(self.change_from)
            self.cf_label = Label(self.change_from, text="CHOOSE ITEMS FROM THE CATEGORY")
            
            scrollbar = Scrollbar(self.cf_listbox)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.f_category_listbox = Listbox(self.cf_listbox, yscrollcommand=scrollbar.set, exportselection=False)

            for i in range(len(sub_categories[self.selection-1])):
                self.f_category_listbox.insert(END, sub_categories[self.selection-1][i])

            self.f_category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
            scrollbar.config(command=self.f_category_listbox.yview)

            self.f_category_listbox.selection_clear(0, END)
            self.f_category_listbox.selection_set(0)
            
            self.cf_label.pack()
            self.cf_listbox.pack(fill=BOTH, expand=True)
            self.change_from.pack(side=LEFT, fill=BOTH, expand=True)
            self.change_to.pack(side=RIGHT, fill=BOTH, expand=True)
            self.correct_mode_f.pack(fill=BOTH, expand=True)
            self.f_category_listbox.pack()

            self.change_from.focus()
            self.cf_listbox.focus()
            self.f_category_listbox.focus()
            self.f_category_listbox.bind("<BackSpace>", self.change_from_panel_key)
            self.f_category_listbox.bind("<Return>", self.f_fill_data_gate)


    def f_fill_data_gate(self, event):
        self.f_fill_data()

    def f_fill_data(self):
        try:
            self.f_fin_sel = self.f_category_listbox.curselection()[0]
            print sub_categories[self.selection-1][self.f_fin_sel]
        except:
            print "UNKNOWN"

        for widget in self.change_from.winfo_children():
            widget.destroy()

        self.cf_listbox = Frame(self.change_from)
        self.cf_label = Label(self.change_from, text="CHOOSE ITEMS FROM THE CATEGORY")
        
        scrollbar = Scrollbar(self.cf_listbox)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.f_category_listbox = Listbox(self.cf_listbox, yscrollcommand=scrollbar.set, selectmode = MULTIPLE, exportselection=False)
        self.f_cat_output = []

        
        self.f_category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.f_category_listbox.yview)

        self.f_makelist()

        self.f_category_listbox.selection_clear(0, END)
        self.f_category_listbox.selection_set(0)
        
        self.cf_label.pack()
        self.cf_listbox.pack(fill=BOTH, expand=True)
        self.change_from.pack(side=LEFT, fill=BOTH, expand=True)
        self.change_to.pack(side=RIGHT, fill=BOTH, expand=True)
        self.correct_mode_f.pack(fill=BOTH, expand=True)
        self.f_category_listbox.pack()

        self.change_from.focus()
        self.cf_listbox.focus()
        self.f_category_listbox.focus()
        self.f_category_listbox.bind("<BackSpace>", self.f_choose_sub_cat)
        self.f_category_listbox.bind("<s>", self.corr_select)
        self.f_category_listbox.bind("<d>", self.corr_deselect)
        self.master.bind("<Shift-Return>", self.corr_accept)
    

    def f_makelist(self):
        self.f_category_listbox.delete(0, END)
        if self.unknown_bool == True:
            for i in range(len(output_array)):
                if output_array[i] == "?\n" and input_array[i] != "#N/A\n":
                    row = [] #index of the output in the list|index of actual product in the input_array
                    row.append(self.f_category_listbox.index(END))
                    row.append(i)
                    self.f_cat_output.append(row)
                    self.f_category_listbox.insert(END, input_array[i])
        else:
            for i in range(len(output_array)):
                if output_array[i] == keys[sub_categories[self.selection-1][self.f_fin_sel]]:
                    row = [] #index of the output in the list|index of actual product in the input_array
                    row.append(self.f_category_listbox.index(END))
                    row.append(i)
                    self.f_cat_output.append(row)
                    self.f_category_listbox.insert(END, input_array[i])


    def corr_accept(self, event):
        print "Confirmed"
        selected = self.f_category_listbox.curselection()
        self.indexes = []
        self.index_names = {}
        y = 0

        for select in selected:
            for index in self.f_cat_output:
                if index[0] == select:
                    print 
                    print "index[0] = ", index[0]
                    print "index[1] = ", index[1]
                    print "select = ", select
                    print "self.f_category_listbox.get(index[0]) = ", self.f_category_listbox.get(index[0])
                    print "self.t_category_listbox.get(ACTIVE) = ", self.t_category_listbox.get(ACTIVE)
                    print
                   
                    try:
                        output_array.insert(index[1], keys[self.t_category_listbox.get(ACTIVE)])
                        output_array.pop(index[1]+1)
                        print "%r"%self.t_category_listbox.get(ACTIVE), "at index = ", index[1]
                    except:
                        print "Choose the right category"

        self.f_makelist()


    def t_choose_sub_cat(self, event):        
        self.selection = self.t_category_listbox.curselection()[0]

        for widget in self.change_to.winfo_children():
            widget.destroy()

        self.ct_listbox = Frame(self.change_to)
        self.ct_label = Label(self.change_to, text="CHOOSE THEIR NEW CATEGORY")
        
        scrollbar = Scrollbar(self.ct_listbox)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.t_category_listbox = Listbox(self.ct_listbox, yscrollcommand=scrollbar.set, exportselection=False)

        for i in range(len(sub_categories[self.selection])):
            self.t_category_listbox.insert(END, sub_categories[self.selection][i])

        self.t_category_listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.t_category_listbox.yview)

        self.t_category_listbox.selection_clear(0, END)
        self.t_category_listbox.selection_set(0)
       
        self.ct_label.pack()
        self.ct_listbox.pack(fill=BOTH, expand=True)
        self.change_to.pack(side=RIGHT, fill=BOTH, expand=True)
        self.correct_mode_f.pack(fill=BOTH, expand=True)
        self.t_category_listbox.pack()

        self.change_to.focus()
        self.ct_listbox.focus()
        self.t_category_listbox.focus()
        self.t_category_listbox.bind("<BackSpace>", self.change_to_panel_key)

    
    def change_from_panel_key(self, event): 
        self.change_from_panel()


    def change_to_panel_key(self, event): 
        self.change_to_panel()


    def left_panel(self, event):
        self.correct_mode_f.focus()
        self.change_from.focus()
        self.cf_listbox.focus()
        self.f_category_listbox.focus()


    def right_panel(self, event):
        self.correct_mode_f.focus()
        self.change_from.focus()
        self.ct_listbox.focus()
        self.t_category_listbox.focus()


    def corr_select(self, event):
        self.f_category_listbox.select_set(self.f_category_listbox.index(ACTIVE))
        print(self.f_category_listbox.get(ACTIVE))


    def corr_deselect(self, event):
        self.f_category_listbox.select_clear(self.f_category_listbox.index(ACTIVE))

#OTHER FUNCTIONS
################################################################################################

def regex(exp,number):
	for n in range(len(input_array)):
		val = None
		match_exp = re.search(exp, input_array[n], flags=re.IGNORECASE)
		if match_exp:
			val = number
                save_value_to_array(val, n)


def read_files(input_file = input_src, output_file = output_src):
    global input_array
    global output_array

    del input_array[:]
    del output_array[:]

    with open(input_file, 'r') as file:
        for line in file:
            input_array.append(line)
    with open(output_file, 'r') as f:
        for line in f:
            output_array.append(line)
    with open(cat_src, 'r') as f:
        for line in f:
            cat_array.append(line)
    with open(key_src, 'r') as f:
        for line in f:
            key_array.append(line)

"""
    if len(output_array) != len(input_array):
            output_array = [None]
            output_array = [ "\n" for y in range( len(input_array) ) ]
            print len(output_array), len(input_array)
"""

def prepare_database(input_file = input_data_src, output_file = output_data_src): 
    
    global input_data
    global output_data

    del input_data[:]
    del output_data[:]

    with open(input_file, 'r') as file:
        for line in file:
            input_data.append(line)
    with open(output_file, 'r') as f:
        for line in f:
            output_data.append(line)
"""
    if len(output_data) != len(input_data):
            output_data = [None]
            output_data = [ "\n" for y in range( len(input_data) ) ]
            print len(output_data), len(input_data)
"""

def save_array_to_file(input_file = input_src, output_file = output_src):
        with open(input_file, "w") as f:
            for _ in range(len(input_array)):
                f.write(str(input_array[_]))
	with open(output_file, "w") as f:
	    for _ in range(len(output_array)):
		f.write(str(output_array[_]))


#MAIN
################################################################################################

def main():
    read_files()
    root = Tk()
    root.geometry("800x600")
    app = GUI(root)
    root.mainloop()
    
main()
