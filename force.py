try:
    import stopwatch
except ImportError:
    print "Couldn't import stopwatch"
try:
    from copy import deepcopy
except ImportError:
    print "Couldn't import deepcopy"
try:
    import re
except ImportError:
    print "Couldn't import re"
try:
    from Tkinter import * 
except ImportError: 
    from tkinter import *
except:
    print "Couldn't load tkinter module"


#TEST DATASET:
#Undone:
tu_nam = ['WAFELKI 8X20x8G']
tu_key = ['?']
#Done:
td_nam = ['LIPA 20X1x8G']
td_key = ['131']


class Jedi:
    #TO-DO: 
    """
    Rearrange the whole module to make slicin' and sizin' completely independent. 
    Optimize wherever possible. 

    """

    """
    THE AWSOME DESCRIPTION:
    Size of the list doesn't matter. He'll slice it and size it up for you

    Yoda takes two lists as parameters and compares all items in the first one
    to all items in the second one. He produces a few multi-dimensional arrays
    as a result:

    u_arr = input array of undone items 
    d_arr = input array of done items (with asigned keys)
    sims = output array of items with assigned similarity
   
    NOTE:
    If you want to compare just one product to another list of products remember to put it 
    as a first parameter in a list, eg. ["Knorr zupa"]

    """
    def __init__(self, u_nam = tu_nam, u_key = tu_key, d_nam = td_nam, d_key = td_key):
        """
        u_nam = list of undone products names, u_key = list of undone products corresponding keys
        Same goes for d_nam and d_key
        If no arguments specified he will work on the test dataset

        """
        print
        print "New Jedi"

        #Passing parameters:
        self.u_nam = u_nam 
        self.u_key = u_key 
        self.d_nam = d_nam
        self.d_key = d_key
        
        #CORE YODA ITEMS:
            #INPUT:
        self.u_arr = [] #our undone_array[index[0 = name, 1 = key]]
        self.d_arr = [] #our done_array[index[0 = name, 1 = key]] 
        #d_arr can be the same as u_arr if you want to compare products from the same set
            #WEIGHTS:
        self.w1 = 0
        self.w2 = 0
        self.w3 = 0

            #OUTPUT:
        self.slic_u_arr = []#array of sliced products which need to be finished 
        self.slic_d_arr = []#array of products in the database (with assigned categories)
        self.sims = [] 
        #array produced as a result of comparing each product in u_arr to each product in d_arr. 
        #[x] - index of item in u_arr
        #[x][0] - that item properties
        #[x][0][0] - sliced name of that item (String)
        #[x][1] - all compared items
        #[x][1][y] - index of object which we compare to 
        #[x][1][y][0] - sliced name of that item (String)
        #[x][1][y][1] - similarity (Float)
        #[x][1][y][2] - index of that item (Int)


        #Filling items with data:
        self.fill_arrs() #fill data arrays 
        self.slice_products() #fill slic_ arrays
        
        print "Members in the dataset: ", len(self.u_arr)
        print "Members in the database: ", len(self.d_arr)
        print
        

    def countdown(self, extent, n_of_products):
        del self.u_arr[:]
        del self.d_arr[:]

        time = stopwatch.Timer()
        self.fill_arrs()
        print
        print "Elapsed time for fill_ars = ", time.elapsed
        print "Number of item(s) compared: ", len(self.u_arr), "Number of items in the dataset: ", len(self.d_arr)
        mark = time.elapsed
        self.compare_products(self.u_arr, self.d_arr)
        print "Elapsed time for compare_products = ", time.elapsed-mark
        mark = time.elapsed
        self.filter_products(extent)
        print "Elapsed time for filter_products = ", time.elapsed-mark
        time.stop()
        print "Elapsed time for 1 product = ", time.elapsed
        print "Elapsed time for ", n_of_products, " products = ", time.elapsed*n_of_products
        print


    def fill_arrs(self):
        for index in range(len(self.d_nam)): 
            column = []
            try:
                column.append(self.d_nam[index])
                column.append(self.d_key[index])
            except IndexError:
                print "Size of d_key doesn't match d_nam"
            self.d_arr.append(column)

        for index in range(len(self.u_nam)): 
            column = []
            try:
                column.append(self.u_nam[index])
                column.append(self.u_key[index])
            except IndexError:
                print "Size of u_key doesn't match u_nam"
            self.u_arr.append(column)

        """
        print
        print "Undone array = ", self.u_arr
        print "Size = ", len(self.u_arr)
        print
        print "Done array = ", self.d_arr
        print "Size = ", len(self.d_arr)
        print
        """

    def slice_string(self, u_str):        
        #print
        #EXAMPLE: J.D.SMOOTH ORIG BBQ SAUCE260g 300
        #print "Original expression: ", u_str

        slice_arr = []

        #Find the number and unit expressions in the string
        num_str = re.findall(r"\d[\w]*", u_str)
        num_str = ''.join(num_str)
        
        numbers = re.findall(r"[\d]+", num_str)
        units = re.findall(r"[\D]+", num_str)


        #Substract the num_str and add leftovers to a single str
        rest_str = re.split(r"\d[\w]*", u_str)
        rest_str = ''.join(rest_str)

        #Find all seperate words in the remaining str
        #words = re.findall(r"[^\.\ ]+", rest_str)
        words = re.findall(r"[\w]+", rest_str)

        #Add all expressions to slice_arr
        slice_arr.append(words)
        slice_arr.append(numbers)
        slice_arr.append(units)
        #print "Sliced string: ", slice_arr
        #RESULT: ['J','D','SMOOTH','ORIG','BBQ','SAUCE',['260g','300',['g'],[]]]
        #print
        return slice_arr


    def compare_slice(self, array1, array2): 
        #Compare each part of product (word, number, unit)
        similarities = 0 #similarities of each part summed up

        #print "arrays = ", array1, array2
        #print "len = ", len(array1), len(array2)

        if len(array1) > len(array2):#check which slice is bigger - it will be always in the denominator
            n_of_words = len(array1)
        else:
            n_of_words = len(array2)

        for word1 in array1: 
            for word2 in array2:
                #Check which word is bigger to avoid different results for different orderings
                if len(word1) < len(word2):
                    match = re.search(word1, word2, flags=re.IGNORECASE)
                    if match and match.start() == 0:
                        comp = float(len(word1))/len(word2) #similarity of ind. part
        
                        if comp > 1:
                            print "Error while comparing:"
                            print array1
                            print array2
                            print "(if)Compability > 1"

                        similarities += comp
                        break #to avoid repetitions
                else:
                    match = re.search(word2, word1, flags=re.IGNORECASE)
                    if match and match.start() == 0:
                        comp = float(len(word2))/len(word1)

                        if comp > 1:
                            print "Error while comparing:"
                            print array1
                            print array2
                            print "(else)Compability > 1"

                        similarities += comp
                        break

        similarity = similarities/(n_of_words)
        
        return similarity


    def compare_2_products(self, u_slic_str, d_slic_str, weight1 = None, weight2 = None, weight3 = None):
        #print
        #print "Calculating Similarity:"
        #Compare each slice (words, numbers, units) in any 2 products
        similarity = 0
        words = True
        numbers = True
        units = True

        try:
            sim1 = self.compare_slice(u_slic_str[0], d_slic_str[0]) #Words
        except:
            #print "The product has no words"
            sim1 = 0
            words = False
        try:
            sim2 = self.compare_slice(u_slic_str[1], d_slic_str[1]) #Numbers
        except:
            #print "The product has no numbers"
            sim2 = 0
            numbers = False
        try:
            sim3 = self.compare_slice(u_slic_str[2], d_slic_str[2]) #Units
        except:
            #print "The product has no units"
            sim3 = 0
            units = False
       
        #Weights(Words, Numbers, Units)
        if words:
            if weight1 != None:
                w1 = weight1
            elif len(u_slic_str[0]) > len(d_slic_str[0]): #The product which has more words adds more to the weights
                w1 = len(u_slic_str[0])
            else:
                w1 = len(d_slic_str[0])
        else:
            w1 = 0

        if numbers:
            if weight2 != None:
                w2= weight2
            elif len(u_slic_str[1]) > len(d_slic_str[1]): #The product which has more numbers adds more to the weights
                w2 = len(u_slic_str[1])
            else:
                w2 = len(d_slic_str[1])
        else:
            w2 = 0
        
        if units:
            if weight3 != None:
                w3 = weight3
            elif len(u_slic_str[2]) > len(d_slic_str[2]): #The product which has more units adds more to the weights
                w3 = len(u_slic_str[2])
            else:
                w3 = len(d_slic_str[2])
        else:
            w3 = 0

        similarity = (sim1*w1 + sim2*w2 + sim3*w3) / float(w1+w2+w3)

        """ 
        print "Similarities: sim1 = ", sim1, ", sim2 = ", sim2, ", sim3 = ", sim3
        print "Weights: w1 = ", w1, ", w2 = ",  w2, ", w3 = ", w3
        print "Similarities with weights: sim1 = ", sim1*w1, ", sim2 = ", sim2*w2, ", sim3 = ", sim3*w3
        print "Similarity = ", similarity
        print
        """

        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
    
        return similarity


    def slice_products(self):
        print "Slicin' products"
        for x in range(len(self.u_arr)):
            u_item_row = []
            u_item = self.slice_string(self.u_arr[x][0])
            u_item_row.append(u_item)
            u_item_row.append(x)
            self.slic_u_arr.append(u_item_row)
        
        for x in range(len(self.d_arr)):
            d_item_row = []
            d_item = self.slice_string(self.d_arr[x][0])
            d_item_row.append(d_item)
            d_item_row.append(x)
            self.slic_d_arr.append(d_item_row)
        """
        print "Outcome:"
        print self.slic_u_arr[0:10]
        print
        print self.slic_d_arr[0:10]
        """

    def compare_products(self, index, w1=None, w2=None, w3=None, within=False):
        #change within to True if you only want to compare items from the slic_u_arr
        del self.sims[:]
        sims_row = []
        u_item_row = []
        d_item_column = []
        u_item = self.slic_u_arr[index][0]
        u_item_row.append(u_item)
        u_item_row.append(index)

        if within == False:
            for x in range(len(self.slic_d_arr)):
                d_item_row = []
                d_item = self.slic_d_arr[x][0]
                d_item_row.append(d_item)
                d_item_row.append(self.compare_2_products(self.slic_u_arr[index][0], self.slic_d_arr[x][0], w1, w2, w3))
                d_item_row.append(x)
                d_item_column.append(d_item_row)
        else:
            for x in range(len(self.slic_u_arr)):
                d_item_row = []
                d_item = self.slic_u_arr[x][0]
                d_item_row.append(d_item)
                d_item_row.append(self.compare_2_products(self.slic_u_arr[index][0], self.slic_u_arr[x][0], w1, w2, w3))
                d_item_row.append(x)
                d_item_column.append(d_item_row)

        sims_row.append(u_item_row)
        sims_row.append(d_item_column)
        self.sims.append(sims_row)
         
    
    def filter_products(self, extent = 0.0):
        #Filtering out the products below certain similarity 
        sims2 = deepcopy(self.sims)
        pop_arr = [] #Array of indexes which have to go

        try: 
            #Finding indexes which fall below criteria:
            for x in range(len(self.sims[0][1])):
                if sims2[0][1][x][1] < extent:
                    pop_arr.append(sims2[0][1][x][2])
            
            #Removing the items based on these indexes: 
            org_len = len(sims2[0][1])
            for x in range(len(sims2[0][1])):
                if len(sims2[0][1]) == org_len - len(pop_arr):
                    break
                else: 
                    for y in range(len(pop_arr)):
                        if sims2[0][1][x][2] == pop_arr[y]:
                            sims2[0][1].pop(x)
        except:
            print "filter_products function in Yoda crashed"

        #Sorting by similarity
        sims_sorted = sorted(sims2[0][1], key=self.get_similarity, reverse=True)#<---CHANGE TO sort(reverse=True)
        
        sims2[0][1] = sims_sorted 
        """
        print
        print "FILTERED PRODUCTS:"
        for product in sims2[0][1]:
            print product

        print
        """
        return sims2


    def get_similarity(self, item):
        return item[1]
   
    
    def get_w1(self):
        return self.w1


    def get_w2(self):
        return self.w2


    def get_w3(self):
        return self.w3

def main():
    qui_gon = Jedi()


if __name__ == "__main__": main()
