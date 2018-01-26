from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='dupfileremover',
      version='0.2',
      description='A command line utility that helps you find  and remove duplicate files',
      long_description=readme(),
      url='http://github.com/kpeterstech/dupfileremover',
      author='Kit Peterson',
      author_email='kpeterstech@gmail.com',
      license='MIT',
      packages=['dupfileremover'],
      install_requires=[
          'Click',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['dupfileremover=dupfileremover.command_line:cli']
      })
