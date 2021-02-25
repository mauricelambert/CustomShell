from setuptools import setup, find_packages
import CustomShell

setup(
    name = 'CustomShell',
 
    version = CustomShell.__version__,
    packages = find_packages(),
    install_requires = [],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This script implement a Custom Shell.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/CustomShell',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
 
    entry_points = {
        'console_scripts': [
            'CustomShell = CustomShell:shell'
        ],
    },
    python_requires='>=3.6',
)