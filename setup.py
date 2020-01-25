from setuptools import setup

setup(
    name='PCRD-DiscordBot',
    version='1.0',
    description='Discord bot for PCRD player to record their clan battle result',
    author='stkoso',
    author_email='stkoso0835@gmail.com',
    install_requires=['google-api-python-client', 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib', 'pytz', 'dblpy', 'discord.py']
)
