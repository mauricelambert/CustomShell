#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file implements a Custom Shell.
"""

###################
#    This file implement a Custom Shell.
#    Copyright (C) 2021  Maurice Lambert

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

__version__ = "0.1.2"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements a Custom Shell.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/CustomShell"

copyright = """
CustomShell  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["Shell", "CONFIG_VAR", "main"]

from os import system, getcwd, path, chdir, listdir, device_encoding
from configparser import ConfigParser, NoOptionError
from logging import StreamHandler, Formatter, Logger
from time import localtime, strftime
from typing import TypeVar, List
from getpass import getuser
from cmd import Cmd
import platform
import logging
import sys
import os

Config = TypeVar("Config", str, None)

if os.name == "nt":
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
    "{N}": platform.node,
    "{P}": getcwd,
    "{p}": lambda: path.dirname(getcwd()),
    "{T}": lambda: strftime("%H:%M:%S", localtime()),
    "{D}": lambda: strftime("%y-%m-%d", localtime()),
    "{S}": platform.system,
    "{o}": lambda: sys.platform,
    "{s}": lambda: os.name,
    "{n}": lambda: "\n",
    "{a}": lambda: "\7",
    "{e}": lambda: sys.executable,
    "{v}": lambda: (
        f"{sys.version_info.major}."
        f"{sys.version_info.minor}.{sys.version_info.micro}"
    ),
    "{V}": platform.version,
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
    This function create a custom logger.
    """

    logger = logging.getLogger(__name__)  # default logger.level == 0

    formatter = Formatter(
        fmt=(
            "%(asctime)s%(levelname)-9s(%(levelno)s) "
            "{%(name)s - %(filename)s:%(lineno)d} %(message)s"
        ),
        datefmt="[%Y-%m-%d %H:%M:%S] ",
    )
    stream = StreamHandler(stream=sys.stdout)
    stream.setFormatter(formatter)

    logger.addHandler(stream)

    return logger


logger: Logger = get_custom_logger()


class Shell(Cmd):

    """
    This class implement the custom shell.
    """

    def __init__(self):
        super().__init__()

        self.encoding = device_encoding(0).casefold()
        self.ref_encoding = "utf-8".casefold()
        self.state = None
        self.config = ConfigParser()
        self.config_path = path.join(path.expanduser("~"), "Shell.ini")

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
        This function return config or None
        """

        logger.debug("Get configuration...")
        try:
            return self.config.get(section, value)
        except NoOptionError:
            logger.warning("Configuration error.")
            return None

    def format(self, string: str) -> str:

        """
        This fonction format string template.
        """

        logger.debug(f"Format string: {string}.")
        for substring, function in self.var.items():
            string = string.replace(substring, function())

        logger.debug(f"Add color: {string}.")
        for color, code in UNIX_COLOR.items():
            string = string.replace(color, code)

        logger.info(f"Formatted string: {string}")
        return string

    def check_config_file(self) -> bool:

        """
        Check the config file and write it (with default config) if not exist.
        """

        logger.debug("Get configuration...")

        if not path.exists(self.config_path):
            logger.info("Configuration file exist.")

            self.config.update(DEFAULT_CONFIG)
            logger.info("Configuration is updated.")

            with open(self.config_path, "w") as configfile:
                self.config.write(configfile)

            logger.info("Configuration is saved.")
            return False
        return True

    def do_cd(self, arg: str) -> bool:

        """
        Command cd to change the current directory.
        """

        logger.debug("Command to change the directory.")

        try:
            chdir(arg)
        except FileNotFoundError:
            logger.error('An error is raised on "cd" command.')
            system("cd " + arg)
            self.state = True
        else:
            self.state = False

        return False

    def do_GetConfigFile(self, arg: str) -> bool:

        """
        Command to get the configuration file path.
        """

        logger.debug("Print the configuration file path.")
        print(self.config_path)
        self.state = False
        return False

    def do_configfile(self, arg: str) -> bool:

        """
        Command to get the configuration file path.
        """

        logger.debug("Print the configuration file path.")
        print(self.config_path)
        self.state = False
        return False

    def do_help(self, arg: str) -> bool:

        """
        Command help.
        """

        logger.debug(f"Command help: {arg}")
        self.state = system(f"help {arg}")
        return False

    def do_exit(self, arg: str) -> bool:

        """
        Command exit, quit and close the shell with error code 0.
        """

        logger.debug("Command exit.")
        return True

    def do_quit(self, arg: str) -> bool:

        """
        Command exit, quit and close the shell with error code 0.
        """

        logger.debug("Command quit.")
        return True

    def default(self, arg: str) -> bool:

        """
        Execute command line.
        """

        logger.debug(f"Command: {arg}")

        try:
            self.state = system(arg)
        except KeyboardInterrupt:
            logger.info("A KeyboardInterrupt error is raised.")
            print('Use "exit" command to quit the terminal.')

        return False

    def precmd(self, arg: str) -> str:

        """
        This function change ALIAS into real command.
        """

        logger.debug("Resolve alias...")

        for alias, command in self.config["ALIAS"].items():
            if arg.startswith(alias):
                logger.info(f"Alias found: {alias} -> {command}")
                arg = arg.replace(alias, command, 1)

        return arg

    def postcmd(self, stop: bool, arg: str) -> bool:

        """
        This function re-write the prompt value.
        """

        logger.debug("Build the new prompt...")
        self.prompt = self.format(self.prompt_template)

        if stop:
            return True

        return False

    def preloop(self) -> None:

        """
        This function print intro and change the Unix Shell Color.
        """

        logger.debug("Initialize the shell...")
        self.intro = self.format(self.intro_template)
        self.onecmd(self.format(self.start_intro_template))
        print(self.intro)
        self.onecmd(self.format(self.end_intro_template))

        self.intro = ""

    def postloop(self) -> None:

        """
        This function print quit and change the Unix Shell Color.
        """

        logger.debug("Quit the shell...")
        self.quit = self.format(self.quit_template)
        self.onecmd(self.format(self.start_quit_template))
        print(self.quit)
        self.onecmd(self.format(self.end_quit_template))

        self.quit = ""

    def completedefault(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:

        """
        This function defines the default completion (files an directories).
        """

        logger.debug("File completion...")
        args = line.split()
        path_ = args[-1]
        directory, file = path.split(path_)
        return [f for f in listdir(directory or None) if f.startswith(file)]

    def completenames(self, line: str, state: str):

        """
        This function defines the default completion (files an directories).
        """

        logger.debug("File completion...")
        args = line.split()
        path_ = args[-1]
        directory, file = path.split(path_)
        return [f for f in listdir(directory or None) if f.startswith(file)]

    def complete_help(self, *args):

        """
        This function returns a empty list.
        """

        logger.debug("No completion for help command.")
        return []


def main():
    print(copyright)

    logger.debug("Build the Shell...")
    logger.level = 51

    shell = Shell()

    while True:
        try:
            logger.debug("Start a cmdloop...")
            shell.cmdloop()
        except Exception as e:
            logger.error(f'An exception is raised: {e.__class__} "{e}"')
            print(f"{e.__class__}: {e}")
            if isinstance(FileNotFoundError, e):
                logger.warning(
                    "Current folder probably no longer exists, the current"
                    " directory is replaced by the root directory."
                )
                chdir("/")
        else:
            logger.warning("Exit.")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
