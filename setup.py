"""
PyPI setup file
"""

from setuptools import setup


setup(
    name='pyng3',
    packages=['pyng'],
    version='3.0.0',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/Pyng',

    description='Simple, pretty ping wrapper (for *nix)',
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    entry_points={
        'console_scripts': [
            'pyng=pyng.main:main',
            'pyng3=pyng.main:main',
        ],
    },
)
