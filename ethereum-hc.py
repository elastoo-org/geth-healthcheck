import BaseHTTPServer
import httplib
import json
import os

HC_HOST = os.getenv('HC_HOST', "127.0.0.1")
HC_PORT = os.getenv('HC_PORT', 8082)

RPC_HOST = os.getenv('RPC_HOST', '127.0.0.1')
RPC_PORT = os.getenv('RPC_PORT', 8545)

RPC_TIMEOUT = os.getenv('RPC_TIMEOUT', 2)
FAIL_CODE = os.getenv('RPC_FAIL_CODE', 500)


class CheckHealth:

    def __init__(self, host, port, timeout):
        self.conn = httplib.HTTPConnection(host, port, timeout=timeout)

    def check(self):
        ret = False
        params = '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":42}'
        headers = { "Content-type": "application/json" }
        self.conn.request("POST", "", params, headers)
        response = self.conn.getresponse()
        result = json.loads(response.read())
        if str(result['result']) == 'False':
            ret = True
        self.conn.close()
        return ret


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        ret_code = 200
        hc = CheckHealth(RPC_HOST, RPC_PORT, RPC_TIMEOUT)
        if not hc.check():
            ret_code = FAIL_CODE
        del hc
        s.send_response(ret_code)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write('OK')

httpd = BaseHTTPServer.HTTPServer((HC_HOST, HC_PORT), RequestHandler)
httpd.serve_forever()
