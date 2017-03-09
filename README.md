
Python - MySQL Component: 
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
