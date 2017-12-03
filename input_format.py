import re
import sys

#program for formatting input_file
#argument 1 - input file
#argument 2 - output file

def main():
    f = open(sys.argv[2], 'w') 
    with open(sys.argv[1], 'r') as file:
        for line in file:

            if line != "#N/A\n":
                f_line = re.findall(r"[^\ \.]+", line.upper())
                final_line = ''

                for part in f_line:
                    if part == '\n':
                        continue
                    else: 
                        part = re.findall(r"[\w]+", part)
                        part = 'q'.join(part)
                        final_line += part + ' ' 
                
                try:
                    if final_line[-1] != 'n':
                        final_line += '\n'
                except:
                    "string index out of range"

                print(f_line)
                print(final_line)
                f.write(final_line)
            else:
                f.write(line)

    f.close()
    

main() 
