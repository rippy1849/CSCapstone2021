import obspython as obs
import os, select
from enum import Enum

ENCODING = "utf-8"
SUBNAME = "subtitles"
PIPENAME = "inpipe"

#########################
# CREATE THE NAMED PIPE #
#########################

# get the path to the file
cwd = os.getcwd()
fname = cwd + "/Code/obs_scripts/" + PIPENAME

print("cwd is " + cwd)
print("Initializing "+PIPENAME+"...")

# check if pipe already exists by trying to delete it
try:
	os.remove(fname)
	print("Deleted existing file...")
except FileNotFoundError:
	pass

# create the pipe
os.mkfifo(fname)

# open it using the linux syscall
# open with RDWR, RDONLY causes issues
fd = os.open(fname, os.O_RDWR | os.O_NONBLOCK)

print( PIPENAME+" active!" )


########################
# INIT POLLING OBJECTS #
########################
pollobj = select.poll()
pollobj.register(fd, select.POLLIN)


##################
# MISC VARIABLES #
##################

class cameras(Enum):
	# camera name -- obs source name #
	CAMERA1 = "cam1" 
	CAMERA2 = "cam2"
	CAMERA3 = "cam3"


############
# COMMANDS #
############

# determine which command to execute based on the given user input
def interp( scene, msg ):
	
	# find the command
	# if the msg contains a transcript
	if msg.startswith("text{"):
		
		# trim the string so that we are only passing the text
		msg = msg[5:-1]
		
		# call the subtitle command
		subtitle( scene, msg )
		
	# if the msg is starting a splitscreen
	elif msg.startswith("split{"):
		pass
	
	# if the msg is telling us to fullscreen a camera
	elif msg.startswith( "fullscreen{" ):
		
		# trim the string so that we have only the camera name
		msg = msg[11:-1]
		
		# make sure this is reall the name of a camera
		try:
			# call the fullscreen command
			fullscreen( scene, cameras[msg] )
		except KeyError as e:
			print("Unrecognized camera: " + msg)
	
	else:			
		# otherwise, this is an unrecognized command
		print( "Unrecognized command: " + msg )

def subtitle( scene, text ):
	
	# get the subtitle text source
	source = obs.obs_get_source_by_name( SUBNAME )
	
	# get the subtitle's settings
	settings = obs.obs_source_get_settings( source )
	
	# change the text content
	obs.obs_data_set_string(
		settings, "text", text
	)
	
	# update the subtitles object
	obs.obs_source_update( source, settings )
	
	#close the source and settings objects
	obs.obs_data_release( settings )
	obs.obs_source_release( source )

# split the screen between cameras 1 and 2
def splitscreen( scene, c1, c2 ):
	pass

# enlarge a camera feed to fill the screen
def fullscreen( scene, c ):
	
	# otherwise, hide all other cameras...
	source_list = obs.obs_scene_enum_items( scene )
	
	# for each item in the list...
	for item in source_list:
		# get the source
		source = obs.obs_sceneitem_get_source( item )
		
		# get the name of the soure
		name = obs.obs_source_get_name( source )
		
		#make sure that this source is a camera
		try:
			# if this doesn't return an error, source is a camera
			cameras(name)
			
			# get data from the source
			data = obs.obs_source_get_settings( source )
			
			# if the name matches c...
			if ( cameras(name) == c ):
				
				# make it visible
				obs.obs_sceneitem_set_visible( item, True )
				
			
			# otherwise...
			else:
				#make it invisible
				obs.obs_sceneitem_set_visible( item, False )
				
				
		except ValueError as e:
			# this is not a camera, so we do nothing
			pass
	
	# free up memory
	obs.sceneitem_list_release( source_list )


#################
# OBS FUNCTIONS #
#################

# Description displayed in the Scripts dialog window
def script_description():
	return """POST PROCESSING
		Manipulates the live stream, controlled by command input via inpipe."""

# called when the script is being unloaded
def script_unload():
	# close the file descriptor
	os.close(fd)


###############
# UPDATE LOOP #
###############

# the update loop is called every frame
def script_tick(seconds):

	# get scene as source
	current_scene = obs.obs_frontend_get_current_scene()
	
	# if successful...
	if current_scene:
	
		# get the scene object
		scene = obs.obs_scene_from_source(current_scene)
		
		# check for new data from inpipe
		retval = pollobj.poll(0);
		
		# we have data to read when len(retval) > 0
		if (len(retval) != 0):
			
			# read the data
			# we're assuming it's in utf-8
			msg = os.read(fd, 100).decode(ENCODING)
			
			# remove whitespace/newlines from msg
			msg = msg.rstrip()
			msg = msg.rstrip("\n")
			
			print( msg )
			interp( scene, msg )
	
		# free up memory
		obs.obs_scene_release(scene)
