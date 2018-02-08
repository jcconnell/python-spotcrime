"""Setup."""

from setuptools import find_packages, setup

setup(
    name='spotcrime',
    version='1.0.1',
    description='Provides basic API to spotcrime.com.',
    url='https://github.com/jcconnell/python-spotcrime',
    license='MIT',
    author='jcconnell',
    author_email='jamescarltonconnell@gmail.com',
    packages=find_packages(),
    install_requires=['requests==2.12.4'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        ]
)
