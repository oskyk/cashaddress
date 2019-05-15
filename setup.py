from distutils.core import setup
from setuptools import find_packages

setup(name='cashaddress',
      version='1.0.6',
      packages=find_packages(),
      description='Python tool for converty bitcoin cash legacy addresses',
      author='Oskar Hladky',
      author_email='oskyks1@gmail.com',
      url='https://github.com/oskyk/cashaddress',
      download_url='https://github.com/oskyk/cashaddress/archive/1.0.4.tar.gz',
      python_requires='>=2.7',
      keywords=['bitcoincash', 'bch', 'address', 'cashaddress', 'legacy', 'convert'],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
)
