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

    # EMBEDDED VARIBLE
    embedded_var = re.findall(r'\{(.+?)\}', txt)
    for var in embedded_var:
        txt = re.sub(r'(\{.+?\})', in_game_vars[var], txt, count = 1)
        
    for char in txt:
        print(char, end='')
        stdout.flush()
        sleep(0.02)

def play(gest_file):
    if not(isfile(gest_file)):
        print("Error: The requested GEST game cannot be found")
        return
    with open(gest_file, 'r') as f:
        for line in f.readlines():
            
            if(trim(line).startswith('#')):
                continue
            # COMMAND WITH VARIABLE 
            com = re.search(r'\[[ ]*(.+?)[ ]*:[ ]*(.+?)[ ]*\][ ]*(.+?)$', line)
            if com:
                if(com.group(1) == 'input'):
                    txtout(com.group(3) + ' ')
                    in_game_vars[com.group(2)] = input()
                    
            # VARIABLE EQUALITY CONDITION
            
            
            else:
                txtout(line)

if __name__=='__main__':
    try:
        play(argv[1])
    except KeyboardInterrupt:
        exit()
