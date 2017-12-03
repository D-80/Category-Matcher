import re
import sys
from math import sqrt

#program for finding quantity of products based on their input values
#argument 1 - input file
#argument 2 - output file


regex_definitions = 19                                          # NUMBER OF RE DEFINITIONS

values_array = []                                               # Input array with all words
regex_values_array = [[] for y in range(regex_definitions)]     # Arrays with regex data
final_array = []                                                # Output array with target content

input_file = sys.argv[1]
output_file = sys.argv[2]


def readFile():
    print "readFile()"
    with open(input_file, 'r') as file:
        for line in file:
            values_array.append(line)


def single_el(n, element, multiplier):

    if element:
        # print(n + 1, 'found')
        eq = int(element.group(1)) * multiplier
        regex_values_array[n].append(eq)
    else:
        regex_values_array[n].append('')


def single_el_coma(n, element, multiplier):

    if element:
        """
        coma_end = re.search(r"[\d]+[' ']+\.", str(element.group()))
        if coma_end:
            print element.group(), " has ", coma_end.group(), " at the end"
        else:
        """
        eq = str(element.group(1))
        eq = eq.replace(",", ".")
        eq = eq.replace(" ", "")
        eq = float(float(eq) * multiplier)
        eq = round(eq, 2)
        regex_values_array[n].append(eq)
    else:
        regex_values_array[n].append('')


def double_el_add(n, element, multiplier):

    if element:
        eq = int(element.group(1)) + int(element.group(2)) * multiplier
        regex_values_array[n].append(eq)
    else:
        regex_values_array[n].append('')


def double_el_multiple(n, element, multiplier):

    if element:
        element_1 = float(element.group(1).replace(",", "."))
        element_2 = float(element.group(2).replace(",", "."))
        eq = float(element_1 * element_2) * multiplier ** 2
        eq = round(eq, 2)
        regex_values_array[n].append(eq)
    else:
        regex_values_array[n].append('')


def double_el_div(n, element, multiplier):

    if element:
        eq = int(element.group(1)) * multiplier
        eq_2 = int(element.group(2)) * multiplier

        if eq > eq_2:
            regex_values_array[n].append(eq)
        else:
            regex_values_array[n].append(eq_2)
    else:
        regex_values_array[n].append('')


