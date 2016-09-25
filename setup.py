from setuptools import setup

setup(name='botbullet',
      version='0.0.3',
      description='A human-bot interface powered by Pushbullet',
      url='https://github.com/antfu/botbullet',
      author='Anthony Fu',
      author_email='anthonyfu117@hotmail.com',
      license='MIT',
      packages=['botbullet'],
      install_requires=[
        'biconfigs',
        'pushbullet.py'
      ],
      dependency_links=[
         "git+https://github.com/antfu/biconfigs.git"
      ],
      zip_safe=False)
