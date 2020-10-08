from distutils.core import setup
from setuptools import find_packages

setup(name='cashaddress-regtest',
      version='1.1.0',
      packages=find_packages(),
      description='Python tool for convert bitcoin cash and legacy addresses',
      author='Nicolai Skye',
      author_email='nicolaiskye@icloud.com',
      url='https://github.com/nicolaiskye/cashaddress',
      download_url='https://github.com/nicolaiskye/cashaddress/archive/1.1.0.tar.gz',
      python_requires='>=2.7',
      keywords=['bitcoincash', 'bch', 'address', 'cashaddress', 'legacy', 'convert'],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
)
