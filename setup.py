##wget "http://python-distribute.org/distribute_setup.py"
#import distribute_setup
#distribute_setup.use_setuptools()

from setuptools import setup, find_packages


packages = find_packages()
install_requires = [line.strip() for line in open("requirements.txt").readlines()]

try:
    long_description = open('README.md', 'r').read()
except:
    long_description = 'UNKNOWN'

setup(
    name='graphlab_extras',
    version='0.0.1',
    description='GraphLab extras',
    keywords=['graphlab', 'extras'],
    author='Will Fitzgerald',
    author_email='will.fitzgerald@gmail.com',
    url='https://github.com/willf/graphlab_extras',
    license='Attribution 4.0 International (CC BY 4.0)',
    packages=packages,
    long_description=long_description,
    install_requires=install_requires,
    package_data={'' : ['README.md'] }  # NOTE: MANIFEST.in overrides this
)
