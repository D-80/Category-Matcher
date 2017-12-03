import sys

#program for formatting output data
#argument 1 - input file
#argument 2 - output file

def main():

    new_arr = []
    x = 0

    with open(sys.argv[1], 'r') as f:
        for line in f:
            new_line = line.rstrip()
            new_arr.append(new_line)
            x+=1

    with open(sys.argv[2], 'w') as f:
        for line in new_arr:
            f.write(line+'\n')


main()
