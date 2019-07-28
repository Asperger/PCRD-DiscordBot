# PCRD-DiscordBot
## Installation
 * Install [Python3](https://www.python.org/downloads/). Version 3.6 is preferred
 * Install [pip](https://pip.pypa.io/en/stable/installing/)
 * Copy the source into your favorite folder
 * Run `python setup.py`. If you have different version of python installed, be sure you use version 3 or above, i.e., `python3 setup.py`.
## Setup
#### Database
 Prepare a database engine(I use sqlserver here) and specify the connection information in utils/db_conn.json as:
 ```
 {
    "server":"your.server.dns",
    "user":"your_account",
    "password":"your_password",
    "database":"your_database"
 }
 ```
 In the database, 2 tables are needed:
 ```
CREATE TABLE [dbo].[TimeTable](
	[user_id] [bigint] NOT NULL,
	[rounds] [int] NOT NULL,
	[boss] [int] NOT NULL,
	[damage] [int] NULL,
	[play_date] [date] NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[TimeTable] ADD  CONSTRAINT [DF_TimeTable_damage]  DEFAULT ((0)) FOR [damage]
GO
ALTER TABLE [dbo].[TimeTable] ADD  CONSTRAINT [DF_TimeTable_play_date]  DEFAULT (CONVERT([date],switchoffset(getdate(),'+03:00'),(1))) FOR [play_date]
GO

CREATE TABLE [dbo].[UserTable](
	[user_id] [bigint] NOT NULL,
	[damage] [int] NULL,
	[normal_play] [int] NULL,
	[last_play] [int] NULL,
	[compensate_play] [int] NULL,
	[missing_play] [int] NULL,
	[play_date] [date] NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_damage]  DEFAULT ((0)) FOR [damage]
GO
ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_normal_party]  DEFAULT ((0)) FOR [normal_play]
GO
ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_last_play]  DEFAULT ((0)) FOR [last_play]
GO
ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_complement_party]  DEFAULT ((0)) FOR [compensate_play]
GO
ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_missing_party]  DEFAULT ((0)) FOR [missing_play]
GO
ALTER TABLE [dbo].[UserTable] ADD  CONSTRAINT [DF_UserTable_play_date]  DEFAULT (CONVERT([date],switchoffset(getdate(),'+03:00'),(1))) FOR [play_date]
GO
 ```
 Be noted that `'+03:00'` represents the daily settlement time of clan battle as 00:00:00 UTC+03:00.
#### Discord Application
 Prepare your discord bot instance at [discordapp.com](https://discordapp.com/developers/applications/) and put the token in utils/token.json as:
 ```
 {
    "token": "your_token"
 }
 ```
## Get started
 * You might need a way to shut your bot peacefully. Replace the magic id in main.py with your own [discord id](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-).
 * Run `python main.py`. Again, use python of version 3 or above.
 * If something wrong happens, type `!stop` in discord to shut your bot down. Otherwise you have to Ctrl-C in your machine. 
