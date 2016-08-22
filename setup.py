from setuptools import setup

setup(name='amspy',
      version='0.0.5',
      summary='Simple Python Library for Azure Media Services REST API',
      description='The amspy is a library to provide a simple Azure Media Services REST interface for python. This is a personal project and NOT an official implementation of the Azure Media Services SDK for python. The only purpose of this library is for educational purposes, so people can have an easy way to understand how to interact with cloud REST apis, and learn from the examples provided in this module as well as the debug information available in the logs. Any feedback, comments or bugs, please send directly to the module owner, and go to https://azure.microsoft.com if you are looking for official Microsoft Azure SDKs.',
      url='http://github.com/msleal/amspy',
      author='msleal',
      author_email='msl@eall.com.br',
      license='MIT',
      packages=['amspy'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
