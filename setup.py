from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]


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
      setup_requires=['pbr'],
      pbr=True,

      install_requires=reqs)
