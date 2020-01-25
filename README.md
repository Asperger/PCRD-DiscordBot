# PCRD-DiscordBot
## Installation
 * Install [Python](https://www.python.org/downloads/). **Version 3.6 is required**.
 * Install [pip](https://pip.pypa.io/en/stable/installing/).
 * Install [Python setuptools](https://pypi.org/project/setuptools/).
 * Copy or clone the source into your favorite folder.
 * Run `python setup.py install`.
## Setup
#### Discord Application
 Prepare your discord bot instance at [discordapp.com](https://discordapp.com/developers/applications/) and put the token in utils/token.json as:
 ```
 {
    "token": "your_token"
 }
 ```
#### Google Authentication
 Enable google sheets API with a certain google account. Check [this](https://developers.google.com/sheets/api/quickstart/python) for details.
 Save the credentials in utils/credentials.json.
## Get started
 * Run `python main.py`
 * If something wrong happens, ask admin to type `!stop` in discord to shut the bot down. Otherwise you have to kill it in your machine. 
