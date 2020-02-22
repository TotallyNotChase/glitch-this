from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

setup(
    name='glitch_this',
    version='0.0.2',
    author='TotallyNotChase',
    author_email='44284917+TotallyNotChase@users.noreply.github.com',
    description='A package to glitch images',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/TotallyNotChase/Glitch-and-Gif',
    packages=find_packages(),
    install_requires=[
        'Pillow>=6.2.1',
        'numpy>=1.18.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT Licence",
    ],
)
