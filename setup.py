#! /usr/bin/env python

from setuptools import setup, find_packages

setup(name='imessage',
      version='0.0.1',
      license='BSD',
      author='John Wiggins',
      author_email='jwiggins@enthought.com',
      description='A library for communicating with iMessage',
      long_description='',
      url='https://github.com/jwiggins/imessage',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Operating System :: MacOS',
      ],
      packages=find_packages(),
      package_data={},
      )
