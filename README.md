
This system have Python-MySQL module and Php-MySQL module. The python module downloads 
the changes made by the specified users ( i.e. buildings mapped by users in osm) and populates the MySQL database.
The Php module generates reports based on the data in the MySQL database.

----------------------------------------------------------------------

Python - MySQL Module: 

Python program that regers to the OSM changeset XML data for each user 
and count the number of nodes and building ( i.e. way) created , modified and deleted by the user. 
This program downloads the new changes made by the user and stores the data in MySQL database.

The program is scheduled to run at 6:00 a.m. ( local time) every day.

Contents:

mysqlConnection.py : mysql user credentials
osmUserList.py : osm user list  and targetCountryToMatch ( if we need to filter changes only for specific country )
OSMChangesetAnalysis.py : Main Program
osm_contributions.sql : mysql schema for database `osm_contributions`

Run the Program:
 python OSMChangesetAnalysis.py 

Run in background: 
 nohup OSMChangesetAnalysis.py &
 
Results:
	Stored in the mysql database table
	
----------------------------------------------------------------------
Php -MySQL Module:

This component should be uploaded in the web server (e.g. /var/www/html)
The database populated by the Python component is accessed by this component to generate exvel reports

Contents:

mysqlConnect.php : mysql user credentials 
index.html  : basic html file with links to getDailyReport.php, getMonthlyReport.php and getOverallReport.php

-----------------------------------------------------------------------
OSM changeset Concept:

We are counting the number of nodes/building created by users.

1 . First get the changeset file of the user. This file contains the XML data with 100 changeset IDs by specified user.

	http://api.openstreetmap.org/api/0.6/changesets?display_name=bidurdevkota
	
	This returns the most recent 100 changesets. If the 100th changeset  has  created_at="2017-02-02T09:11:31Z", 
	then the next 100 older changesets can be queried by:
	
	http://api.openstreetmap.org/api/0.6/changesets?display_name=bidurdevkota&time=2001-01-01,2017-03-03T09:11:31Z

2 . Next, get the changeset IDs from the xml file in step 1. For each changeset ID, another xml file can be obtained 
    contains the data of node / way created/modified/deleted by the user). The URL to download this file is in the form
    http://api.openstreetmap.org/api/0.6/changeset/#ChangesetID/download
    E.g. http://api.openstreetmap.org/api/0.6/changeset/46713776/download



