import os
from setuptools import setup, find_packages
import pylox


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pylox',
    version=pylox.__version__,
    author='Sasha Matijasic',
    author_email='sasha@selectnull.com',
    packages=find_packages(),
    url='https://github.com/selectnull/pylox',
    license='MIT',
    description='Python implementation of Lox programming language',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pylox = pylox.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
