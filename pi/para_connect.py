#NOTE: WRAP ALL THIS INSIDE A FORM TAG IN MODELS VIEW IN DJANGO AND SET stdoutLines TO BE A VAR
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import paramiko
import sys
import time

f=open("address.txt","r")
lines=f.readlines()
address=lines[0]
f.close()


results = []
#Address is the ip of pi, read from external file while uploading to github
def ssh_conn(address):
	client = paramiko.SSHClient()
	#Needs to have logged into the pi once from host before
			#Will need to ssh into pi from server when deploying
	client.load_system_host_keys()
	client.connect(address, username='pi', password='raspberry')

	stdin, stdout, stderr = client.exec_command('python	example2.py')
	while not stdout.channel.exit_status_ready():
		if stdout.channel.recv_ready():
			stdoutLines = stdout.readlines()
			print (stdoutLines)
	#Once the loop finishes it prints the results

	for line in stdout:
		results.append(line.strip('\n'))

ssh_conn(address)

for i in results:
	print(i.strip())

sys.exit()

