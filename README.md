Gateway Load Tester
===

Load tester is a python script utilizing curl to randomly creat many user-defined http requests to SeaCat Gateways/Concentrators.

# Running the script

Run:

```
python seacat_load_tester.py 20
```

The script will run at most 20 concurrent curl http calls to addresses defined in configuration.

The argument is optional and defaults to 20.

You can kill the process by hitting ```Ctrl-C```

# Output

Output of the script will look similar to this:

```
[0 +10 -0]
[10 +10 -0]
[20 +10 -0]
[30 +10 -0]
[40 +10 -5]
[45 +10 -8]
[47 +10 -8]
...
```

What you see is:

0. Amount of running curl threads (45)
1. Threads started this second (+10)
2. Threads exited this second (-8)

# Configuration

After import statements in the scipt file there is a dictionary **TEST_CONFIG**. Modify it at will.

**Example**:

```
TEST_CONFIG = {
	'concentrators': [
		{'ip':"192.168.0.20", 'port_from': 8000, 'port_to': 25499},
		{'ip':"192.168.0.13", 'port_from': 8000, 'port_to': 25499},
	],
	'endpoints': [
		{'host': 'apl', 'paths': ['/test/service1', '/test/service1/example']},
		{'host': 'apl1', 'paths': ['/test/service2', '/test/service2/example']},
	],
}
```

Here is an example of what commands will be executed from the script:

- curl -H 'X-SC-HOST: apl1' http://192.168.0.13:22999/test/service2/example
- curl -H 'X-SC-HOST: apl' http://192.168.0.20:8999/test/service2
- ...