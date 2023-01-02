#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a customizable shell.
#    Copyright (C) 2021, 2022, 2023  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This file implements a customizable shell.
"""

__version__ = "0.2.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This file implements a customizable shell.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/CustomShell"

copyright = """
CustomShell  Copyright (C) 2021, 2022, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

print(copyright)

__all__ = ["Shell", "CONFIG_VAR", "main"]

from os import system, getcwd, chdir, listdir, device_encoding, name
from sys import platform, stderr, exit, executable, version_info
from platform import node, system as operatingsystem, version
from os.path import dirname, split, expanduser, join, isfile
from configparser import ConfigParser, NoOptionError
from logging import StreamHandler, Formatter, Logger
from shlex import split as shellsplit
from collections.abc import Callable
from time import localtime, strftime
from typing import TypeVar, List
from contextlib import suppress
from logging import getLogger
from functools import partial
from getpass import getuser
from cmd import Cmd

Config = TypeVar("Config", str, None)

def get_cwd(function: Callable) -> None:

    """
    This function gets current directory and excepts exception.
    """
    
    with suppress(FileNotFoundError):
        Shell.cwd = getcwd()
        return function()
    
    logger_warning(
        "Current folder probably no longer exists, the current"
        " directory is replaced by the parent directory."
    )
    cwd = Shell.cwd = dirname(Shell.cwd)
    chdir(cwd)
    return get_cwd(function)

if name == "nt":
    DEFAULT_CONFIG = {
        "DISPLAY": {
            "prompt": (
                "{E} {color}{green}{U}{color}{reset}@{color}{green}{N}"
                "{color}{reset}:{color}{green}{P}{color}{reset}$"
            ),
            "start_intro": "echo {a}",
            "end_intro": "echo {a}",
            "intro": (
                "{S} \t{V} \t[{s}, {o}] {n}"
                "Python  \t{v} \t\t[{e}]{n}"
                "CustomShell \t{c} \t\t[GPL-3.0]{n}"
                "{n}{color}{bgwhite}{color}{bold}{blue}"
                "*** {D} {T} - Welcome in CustomShell {U} ! ***"
                "{color}{reset}{n}"
            ),
            "start_quit": "echo {a}",
            "end_quit": "echo {a}",
            "quit": (
                "{n}{color}{bgwhite}{color}{underline}{red}"
                "*** {D} {T} - Bye {U} ! ***"
                "{color}{reset}{n}"
            ),
        },
        "ALIAS": {"pyc ": "python -c ", "pym ": "python -m "},
    }
else:
    DEFAULT_CONFIG = {
        "DISPLAY": {
            "prompt": (
                "{E} {color}{green}{U}{color}{reset}@{color}{green}{N}"
                "{color}{reset}:{color}{green}{P}{color}{reset}$"
            ),
            "start_intro": "echo {a}",
            "end_intro": "echo {a}",
            "intro": (
                "{S} \t{V} \t[{s}, {o}] {n}"
                "Python  \t{v} \t\t[{e}]{n}"
                "CustomShell \t{c} \t\t[GPL-3.0]{n}"
                "{n}{color}{bgwhite}{color}{bold}{blue}"
                "*** {D} {T} - Welcome in CustomShell {U} ! ***"
                "{color}{reset}{n}"
            ),
            "start_quit": "echo {a}",
            "end_quit": "echo {a}",
            "quit": (
                "{n}{color}{bgwhite}{color}{underline}{red}"
                "*** {D} {T} - Bye {U} ! ***"
                "{color}{reset}{n}"
            ),
        },
        "ALIAS": {"pyc ": "python3 -c ", "pym ": "python3 -m "},
    }

CONFIG_VAR = {
    "{U}": getuser,
    "{N}": node,
    "{P}": partial(get_cwd, getcwd),
    "{p}": partial(get_cwd, lambda: dirname(getcwd())),
    "{T}": lambda: strftime("%H:%M:%S", localtime()),
    "{D}": lambda: strftime("%y-%m-%d", localtime()),
    "{S}": operatingsystem,
    "{o}": lambda: platform,
    "{s}": lambda: name,
    "{n}": lambda: "\n",
    "{a}": lambda: "\7",
    "{e}": lambda: executable,
    "{v}": lambda: (
        f"{version_info.major}."
        f"{version_info.minor}.{version_info.micro}"
    ),
    "{V}": version,
    "{c}": lambda: __version__,
}

