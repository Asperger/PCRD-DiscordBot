# PCRD-DiscordBot
## Installation
 * Install [Python](https://www.python.org/downloads/). **Version 3.6 is preferred**.
 * Install [pip](https://pip.pypa.io/en/stable/installing/) if you haven't.
 * **Upgrade the built-in sqlite3 in Python to at least 3.25.0**. Run `python -c "import sqlite3; print(sqlite3.sqlite_version)"` to check that.
 * Copy the source into your favorite folder.
 * Run `python setup.py`.
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
