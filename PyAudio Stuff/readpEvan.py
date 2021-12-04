import os
import select
from message import decode_msg_size

def get_message(fifo: int) -> str:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size).decode("utf8")
    return msg_content

import pyaudio
import wave
import audioop
import matplotlib
import math

try:

	 #changing the input device index to give individual streams to each microphone and record each. Then test at intervals to get the triangulation. 
	 
	chunk = 1024      # Each chunk will consist of 1024 samples
	sample_format = pyaudio.paInt16      # 16 bits per sample
	channels = 1     # Number of audio channels
	fs = 44100        # Record at 44100 samples per second
	time_in_seconds = 5
	#filename = "soundsample2.wav"


				
	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	info = p.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')
	print(numdevices)
	for i in range(0, numdevices):
		  if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			   print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')) 
				
	print('-----Now Recording-----')
	input_device_index=0
	#Open a Stream with the values we just defined
	stream = p.open(format=sample_format,input_device_index=2,
					channels = channels,
					rate = fs,
					frames_per_buffer = chunk,
					input = True)
	frames = []  # Initialize array to store frames             
					
	stream2 = p.open(format=sample_format,input_device_index=3,
					channels = channels,
					rate = fs,
					frames_per_buffer = chunk,
					input = True)
	frames2 = []  # Initialize array to store frames              

	stream3 = p.open(format=sample_format,input_device_index=4,
					channels = channels,
					rate = fs,
					frames_per_buffer = chunk,
					input = True)
	frames3 = []  # Initialize array to store frames 
				 
					

	 
	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * time_in_seconds)):
		data = stream.read(chunk,exception_on_overflow = True)
		frames.append(data)
	rms = audioop.rms(data,2)
	decibel = 20 * math.log10(rms)
	print (decibel , "decibel")


	 

	 
	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * time_in_seconds)):
		data2 = stream2.read(chunk,exception_on_overflow = True)
		frames2.append(data2)
	rms2 = audioop.rms(data2,2)
	decibel2 = 20 * math.log10(rms2)
	print (decibel2 , "decibel2")


	 
	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * time_in_seconds)):
		data3 = stream3.read(chunk,exception_on_overflow = True)
		frames3.append(data3)
	rms3 = audioop.rms(data3,2)
	decibel3 = 20 * math.log10(rms3)
	print (decibel3 , "decibel3")

	#cap=audioop.avg(data3,2)
	#print(cap)
	# Stop and close the Stream and PyAudio
	stream.stop_stream()
	stream.close()
	p.terminate()
	#stream2.stop_stream()
	#stream2.close()
	#p.terminate()
	#stream3.stop_stream()
	#stream3.close()
	#p.terminate()
	#print (frames[1])
	direction = 0
	print('-----Finished Recording-----')
	#if (decibel >decibel2) and (decibel2 >decibel3):
	#	direction = 2
	#	elif (decibel3 >decibel2) and (decibel2 >decibel):
	#		direction = 4
	#	elif ((decibel2 >decibel3) and (decibel3 >decibel)) or ((decibel2 >decibel) and (decibel >decibel3)):
	#		direction = 3
	#	elif ((decibel >decibel3) and (decibel3 >decibel2)) or ((decibel3 >decibel) and (decibel >decibel2)):
	#		direction = 1
	#		else direction = 0
	#print(direction)
		
	z1 = decibel - decibel2
	z2 = decibel3 - decibel2
	z3 = decibel - decibel3
	print(z1)
	print(z2)
	print(z3)

	# Open and Set the data of the WAV file
	file = wave.open(filename, 'wb')
	file.setnchannels(channels)
	file.setsampwidth(p.get_sample_size(sample_format))
	file.setframerate(fs)
	 
	#Write and Close the File
	file.writeframes(b''.join(frames))
	file.close()

except Exception as e:
	print( e )
	print( "didn't crash" )


if __name__ == "__main__":
    # Make the named pipe and poll for new messages.
    IPC_FIFO_NAME = "hello_ipc"
    os.mkfifo(IPC_FIFO_NAME)
    try:
        # Open the pipe in non-blocking mode for reading
        fifo = os.open(IPC_FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)
        try:
            # Create a polling object to monitor the pipe for new data
            poll = select.poll()
            poll.register(fifo, select.POLLIN)
            try:
                while True:
                    # Check if there's data to read. Timeout after 2 sec.
                    if (fifo, select.POLLIN) in poll.poll(2000):
		    	# Do something with the message
                        msg = get_message(fifo)
                        print(msg)
                    else:
		    	# No data, do something else
                        print("Nobody here :(")
            finally:
                poll.unregister(fifo)
        finally:
            os.close(fifo)
    finally:
    	# Delete the named pipe when the reader terminates
        os.remove(IPC_FIFO_NAME)
