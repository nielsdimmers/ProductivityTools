# productivity tools
Tools to help me be more productive

Currently, the tool supports the following commands:

```
tk - add a task
log - do a log check
daily - get a daily update
b - add a grocery (send empty to get list)
week - return the week number
weight - set your weight
grateful - set your grateful thought
goal - set your goal (or leave empty to get it)
```
Add a / before it in telegram to execute them when sending messages to the bot.

# Instructions to auto run
I finally figured out how to do this, so I'm saving it here. I did this on my raspberry pi.

Add below text to a file in the system services folder (``/etc/systemd/system``). Fill in the correct locations and you might want to change the user and group if you're on a different system.

```
[Unit]
Description = Productivity Tools Bot Listener
After=multi-user.target

[Install]
WantedBy=multi-user.target

[Service]
ExecStart=python3 <Location of the listener file here>
Type=simple
User=pi
Group=pi
WorkingDirectory= <folder of the listener file here>
```

Start the deamon: ``systemctl start <name of the service file>``

Configure to start at boot: ``systemctl enable <name of the service file>``

# How to send an e-mail
First, make sure the script mailcheck is ran at regular intervals, and create a `config_mail` with the required configuration. See `config_mail.default` for an example

Send an e-mail to the given e-mail address with the in config_mail specified indicators, and the text between the indicators will be added as an journal entry.

# Change log
(most recent on top)

## 2023-01-30
+ (major) added functionality to be able to write a journal entry based on an e-mail message.

## 2023-01-29.1
Had a lot of pi reboots this week, and restarting the process is something I haven't forgotten yet, but just don't want to be bothered with.
+ (minor) Bot sends me a message when it boots
+ (minor) Added information on how to auto start the bot at reboot
+ (minor) Downsized the journal to 99 lines, but maybe need to split that one op for clarification reasons.

## 2023-01-29
+ (minor) Fixed daily journal goal
+ (major) Added word count (including setting the property) to daily journal

## 2023-01-27.1
Sorry, but this one was too cool to let it slide!
+ (medium) The Telegram response is sent in markdown! Works for tasks and groceries.

## 2023-01-27
+ (minor)  fixed command list above to use newlines
+ (major)  fixed weight command
+ (minor)  removed wishlist from readme page, it's in the todo list now.
+ (major)  big overhaul of the journal and notion pages, not naming functions by property name caused removal of duplicate code
+ (medium) the listener can now directly use journal instead of going through notion. 

## 2023-01-08
+ (medium) Added feedback to micro journal (you now get a confirmation message or error message)
+ (minor)  Added a list of commands to the README file
+ (minor)  Fixed a bug with command ``/b`` where there wasn't a response (related to ``async`` / ``await``)
+ (medium) Added functionality so that an empty ``/grateful`` shows the grateful message
+ (minor)  Added markup to more explicitly show commands in the readme

## 2023-01-02
+ (minor)  fixed the date on the previous update
+ (minor)  removed some commented-out code in the listener
+ (medium) removed the escape text function, since it wasn't used
+ (major)  added micro journaling functionality, based on everything I send to the bot
+ (minor)  added change impact to items (minor, medium, major, breaking)

## 2023-01-01.2
Removed annoying print printing responses

## 2023-01-01.1
Forgot the most important one! Moved to Python telegram bot 20.0b, so you need to update!

## 2023-01-01
Happy new year!
+ Fixed my changing the status property from a select to a status, breaking the daily.
+ Added ``/goal`` command to retrieve and set the goal of today
+ added ``/grateful`` command to set what I'm grateful for today

## 2022-12-09
+ Moved my goals to "Goals", so I needed to switch database. Added the config to the config file as well.

## 2022-08-24.1
+ Added error handling when telegram returns a network error, also logs the telegram message

## 2022-08-24
+ Fix bug where daily message was not sent when journal was not available because of config issues

## 2022-08-09 Listener overhaul and cleanup
+ Forgot to save the config.default, so it still has notion defaults in it which were moved to config_notion. Removed them.
+ Minor sonarqube fixes in config.py
+ Switched the task split from // to \n (newline)
+ Fixed bug which resulted in a crash when calling daily with a config file
+ Did quite a major overhaul of the listener, shortening it with about 20 lines. Instead of separate functions, a command executer is called which handles the commands. This saves a lot of if-statements checking for the user, but also allows for single line methods to be in the switch and the notion object is only created when needed. This had some effect in the log as well, where two new methods have been created removing them from the listener.
+ Log now also uses local config variable instead of global
+ Shortened the grocery list method and reordered it a bit
+ made global variable in notion journal interface more local

