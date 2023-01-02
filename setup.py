import platform
import CustomShell as package
from setuptools import setup
from subprocess import check_call, DEVNULL
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopScript(develop):
    def run(self):

        if platform.system() == "Windows":
            check_call(
                [
                    r"C:\WINDOWS\system32\reg.exe",
                    "add",
                    r"HKEY_CURRENT_USER\Console",
                    "/v",
                    "VirtualTerminalLevel",
                    "/t",
                    "REG_DWORD",
                    "/d",
                    "0x00000001",
                    "/f",
                ],
                stdout=DEVNULL,
                stderr=DEVNULL,
            )  # Active colors in console

        develop.run(self)


class PostInstallScript(install):
    def run(self):

        if platform.system() == "Windows":
            check_call(
                [
                    r"C:\WINDOWS\system32\reg.exe",
                    "add",
                    r"HKEY_CURRENT_USER\Console",
                    "/v",
                    "VirtualTerminalLevel",
                    "/t",
                    "REG_DWORD",
                    "/d",
                    "0x00000001",
                    "/f",
                ],
                stdout=DEVNULL,
                stderr=DEVNULL,
            )  # Active colors in console

        install.run(self)


setup(
    name=package.__name__,
    version=package.__version__,
    py_modules=[package.__name__],
    install_requires=[],
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    description=package.__description__.strip(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=package.__url__,
    project_urls={
        "Documentation": "https://mauricelambert.github.io/info/python/code/CustomShell.html",
        "Executable": "https://mauricelambert.github.io/info/python/code/CustomShell.pyz",
    },
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    keywords=[
        "Shell",
        "Command",
        "Terminal",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    entry_points={
        "console_scripts": ["Shell = CustomShell:main"],
    },
    license=package.__license__,
    cmdclass={
        "develop": PostDevelopScript,
        "install": PostInstallScript,
    },
)
