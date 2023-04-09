from sys import argv, stdout, exit
from time import sleep
from os.path import isfile, abspath
import re
#from keyboard import is_pressed
import pickle
import colorama
from colorama import Fore

def init_in_game_vars(gest_file):
    in_game_vars['gest_file'] = abspath(gest_file)
    in_game_vars['line_index'] = 0
    gsav_file = re.search(r'^(.+?)\.gest$', abspath(gest_file))
    in_game_vars['gsav_file'] = gsav_file.group(1) + '.gsav'
    return

def save():
    gsav_file.seek(0)
    pickle.dump(in_game_vars, gsav_file)

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

def play():
    with open(in_game_vars['gest_file'], 'r') as f:
        lines = f.readlines()
        line_index = in_game_vars['line_index']
        while(True):
            in_game_vars['line_index'] = line_index
            save()
            if(line_index >= len(lines)):
                break
            line = lines[line_index]

            # COMMENTS
            if('#' in line):
                if (trim((lines[line_index])).startswith('#')):
                    line_index += 1
                    continue
                else:
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
                        txtout(Fore.YELLOW + "\nInvalid input:"+ Fore.RESET +" Try again\n\n"+ Fore.RESET)
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
                        print(Fore.RED + "\nError:" + Fore.RESET +" endblock not found")
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
    save()

def main():
    global in_game_vars
    global gsav_file
    in_game_vars = {}
    gsav_file = None
    if len(argv)<2:
        print(Fore.RED + "\nError:" + Fore.RESET + " Argument not provided")
        exit()
    file = argv[1]
    if not(isfile(file)):
        print(Fore.RED + "\nError:" + Fore.RESET + " This file cannot be located")
    try:
        if(file.endswith('.gest')):
            init_in_game_vars(file)
            gsav_file = open(in_game_vars['gsav_file'], 'wb')
            play()
            gsav_file.close()
        elif(file.endswith('.gsav')):
            with open(file, 'rb') as sf:
                in_game_vars = pickle.load(sf)
            gsav_file = open(in_game_vars['gsav_file'], 'wb')
            play()
            gsav_file.close()
        else:
            print(Fore.RED + "\nError:" + Fore.RESET + " Unrecognized file type. \
Only .gest and .gsav file extentions are supported")
    except KeyboardInterrupt:
        exit() #exit the game in case the user press `ctrl+C` which raises a KeyboardInterrupt

if __name__=='__main__':
    main()
