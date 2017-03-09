
This system have Python-MySQL module and Php-MySQL module. The python module downloads 
the changes made by the specified users ( i.e. buildings mapped by users in osm) and populates the MySQL database.
The Php module generates reports based on the data in the MySQL database.

----------------------------------------------------------------------

Python - MySQL Module: 

Python program that regers to the OSM changeset XML data for each user 
and count the number of building created  (XML data: create/way/tag = 'building' ) by the user. 
This program downloads the new changes made by the user and stores the data in MySQL database.

The program is scheduled to run at 6:00 a.m. ( local time) every day.

Contents:
mysqlConnection.py : mysql user credentials
osmUserList.py : osm user list
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


