#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='nose-moretodo',
    version='1.0a1',
    description='Mark tests to-do in the spirit of Test::More',
    author='Mark Paschal',
    author_email='markpasc@markpasc.org',

    py_modules=['moretodo'],
    provides=['moretodo'],
    requires=['nose(>=1.10)'],

    entry_points={
        'nose.plugins.0.10': [
            'moretodo = moretodo:MoreTodo',
        ],
    },
)
