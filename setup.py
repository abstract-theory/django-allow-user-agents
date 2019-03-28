import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-allow-user-agents',
    version='0.9',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A Django app for limiting page access to whitelisted user-agents',
    long_description=README,
    url='https://github.com/abstract-theory',
    author='',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',        
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',        
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
