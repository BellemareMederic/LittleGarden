from setuptools import setup

setup(
   name='LittleGarden',
   version='1.0',
   description='Application to controle water and light on plant',
   author='Médéric Bellemare',
   author_email='bellemaremederic@gmail.com',
   packages=['LittleGarden'],  #same as name
   install_requires=[
          'RPi.GPIO',
      ],
)