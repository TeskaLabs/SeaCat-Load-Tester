#!/usr/bin/python
import sys, subprocess, time, os
import random
from subprocess import Popen, PIPE, STDOUT


TEST_CONFIG = {
	'concentrators': [
		{'ip':"90.183.120.10", 'port_from': 8000, 'port_to': 25499},
		{'ip':"90.183.120.11", 'port_from': 8000, 'port_to': 25499},
	],
	'endpoints': [
		{'host': 'apl', 'paths': ['/FiskalServer/fileservice', '/FiskalServer/fileupload']},
		{'host': 'apl1', 'paths': ['/FiskalServer/fileservice', '/FiskalServer/fileupload']},
	],
}

DEVNULL = open(os.devnull, 'w')

def create_tester_subprocess():
	# Pick random concentrator
	concentrators = TEST_CONFIG.get('concentrators', [])
	c = concentrators[random.randint(0, len(concentrators)-1)]
	# Random endpoint
	endpoints = TEST_CONFIG.get('endpoints', [])
	e = endpoints[random.randint(0, len(endpoints)-1)]
	# Random path
	p = e.get("paths", [])[random.randint(0, len(e.get("paths", []))-1)]

	host 	= e.get("host")
	ip 		= c.get("ip")
	port 	= str(random.randint(c.get("port_from"), c.get("port_to")))
	path 	= p

	# Prepare curl
	cmd = "curl -H 'X-SC-HOST: {}' ".format(host)
	cmd += 30 * (" http://{}:{}{}".format(ip, port, path))
	
	# Return subprocess obj
	return subprocess.Popen(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)


RUNNING = True


def main(argv):
	thread_count = 20 if len(argv) == 0 else int(argv[0])
	tester_subprocesses = []

	while RUNNING:
		stat_running = len(tester_subprocesses)
		stat_started = 0
		stat_exited = 0

		x = thread_count - stat_running
		if (x > 60): x = 60
		if (x > 0):
			for i in range(x):
				tester_subprocesses.append(create_tester_subprocess())
				stat_started += 1

		for p in tester_subprocesses:
			returncode = p.poll()
			if returncode is not None:
				tester_subprocesses.remove(p)
				stat_exited += 1
				if returncode != 0:
					print "[Error] {}".format(returncode)

		time.sleep(1)
		print("[{} +{} -{}]".format(stat_running, stat_started, stat_exited))



if __name__ == "__main__":
	main(sys.argv[1:])
