from setuptools import setup

setup(
    name='EveHolder',
    version='0.9',
    packages=['mysite', 'eve_holder', 'eve_holder.tests', 'eve_holder.management', 'eve_holder.management.commands',
              'eve_holder.migrations', 'eve_holder.templatetags'],
    url='https://eve-holder.herokuapp.com/',
    license='',
    author='Eve Group',
    author_email='james31366@gmail.com',
    description='Web Application for Event'
)
