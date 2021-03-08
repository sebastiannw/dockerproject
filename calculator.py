#!/usr/bin/env python

# Loads sys module needed to read txt input file
import sys

# Maintains error messages as global variables
ERROR_MESSAGE = 'Invalid command "{}" was ignored.'
OPERATION_ERROR = 'Operation "{}" is not defined.'
REGISTER_ERROR = 'Register "{}" should not be a number.'
PRINT_ERROR = 'Print command is not well specified.'
RECURSION_ERROR = 'Register "{}" is dependent on itself.'
COMMAND_ERROR = 'Command must have 2 or 3 arguments.'

class Register:
    '''
    Creates Register objects to store the 'formula' to calculate their value
    in self.log whenever they are called or printed.
    '''
    def __init__(self, name):
        '''
        Initiates with attributes name, value=0 and empty log. self.log (list of
        lists) will record each operation to this registry as a list:
        [op: operation,
         va: value,
         dependency: flag 0 when value is a number, 1 when its another register,
         executed: flag False when this op hasn't run, True when it has]
        '''
        self.name = name
        self.value = 0
        self.log = []

    def add(self, value):
        self.value += value

    def subtract(self, value):
        self.value -= value

    def multiply(self, value):
        self.value *= value

    # More operations can be defined as additional methods here. For example:
    #def divide(self, value):
        #self.value /= value

def is_float(x):
    '''Validates if an input x (str) contains a float number.'''
    try:
        float(x)
        return True
    except ValueError:
        return False

def is_valid_operation(rg, op, va):
    '''
    Validates an input operation. Returns False if operation op is not defined
    in class Register or if register rg is a number.
    '''
    dummy = Register('')
    line = ' '.join([rg, op, va])

    try:
        getattr(dummy, op)
        assert is_float(rg) == False
        return True
    except AttributeError:
        # Prints error message if op doesn't exist
        print(ERROR_MESSAGE.format(line), OPERATION_ERROR.format(op))
        return False
    except AssertionError:
        # Prints error message if rg is numeric
        print(ERROR_MESSAGE.format(line), REGISTER_ERROR.format(rg))
        return False

def is_valid_print(pr, ar, registers):
    '''
    Validates a print command (2 arguments). Returns False if first argument pr
    is not the word 'print' or if the registry rg is not declared beforehand.
    '''
    line = ' '.join([pr, ar])

    try:
        assert pr == 'print'
        assert ar in registers
        return True
    except AssertionError:
        print(ERROR_MESSAGE.format(line), PRINT_ERROR)
        return False

def update_value(register, registers):
    '''
    Takes the input register and runs every operation in its log that has not
    been executed yet to update its value. After an opertion is executed it
    flags it as True in its log entry. If an operation calls another register in
    registers, it updates that one's value recursively first.
    '''
    for i, (op, va, dependency, executed) in enumerate(register.log):
        if executed: continue # skips if flagged as executed

        if not dependency:
            # Updates when va is a number (base case)
            getattr(register, op)(float(va))
            register.log[i][-1] = True # flag as executed

        else:
            # Updates when va is another register (recursive case)
            update_value(registers[va], registers)
            getattr(register, op)(registers[va].value)
            register.log[i][-1] = True # flag as executed


def get_cmd_input():
    '''Requests and reads input from command prompt. Returns list of lines.'''
    lines = [input().lower()]

    while lines[-1] != 'quit':
        lines.append(input().lower())

    return lines[:-1]

def get_txt_input():
    '''Reads instructions/commands from txt file. Returns list of lines.'''
    file = open(sys.argv[1], 'r')
    lines = [line.strip().lower() for line in file]
    lines = lines[:-1] if (lines[-1] == 'quit') else lines

    return lines

def execute_commands(lines):
    '''
    Loops through commands in lines (list of str). Creates instances of Register
    when one is called and stores every operation in its log. Calls
    update_value() only when a print statement is made (lazy evaluation).
    '''
    registers = {} # dict. of register objects with its input str. as key

    for line in lines:
        args = line.split() # list of each word in current line

        try:
            # Check if line contains valid input
            assert (len(args) in [2, 3]) or (args == ['quit'])
        except AssertionError:
            # Contains 0, 1, 4 or more words are input in one line (skips line)
            print(ERROR_MESSAGE.format(line), COMMAND_ERROR)
            continue

        if len(args) == 3:
            # Case when line contains an operation (3 input words)
            rg, op, va = args[0], args[1], args[2]
            if not is_valid_operation(rg, op, va): continue # skips if not valid
            if rg not in registers: registers[rg] = Register(rg)
            dependency = 0

            if not is_float(va):
                # If va is not numerical, creates new Register and sets
                # dependency to 1 for log
                if va not in registers: registers[va] = Register(va)
                dependency = 1

            # Records in log
            registers[rg].log.append([op, va, dependency, False])


        elif len(args) == 2:
            # Case when line contains a print statement (2 words)
            pr, ar = args[0], args[1]
            if not is_valid_print(pr, ar, registers): continue
            try:
                update_value(registers[ar], registers)
                print(round(registers[ar].value) # so it won't print '.0'
                      if (registers[ar].value % 1) == 0
                      else registers[ar].value)
            except RecursionError:
                print(ERROR_MESSAGE.format(line), RECURSION_ERROR.format(ar))

        else:
            # Case when current line is 'quit'. Stops program.
            break

if __name__ == '__main__':
    # Executes script from command prompt
    try:
        lines = get_txt_input()
    except (IndexError, FileNotFoundError):
        lines = get_cmd_input()
        print('')

    execute_commands(lines)
