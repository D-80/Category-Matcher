import re
from bs4 import BeautifulSoup
try:
    from Tkinter import * 
except ImportError: 
    from tkinter import *


input_array = []
output_array = []
cat_array = []
key_array = []
categories = {} #categories[n] to get name of the row in sub_categories
sub_categories = [] #multidimensional array of sub_categories 
keys = {} #keys[category_name] to get category number from its name
syek = {} #syek[self.output_column[n]] to get category name from its number

cat_file = "cat.txt"
key_file = "key.txt"


def load_page(page_addr):
    with open(page_addr) as fp:
        soup = BeautifulSoup(fp)
    soup = BeautifulSoup("<hrml>data</html>")


def regex(exp,number):
	for n in range(len(input_array)):
		val = None
		match_exp = re.search(exp, input_array[n], flags=re.IGNORECASE)
		if match_exp:
			val = number
                save_value_to_array(val, n)


def read_files(input_file, output_file):
    global output_array

    del input_array[:]
    del output_array[:]

    with open(input_file, 'r') as file:
        for line in file:
            input_array.append(line)
    with open(output_file, 'r') as f:
        for line in f:
            output_array.append(line)
    with open(cat_file, 'r') as f:
        for line in f:
            cat_array.append(line)
    with open(key_file, 'r') as f:
        for line in f:
            key_array.append(line)

    if len(output_array) != len(input_array):
            output_array = [None]
            output_array = [ "\n" for y in range( len(input_array) ) ]
            print len(output_array), len(input_array)


def save_array_to_file(output_file):

	with open(output_file, "w") as f:
		for _ in range(len(output_array)):
			f.write(str(output_array[_]))

