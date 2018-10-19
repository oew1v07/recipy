"""
Functions to access information about the execution environment.
"""

# Copyright (c) 2015-2016, 2018 University of Edinburgh,
# University of Southampton and Netherlands eScience Center.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import getpass
import os.path
import platform
import sys
import pkg_resources
from dateutil.parser import parse


def get_str_as_date(date_str):
    """
    Convert string to date object.

    :param date_str: Date string e.g. '2016-09-12T09:40:20'
    :type date_str: str or unicode
    :return: date
    :rtype: datetime.datetime
    """
    return parse(date_str)


def get_tinydatestr_as_date(date_str):
    """
    Convert TinyDate string to date object.

    :param date_str: Date string e.g. '{TinyDate}:2016-09-12T09:40:20'
    :type date_str: str or unicode
    :return: date
    :rtype: datetime.datetime
    """
    return parse(date_str.replace('{TinyDate}:', ''))


def get_user():
    """
    Get current user.

    :return: current user
    :rtype: str or unicode
    """
    return getpass.getuser()


def get_python_exe():
    """
    Get Python executable path.

    :return: Python executable path
    :rtype: str or unicode
    """
    return sys.executable


def get_python_version():
    """
    Get Python version.

    :return: Python version
    :rtype: str or unicode
    """
    return sys.version.split("\n")[0]


def get_os():
    """
    Get operating system.

    :return: operating system
    :rtype: str or unicode
    """
    return platform.platform()


def is_package_installed(packages, package):
    """
    Is a package installed?

    :param packages: installed packages and versions, keyed by package
    name
    :type packages: dict of str or unicode => str or unicode
    :param package: Package name
    :type package: str or unicode
    :return: True if it is installed, False otherwise
    :rtype: bool
    """
    return package in packages


def get_package_version(packages, package):
    """
    Get version of installed package.

    :param packages: installed packages and versions, keyed by package
    name
    :type packages: dict of str or unicode => str or unicode
    :param package: Package name
    :type package: str or unicode
    :return: Package version
    :rtype: str or unicode
    :raises KeyError: if the package is not installed
    """
    return packages[package]


def get_packages():
    """
    Get list of installed packages and their versions.

    :return: installed packages and versions, keyed by package name
    :rtype: dict of str or unicode => str or unicode
    """
    packages = pkg_resources.working_set
    packages_dict = {}
    for package in packages:
        # Some packages are imported using their `package.key` (keys do not
        # contain capitals), e.g., gdal. Others are imported using their
        # `package.project_name`, e.g., netCDF4. So, both the `key` and
        # `project_name` are added to the `packages_dict`.
        modules_from_package = package._get_metadata('top_level.txt')
        for mod in modules_from_package:
            packages_dict[mod] = package.version

        packages_dict[package.key] = package.version
        packages_dict[package.project_name] = package.version
    return packages_dict


def get_home_dir():
    """
    Get home directory.

    :return: home directory
    :rtype: str or unicode
    """
    return os.path.expanduser("~")
