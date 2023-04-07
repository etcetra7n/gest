from sys import argv, stdout, exit
from time import sleep
from os.path import isfile
import re
from keyboard import is_pressed

in_game_vars = {}

def save():
    fname = re.search(r'^(.+?)\.')
    with open(fname.group(1) + '.gsave', 'w') as sfile:
        sfile.write(argv[1])


def trim(str):
    begin = 0
    end = len(str)
    for i, c in enumerate(str):
        if(c != ' '):
            begin = i
            break
    for i, c in enumerate(reversed(str)):
        if(c != ' '):
            end = len(str)-i
            break
    return str[begin:end]

def txtout(txt):

    '''
    EMBEDDED VARIBLE
    Syntax:
        some text {var} some text...
    for example:
        My name is {name}
    '''
    embedded_var = re.findall(r'\{[ ]*(.+?)[ ]*\}', txt)
    for var in embedded_var:
        txt = re.sub(r'(\{.+?\})', in_game_vars[var], txt, count = 1)

    for char in txt:
        print(char, end='')
        stdout.flush()
        sleep(0.02)

def play(gest_file):
    if not(isfile(gest_file)):
        print("\nERROR: The requested GEST game cannot be found")
        return
    with open(gest_file, 'r') as f:
        lines = f.readlines()
        line_index = 0;
        while(True):
            if(line_index >= len(lines)):
                break
            line = lines[line_index]

            # COMMENTS
            if('#' in line):
                chr_index = line.find('#')
                line = line[:chr_index] + '\n'

            '''
            COMMAND WITH VARIABLE
            Syntax:
                [command: var] text
            for example:
                [input: name] Enter your name:
            '''
            com = re.search(r'\[[ ]*(.+?)[ ]*:[ ]*(.+?)[ ]*\][ ]*(.+?)$', line)
            if com:
                command = com.group(1)
                var = com.group(2)
                prompt = com.group(3)
                if(command == 'input'):
                    '''
                    INPUT COMMAND
                    Syntax:
                        [input: var] some text
                    for example:
                        [input: name] Enter your name:
                        
                    The name will be stored in the varible 'name' which
                    can be accessed by `{name}`
                    '''
                    txtout(prompt + ' ')
                    in_game_vars[var] = input()
                    line_index += 1
                    continue
                
                elif(command == 'yes_or_no'):
                    '''
                    YES_OR_NO COMMAND
                    Syntax:
                        [yes_or_no: var] some question
                    for example:
                        [yes_or_no: p] Are you ready to proceed
                    while playing the above example yould be displayed
                    as:
                        Are you ready to proceed (y/n): 
                    '''
                    txtout(prompt + ' (y/n): ')
                    inp = input()
                    if inp == 'y':
                        in_game_vars[var] = 'yes'
                    elif inp == 'n':
                        in_game_vars[var] = 'no'
                    else:
                        txtout("Invalid input. Try again\n\n")
                        continue
                    line_index += 1
                    continue

            '''
            VARIABLE EQUALITY CONDITION
            Syntax:
                [{var} value]
                ...
                [endblock]

                    (OR)

                [{var} "value"]
                ...
                [endblock]

                    (OR)

                [{var} 'value']
                ...
                [endblock]
            '''
            con = re.search(r'\[[ ]*\{(.+?)\}[ ]+[\'"]?(.+?)[\'"]?[ ]*\]', line)
            if con:
                if in_game_vars[con.group(1)] == con.group(2):
                    line_index += 1
                    continue

                else:
                    jump_to = line_index
                    for i in range(line_index+1, len(lines)):
                        if re.match(r'\[[ ]*endblock[ ]*\]', lines[i]):
                            jump_to = i+1
                            break
                    else:
                        print("\nGAME SYNTAX ERROR: endblock not found")
                        exit()
                    line_index = jump_to
                    continue

            if re.match(r'[ ]*\[[ ]*endblock[ ]*\]', line):
                line_index += 1
                continue
            if re.match(r'[ ]*\[[ ]*abort[ ]*\]', line):
                break

            txtout(trim(line))
            line_index += 1

if __name__=='__main__':
    try:
        play(argv[1])
    except KeyboardInterrupt:
        exit()
