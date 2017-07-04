# What is post2ws
This application is a websocket client that can be used with HTTP post request.
It uses [Twisted](https://twistedmatrix.com/trac/)
This is useful if you want to expose local websocket using a simple entry point, or control websocket with client that can't connect with websocket.   
This is of course slower than using a persistant connection.

# Applications
## Tasker
While you can control non-ssl websocket with tasker and some javascript, this doesn't works with SSL websocket.
You can use
* Create a task
* Network/Post HTTP
* Data/File

```
url=wss://localhost:42001
password=HorseBatteryStaple (optional) 
message="/on"
```

# Arguments
```
optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  (default:443)
  -l PASSWORD, --password PASSWORD Relay Password
```
