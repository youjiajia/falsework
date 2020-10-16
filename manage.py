#!/usr/bin/env python
import sys
import logging
from common.utils import get_local_now


def load_local_command(command):
    module_name = 'commands.%s' % command
    module = __import__(module_name, {}, {}, ['*', ])
    return module


def run_command(command):
    command_module = load_local_command(command)

    logging.info(get_local_now())
    if not command_module:
        print(f'no command named: f{command}')
    else:
        getattr(command_module, 'main')(*sys.argv[2:])


if __name__ == '__main__':
    command = sys.argv[1]
    run_command(command)