## 2022-08-07 The config separator
+ Instead of using globals (very unsafe!) I  now use class variables to keep things a bit safer. For log, config and other classes which are needed amongst subs
+ split the config in two files, a config, with telegram and general settings, and config_notion, with the notion specific settings. Now, telegram doesn't have (direct) access to the notion API key and vice versa.

## 2022-08-06 notion_journal_interface
+ Created notion_journal to support future additional features to fill the journal from telegram

## 2022-08-05 weeknumber command and task contents
+ Added ``/week`` command to get the current week number
+ use // when creating a task to add content (text only) (NOTE: Adding (a lot of) content might take a bit longer, since they require separata API calls to notion)
+ Fixed a bug with global commands
+ Allow for tasks without a status
+ shortened the notion interface

## 2022-07-31 Commander's Intent
+ Renamed the goal, so need to rename it in this app as well
+ Added some future ideas to the Readme

## 2022-07-26 Sonarqube safe (naming conventions...)
+ removed addToInbox.py, it did not have any added value anymore
+ Installed sonarqube and removed all errors and warnings. Naming conventions are a bit diffrent from Java which I was used to.

## 2022-07-25 Config and logging updates
+ Added separate config class to ease up the config handling
+ Added separate log class for the same reason, if you are upgrading to this version, make sure to add a new config section [general] with the item LOGFILE_NAME, see config.default .
+ Added a script to cronjob to tell me how big the logfile is, it is also possible to send the ``/log`` command now
+ small change in daily uses string replacement instead of concatenation to prevent (accidental) text issues
+ small change in daily script to URL encode the result

## 2022-07-01.3 Duplicate code removal
+ Removed A LOT of duplicate code, by making daily.py use the notion interface instead of its own code.
+ removed a call to a notion config in the listener, by making a separate notion interface sub for it

## 2022-07-01.2 Fix repeating goal message
+ The goal message was added to every task, found out in production. Fortunately, it was a quick fix.

## 2022-07-01.1 Added daily goal to daily message
+ If a goal is defined, it will be added to the daily message.

## 2022-07-01 Oopsie
+ Main wasn't supposed to go to v20 yet, because then it can't be updated on production anymore, so reverting changes.

## 2022-06-30.1
+ Created branch for python-telegram-bot version 20.0a2 which is still in alfa, but should be released soon

## 2022-06-30 Status check
+ Added a check to see if status is empty and work around that

## 2022-06-28 Let's go public!
+ Moved to public repository
+ added default config.default. Enter details en rename to config to use this

## 2022-06-26.3
+ added ``/daily`` command to show daily info

## 2022-06-26.2
+ Moved the add grocery functionality to notion class
+ removed abundand printline
+ Moved the request grocery list to notion class as well
+ shortened the special chars array

## 2022-06-26.1
+ Moved the creation of a task to its separate notion interface object, pycache was created so I added it to gitignore

## 2022-06-26
+ To enable for public: removed chat ID from the code
+ added the ability to add groceries using the ``/b`` command, it now shows groceries when empty, but adds a grocery when not empty
+ Added link to grocery list from config
+ Instead of creating the URL myself, just grab the URL from the task response (DUH!)
+ Tried to refactor as much as possible to get it below 100 lines, but ended up creating another todo

## 2022-06-20 listener updates
+ Removed some notion direct links from the listener
+ Remove some test based printlines
+ Added ``/b`` command, which shows the grocery list

## 2022-06-19 Added the listener
+ Added a listener.py which starts a listener on ``/tk`` commands and creates a task in the inbox.

## 2022-06-18 Dynamic config file
+ To support crontab automation, a cmd option is enabled to support for a dynamic config file

## 2022-06-16 Telegram
+ Moving to telegram turend out to be WAY easier than expected, so here it is.

## 2022-06-15.1 Daily.py
+ first version of daily.py which gives a summary of today's tasks (just the titles) from notion's tasks database

## 2022-06-15 Move to notion
+ Moved the jira queries and linux commands to notion
+ this setup is mainly intended for stuff that's actually executable.

## 2022-06-14 Tiniest update
+ Removed a line from the AddToInbox python script, added a todo to the readme

## 2022-06-10 Counting lines
+ Added counting lines command combo to linux commands

## 2022-06-09 Jira Queries
+ Updated linux commands with the correct script
+ Removed json dependency from addtoinbox.py
+ Removed how to install a new computer from the readme and moved it to Notion where it fits better.
+ New file with interesting Jira JQL queries to remember

## 2022-06-08 new addtoinbox script 
+ Minor changes to readme (consistency, clarity)
+ Added a .gitignore for OS specific files and .config containing secrets
+ Added a addToInbox.py script, which adds the cmd text to the inbox database in notion

## 2022-06-08 First version
+ Added the first version of a more complete readme
+ Expanded the commands to contain an easier wordcount command

