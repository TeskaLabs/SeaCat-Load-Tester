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
		{
			'host': 'apl',
			'paths': ['/FiskalServer/syncservice'],
			'payload' : '/root/hessianreq_isAlive.bin'
		},
		{
			'host': 'apl1',
			'paths': ['/FiskalServer/syncservice'],
			'payload' : '/root/hessianreq_isAlive.bin'
		},
	],
}

DEVNULL = open(os.devnull, 'w')

def create_tester_subprocess():
	# Pick random concentrator
	concentrators = TEST_CONFIG.get('concentrators', [])
	endpoints 			= TEST_CONFIG.get('endpoints', [])
	# Concentrator
	rand_concentrator 	= concentrators[random.randint(0, len(concentrators)-1)]
	ip 					= rand_concentrator.get("ip")
	rand_port 			= str(random.randint(rand_concentrator.get("port_from"), rand_concentrator.get("port_to")))
	# Endpoint
	rand_endpoint 		= endpoints[random.randint(0, len(endpoints)-1)]
	rand_path 			= rand_endpoint.get('paths', [])[random.randint(0, len(rand_endpoint.get("paths", []))-1)]
	payload 			= rand_endpoint.get("payload")
	host 				= rand_endpoint.get("host")

	# Prepare curl
	cmd = "curl -H 'X-SC-HOST: {}'".format(host)
	if payload is not None:
		cmd += " -H 'Content-Type: x-application/hessian' -X POST --data-binary @{}".format(payload)
	cmd += 30 * (" http://{}:{}{}".format(ip, rand_port, rand_path))
	
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
