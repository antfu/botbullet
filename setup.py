from setuptools import setup

setup(name='botbullet',
      version='0.0.2',
      description='A human-bot interface powered by Pushbullet',
      url='https://github.com/antfu/botbullet',
      author='Anthony Fu',
      author_email='anthonyfu117@hotmail.com',
      license='MIT',
      packages=['botbullet'],
      dependency_links=[
         "git+https://github.com/antfu/biconfigs.git",
         "git+https://github.com/antfu/pushbullet.py.git"
      ],
      zip_safe=False)
