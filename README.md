![CustomShell logo](https://mauricelambert.github.io/info/python/code/CustomShell_small.png "CustomShell logo")

# CustomShell

## Description

This package implements a Customizable Shell.

## Requirements

This package require:
 - python3
 - python3 Standard Library

## Installation

```bash
pip install CustomShell
```

## Usages

### Command lines

```bash
python3 -m CustomShell
python3 CustomShell.pyz
Shell
```

![Demonstration Linux](https://mauricelambert.github.io/info/python/code/CustomShell_linux.JPG)
![Demonstration Windows](https://mauricelambert.github.io/info/python/code/CustomShell_windows.JPG)

### Python3

```python
from CustomShell import main
main()

from CustomShell import Shell
shell = Shell()
shell.cmdloop()
```

## Configuration

### Default

Default configuration file path:
 - **Windows**: `C:\\Users\\<username>\\Shell.ini`
 - **Linux**: `~/Shell.ini`

```ini
[DISPLAY]
prompt = {E} {color}{green}{U}{color}{reset}@{color}{green}{N}{color}{reset}:{color}{green}{P}{color}{reset}$
start_intro = echo {a}
end_intro = echo {a}
intro = {S}     {V}     [{s}, {o}] {n}Python    {v}         [{e}]{n}CustomShell     {c}         [GPL-3.0]{n}{n}{color}{bgwhite}{color}{bold}{blue}*** {D} {T} - Welcome in CustomShell {U} ! ***{color}{reset}{n}
start_quit = echo {a}
end_quit = echo {a}
quit = {n}{color}{bgwhite}{color}{underline}{red}*** {D} {T} - Bye {U} ! ***{color}{reset}{n}

[ALIAS]
pyc  = python -c 
pym  = python -m 


```

### Variables for configuration

```
{U} = username,
{N} = hostname,
{P} = current path,
{p} = directory,
{T} = time,
{D} = date,
{o} = operatoring system (win32, linux, ...),
{S} = system (Windows, Linux, ...),
{s} = system (nt, posix...),
{n} = new line (\n),
{a} = ASCII character 7 (sound),
{e} = python executable,
{v} = python version,
{V} = system version,
{c} = CustomShell version,
{E} = status of the last command execution,
```

### Unix Color

```
{black} {red} {green} {other} {blue} {purple} {cyan} {white} {bgblack} {bgred} {bggreen} {bgother} {bgblue} {bgpurple} {bgcyan} {bgwhite} {texte} {bold} {underline} {reset} {color}
```

 - To make a white background you can use: `{color}{bgwhite}`.
 - To make a blue bold text you can use: `{color}{bold}{blue}`.
 - To make a red undernline text you can use: `{color}{underline}{red}`.
 - To reset color: `{color}{reset}`.

## Links

 - [Github Page](https://github.com/mauricelambert/CustomShell)
 - [Pypi](https://pypi.org/project/CustomShell/)
 - [Documentation](https://mauricelambert.github.io/info/python/code/CustomShell.html)
 - [Executable](https://mauricelambert.github.io/info/python/code/CustomShell.pyz)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
