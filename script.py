import sys
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TOKEN = '' # Add your token here

backupdir = "backup/" # directory you want backed up
backupfile = "KaliPiBackUp.tar.gz" # File name to save backup as
dropboxfile = "/KaliPiBackUp.tar.gz" # Location on dropbox to save

def SendToDB(backupfile, dropboxfile):
	with open(backupfile, 'rb') as f:
		print("Uploading " + backupfile + " to Dropbox as " + dropboxfile + "...")
		try:
			dbx.files_upload(f.read(), dropboxfile, mode=WriteMode('overwrite'))
		except ApiError as err:
			if (err.error.is_path() and err.error.get_path().reason.is_insufficient_space()):
				sys.exit("ERROR: Cannot back up; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()

def MakeArchive(backupdir, backupfile):
	exists = os.path.isfile(backupfile)
	if exists:
		os.remove(backupfile)
	tarstring = "tar -zcvf " + backupfile + " " + backupdir
	os.system(tarstring)
	exists = os.path.isfile(backupfile)
	if exists:
		return True
	else:
		return False





print("Creating a Dropbox object...")
dbx = dropbox.Dropbox(TOKEN)
try:
	dbx.users_get_current_account()
except AuthError:
	sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

print("Archiving Folder " + backupdir)
archiveMade = MakeArchive(backupdir, backupfile)
if (archiveMade):
	SendToDB(backupfile, dropboxfile)
else:
	print("Error with upload")