def regex():
    print "regex()"
    for _ in range(len(values_array)):

        #print values_array[_]

        G_val = re.search('.*[^0-9x+/(](\d+)\s*[G]', values_array[_], flags=re.IGNORECASE)                              # 100G, 100 G                       1
        M_val = re.search('.*[^0-9x+/(](\d+)\s*[M]', values_array[_],flags=re.IGNORECASE)                               # 200M, 200 m                       2
        mm_val = re.search('.*[^0-9x+/(](\d+)\s*MM', values_array[_], flags=re.IGNORECASE)                              # 100mm, 100 mm                     3
        L_val = re.search('.*[^0-9x+/(](\d+)\s*L', values_array[_], flags=re.IGNORECASE)                                # 100L, 100 L                       4
        cL_val = re.search('.*[^0-9x+/(](\d+)\s*CL', values_array[_], flags=re.IGNORECASE)                              # 100cL, 100 cL                     5
        KG_val = re.search('.*[^0-9x+/(](\d+)\s*K[^a]', values_array[_], flags=re.IGNORECASE)                           # 100kg, 100 kg                     6
        KG_val_2 = re.search('.*kg\s*(\d+)', values_array[_], flags=re.IGNORECASE)                                      # kg1, kg 1                         7
        SZT_val = re.search('.*[^0-9x+/(](\d+)\s*SZT', values_array[_], flags=re.IGNORECASE)                            # 100szt, 100 szt                   8
        S_val = re.search('.*[^0-9x+/(](\d+)\s*S', values_array[_], flags=re.IGNORECASE)                                # 100S, 100 S                       9
        last_number_val = re.search('.*[^0-9x+/(](\d+)\s*$', values_array[_], flags=re.IGNORECASE)                      # 150 as last                       10 DEPRECATED
        last_number_coma_val = re.search('.*[^0-9x+/(](\d+\s?[.,]\s?\d*)\s*$', values_array[_], flags=re.IGNORECASE)    # 150,5 as last                     11 DEPRECATED
        last_number_alcohol_val = re.search('.*[^0-9x+/(](0\s?[.,]\s?\d*)\s*$', values_array[_], flags=re.IGNORECASE)   # 0,7 as last                       12 DEPRECATED
        coma_KG_val = re.search('.*[^0-9x+/(](\d+[.,]\d+)\s*[K][^0-9xa+/%]', values_array[_], flags=re.IGNORECASE)      # 3,5kg                             13
        coma_L_val = re.search('.*[^0-9x+/(](\d+\s?[.,]\s?\d*)L', values_array[_], flags=re.IGNORECASE)                 # 1,5L                              14
        coma_G_val = re.search('.*[^0-9x+/(](\d+\s?[.,]\s?\d*)G', values_array[_],flags=re.IGNORECASE)                  # 1,5G                              15
        div_val = re.search('.*[^0-9x+/(](\d+)\s*/\s*(\d+)', values_array[_], flags=re.IGNORECASE)                      # 50/30                             16
        add_val = re.search('.*[^0-9x+/(](\d+)\s*\+\s*(\d+)\s*[G]', values_array[_], flags=re.IGNORECASE)               # 9+1G,  9 + 1                      17
        multiply = re.search('.*[^0-9x+/(](\d+)\s*[X*]\s*(\d+[,.]*\d*)', values_array[_], flags=re.IGNORECASE)          # 4x100, 4 x 40,  6X0.33            18
        L_multiply = re.search('.*[^0-9x+/(](\d+)\s*[X*]\s*(\d+[,.]*\d*)L', values_array[_], flags=re.IGNORECASE)       # 4x100L, 4 x 40,  6X0.33           19

        # ToDo BOX40G, 200%1
        single_el(0, last_number_val, multiplier=1)
        single_el_coma(1, last_number_coma_val, multiplier=1)
        single_el_coma(2, last_number_alcohol_val, multiplier=1000)
        single_el(3, M_val, multiplier=1)
        single_el(4, L_val, multiplier=1000)
        single_el(5, KG_val_2, multiplier=1000)
        single_el(6, KG_val, multiplier=1000)
        single_el(7, SZT_val, multiplier=1)
        single_el(8, S_val, multiplier=1)
        single_el(9, G_val, multiplier=1)
        single_el(10, mm_val, multiplier=1)
        single_el(11, cL_val, multiplier=10)
        single_el_coma(12, coma_KG_val, multiplier=1000)
        single_el_coma(13, coma_L_val, multiplier=1000)
        single_el_coma(14, coma_G_val, multiplier=1)
        double_el_div(15, div_val, multiplier=1)
        double_el_add(16, add_val, multiplier=1)
        double_el_multiple(17, multiply, multiplier=1)
        double_el_multiple(18, L_multiply, multiplier=sqrt(1000))
        


def add_numbers_to_final_array():
    print "add_numbers_to_final_array()"
    for j in range(len(regex_values_array[0])):

        final_array.append('')
        for i in range(regex_definitions):
            if regex_values_array[i][j] != '':
                final_array[j] = regex_values_array[i][j]


def all_data_count():

    global all_numbers
    all_numbers = 0

    for n in range(len(values_array)):
        data = re.search('.*(\d).*', values_array[n])
        if data:
            all_numbers += 1
    print('\nAll lines ' + str(all_numbers))


def write_to_file():
    print "write_to_file()"
    with open(output_file, 'w') as file:
        for n in range(len(final_array)):
            file.write(str(final_array[n]) + '\n')

    print('Succesfully wrote to file ' + str(output_file))

'''
def debug():
    fileName = 'Data\\debug.txt'
    with open(fileName, 'a') as file:
        file.write('num_of_wrong_regexp ' + str(num_of_wrong_regexp) + '\n')
        file.write('num_of_duplicate_regexp ' + str(num_of_duplicate_regexp) + '\n')
        file.write('\n')
'''

def main():
    readFile()
    regex()
    add_numbers_to_final_array()
    write_to_file()
    all_data_count()

main()
