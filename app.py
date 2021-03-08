#!/usr/bin/env python
import click

@click.command()
def hello():
    click.echo('Project 2 Test!')
    
if __name__ == '__main__':
    hello()