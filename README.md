Gateway Load Tester
===

Load tester is a python script utilizing curl to randomly creat many user-defined http requests to SeaCat Gateways/Concentrators.

# Running the script

Run:

```
python seacat_load_tester.py 1000
```

The script will run at most 1000 concurrent curl processes that make http calls to addresses defined in configuration.

The argument is *optional* and defaults to *20*.

You can kill the process by hitting ```Ctrl-C```

# Configuration

The script is configured by a configuration dictionary which is **inside the script** after import statements. The dictionary is named **TEST_CONFIG**. Modify it at will.

**Example**:

```
TEST_CONFIG = {
	'concentrators': [
		{'ip':"192.168.0.20", 'port_from': 8000, 'port_to': 25499},
		{'ip':"192.168.0.13", 'port_from': 8000, 'port_to': 25499},
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
```

The script then chooses a **random concentrator** and a **random port** from the specified range.

Then the script chooses a **random endpoint** which is defined by

0. **host**: value of header 'X-SC-HOST'
1. **random path**: the URI part
2. **payload**: path to the binary payload file. If not specified, a GET request is sent, otherwise *-X POST* and *-H "Content-Type: x-application/hessian""* options are set to curl

Here is an example of what commands will be executed from the script:

- curl -H 'X-SC-HOST: apl1' http://192.168.0.13:22999/test/service2/example
- curl -H 'X-SC-HOST: apl' http://192.168.0.20:8999/test/service2
- ...

# Output
0. Amount of running curl threads (45)
1. curls started this second (+10)
2. curls exited this second (-8)

**Script is launching new curl processes:**

```
[0 +10 -0]
[10 +10 -0]
[20 +10 -0]
...
```

**Script is waiting for all curls to get response** (too large response time, server side troubles):

```
[1000 +0 -0]
[1000 +0 -0]
[1000 +0 -0]
...
```

**A curl responded with an error code**:

```
[Error] 7
```

where 7 is curl return code. See [libcurl error codes](https://curl.haxx.se/libcurl/c/libcurl-errors.html)

