from setuptools import setup, find_packages
from pip.req import parse_requirements
import os
from setuptools import Command
import sys


def release(args):
    print(args)
    version = args[0].split('.')
    version = "{}.{}.{}".format(version[0], version[1], version[2])
    import json
    with open('./package.json', 'r+', encoding='utf-8') as f:
        package = json.load(f)
        package['version'] = version
        f.seek(0)
        json.dump(package, f, ensure_ascii=False, indent=2)
    if '--commit' in args:
        print('committing')
        os.system('git commit -m "chore(release): {}"'.format(version))
        os.system('git tag v{}'.format(version))
    print(args)


cmds = {"build": 'python setup.py bdist_wheel',
        'changelog':
            "conventional-changelog -p angular -i CHANGELOG.md -s -r 0",
        'clean': 'rm -r sdu_bkjws.egg-info build dist',
        'release': release
        }

for cmd, value in cmds.items():
    if cmd == sys.argv[1]:
        if isinstance(value, str):
            os.system(value)
        else:
            value(sys.argv[2:])
        exit(0)

setup(name='sdu_bkjws',
      version='0.1.0',
      url='https://github.com/Trim21/sdu_bkjws',
      platforms=['any'],
      license='GPLv3',
      author='Trim21',
      author_email='trim21me@gmail.com',
      description='sdu bkjws libary',
      packages=find_packages('sdu_bkjws', exclude=['tests']),
      long_description=open('readme.md', 'r', encoding='utf-8').read(),
      zip_safe=True,
      install_requires=open('requirements.txt', 'r',
                            encoding='utf-8').read().splitlines()
      )
