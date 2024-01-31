from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from requests.exceptions import ConnectionError


APIKEY = "YOUR SYNCTHING API KEY HERE"
PORT = 8080
SYNCTHING_FOLDER_TO_SHARE = "archlinux"


def validate_devid(s):
    if len(s) > 100:
        return False
    for c in s:
        if not c.isalnum() and not c == "-":
            return False
    return True


class RequestHandler(BaseHTTPRequestHandler):
    def parsestring(self, s):
        url = "http://127.0.0.1:8384/rest/svc/deviceid"
        payload = {"id": s}
        headers = {"X-API-Key": APIKEY}
        r = requests.get(url, params=payload, headers=headers)
        try:
            return r.json()["id"]
        except:
            return None

    def add_device(devid):
        device = {"deviceID": devid}
        headers = {"X-API-Key": APIKEY}
        url = "http://127.0.0.1:8384/rest/system/config"
        config = requests.get(url, headers=headers).json()
        for i, folder in enumerate(config[0]["folders"]):
            if folder["id"] == SYNCTHING_FOLDER_TO_SHARE:
                config[0]["folders"][i]["devices"] += device
                break
        r = requests.post(url, headers=headers, data=config)

    def respond(self, code, message):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        self.wfile.write(b"\n")

    def do_GET(self):
        s = self.path
        if s[0] == "/":
            s = s[1:]
        if not validate_devid(s):
            self.respond(400, "Invalid device ID.")
            print("Invalid device ID.")
            return
        print(self.requestline)
        try:
            devid = self.parsestring(s)
            if devid:
                self.add_device(devid)
                self.respond(200, "Device successfully added.")
            else:
                self.respond(400, "Invalid device ID.")
        except:
            self.respond(500, "Something went wrong.")


def main():
    print("Setting up server on port", PORT)
    httpd = HTTPServer(("", PORT), RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
