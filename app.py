#!/usr/bin/env python
import click
from calculator import get_txt_input, get_cmd_input, execute_commands

@click.command()
def hello():
    click.echo('Project 2 Test!')
    
#if __name__ == '__main__':
    #hello()

if __name__ == '__main__':
    # Executes script from command prompt
    try:
        lines = get_txt_input()
    except (IndexError, FileNotFoundError):
        lines = get_cmd_input()
        print('')

    execute_commands(lines)