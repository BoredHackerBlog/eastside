import telnetlib #To connect to android emulator
import random #For generating random numbers
from time import sleep #For pausing

print "Welcome to eastside\n"

host = raw_input("Enter emulator IP: ") #Typically be localhost, unless we do emulation with multiple machines
port = raw_input("Enter emulator port: ") #Typically 5554. More emulations = higher number

def cleanup(): #Reads telnet output and gets us to the right position to enter commands
	while (len(emuconn.read_until('\n', 1)) != 0):
		emuconn.read_until('\n', 1)

def gpsfunc(): #To change GPS location
	#Get inputs
	long = raw_input("longitude: ")
	lat = raw_input("latitude: ")
	alt = raw_input("altitude: ")

	#execute command
	cleanup()
	emuconn.write("geo fix " + long + " " + lat + " " + alt + "\n")
	
	#Go back to the main menu
	opfunc()
	
def smsfunc(): #To emulate SMS
	sender = raw_input("senders phone number: ")
	message = raw_input("message: ")
	
	cleanup()
	emuconn.write("sms send " + sender + " " + message + "\n")
	
	opfunc()

def callfunc(): #To emulate phone calls
	caller = raw_input("callers phone number: ")
	
	cleanup()
	emuconn.write("gsm call " + caller + "\n")
	
	opfunc()
	
def randomfunc(): #This randomly does SMS and phone calls
	callstr = "gsm call "
	smsstr = "sms send "
	while True: #Infinit loop
		phonenumber = str(random.randint(100000000,999999999)) #Create random phone number, convert it to string
		if (random.randint(1,10) > 5): #Randomly decide if we want SMS or phone call
			#Phone call
			randstr = callstr + phonenumber + "\n"
			cleanup()
			emuconn.write(randstr) #Make the call
			sleep(random.randint(1,5)) #Wait for 1-5 seconds
			cleanup()
			emuconn.write("gsm accept " + phonenumber + "\n") #Accept the call
			sleep(random.randint(1,5)) #Wait for 1-5 seconds
			cleanup()
			emuconn.write("gsm cancel " + phonenumber + "\n") #Hang up
			
		else:
			#SMS
			randstr = smsstr + phonenumber
			randstr = randstr + " h3ll0\n" #send h3ll0
			cleanup()
			emuconn.write(randstr)
		
		sleep(random.randint(1,30)) #Wait for 1-30 seconds

def opfunc(): #Main menu
	print ("Options")
	print ("1. Change GPS location")
	print ("2. Send an SMS")
	print ("3. Call emulation")
	print ("4. Randomly do SMS and Call emulation (it will keep running)")
	print ("5. Kill emulator")
	print ("6. Quit eastside")
	option = int(raw_input("Option: ")) #Get option
	
	if option==1:
		gpsfunc()
	elif option==2:
		smsfunc()
	elif option==3:
		callfunc()
	elif option==4:
		randomfunc()
	elif option==5:
		cleanup()
		emuconn.write("kill\n")
		quit()
	elif option==6:
		quit()
	else:
		print "That option does not exist. Bye"
		quit()

try:
	emuconn = telnetlib.Telnet(host,port)
	print "Connected to " + host + ":" + port + "\n"
	opfunc()
except:
	print "Couldn't connect"
	quit()
