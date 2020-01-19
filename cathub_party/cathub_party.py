import pickle
import os
import requests
import base64
import urllib.parse
import re
from pwn import *

def is_cathub(context):
    if 'CAT PARTY!!!!!!' in context:
        return 'CAT PARTY!!!!!!'
    else:
        return 'NO'



url = "https://edu-ctf.csie.org:10190/login.php"
req = requests.post(url, cookies={'session':'79604029-30a2-40fa-a6a2-9227588238e0'},data={'user': '000000', 'pass': '000000'}, allow_redirects=False, verify=False)

sid = req.cookies["PHPSESSID"]
flag = req.cookies["FLAG"]

urlParty = "https://edu-ctf.csie.org:10190/party.php"
reqParty = requests.get(urlParty, cookies={'PHPSESSID': sid, 'FLAG': flag}, allow_redirects=False, verify=False)
real_flag =  base64.b64decode(urllib.parse.unquote(flag))
print('FLAG:', flag)

for i in range(96):
    i += 1
    fakeflag = urllib.parse.quote(base64.b64encode(real_flag[-i:]))
    reqParty = requests.get(urlParty, cookies={'PHPSESSID': sid, 'FLAG': fakeflag}, allow_redirects=False, verify=False)
    if  is_cathub(reqParty.text).strip() == 'CAT PARTY!!!!!!':
        print('the block size is ', i)
        break


leak = b''

def oracle(block0, block1, block2, leak):
    padding_num = 1
    first = 1
    while padding_num <= 16:
        for j in range(255):
            if first:
                j += 1
            if padding_num == 1:
                b1 = block1[:-padding_num] + p8(block1[-padding_num] ^ j)
            #elif padding_num == 16:
            #    b1 = p8(block1[0] ^ j) + block1[-padding_num+1:]
            else:
                b1 = block1[:-padding_num] + p8(block1[-padding_num] ^ j) + block1[-padding_num+1:]
            if block0 == '':
                fakeflag = urllib.parse.quote(base64.b64encode(b1 + block2))
            else:
                fakeflag = urllib.parse.quote(base64.b64encode(block0 + b1 + block2))
            reqParty = requests.get(urlParty, cookies={'PHPSESSID': sid, 'FLAG': fakeflag}, allow_redirects=False, verify=False)
            
            if  is_cathub(reqParty.text).strip() == 'CAT PARTY!!!!!!':
                first = 0
                print('PARTY TIME!!! ', 'index:', j)
                leak = p8(padding_num ^ j) + leak
                if padding_num == 1:
                    block1 = block1[:-padding_num] + p8(block1[-padding_num] ^ j)
                elif padding_num == 16:
                    b1 = p8(block1[-padding_num] ^ j) + block1[-padding_num+1:]
                else:
                    block1 = block1[:-padding_num] + p8(block1[-padding_num] ^ j) + block1[-padding_num+1:]

                b1 = block1[-padding_num:]
                block1 = block1[:-padding_num]
                for i, _ in enumerate(range(padding_num)):
                    block1 += (p8(b1[i] ^ (padding_num) ^ (padding_num+1)))
                print('leak: ', leak)
                padding_num += 1
                break
            if j == 254:
                print('ERROR!! in padding number', padding_num)
    return leak

leak = oracle(real_flag[48:64], real_flag[64:80], real_flag[80:], leak)
leak = oracle(real_flag[32:48], real_flag[48:64], real_flag[64:80], leak)
leak = oracle(real_flag[16:32], real_flag[32:48], real_flag[48:64], leak)
leak = oracle(real_flag[:16], real_flag[16:32], real_flag[32:48], leak)
leak = oracle('', real_flag[:16], real_flag[16:32], leak)

