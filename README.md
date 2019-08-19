TwatBot2
========
Twatbot reborn. Posts things from IRC to twitter and reddit.
Has other features too.

Installation
============
You'll need the following:

* python2
* python-twisted
* python-mysqldb
* python-twitter

* A running mysql instance with a user and password:
```
create user 'mysql_user'@'localhost' identified by 'some_pw';
create table tell(
  `sender` varchar(32) NOT NULL,
  `to` varchar(32) NOT NULL,
  `message` text not null,
  `time` datetime not null);
alter table service_nicks ADD PRIMARY KEY(irc_nick,service);
alter table service_nicks ADD constraint nick_service UNIQUE (irc_nick,service);    
create table service_nicks(
  irc_nick varchar(32) not null,
  service varchar(32) not null,
  service_nick varchar(32) not null);
```

* Files called: 
  * admin (be sure to add your nick here)
  * greets
  * keys
  * ignores

Running
=======
Run from the command line, the server name is the first argument, the channels are space separated #channels

eg: `python Twatbot2.py irc.freenode.net #channel1 #channel2`

Keys
====
If you want all the features, you need to make a keys file and give it key value pairs for the services you want to use:


* consumer_key 
* consumer_secret
* access_token_key 
* access_token_secret 
* nickpass (nickserv password)
* steam_api_key 
* mysql_user 
* mysql_pass 
* mysql_db
* lastfm_api_key
* lastfm_secret 
* reddit_user 
* reddit_pass 

The first 4 are for twitter and you need to make a new twitter app and use the scripts provided with python-twitter to get your keys.

Usage
=====
Usage is typically from IRC and allows you to interact with its functionality with the format `^command`.

Admin functionality allows ignoring, removing tweets, reloading plugin modules.

Extension
=========
To add more plugins, add them to the list in `Twatbot2.py` and also in `__init__.py` in the plugins directory.
To add functions to your plugin, they must take parameters:
* `conn` informations about the connection that allows you to send messages and access information about channels
* `data` data about the current message
