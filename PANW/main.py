import os
import sys
import keywords
import re

dir = sys.argv[1]
rules = keywords.rules
regword = keywords.regword
regline = keywords.regline
found = False

# Handle the file
def handle(currentfile):

    with open(currentfile) as f:
        lines = f.readlines()
        line_number = 0
        for line in lines:
            scan_line(line, line_number)
            line_number += 1


# Scan for keywords
def scan_line(line, line_number):
    for word in line.split():
        pattern_a = "Line " + str(line_number) + " has the word"
        pattern_b = " in it:"
        # Search for word in length >= 80           rule #3
        if len(word) >= 80:
            found = True
            print(pattern_a, word, pattern_b)
            print(line)
        # Search for word in rules                  rules #1, 5
        for keyword in rules:
            if word == keyword:
                found = True
                print(pattern_a, word, pattern_b)
                print(line)
        # Search for Regular expressions words      rule #2
        for reg in regword:
            res = re.findall(reg, word)
            if res:
                found = True
                print(pattern_a, res, pattern_b)
                print(line)
        # Search for Regular expressions line       rule #4
        for reg in regline:
            res = re.findall(reg, line)
            if res:
                found = True
                print(pattern_a, res, pattern_b)
                print(line)


# Find envirenmen variabels in the name BC_SPECIAL_WORD and add it to keywords
def add_BC_SPECIAL_WORD():
    for variable in os.environ:
        if variable == 'BC_SPECIAL_WORD':
            rules.append((os.getenv(variable)))


if __name__ == '__main__':

    # add BC_SPECIAL_WORD to the keywords
    add_BC_SPECIAL_WORD()

    # Iterate over the given path recursively
    for subdir, dirs, files in os.walk(dir):
         for filename in files:
            filepath = subdir + os.sep + filename

            # Check file extension ends with .txt
            if filepath.endswith(".txt"):
                found = False
                handle(filepath)
                if found:
                    print("found in file: ", filepath)


