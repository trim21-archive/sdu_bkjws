import json
import os
import sys

from setuptools import setup, find_packages


def release(args):
    print(args)
    version = args[0].split('.')
    version = "{}.{}.{}".format(version[0], version[1], version[2])
    with open('./package.json', 'r+', encoding='utf-8') as f:
        package = json.load(f)
        package['version'] = version
    with open('./package.json', 'w', encoding='utf-8') as f:

        json.dump(package, f, ensure_ascii=False, indent=2)
    os.system("conventional-changelog -p angular -i CHANGELOG.md -s -r 0")
    if '--commit' in args:
        print('committing')
        os.system('git add CHANGELOG.md package.json')
        os.system('git commit -m "chore(release): {}"'.format(version))
        os.system('git tag v{}'.format(version))


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

with open('./package.json', 'r', encoding='utf-8') as f:
    version = json.load(f)['version']
print(version)
setup(name='sdu_bkjws',
      version=version,
      url='https://github.com/Trim21/sdu_bkjws',
      platforms=['any'],
      license='GPLv3',
      author='Trim21',
      author_email='trim21me@gmail.com',
      description='sdu bkjws library',
      packages=find_packages('.', exclude=['*test', 'test*', 'test', '*test*']),
      long_description=open('readme.md', 'r', encoding='utf-8').read(),
      zip_safe=True,
      install_requires=open('requirements.txt', 'r',
                            encoding='utf-8').read().splitlines(),
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
      ],
      # classifiers=(
      #     'Natural Language :: Chinese (Simplified)',
      #     'Programming Language :: Python',
      #     'Programming Language :: Python :: 3',
      #     'Programming Language :: Python :: 3.5',
      #     'Programming Language :: Python :: 3.6',
      #     'Programming Language :: Python :: Implementation :: CPython',
      #     'Programming Language :: Python :: Implementation :: PyPy'
      # ),
)
