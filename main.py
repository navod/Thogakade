import click
import sys
from click.decorators import argument

from item import create_item, init




if __name__ == '__main__':
    arguments = sys.argv[1:]

    init(arguments)

    section = arguments[0]
    command = arguments[1]
    params = arguments[2:]

    if section == "item":
        if command == "create":
            create_item(*params)