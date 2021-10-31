import click
import sys
from click.decorators import argument

from item import create_item, get_all_items, init, item_delete, item_view_by_id

if __name__ == '__main__':
    arguments = sys.argv[1:]

    init(arguments)

    section = arguments[0]
    command = arguments[1]
    params = arguments[2:]

    if section == "item":
        if command == "create":
            create_item(*params)
        elif command == "all":
            get_all_items()
        elif command == "view":
            item_view_by_id(*params)
        elif command == "delete":
            item_delete(*params)
