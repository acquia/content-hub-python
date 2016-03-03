from setuptools import *

setup(
  name = 'content_hub_python',
  packages = find_packages(), # this must be the same as the name above
  version = '1.0.0a0',
  description = 'A python client library for Acquia Content Hub',
  author = 'Acquia',
  author_email = 'denes.lados@acquia.com',
  url = 'https://github.com/acquia/content-hub-python', # use the URL to the github repo
  download_url = 'https://github.com/acquia/content-hub-python/tarball/0.1', # I'll explain this in a second
  keywords = ['content-hub', 'acquia'], # arbitrary keywords
  classifiers = [],
)
