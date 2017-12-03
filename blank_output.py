import sys

#program for generating blank output file with proper size
#argument 1 - input file
#argument 2 - output file

def main():
    f = open(sys.argv[2], 'w') 
    with open(sys.argv[1], 'r') as file:
        for line in file:
            f.write("\n")

    f.close()

main() 
