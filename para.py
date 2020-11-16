#NOTE: WRAP ALL THIS INSIDE A FORM TAG IN MODELS VIEW IN DJANGO AND SET stdoutLines TO BE A VAR
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

import paramiko
import sys
import time

#https://www.youtube.com/watch?v=6a8OimVvTEs

results = []

def ssh_conn():
	client = paramiko.SSHClient()
	#Needs to have logged into the pi once from host before
		#Discuss the use of host keys as a security feature
			#Will need to ssh into pi from server when deploying
	client.load_system_host_keys()
	client.connect('192.168.0.45', username='pi', password='raspberry')

	#ssh_stdin, ssh_stdout, shh_stderr = client.exec_command('cd Desktop')
	#ssh_stdin, ssh_stdout, shh_stderr = client.exec_command('ls ./Desktop/weightSensor')
	#ssh_stdin, ssh_stdout, shh_stderr = client.exec_command('python ./Desktop/weightSensor/hx711py/example.py')
	stdin, stdout, stderr = client.exec_command('python	example2.py')
	while not stdout.channel.exit_status_ready():
		if stdout.channel.recv_ready():
			stdoutLines = stdout.readlines()
			print (stdoutLines)
	#Once the loop finishes it prints the results

	for line in stdout:
		#print(line)
		results.append(line.strip('\n'))

ssh_conn()

for i in results:
	print(i.strip())

sys.exit()

