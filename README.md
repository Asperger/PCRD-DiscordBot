# PCRD-DiscordBot
## Installation
 * Install [Python3](https://www.python.org/downloads/). **Version 3.6 is preferred**
 * Install [pip](https://pip.pypa.io/en/stable/installing/)
 * **Upgrade the built-in sqlite3 in Python to at least 3.25.0**
 * Copy the source into your favorite folder
 * Run `python setup.py`. If you have different version of python installed, **be sure you use version 3 or above**, i.e., `python3 setup.py`.
## Setup
#### Database
 Prepare a sqlite database in utils/repo.db and create 2 tables:
 ```
CREATE TABLE "TimeTable" (
	"user_id"	INTEGER NOT NULL,
	"rounds"	INTEGER NOT NULL,
	"boss"	INTEGER NOT NULL,
	"damage"	INTEGER NOT NULL,
	"play_date"	TEXT NOT NULL
);

CREATE TABLE "UserTable" (
	"user_id"	INTEGER NOT NULL,
	"damage"	INTEGER NOT NULL,
	"normal_play"	INTEGER DEFAULT 0,
	"last_play"	INTEGER DEFAULT 0,
	"compensate_play"	INTEGER DEFAULT 0,
	"missing_play"	INTEGER DEFAULT 0,
	"play_date"	TEXT NOT NULL
);
 ```
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
