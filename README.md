# PCRD-DiscordBot
## Installation
 * Install [Python](https://www.python.org/downloads/). **Version 3.6 is required**.
 * Install [pip](https://pip.pypa.io/en/stable/installing/) if you haven't.
 * **Upgrade the built-in sqlite3 in Python to at least 3.25.0**. Run `python -c "import sqlite3; print(sqlite3.sqlite_version)"` to check that.
 * Copy the source into your favorite folder.
 * Run `python setup.py`.
## Setup
#### Discord Application
 Prepare your discord bot instance at [discordapp.com](https://discordapp.com/developers/applications/) and put the token in utils/token.json as:
 ```
 {
    "token": "your_token"
 }
 ```
## Get started
 * Run `python main.py`. Again, use python of version 3 or above.
 * If something wrong happens, ask admin to type `!stop` in discord to shut the bot down. Otherwise you have to kill it in your machine. 
