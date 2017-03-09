import urllib, urllib2
import xml.etree.ElementTree as ET
import pymysql.cursors
import pymysql
import datetime

import schedule
import time

from mysqlConnection import userName, userPassword, hostServer
from osmUserList import userList


# CONFIG


#userList = ['heromiya' ,'bidurdevkota']


changesetIdCollectionFile = "cfile.xml"
changesetDataFile = "dataFile.xml"


#######################################################################

class OSMChangesetAnalysis:

	def __init__(self, name):
		self.name = name
		
	#######################################################################
		
	def connectDB(self):
		# Connect to the database
		connection = pymysql.connect(host= hostServer,
									 user= userName,
									 password= userPassword,
									 db='osm_contributions',
									 charset='utf8mb4',
									 cursorclass=pymysql.cursors.DictCursor)
		return  connection
		
	#######################################################################
	
	def insertData(self,query):									

		try:
			connection = self.connectDB()
			
			with connection.cursor() as cursor:
				
				cursor.execute(query)
			# Need to commit to save changes by commit()
			connection.commit()
			
		except:
			print "Problem in Query: " + query
							
		finally:
			connection.close()	

	#######################################################################
	
			
	def retriveData(self, user):	
		
		idList = []							

		try:
			connection = self.connectDB()			

			with connection.cursor() as cursor:
				# get record
				query = "SELECT  `changeset_id` FROM `contributions` where `username` = '" + user +"'"
				cursor.execute(query) 
				for row in cursor.fetchall():
					
					idList.append(str(row['changeset_id']))
					
				return (idList)
		except:
			print "Problem in Query: " + query
				#row = cursor.fetchone() # to get a single row of data
				
		finally:
			connection.close()
		
		
	#######################################################################
	# function to download the changeset file ( identified by changesetID ) 
	# and return the total changesets made by the user

	def getChangesetFileAndCount(self,changesetID):
		
		dataDownloadURL = "http://api.openstreetmap.org/api/0.6/changeset/" + changesetID +"/download"
		#changesetDataFile = "dataFile_"+ changesetID
		try:
			urllib.urlretrieve (dataDownloadURL, changesetDataFile)
		except:
			print " Error: cannot download the Changeset Data File  from " + dataDownloadURL 
			exit(1)	
		# parse the xml file
		buildingCount = 0
		tree = ET.parse(changesetDataFile)
		root = tree.getroot() # get the root element
		#way1 = root.findall('way')
		#print len(way1)
		
		'''
		for elem in root.findall('way/tag'):
			if( elem.get('k') == 'building'):
				buildingCount += 1
		'''
		# follows the specific xml schema for creating building as in
		# http://api.openstreetmap.org/api/0.6/changeset/#CHNAGESET_ID/download
		for elem in root.findall('create/way/tag'):
			if( elem.get('k') == 'building'):
				buildingCount += 1
		
		return buildingCount

	#######################################################################
	# function to download the  changeset IDs file ( and then the changeset file for each changesetID)
	# of the user and count the changes made 

	def processChangeSetData(self, user):	
			
			# get the changesetID already processed for the user
			
			oldChnagesetIDList = self.retriveData (user)
			#print "Previous List: " + str(oldChnagesetIDList)
						
			# download xml file with user's changesetIDs
			downloadURL = "http://api.openstreetmap.org/api/0.6/changesets?display_name="+user

			try:
				urllib.urlretrieve (downloadURL, changesetIdCollectionFile)
			except:
				print " Error: cannot download the Changeset File  from " + downloadURL 
				exit(1)					
			
			tree = ET.parse(changesetIdCollectionFile)
			root = tree.getroot()
			print "Processing for : "+ (user),
			print "Total old Entries " + str( len(oldChnagesetIDList))
									
			
			for child in root.iter('changeset'):
				
				attributeList = child.attrib
				changesetID =  attributeList['id']
				createdAt = attributeList['created_at']# eg. 2017-02-06T16:57:23Z data contains 'Z' at last which means Zulu time used by UTC and GMT
				# The Z stands for the Zero timezone
				
				# if the changesetID is NEW, then download the file and update database				
				if ( changesetID not in oldChnagesetIDList):
					
										
					totalChangesByUser = self.getChangesetFileAndCount(changesetID)
					createdDate = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ" )

				
					query = "INSERT INTO `contributions` (`id`, `username`, `created_at`, `created_year`, `created_month`, `created_day`, `changeset_id`, `total_changes`) "
					query +="VALUES (NULL, \'"+ str(user) +"\', \'"+ str(createdAt)+"\', \'"+ str(createdDate.strftime("%Y"))+"\', \'"+ str(createdDate.strftime("%m"))+"\', \'"+ str(createdDate.strftime("%d")) +"\', \'"+ str(changesetID) +"\', \'"+ str(totalChangesByUser) +"\')"
					self.insertData(query)
				
			print '...'
				

#######################################################################		

def job():
	
	print "START:OSM Data Import " + str(datetime.datetime.now())
	
	osm_obj1 = OSMChangesetAnalysis("OSM Changeset Analysis")

	for user in userList:
		
		osm_obj1.processChangeSetData(user)
	
	print "END: OSM Data Import " + str(datetime.datetime.now())
	print "Wait until next import tomorrow" 

	
if __name__ == '__main__':

	print("Task Started...")
	#schedule.every().day.at("23:31").do(job)
	schedule.every().day.at("11:41").do(job) # run at 6:00 am

	while 1:
		schedule.run_pending()
		time.sleep(1)
			


	
	
		