UNIX_COLOR = {
    "{black}": "30m",
    "{red}": "31m",
    "{green}": "32m",
    "{other}": "33m",
    "{blue}": "34m",
    "{purple}": "35m",
    "{cyan}": "36m",
    "{white}": "37m",
    "{bgblack}": "40m",
    "{bgred}": "41m",
    "{bggreen}": "42m",
    "{bgother}": "43m",
    "{bgblue}": "44m",
    "{bgpurple}": "45m",
    "{bgcyan}": "46m",
    "{bgwhite}": "47m",
    "{texte}": "0;",
    "{bold}": "1;",
    "{underline}": "4;",
    "{reset}": "0m",
    "{color}": "\x1b[" or "\e[",
}


def get_custom_logger() -> Logger:

    """
    This function builds a custom logger.
    """

    logger = getLogger(__name__)

    formatter = Formatter(
        fmt=(
            "%(asctime)s%(levelname)-9s(%(levelno)s) "
            "{%(name)s - %(filename)s:%(lineno)d} %(message)s"
        ),
        datefmt="[%Y-%m-%d %H:%M:%S] ",
    )
    stream = StreamHandler(stream=stderr)
    stream.setFormatter(formatter)

    logger.addHandler(stream)

    return logger


logger: Logger = get_custom_logger()
logger_debug: Callable = logger.debug
logger_info: Callable = logger.info
logger_warning: Callable = logger.warning
logger_error: Callable = logger.error
logger_critical: Callable = logger.critical
logger_log: Callable = logger.log


