from sys import argv, stdout, exit
from time import sleep
from os.path import isfile, abspath
import re
import pickle
from colorama import Fore
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame.mixer import music, init
from win32api import GetAsyncKeyState
import win32con

__version__ = '1.3.4'

def console_exit():
    print('\n')
    print(Fore.CYAN + "Press ENTER to exit... " + Fore.RESET, end = '')
    stdout.flush()
    #input()
    while(True):
        state = GetAsyncKeyState(win32con.VK_RETURN)
        if state not in [0,1]:
            exit()
    
def init_in_game_vars(gest_file):
    in_game_vars['gest_file'] = abspath(gest_file)
    in_game_vars['line_index'] = 0
    in_game_vars['gsav_file'] = abspath(gest_file)[:-4] + 'gsav'
    in_game_vars['_scene_return'] = []

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

def block(str, lines, line_index):
    jump_index = 0
    for i in range(line_index+1, len(lines)):
        if re.match(r' *\[ *'+str+r' *\]', lines[i]):
            jump_index = i
            break
    else:
        print(Fore.RED + "\n\nScript Error: " + Fore.RESET +"["+ str +"] not found")
        console_exit()
    return jump_index
    
def txtout(txt):

    '''
    EMBEDDED VARIBLE
    Syntax:
        some text {var} some text...
    for example:
        My name is {name}
    '''
    embedded_var = re.findall(r'\{ *([a-zA-Z0-9_]*) *\}', txt)
    for var in embedded_var:
        txt = re.sub(r'({ *'+var+' *})', in_game_vars[var], txt)
    _fast_txt=False
    for char in txt:
        print(char, end='')
        stdout.flush()
        state = GetAsyncKeyState(win32con.VK_CONTROL)
        _fast_txt = state not in [0, 1]
        if _fast_txt:
            sleep(0.008)
        else:
            sleep(0.03)
        
def play():
    if '_bg_music' in in_game_vars:
        music.load(in_game_vars['_bg_music'][0])
        music.play(in_game_vars['_bg_music'][1])
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
            com = re.search(r'\[ *([a-zA-Z_]+) *: *(.+) *\] *(.*)', line)
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
                    #input()
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
                        txtout(Fore.YELLOW + "\nInvalid input:"+ Fore.RESET +" Try again\n\n")
                        continue
                    line_index += 1
                    continue
                elif command == 'musicloop':
                    if '_bg_music' in in_game_vars:
                        music.fadeout(1000)
                    music.load(var)
                    music.play(-1)
                    in_game_vars['_bg_music'] = [var, -1]
                    line_index += 1
                    continue
                elif command == 'music':
                    if '_bg_music' in in_game_vars:
                        music.fadeout(1000)
                    music.load(var)
                    music.play()
                    in_game_vars['_bg_music'] = [var, 0]
                    line_index += 1
                    continue
                elif command == 'play':
                    in_game_vars['_scene_return'].append(line_index+1)
                    for l in range(len(lines)):
                        if re.match(r' *\[ *scene *: *'+ var + r' *\]', lines[l]):
                            line_index = l+1
                            break
                    else:
                        print(Fore.RED+"\nScript Error:"+Fore.RESET+" Scene `"+scene_name+"` is not defined")
                        console_exit()
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
            con = re.search(r'\[ *{ *([a-zA-Z0-9_]+) *} +[\'\"]?(.*?)[\'\"]? *\]', line)
            if con:
                if in_game_vars[con.group(1)] == con.group(2):
                    line_index += 1
                    continue

                else:
                    line_index = block('endblock', lines, line_index)+1
                    continue

            directive = re.search(r'\[ *([a-zA-Z_]*) *\]', line)
            if directive:
                name = directive.group(1)
                if name == 'endscene':
                    line_index = in_game_vars['_scene_return'].pop()
                    # pop() returns and removes the last indice
                    continue
                elif name == 'endblock':
                    line_index += 1
                    continue
                elif name == 'abort':
                    break
                elif name == 'stopmusic':
                    music.fadeout(1000)
                    in_game_vars.pop('_bg_music')
                    line_index += 1
                    continue

            if re.match(r' *\[ *scene *: *([a-zA-Z0-9_-]*) *\]', line):
                line_index = block('endscene', lines, line_index)+1
                continue

            txtout(trim(line))
            line_index += 1
    save()

def main():
    global in_game_vars
    global gsav_file
    in_game_vars = {}
    if len(argv)<2:
        print(Fore.RED + "\nError:" + Fore.RESET + " Argument not provided")
        console_exit()
    if argv[1]=='-v':
        print(__version__)
        console_exit()
    file = argv[1]
    if not(isfile(file)):
        print(Fore.RED + "\nError:" + Fore.RESET + " This file cannot be located")
        console_exit()
    try:
        if(file.endswith('.gest')):
            init_in_game_vars(file)
            gsav_file = open(in_game_vars['gsav_file'], 'wb')
            init() # for music
            play()
            gsav_file.close()
            console_exit()
        elif(file.endswith('.gsav')):
            with open(file, 'rb') as sf:
                in_game_vars = pickle.load(sf)
            gsav_file = open(in_game_vars['gsav_file'], 'wb')
            init() # for music
            play()
            gsav_file.close()
            console_exit()
        else:
            print(Fore.RED + "\nError:" + Fore.RESET + " Unrecognized file type. \
Only .gest and .gsav file extentions are supported")
    except KeyboardInterrupt:
        gsav_file.close()
        console_exit()
        # exit the game in case the user press `ctrl+C` which raises a KeyboardInterrupt

if __name__=='__main__':
    main()
