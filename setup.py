from setuptools import setup

setup(
    name='PCRD-DiscordBot',
    version='1.0',
    description='Discord bot for PCRD player to record their clan battle result',
    author='stkoso',
    author_email='stkoso0835@gmail.com',
    packages=['PCRD-DiscordBot'],
    install_requires=['dblpy', 'discord.py'],
)
