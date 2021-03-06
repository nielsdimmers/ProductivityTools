# productivity tools
Tools to help me be more productive

# Change log
(most recent on top)

## 2022-07-25 Config and logging updates
+ Added separate config class to ease up the config handling
+ Added separate log class for the same reason, if you are upgrading to this version, make sure to add a new config section [general] with the item LOGFILE_NAME, see config.default .
+ Added a script to cronjob to tell me how big the logfile is, it is also possible to send the /log command now
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
+ added /daily command to show daily info

## 2022-06-26.2
+ Moved the add grocery functionality to notion class
+ removed abundand printline
+ Moved the request grocery list to notion class as well
+ shortened the special chars array

## 2022-06-26.1
+ Moved the creation of a task to its separate notion interface object, pycache was created so I added it to gitignore

## 2022-06-26
+ To enable for public: removed chat ID from the code
+ added the ability to add groceries using the /b command, it now shows groceries when empty, but adds a grocery when not empty
+ Added link to grocery list from config
+ Instead of creating the URL myself, just grab the URL from the task response (DUH!)
+ Tried to refactor as much as possible to get it below 100 lines, but ended up creating another todo

## 2022-06-20 listener updates
+ Removed some notion direct links from the listener
+ Remove some test based printlines
+ Added /b command, which shows the grocery list

## 2022-06-19 Added the listener
+ Added a listener.py which starts a listener on /tk commands and creates a task in the inbox.

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

# Todo/wishlist

+ Fix the telegram URL, markup does not work.
+ Add tekst (content) to a note
+ Exception handling when either telegram is not working (auto come back alive), or Notion is not working (send error message to user)
+ Change options using telegram
+ Add info from opensource parlement to daily list
+ upgrade to newest version of python bot: ``pip install -U --pre python-telegram-bot`` and still support it
+ notionInterface.py is too long (max length is 100 lines)