import urllib, urllib2
import xml.etree.ElementTree as ET
import pymysql.cursors
import pymysql
import datetime

import schedule
import time


from geopy.geocoders import Nominatim



from mysqlConnection import userName, userPassword, hostServer
from osmUserList import userList , targetCountryToMatch


# CONFIG

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
	# logs error messages and system data update process start/end time
	def logMessage( self, message ):
		target = open("log.txt", 'a')   
		target.write(str(datetime.datetime.now()) + "\n" + message + "\n" ) 
		target.close()
		
	#######################################################################
	
	def insertData(self,query):									

		try:
			connection = self.connectDB()
			
			with connection.cursor() as cursor:
				
				cursor.execute(query)
			# Need to commit to save changes by commit()
			connection.commit()
			
		except:
			message = "Problem in Query: " + query
			self.logMessage( message )
			print message
			
							
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
			message = "Problem in Query: " + query
			self.logMessage( message )
			print message
				
		finally:
			connection.close()
	
	#######################################################################
			
			
	def getCountryName(self, latitude, longitude):
		
		try:
			geolocator = Nominatim()
			location = geolocator.reverse( str(latitude) + "," +str(longitude) , language='en')			
			address = location.address.split(",")			
			country = address[-1].strip().encode('utf-8')  # strip() is used to remove space in front and tail of the text
						
			return country
			
		except:
			
			message = " Error: cannot get country from latitude longitude pair " + str(latitude) + "," +str(longitude) 
			self.logMessage( message )
			print message
			exit(1)	
		
		
		
	#######################################################################
	# function to download the changeset file ( identified by changesetID ) 
	# and return the total changesets made by the user

	def getChangesetFileAndCount(self,changesetID):
		
		dataDownloadURL = "http://api.openstreetmap.org/api/0.6/changeset/" + changesetID +"/download"
		#changesetDataFile = "dataFile_"+ changesetID
		try:
			urllib.urlretrieve (dataDownloadURL, changesetDataFile)
		except:
			message = " Error: cannot download the Changeset Data File  from " + dataDownloadURL 
			self.logMessage( message )
			print message
			exit(1)	
		
		# parse the xml file
		totalBuildingCreated = 0
		totalBuildingModified = 0
		totalBuildingDeleted = 0
		totalNodeCreated = 0
		totalNodeModified = 0
		totalNodeDeleted = 0
		
		tree = ET.parse(changesetDataFile)
		root = tree.getroot() # get the root element
		#way1 = root.findall('way')
		#print len(way1)
		
		
		# follows the specific xml schema for creating building as in
		# http://api.openstreetmap.org/api/0.6/changeset/#CHNAGESET_ID/download
		
		for elem in root.findall('create/node'):			
			if ( targetCountryToMatch ): # if targetCountryToMatch is given then check
				lat = elem.get('lat')
				lon = elem.get('lon')
				if (self.getCountryName(lat, lon) == targetCountryToMatch):
					totalNodeCreated += 1	
			else:
				totalNodeCreated += 1	
		
		for elem in root.findall('modify/node'):
			
			if ( targetCountryToMatch ):
				lat = elem.get('lat')
				lon = elem.get('lon')
				if (str(self.getCountryName(lat, lon)) == str(targetCountryToMatch)):
					totalNodeModified += 1	
					
			else:
				totalNodeModified += 1
			
		for elem in root.findall('delete/node'):
			totalNodeDeleted += 1		
		
		for elem in root.findall('create/way/tag'):
			if( elem.get('k') == 'building'):
				totalBuildingCreated += 1
				
		for elem in root.findall('modify/way/tag'):
			if( elem.get('k') == 'building'):
				totalBuildingModified += 1	
				
		for elem in root.findall('delete/way'):
			totalBuildingDeleted += 1
		
		
		
		
		return [ totalBuildingCreated , totalBuildingModified, totalBuildingDeleted, totalNodeCreated, totalNodeModified, totalNodeDeleted]
 
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
				message = " Error: cannot download the Changeset File  from " + downloadURL 
				self.logMessage( message )
				print message
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
					
					#get list of building created, building modified, node created, node modified , node deleted					
					totalChangeList = self.getChangesetFileAndCount(changesetID)
					createdDate = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ" )
				
					query = ( "INSERT INTO `contributions` (`id`, `username`, `created_at`, `created_year`, `created_month`," 
							"`created_day`, `changeset_id`, `building_created`, `building_modified`, `building_deleted`, "
							 " `node_created`, `node_modified` , `node_deleted`) " 
					 "VALUES (NULL, \'"+ str(user) +"\', \'"+ str(createdAt)+"\', \'"+ str(createdDate.strftime("%Y"))+"\', \'" 
					 + str(createdDate.strftime("%m"))+"\', \'"+ str(createdDate.strftime("%d")) +"\', \'"+ str(changesetID) 
					 +"\', \'"+ str(totalChangeList[0]) +"\', \'"+ str(totalChangeList[1]) +"\', \'"  
					 + str(totalChangeList[2]) +"\', \'"+ str(totalChangeList[3])+"\', \'" + str(totalChangeList[4])+"\', \'"
					 + str(totalChangeList[5]) +"\')" )
					
					#print query
					self.insertData(query)
				
			print '...'
				

#######################################################################		

def job():		
	
	osm_obj1 = OSMChangesetAnalysis("OSM Changeset Analysis")
	
	message = "START:OSM Data Import " + str(datetime.datetime.now())
	osm_obj1.logMessage( message )

	for user in userList:
		
		osm_obj1.processChangeSetData(user)
	
	message = "END: OSM Data Import " + str(datetime.datetime.now())
	message += "\nWait until next import after 6 Hours\n\n" 
	
	osm_obj1.logMessage( message )

	
if __name__ == '__main__':

	print("Task Started from " + str(datetime.datetime.now()))
	
	#schedule.every(1).minutes.do(job)

	schedule.every().day.at("1:00").do(job) # run at 24:00 thai time
	schedule.every().day.at("7:00").do(job)
	schedule.every().day.at("13:00").do(job) 
	schedule.every().day.at("19:00").do(job) 

	while 1:
		schedule.run_pending()
		time.sleep(1)
		#break
	
	print "END"
			


	
	
		