class GUI(Frame):

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
        print "Shift + N key: Jump to the next unclasified product"
        print "Shift + U key: Assign category Unknown" 
        print "S key: Select in the Regex Panel"
        print "D key: De-select in the Regex Panel"
        print "Home: Copy from the output_array into the output.txt file"
        print "F1: Open the Guidelines Window"
        print
        print

        #top menu
        
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu)
        file_menu.add_command(label="Load Output", command=lambda:self.load_output_window(self))
        file_menu.add_command(label="Save Output as", command=lambda:self.save_as_window(self))
        file_menu.add_command(label="Save Output as output.txt (Home)", command=lambda:self.save(self))
        file_menu.add_command(label="Merge Outputs", command=self.merge_outputs_window)
        file_menu.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file_menu)
        
        edit_menu = Menu(menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        menu.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menu)
        help_menu.add_command(label="Guidelines (F1)", command=self.guidelines)
        menu.add_cascade(label="Help", menu=help_menu)
        
    #LAYOUT
        #main_frame
        main_frame = Frame(self.master)

        scrollbar = Scrollbar(main_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.done_panel = Frame(main_frame)
        self.done_label = Label(self.done_panel, text="Done:")
        self.done_button = Button(self.done_panel, text="Update", command=lambda:self.count_done(self))
        self.anchor_label = Button(self.done_panel, text="Set anchor to: ", command=self.set_anchor)
        self.anchor = 0
        self.anchor_text = StringVar()
        self.anchor_entry = Entry(self.done_panel, text=self.anchor_text)
        self.anchor_entry.pack(side=RIGHT)
        self.anchor_label.pack(side=RIGHT)
        self.done_button.pack(side=RIGHT)
        self.done_label.pack(side=RIGHT)
        self.done_panel.pack(side=TOP)
        self.load_anchor()

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
        
        #input/categories/output_column
        self.input_column = Listbox(main_frame, yscrollcommand=scrollbar.set)
        for i in range(len(input_array)):
            self.input_column.insert(END, str(i) + ":  " + input_array[i])
        self.input_column.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.categories_column = Listbox(main_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(input_array)):
            self.categories_column.insert(END, syek[output_array[i]])
        self.categories_column.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.output_column = Listbox(main_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(input_array)):
            self.output_column.insert(END, output_array[i])
        self.output_column.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        
        scrollbar.config(command=self.scroll)

        #pack
        main_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        #results
        self.res_frame = Frame(self.master)
        self.res_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        self.pack()

        """
        #category menu
        self.e = ''
        self.cat_menu = Menu(self.master)
        self.cat_menu.add_command(label="Exit", command=self.cat_menu.grab_release())
        self.cat_menu.add_command(label="Add Category", command=self.add_category)
        """
        self.count_done(self)
        main_frame.focus()
        self.input_column.focus()
        self.key_bindings()
        
    def key_bindings(self):
        self.master.bind("<Return>", self.choose_cat)
        self.master.bind("<Home>", self.save)
        self.master.bind("<Shift-N>", self.select_next)
        self.master.bind("<Shift-U>", self.unknown)
        self.master.bind("<Shift-BackSpace>", self.choose_cat)
        self.master.bind("<F1>", self.guidelines_hotkey)

    
    def unbind_all(self):

        self.master.unbind("<Down>")
        self.master.unbind("<Shift-Return>")
        self.master.unbind("<n>")
        self.master.unbind('<s>')
        self.master.unbind('<d>')

    
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

        product_label = Label(self.res_frame, text=self.product)
        product_label.pack()

        self.search_box = Frame(self.res_frame)
        self.search_label = Label(self.search_box, text="Search: ")
        self.search_string = StringVar()
        self.search_entry = Entry(self.search_box, text=self.search_string)

        self.search_label.pack(side=LEFT)
        self.search_entry.pack(side=RIGHT)
        self.search_box.pack()

        scrollbar = Scrollbar(self.res_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.category_listbox = Listbox(self.res_frame, yscrollcommand=scrollbar.set, exportselection=False)
        for i in range(len(categories)):
            self.category_listbox.insert(END, categories[i])

        #self.category_listbox.insert(END, "NOT EVEN CLOSE")

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


    def choose_cat2_gate1(self, event): #if through choose_cat
        self.selection = self.category_listbox.curselection()[0]
        self.parent_cat2 = self.category_listbox.get(self.category_listbox.curselection()[0])
        self.choose_cat2()


    def search_cat(self, event):
        print self.search_string.get()

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
        print(self.category_listbox.size())
        print(self.selection)

        """
        if self.category_listbox.size() > 1 and self.selection == self.category_listbox.size()-1:
            output_array.insert(self.input_column.curselection()[0],"?\n")
            output_array.pop(self.input_column.curselection()[0]+1)
            print "No category at index = ", self.input_column.curselection()[0]
            self.update_output_array()
        """
        
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


    def fill_data(self):
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

        self.confirm_button = Button(self.res_frame, text="Confirm", command= lambda:self.confirm(self))

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

        scrollbar = Scrollbar(self.outcomes_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.outcomes_table = Listbox(self.outcomes_frame, yscrollcommand=scrollbar.set, selectmode = MULTIPLE, exportselection=False)

        self.outcomes_table.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.outcomes_table.yview)

        for n in range(len(input_array)):

        	match_exp = re.search(reg_exp, input_array[n], flags=re.IGNORECASE)
                raw_string = "%r"%input_array[n]

		if match_exp:
                    if self.output_column.get(n) == self.category_no:
                        print input_array[n]," is already assigned to ",self.category_name
                    elif self.output_column.get(n) == "\n":
                        column = []
                        column.append(raw_string)
                        column.append(n)
                        self.outcomes2.append(column)
                        self.outcomes_table.insert(END, raw_string)
                    else:
                        column = []
                        column.append(raw_string)
                        column.append(n)
                        self.outcomes2.append(column)
                        self.outcomes_table.insert(END, syek[self.output_column.get(n)]+":   "+raw_string)
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
        print "confirm"
        selected = self.outcomes_table.curselection()
        self.indexes = []
        self.index_names = {}
        y = 0

        #iterating over the whole selection looking for index numbers
        for select in selected:
            for x in range(len(self.outcomes2)):
                if self.outcomes2[x][0] == self.outcomes_table.get(select):
                    self.indexes.append(self.outcomes2[x][1])
                    self.index_names[self.indexes[y]] = self.outcomes2[x][0]
                    y+=1

        self.adding_changes()


    def adding_changes(self):
        #creating backup:
        self.undo_output_array = output_array[:]
        print(self.undo_output_array[0])

        print "adding changes"
        for n, index in enumerate(self.indexes):
            if output_array[index] != "\n" and str(self.category_no) != output_array[index]:
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

    
    def update_output_array(self):#<---really it's update_output_column
        print "updating output column"
        #print "old output column size = ", self.output_column.size()
        self.output_column.delete(0, self.output_column.size())
        for i in range(len(input_array)):
            self.output_column.insert(END, output_array[i])
        self.output_column.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        #print "new output column size = ", self.output_column.size()
        
        self.categories_column.delete(0, self.categories_column.size())
        for i in range(len(input_array)):
            self.categories_column.insert(END, syek[output_array[i]])
        self.categories_column.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.count()
        self.select_next_action()
        self.choose_cat_action()

    
    def undo(self):
        global output_array
        output_array = self.undo_output_array[:]
        self.update_output_array()


    def are_you_sure(self, product, old_key, new_key, index):
        print "are you sure?"
        self.sure_window = Toplevel(self.master)
        self.sure_window.geometry("400x300")
        self.sure_window.wm_title(product)
        quest = "Do you want to replace the category\n\n"+syek[old_key]+"\n\nwith\n\n"+syek[new_key]+"?"
        self.sure_label = Label(self.sure_window, text=quest)
        self.answ_panel = Frame(self.sure_window)
        self.yes = Button(self.answ_panel, text="Yes", command=lambda:self.yes_i_am(new_key, index))
        self.no = Button(self.answ_panel, text="No", command=self.fuck_off)
        
        self.sure_label.pack()
        self.answ_panel.pack(side=BOTTOM)
        self.yes.pack(side=LEFT)
        self.no.pack(side=RIGHT)

    
    def yes_i_am(self, new_key, index):
        output_array.insert(index, str(self.category_no))
        output_array.pop(index+1)
        print "%r"%output_array[index], "at index = ", index
        self.update_output_array()
        self.sure_window.destroy()
        self.adding_changes()


    def fuck_off(self):
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


    def save_anchor(self):
        with open("anchor.txt", 'w+') as file:
            file.write(self.anchor)
            file.seek(0)
            print "Anchor position saved to ", self.anchor


    def load_anchor(self):
        with open("anchor.txt", 'r') as file:
            self.anchor = file.read()
            print "Anchor position is ", self.anchor


    def save_action(self):
        save_array_to_file("output.txt")
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
        f = open(self.file_name.get(), "w+")
        save_array_to_file(self.file_name.get())
        f.close()
        print("Progress Saved")


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
            read_files("input.txt",self.load_entry.get())
            loaded = True
        except IOError:
            print "I hate to say it, but it looks like the system you're searching for doesn't exist." 
            loaded = False
        if loaded == True:
            print "File ",self.load_entry.get()," successfully loaded"
            self.popup_window.destroy()
        self.update_output_array()
    

    def guidelines_hotkey(self, event):
        self.guidelines()


    def guidelines(self):
        with open("guidelines.txt", 'r') as file:
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

#all good up to this point



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
                    self.key1 = syek[self.f1_array[x][:-2]+"\n"]#OK
                else:
                    self.key1 = syek[self.f1_array[x]] #OK
                if self.var2.get() == 1: #SAME FOR THE FILE2
                    self.key2 = syek[self.f2_array[x][:-2]+"\n"]#OK
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

        """        else: #IN EVERY OTHER CASE
                    self.choose_wisely(input_array[x], self.f1_array[x], self.f2_array[x], x) #OK
                    break
        """

    def choose_wisely(self, product, old_key, new_key, index): #NEW KEY = self.f1_array[], OLD KEY = self.f2_array[], index = x from compare_files
       
        if len(self.f3_array) == len(self.f1_array): #OK 
            self.write_to()
            print "Merge finished"#+
        else: 
            print "Choose wisely"
            print "Windows format f1 = ",self.var1.get(), " f2 = ",self.var2.get()
            
            print "Index = ",index

            """
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
            """
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


    def write_to(self):

        with open(self.name3.get(), 'w+') as file:
            for line in self.f3_array:
                file.write(line)


    def focus_on_search(self, event):
        self.res_frame.focus()
        self.category_listbox.focus()


    def focus_on_search2(self, event):
        if self.category_listbox.curselection()[0] == 0:
            self.res_frame.focus()
            self.search_box.focus()
            self.search_entry.focus()


    def focus_on_outcomes(self, event):
        self.outcomes_frame.focus()
        self.outcomes_table.focus()


    def focus_on_outcomes2(self, event):
        if self.outcomes_table.index(ACTIVE) == 0:
            self.outcomes_frame.focus()
            self.exp_entry.focus()


    def focus_on_regex(self, event):
        self.outcomes_frame.focus()
        self.exp_entry.focus()


    def select(self, event):
        self.outcomes_table.select_set(self.outcomes_table.index(ACTIVE))

        print(self.outcomes_table.get(ACTIVE))
        for x in range(len(self.outcomes2)):
            if self.outcomes2[x][0] == self.outcomes_table.get(ACTIVE):
                print self.outcomes2[x][1]


    def deselect(self, event):
        self.outcomes_table.select_clear(self.outcomes_table.index(ACTIVE))



def main():

    read_files("input.txt", "output.txt")
    root = Tk()
    root.geometry("800x600")
    app = GUI(root)
    root.mainloop()

main()



""" GARBAGE

    def enter(self, event):
        selection = self.input_column.curselection() 
        print(selection[0])
        try:
            self.cat_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.cat_menu.grab_release()

    def enter_cat(self, event):
        self.e = self.entry.get()
        categories.append(self.e)

        self.sub_menu = Menu(self)
        self.sub_menu.add_command(label="Exit", command=self.cat_menu.grab_release())
        self.sub_menu.add_command(label="Add Category", command=self.add_sub_cat)
        self.cat_menu.add_cascade(label=str(categories[-1]), menu=self.sub_menu)
        
        self.popup_window.destroy()
        print(categories)

        
    def add_category(self):
        self.popup_window = Toplevel()
        self.label = Label(self.popup_window, text="Enter the category name:")
        self.label.pack()
        self.entrytext = StringVar()
        self.entry = Entry(self.popup_window, textvariable=self.entrytext)
        self.entry.pack()
        self.entry.focus()
        self.popup_window.bind("<Return>", self.enter_cat)


    def enter_sub_cat(self, event):
        if(self.entry2.get() != "" and self.entry22.get() != ""):
            sub_categories[self.entry2.get()] = self.entry22.get()
            self.sub_menu.add_command(label=self.entry2.get()+" ("+self.entry22.get()+")", command=self.fill_data) 
            self.popup_window2.destroy()
            print(sub_categories)
        elif(self.entry2.get() != ""):
            self.entry22.focus()
        else:
            print("Enter value")


    def add_sub_cat(self): 
        self.popup_window2 = Toplevel()
        self.label2 = Label(self.popup_window2, text="Enter the sub-category name:")
        self.label2.pack()
        self.entrytext2 = StringVar()
        self.entry2 = Entry(self.popup_window2, textvariable=self.entrytext2)
        self.entry2.pack()
        self.entry2.focus()
        
        self.label22 = Label(self.popup_window2, text="Enter the sub-category key:")
        self.label22.pack()
        self.entrytext22 = StringVar()
        self.entry22 = Entry(self.popup_window2, textvariable=self.entrytext22)
        self.entry22.pack()

        self.popup_window2.bind("<Return>", self.enter_sub_cat)
"""