class Shell(Cmd):

    """
    This class implements the customizable shell.
    """
    
    cwd = getcwd()

    def __init__(self):
        super().__init__()

        self.encoding = device_encoding(0).casefold()
        self.ref_encoding = "utf-8".casefold()
        self.state = None
        self.config = ConfigParser()
        self.config_path = join(expanduser("~"), "Shell.ini")

        self.check_config_file()
        self.config.read(self.config_path)

        self.config.setdefault("ALIAS", {})

        display = "DISPLAY"
        display_conf = DEFAULT_CONFIG[display]

        self.intro_template = (
            self.get_config(display, "intro") or diplay_conf["intro"]
        )
        self.start_intro_template = (
            self.get_config(display, "start_intro")
            or diplay_conf["start_intro"]
        )
        self.end_intro_template = (
            self.get_config(display, "end_intro") or diplay_conf["end_intro"]
        )

        self.prompt_template = (
            self.get_config(display, "prompt") or diplay_conf["prompt"]
        )

        self.quit_template = (
            self.get_config(display, "quit") or diplay_conf["quit"]
        )
        self.start_quit_template = (
            self.get_config(display, "start_quit") or diplay_conf["start_quit"]
        )
        self.end_quit_template = (
            self.get_config(display, "end_quit") or diplay_conf["end_quit"]
        )

        self.var = CONFIG_VAR.copy()
        self.var["{E}"] = self.get_last_command_state

        self.prompt = self.format(self.prompt_template)

    def get_last_command_state(self):

        """
        This function returns the status of the last command.
        """

        if self.state:
            return (
                "\x1b[31m\u2718\x1b[0m"
                if self.encoding == self.ref_encoding
                else "\x1b[41m\x1b[30m[X]\x1b[0m"
            )
        else:
            return (
                "\x1b[32m\u2714\x1b[0m"
                if self.encoding == self.ref_encoding
                else "\x1b[42m\x1b[30m[V]\x1b[0m"
            )

    def get_config(self, section: str, value: str) -> Config:

        """
        This function returns config or None
        """

        logger_debug(f"Getting configuration {section!r}[{value!r}]")
        try:
            return self.config.get(section, value)
        except NoOptionError:
            logger_warning("Configuration not found {section!r}[{value!r}]")
            return None

    def format(self, string: str) -> str:

        """
        This fonction formats string template.
        """

        logger_debug(f"Format string: {string!r}.")
        [string := string.replace(substring, function()) for substring, function in self.var.items() if substring in string]

        logger_debug(f"Add color: {string!r}.")
        [string := string.replace(color, code) for color, code in UNIX_COLOR.items() if color in string]

        logger_info(f"Formatted string: {string!r}")
        return string

    def check_config_file(self) -> bool:

        """
        This function returns True if config file
        exists else writes it and returns False.
        """

        logger_debug("Checking configuration file")

        if not isfile(self.config_path):
            logger_info("Configuration file exists")

            self.config.update(DEFAULT_CONFIG)
            logger_info("Configuration is updated")

            with open(self.config_path, "w") as configfile:
                self.config.write(configfile)

            logger_info("Configuration is saved")
            return False
        return True

    def do_cd(self, directory: str) -> bool:

        """
        This function changes the current directory
        """

        logger_debug("Command to change the directory")

        try:
            chdir(directory)
        except FileNotFoundError:
            logger_error('An exception is raised on "cd" command.')
            system("cd " + directory)
            self.state = True
        else:
            self.state = False
            Shell.cwd = getcwd()

        return False

    def do_GetConfigFile(self, args: str) -> bool:

        """
        This function prints the configuration filename.
        """

        logger_debug("Print the configuration file path")
        print(self.config_path)
        self.state = False
        return False

    def do_configfile(self, args: str) -> bool:

        """
        This function prints the configuration filename.
        """

        logger_debug("Print the configuration file path")
        print(self.config_path)
        self.state = False
        return False

    def do_help(self, args: str) -> bool:

        """
        This function executes the help command.
        """

        logger_debug(f"Command help: {arg}")
        self.state = system("help " + args)
        return False

    def do_exit(self, args: str) -> bool:

        """
        This function closes and quits the shell
        """

        logger_debug("Command exit")
        return True

    def do_quit(self, args: str) -> bool:

        """
        This function closes and quits the shell
        """

        logger_debug("Command quit")
        return True

    def default(self, command: str) -> bool:

        """
        This function executes the command line.
        """

        logger_debug(f"Command: {command!r}")

        try:
            self.state = system(command)
        except KeyboardInterrupt:
            logger_info("A KeyboardInterrupt error is raised")
            print('Use "exit" or "quit" command to quit the terminal.')

        return False

    def precmd(self, command: str) -> str:

        """
        This function searchs and replaces command by alias.
        """

        logger_debug("Resolving alias")
        [logger_info(f"Alias found: {alias!r} -> {command_!r}") or (command := command.replace(alias, command, 1)) for alias, command_ in self.config["ALIAS"].items() if command.startswith(alias)]
        return command

    def postcmd(self, stop: bool, args: str) -> bool:

        """
        This function formats and prints the prompt value.
        """

        logger_debug("Formating the new prompt")
        self.prompt = self.format(self.prompt_template)

        if stop:
            return True

        return False

    def preloop(self) -> None:

        """
        This function prints the start message and
        changes the Unix Shell Colors.
        """

        logger_debug("Initializing the shell")
        format = self.format

        self.intro = format(self.intro_template)
        self.onecmd(format(self.start_intro_template))
        print(self.intro)
        self.onecmd(format(self.end_intro_template))

        self.intro = ""

    def postloop(self) -> None:

        """
        This function prints the exit message and
        changes the Unix Shell Color.
        """

        logger_debug("Quitting the shell")
        format = self.format
        
        self.quit = format(self.quit_template)
        self.onecmd(format(self.start_quit_template))
        print(self.quit)
        self.onecmd(format(self.end_quit_template))

        self.quit = ""

    def completedefault(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:

        """
        This functions returns filenames and directories for completion.
        """

        logger_debug("Searching files for completion")
        startfilename = shellsplit(line)[-1]
        directory, filename = split(startfilename)
        return [file for file in listdir(directory or None) if file.startswith(filename)]

    def completenames(self, line: str, state: str):

        """
        This functions returns filenames and directories for completion.
        """

        logger_debug("Searching files for completion")
        startfilename = shellsplit(line)[-1]
        directory, filename = split(startfilename)
        return [file for file in listdir(directory or None) if file.startswith(filename)]

    def complete_help(self, *args):

        """
        This function returns a empty list for help completion.
        """

        logger_debug("No completion for help command.")
        return []

def start(shell: Shell) -> int:

    """
    This function starts the shell and is recursive.
    """
    
    logger_debug("Starting a cmdloop")
    
    try:
        shell.cmdloop()
    except Exception as e:
        logger_error(f'An exception is raised: {e!r}')
        return start(shell)
    else:
        logger_warning("Exit.")
        return 0
        
    return 127

def main() -> int:
    
    """
    The main function to starts the Shell from the command line.
    """

    logger_debug("Building the Shell.")
    logger.level = 51

    shell = Shell()
    return start(shell)


if __name__ == "__main__":
    exit(main())
