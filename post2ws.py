from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from websocket import create_connection
import ssl
import urlparse
import argparse

VERSION= "v0.3"
port = "443"

parser = argparse.ArgumentParser(description="Relay a websocket message")
parser.add_argument("-p", "--port", default="443",
                    help="443")
parser.add_argument("-l", "--password", required="true",
                    help="Relay Password")
args = vars(parser.parse_args())
print("LibreConnect WebSocket to HTTP Proxy - " + VERSION)
print("By madnerd.org (https://github.com/madnerdorg/post2ws)")

def sendWebSocket(url,password,message):
    """
        Send a message to a websocket
    """
    try:
        ws = create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
    
        if password:
            ws.recv() # @password
            ws.send(password) 
            ws.recv() # @logged
        ws.send(message)
        returnMessage = ws.recv();
        ws.close()
        print(returnMessage)
        return returnMessage
    except Exception as e:
        return e
    

class WebSocketRelay(resource.Resource):
    """
        Relay websocket message from HTTP POST request
    """
    isLeaf = True

    def render_POST(self, request):
        """
            Get Post Request
        """
        if "url" in request.args and \
           "message" in request.args and \
           "relayPassword" in request.args and \
           "password" not in request.args:
            url = request.args["url"][0]
            message = request.args["message"][0]
            relayPassword = request.args["relayPassword"][0]
            if relayPassword == args["password"]:
                # return "ok"
                sendWebSocket(url,False,message)
                return "ok"
            else:
                return "Invalid Password for relay"
        elif "url" in request.args and \
           "message" in request.args and \
           "relayPassword" not in request.args and \
           "password" in request.args:
            url = request.args["url"][0]
            message = request.args["message"][0]
            password = request.args["password"][0]
            relayPassword = password
            if relayPassword == args["password"]:
                return sendWebSocket(url,password,message)
            else:
                return "Invalid Password for relay"
        elif "url" in request.args and \
           "message" in request.args and \
           "relayPassword" in request.args and \
           "password" in request.args:
            url = request.args["url"][0]
            message = request.args["message"][0]
            password = request.args["password"][0]
            relayPassword = request.args["relayPassword"][0]
            if relayPassword == args["password"]:
                return sendWebSocket(url,password,message)
            else:
                return "Invalid Password for relay"
        else:
            return "Invalid request (need url/message/password and or relayPassword)"


endpoints.serverFromString(reactor, b"ssl:"+args["port"]+":privateKey=keys/privkey.pem:certKey=keys/cert.pem").listen(server.Site(WebSocketRelay()))
reactor.run()