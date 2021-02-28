#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This script implement a Custom Shell. """

###################
#    This script implement a Custom Shell.
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

__all__ = ["Shell", "CONFIG_VAR", "main"]

from cmd import Cmd
from os import system, getcwd, path, chdir
from getpass import getuser
from time import localtime, strftime
from socket import gethostname
from configparser import ConfigParser, NoOptionError
from typing import TypeVar
import os
import sys
import platform

Config = TypeVar("Config", str, None)

if os.name == "nt":
    DEFAULT_CONFIG = {
        "DISPLAY": {
            "prompt": "{U}@{N}:{P}$",
            "start_intro": "color a",
            "end_intro": "",
            "intro": "{n}*** {T} - Welcome on CustomShell {U} ! ***{n}",
            "start_quit": "",
            "end_quit": "color 4",
            "quit": "{n}*** Bye {U} ! - {T} ***{n}",
        },
        "ALIAS": {"pyc ": "python3 -c ", "pym ": "python3 -m "},
    }
else:
    DEFAULT_CONFIG = {
        "DISPLAY": {
            "prompt": "{U}@{N}:{P}$",
            "start_intro": "echo '{color}{bgwhite}{color}{bold}{demo}'",
            "end_intro": "echo '{color}{reset}'",
            "intro": "{n}*** {T} - Welcome on CustomShell {U} ! ***{n}",
            "start_quit": "echo '{color}{bgwhite}{color}{underline}{red}'",
            "end_quit": "echo '{color}{reset}'",
            "quit": "{n}*** Bye {U} ! - {T} ***{n}",
        },
        "ALIAS": {"pyc ": "python3 -c ", "pym ": "python3 -m "},
    }

CONFIG_VAR = {
    "{U}": getuser,
    "{N}": gethostname,
    "{P}": getcwd,
    "{T}": lambda: strftime("%H:%M:%S", localtime()),
    "{p}": platform.system,
    "{s}": lambda: os.name,
    "{n}": lambda: "\n",
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
    "{color}": "\e[",
}


class Shell(Cmd):

    """ This class implement the custom shell. """

    def __init__(self):
        super().__init__()

        self.config = ConfigParser()

        self.check_config_file()
        self.config.read("Shell.ini")

        self.config.setdefault("ALIAS", {})

        self.intro_template = (
            self.get_config("DISPLAY", "intro") or DEFAULT_CONFIG["DISPLAY"]["intro"]
        )
        self.start_intro_template = (
            self.get_config("DISPLAY", "start_intro")
            or DEFAULT_CONFIG["DISPLAY"]["start_intro"]
        )
        self.end_intro_template = (
            self.get_config("DISPLAY", "end_intro")
            or DEFAULT_CONFIG["DISPLAY"]["end_intro"]
        )

        self.prompt_template = (
            self.get_config("DISPLAY", "prompt") or DEFAULT_CONFIG["DISPLAY"]["prompt"]
        )

        self.quit_template = (
            self.get_config("DISPLAY", "quit") or DEFAULT_CONFIG["DISPLAY"]["quit"]
        )
        self.start_quit_template = (
            self.get_config("DISPLAY", "start_quit")
            or DEFAULT_CONFIG["DISPLAY"]["start_quit"]
        )
        self.end_quit_template = (
            self.get_config("DISPLAY", "end_quit")
            or DEFAULT_CONFIG["DISPLAY"]["end_quit"]
        )

        self.intro = self.format(self.intro_template)
        self.prompt = self.format(self.prompt_template)
        self.quit = self.format(self.quit_template)

    def get_config(self, section: str, value: str) -> Config:

        """ This function return config or None """

        try:
            return self.config.get(section, value)
        except NoOptionError:
            return None

    def format(self, string: str) -> str:

        """ This fonction format string template. """

        for substring, function in CONFIG_VAR.items():
            string = string.replace(substring, function())

        for color, code in UNIX_COLOR.items():
            string = string.replace(color, code)

        return string

    def check_config_file(self) -> bool:

        """ Check the config file and write it (with default config) if not exist. """

        config_path = path.join(path.expanduser("~"), "Shell.ini")
        if not path.exists(config_path):
            self.config.update(DEFAULT_CONFIG)
            with open(config_path, "w") as configfile:
                self.config.write(configfile)

            return False
        return True

    def do_cd(self, arg: str) -> None:

        """ Command cd to change the current directory. """

        try:
            chdir(arg)
        except FileNotFoundError:
            system(arg)

    def do_exit(self, arg: str) -> None:

        """ Command exit, quit and close the shell with error code 0. """

        return True

    def default(self, arg: str) -> None:

        """ Execute command line. """

        try:
            system(arg)
        except KeyboardInterrupt:
            print("")

    def precmd(self, arg: str) -> str:

        """ This function change ALIAS into real command. """

        for alias, command in self.config["ALIAS"].items():
            if arg.startswith(alias):
                arg = arg.replace(alias, command, 1)

        return arg

    def postcmd(self, stop: bool, arg: str) -> bool:

        """ This function re-write the prompt value. """

        self.prompt = self.format(self.prompt_template)

        if stop:
            return True

        return False

    def preloop(self) -> None:

        """ This function print intro and change the Unix Shell Color. """

        self.onecmd(self.format(self.start_intro_template))
        print(self.intro)
        self.onecmd(self.format(self.end_intro_template))

        self.intro = ""

    def postloop(self) -> None:

        """ This function print quit and change the Unix Shell Color. """

        self.onecmd(self.format(self.start_quit_template))
        print(self.quit)
        self.onecmd(self.format(self.end_quit_template))

        self.quit = ""


def main():
    shell = Shell()
    shell.cmdloop()
    sys.exit(0)


if __name__ == "__main__":
    main()
