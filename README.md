# Productivity tools

This productivity tools program is connecting two api's together. The notion.so api and the telegram api. So it enables me to send stuff to my notion from my telegram, like adding groceries to the list, getting a daily message, set a goal for myself, adding a task or journalling.

Currently, the tool supports the following Telegram commands:

```
tk - add a task
log - do a log check
daily - get a daily update
week - return the week number
weight - set your weight
goal - set your goal (or leave empty to get it)
tomgoal - get or set tomorrow's goal
onepercent - set the one percent improvement for today
legal - get copyright information
fun - get or set the fun action for today
tomfun - get or set the fun action for tomorrow
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
ExecStart=python3 <Location of the script file here> listener
Type=simple
User=pi
Group=pi
WorkingDirectory= <folder of the script file here>
```

Start the deamon: ``systemctl start <name of the service file>``

Configure to start at boot: ``systemctl enable <name of the service file>``

# How to send an e-mail
First, make sure the script mailcheck is ran at regular intervals, and create a `config_mail` with the required configuration. See `config_mail.default` for an example.

Send an e-mail to the given e-mail address with the in config_mail specified indicators, and the text between the indicators will be added as an journal entry.

# Change log
Changelog title formatting is (since 2023-02-10.1 (50)): `YYYY-MM-DD.A (B) C` where A is a counter for the number of changelogs of that day (omitted if it's the first one) and B is the number of changelog entries in total. C is optional and usually the commit message, so a very short summary of what I did. The most recent changelog is on top.

Impact of change can be any of:

+ `minor` Dotting I's and crossing T's, refactoring and other changes without functional impact. Updates on documentation
+ `medium` There is functional impact, stuff changes, but nothing like a new command.
+ `major` Adding functionality or interfaces, adding an entire class (even when it's just refactoring)
+ `bug` Fixing a bug (introduced with 2023-02-12 (53))

To count the lines of code, use `find . -type f -name "*.py" -exec wc -l {} +`

## 2024-XX-XX (88) removed habitify, bugfixes and minor improvements
+ (minor) The count in the previous release was a little off, fixed that
+ (minor) Made `get_journal_property` in `notion_journal_interface` more efficient by making it use get_page instead of calling the script by itself
+ (bug) When executed from a different folder than the script's root, the daily script would crash because it couldn't find the journal_prompts.txt. Had to import two modules, but fixed it!
+ (minor) Clarified that the min retrieve time should be in seconds in the notion.default settings
+ (bug) forced `get_daily_data` to use today's date, since some of the information it showed was from the date the script was executed.
+ (major) Removed habitify.py, since it wasn't in use.

## 2024-01-10.2 (87) Fix AI bot count in wrong journal
+ (bug) In the daily message, I report on yesterday's AI usage, but put the value in today's journal. Fixed that.
+ (minor) Removed an unneeded dependency from the script (still quite a lot of dependencies there...)
+ (minor) Removed some unneeded comments from the json builder.
+ (minor) Added the command to count the number of lines of code to the README


| Property | Value |
| :--- | :--- |
| Lines of python code | 796 |

## 2024-01-10.1 (86) Count AI uses
+ (major) Added a new interface with a new database which contains AI uses. The number for today is counted and put into the journal field, so I can keep track. This needs a new config variable with the databse ID of the AI uses count.

## 2024-01-10 (85) Add journal prompt
+ (major) Added a journal prompt (question), shown in the daily update and filled in in the journal of today. You can add your own prompts to journal_prompts, remove as you like.

## 2024-01-07 (84) JSON to class 
+ (minor) Removed an old add grocery function from notion
+ (minor) Removed a test function from the notion journal interface
+ (minor) Cleaned up the `get_journal_property` function in the journal interface
+ (major) Added `notion_json_builder` and moved most of the json texts (except those in global_vars) to that file as classes for readability

## 2023-12-31.2 (83) Save the readme
+ (bug) Forgot to save the readme, showing weird text instead of the update below

## 2023-12-31.1 (82) Text interface and bugfixes
+ (bug) Removed the test journal for sure (See #80)
+ (minor) Rearranged the imports in the script
+ (major) Added a text interface, with additional functionality for giving the interface on the commandline, doing a little overhaul of the commandline argument functionality
+ (medium) Fixed the telegram interface so it doesn't use Request anymore, which is kinda an ugly way to talk to Telegram
+ (minor) The listener script gets an interface from the generic script, and doesn't create it itself, which allows for more flexibility

## 2023-12-31 (81) Separate telegram interface
I put the telegram interface functionality in a separate class. This gives more flexibility on the view part (which is now truly separate from the controller). I got the idea when making the report required me to implement telegram code I've implemented a few times before, indicating that this telegram code is not truly separate.
+ (major) Created "telegram_interface" which is exactly that, an interface for telegram.
+ (medium) Buffed up the weight graph in the daily report a little, so it now shows values and some other niceties. Colors are better.
+ (medium) The report module doesn't use a file anymore, so the tmp folder has become obsolete
+ (bug) removed the test command from the usage script, which has been removed

## 2023-12-30 (80) bugfixes and removal of test journal
+ (minor) forgot to add to previous commit it requires matplotlib from now on.
+ (bug) Added a check for existence of image before sending to prevent erroring out
+ (minor) removed the test journal script because it's gotten out of use
+ (bug) removed the import of the test journal which prevents the script from running

## 2023-12-28 (79) Weight Graph
In order to be able to keep using the daily command or daily update, you need a new config item in the generic config. Create a new section `report` and add a config item `REPORT_LOOKBACK_LENGTH`. The script now also needs a temporary folder called `tmp`, and matplotlib needs to be installed.
+ (major) Added a graph with weight history to the daily graph

## 2023-12-21 (78) Tomorrow's fun updated goal
+ (bug) Fixed a bug where command `tomfun` updates the goal instead of the fun in Notion

## 2023-12-14 (77) Fun and removed domain
+ (major) Removed the commands `domain` and `domainoverview` because they didn't really work and didn't turn out to add value
+ (major) Added commands `fun` and `tomfun` to describe the fun thing I want to do for this day (and this one is actually the one for today!)

## 2023-10-20.1 (76) New command: Domain overview!
+ (major) moved the functionality of command `domain` to the new command `domainoverview`
+ (major) the now `domain` command requires a domain name and shows the clients which connected to that domain

## 2023-10-20 (75) New command: Domain!
+ (major) added a new command, `domain` gives you the pihole most accessed domains form the last 24 hours (give a number to adjust the hours)
+ (bug) removed a forgotten printline command
Want to use the new `domain` command? fill in the default domaincheck config file and remove the .defailt!

## 2023-10-19 (74) Updating commands for the new year
+ (major) Removed commands `grateful`, `frog` and `tomfrog` because they've been gotten out of use. Note that this also removes some config values from the config, check the config_notion.default to see which ones they are.
+ (major) Removed the focus goal, because that habitify task has become obsolete
+ (major) Changed some global vars to fit with the new variable descriptions. This is a major change, because this might break implementations elsewhere.
+ (medium) The words reply message now also shows the words target

## 2023-08-22 (73) Added personal focus goal in daily message, removed task list
+ (minor) Updated readme with the new commandslist (see previous commit for new commands)
+ (medium) Daily does not give a list of tasks anymore
+ (major) Added habitify interface and a message saying something about my personal focus goal.

## 2023-08-09 (72) New commands: onepercent, frog, tomfrog. Remove groceries command
+ (minor)  Updated the notion_config.default with a required variable for the words command
+ (major)  Rmoved the /b command and all code related to it, since grocery list is kept elsewhere
+ (major)  Added command `onepercent` to set the one percent improvement
+ (major)  Added command `frog` to check (and set) today's frog you're going to eat
+ (major)  Added command `tomfrog` for tomorrow's frog
+ (minor)  Clarified hidden commands in the script
+ (medium) Updated the words command a bit, to show percentage towards goal

## 2023-06-26 (71) Add `words` command
 + (major) Added a new script command and a listener command, 'words', which gives the length of the journal of that day.

## 2023-06-22 (70) Add date to response message
+ (medium) When retrieving or setting a property, the date of the journal is set on or retrieved from is given to make an additional check.

## 2023-06-20 (69) telegram micro Journal wrong date fix
+ (bug) So (68) was fine for fields (like weight) but not for journal entries, where the journal was created on a different place. This resulted in different behaviour between telegram journal entries, and pretty much everything else. This should fix that now.

## 2023-06-09 (68) Force fix date bug
Yesterday's fix wasn't working, so reverted it. Now I've forced the date onto the journal to make sure it updates the correct date.
+ (bug) And another attempt at this pesky bug!

## 2023-06-08 (67) Attempt to solve date bug
Ok, so the bug is still here and I think how it works. It looks like it opens the notion record at boot (or at least, very early) and then keeps it open. So the next day, it doesn't recognise a day has passed and just updates the same record. The changes in this release should solve that, but I'm honestly not sure, because I can only test it when a day has passed.
+ (bug) Another attempt at the wrong journal bug.

## 2023-06-05 (66) improve log and weirdly fixing journal wrong date
+ (bug) improved error logging by logging all errors, and clarifying which errors are created by the program (easier grep-ing)
+ (bug) the production version of notion currently posts some details to the wrong journal (the one from yesterday), but this seems to be fixed in this version (how? I don't know!)

## 2023-02-22.1 (65) mailcheck fix
+ (bug)   Mailcheck wouldn't work because the global vars were not accessible.
+ (minor) Another attempt at the line count table thing

## 2023-02-22 (64) script variable bugfix
+ (bug)   `script.py` would not execute because variable was referenced before creation.

| Property | Value |
| :--- | :--- |
| Lines of python code | 479 |

## 2023-02-20 (63) Performance improvement
+ (minor)  Moved the license back to the root directory, since it wasn't recognised by Github.
+ (minor)  Upgraded the notion version of the notion interface to 2022-06-28, no additional changes were required
+ (minor)  Prevented the test from loading (creating) a journal even though it would never be evoked.
+ (minor)  Shortened notion journal interface a bit.

In attempting to shorten the notion journal, I printed the date of the journal, and found that when the listener was started, the test page (dated according to the test date in the config) was created and opened. This happens because the script loads the test, and the test loads the class, which loads the journal entry by default. I worked around this to create an `__init__`, but it also meant that in the journal entry, the config was loaded which I wanted to prevent (to keep it open for longer than strictly necessary). So I moved that declaration to the init def as well.

This led to me wondering whether it is strictly necessary to declare variables in the class, if they are used (and declared) elsewhere. The answer is no, so I removed a few of those as well. Just make sure you declare them in init and you should be fine.

Performance is now significantly better. It feels more secure as well, although that is marginal.

| Property | Value |
| :--- | :--- |
| Lines of python code | 479 |

## 2023-02-19 (62) Big script overhaul, cleanup & documentation
+ (major)  Shortened the listener, it should now be started from script.py
+ (major)  Modified the mailcheck so that it can be run from the script now.
+ (medium) Moved the Nconfig folder to config (you know the N stands for Niels, right?)
+ (major)  Added command `legal` to show legal information, can be kicked off from both command line as well as from the bot.
+ (minor)  Added documentation related to a code of conduct, contributing and security
+ (minor)  Moved many of the notion field names to global vars, so they are easier to change
+ (minor)  Deleted `update.py` script, since I'm to scared to do it that way and usually do this manually.
+ (minor)  Updates to previous release notes to correct some typo's and spelling errors
+ (minor)  Minor updates to reduce the number of lines of code and clean up a bit.

Someone forked my code, so I got scared and added a bunch of legal stuff ;-).

If you look at it, it is quite amazing with how much I'm able to achieve with not even 500 lines of python code and some config files (and 300 lines of documentation, but OK). I did some creative actions to really condense the code, and I think there are a few more possible, but this a lot, I'm quite proud of the result I achieved.

## 2023-02-18.3 (61) GO TO BED, NOW!
+ (minor) You should have saved README.md before you committed... XD

## 2023-02-18.2 (60) test_journal to script
+ (minor) Turned `test_journal.py` script into a class which can now be called from `script.py`
+ (major) Forgot to add files to previous commit, so they're in this one now, which is lucky, because I had to fix the title of the previous one wich was a mess. Guess I'm tired XD.

## 2023-02-18.1 (59) new script.py and mailcheck cleanup
+ (major)  Introduced `script.py` to replace `logCleanupReminder.py` and `daily.py` reducing the number of files
+ (bug)    weird stuff would happen if you send a microjournal e-mail with windows whitespaces in them.
+ (medium) In an attempt to shorten the mailcheck, I greatly improved performance and shortened it. It now uses an IMAP query to select the e-mails, instead of filtering for them in code which means retrieving every mail in your inbox. Requires a change in `config_mail`. Look for `allowed_senders_query` in `config_mail.default`

## 2023-02-18 (58) Fix config file bug
+ (bug) In some situations, it was difficult to locate the config file, simplified that now. Config should always be in the Nconfig folder, it is not possible anymore to give in a separate config in the command line. The application assumes Unix based system, but if you want to adapt it to Windows, you should check `confg.py`.

## 2023-02-17 (57) add links to daily
+ (minor) Added tomorrow's goal command to the documentation above
+ (major) Added links to the daily message to tasks and today's journal
+ (minor) Added a test for the `get_url` of the journal interface
+ (minor) Refactored the notion interface a bit so it is more in line with the journal interface and consumes a few less lines.

## 2023-02-14.1 (56) Cutting off just a little to little
+ (bug) I copied the old goal command without realising the command got longer and now the last two letters of the command are in the goal. Fixed.

## 2023-02-14 (55) Tomorrow`s goal
+ (bug)   Fixed when sending a certain double quote (") the journal processing crashes
+ (major) added command `tomgoal` to set (and get) tomorrow's goal

## 2023-02-12.1 (54) create config folder, extend usage of global vars
NOTE: This is quite a big breaking change. Run the python script `update.py` after you've pulled this release. __You have been warned.__

+ (major) Moved all the config files to the config directory
+ (minor) Updated the log cleanup reminder to use `global_vars`
+ (minor) Updated log to use `global_vars` as well
+ (minor) Updated the log cleanup reminder to use `log`, getting rid of some duplicate code
+ (minor) Updated the daily message to use `global_vars` as well, shortening it a bit.
+ (minor) Deprecated breaking impact of change. Added impact of change explanation to README.md

## 2023-02-12 (53) Fix empty goal bug & testdate is configurable.
+ (minor) Set the test date to a config date, to prevent my date of birth being visible everywhere. The date can be changed now.
+ (minor) Added "bug" impact possibility because frankly, I'm finding a lot of bugs.
+ (bug)   Fixed that if the goal is empty, it would break (fixes other breaks as well)
+ (minor) Added a test for `count_words` and for adding a microjournal.


## 2023-02-11 (52) Fix newline bug
+ (medium) Fix a bug where a newline in a journal would break the journal causing it to not be added to notion, if it's shorter than threshold. The fix is done by always splitting paragraphs in separate messages.
+ (minor) Changed description at top of README to more clarify what this program actuall is.

## 2023-02-10.2 (51) journal overhaul
+ (minor) Fix bug where global var 	`MIN_RETRIEVE_TIME` wasn't converted to int breaking the journal.
+ (major) Did a big efficiency overhaul of the journal interface. It should be (a little bit) faster and is about 1/5th shorter with more functionality
+ (major) Added functionality to delete a journal, only works for specific date (1987-10-20)
+ (major) Added a test script: `test_journal`
+ (minor) Made the creation of the journal based on the date of the journal, instead of today
+ (major) Journal interface now uses the new API version

## 2023-02-10.1 (50) Cosmetics, globalisation and cleanup
+ (minor) Removed a useless check for '\n' in journal interface long message check
+ (minor) Used global_vars more widely throughout the journal interface (for URLs and such)
+ (minor) Made the max journal entry length and minimum page retrieve time a configurable variable
+ (minor) Translated some Dutch inline comments to English
+ (minor) Added a changelog number counter between brackets to the title of the changelog entry. So changelog numbering is now `YYYY-MM-DD.A (B)` where A is a counter for the number of changelogs of that day (omitted if it's the first one) and B is the number of changelog entries in total.

Hooray! Number 50! Never thought I'd get this far.

## 2023-02-10
+ (major) Moved the limit check to `notion_journal_interface` so that sending telegram messages longer than 2000 characters is handled OK, without duplicating code, because it's removed from mailcheck now.

## 2023-02-07.1
+ (minor) Remove two debug printlines

## 2023-02-07
+ (minor) The journal functionality crashes because it's trying to decode iso-8859-1 as utf-8 when none is given. This crashes with special characters (like é). When Outlook sends an iso-8859-1 mail, the charset is configured to None, so now I have no other choice to accept that when None is given, iso-8859-1 is used.

## 2023-02-04
+ (minor) Fixed a bug where the daily would crash if it encountered a different type than paragraph in the text of yesterday's journal when counting words.

## 2023-02-03
+ (major) Completely overhauled the e-mail to micro journal functionality.
+ (minor) The submit journal entry in the notion class now allows setting a variable to leave the timestamp of the entry out. This is to support long e-mail entries and allow for different e-mail programs to be able to send mail.

The e-mail functionality is still experimental at best. It won't break the system or my journal entry, but that's all the guarantee you get. You might lose some journal entries because they are archived without processing them in notion. You might also get weird error messages. The insecurity sits in the many ways e-mails can be formatted and configured. It is also difficult to get a clear way to get the different parts of an e-mail (like headers and the body) without doing stuff I pretty much copied from the internet. Also, the code can use some maintenance and variable names are sketchy in places.

## 2023-01-30.2
+ (minor) renaming the config to `mail_config` to work around the problem of logging wich probably catches the wrong config. Removed the dependancy from log to make sure it's fixed.

## 2023-01-30.1
+ (minor) Fixed indentation bug

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

