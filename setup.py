from setuptools import setup, Extension
import os

_VERSION_ = '0.2'

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pymys',
      version=_VERSION_,
      description='It is a module to make easier communication with MySensor\'s network.',
      author='Alfredo Miranda',
      author_email='alfredocdmiranda@gmail.com',
      url='https://github.com/alfredocdmiranda/pymys',
      keywords="MYS MySensors",
      license='MIT',
      long_description=read('DESCRIPTION.rst'),
      classifiers=CLASSIFIERS,
      packages=['pymys'])