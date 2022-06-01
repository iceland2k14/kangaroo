# -*- coding: utf-8 -*-
"""
Usage :
 > python kangaroo.py -p 0352b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e -keyspace 935da71d7350734c3472fe305fef82ab8aca644fb:935da71d7350734c3472fe305fff82ab8aca644f9
 > python kangaroo.py -p 02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630 -keyspace 800000000000000000000000000000:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF -rand -ncore 7
 > python kangaroo.py -p 0425c2d005f3036c13070afcf139a18ce69355c3158e017cd99ae72d815d74c54fb3c7c0bc9f4089284cc2de737024d50328884282a8b9bbbaf989747198971669 -rand1
 > python kangaroo.py -p 02ca298581993a21f38083092001dfa86a2f4aa06e75867a3fece2b5b96a253e20 -keyspace 1:ffffffffffff -ntu

@author: iceland
@Credit: JLP
"""
import bit
# from coincurve import PublicKey
import ctypes
import platform
import sys
import os
import random
import argparse
import signal


###############################################################################
parser = argparse.ArgumentParser(description='This tool use Kangaroo algo for searching 1 pubkey in the given range using multiple cpu', 
                                 epilog='Enjoy the program! :)    Tips BTC: bc1q39meky2mn5qjq704zz0nnkl0v7kj4uz6r529at')
parser.version = '10052022'
parser.add_argument("-p", "--pubkey", help = "Public Key in hex format (compressed or uncompressed)", required=True)
parser.add_argument("-keyspace", help = "Keyspace Range ( hex ) to search from min:max. default=1:order of curve", action='store')
parser.add_argument("-ncore", help = "Number of CPU to use. default = Total-1", action='store')
parser.add_argument("-n", help = "Total range search in 1 loop. default=72057594037927935", action='store')
parser.add_argument("-rand", help = "Start from a random value in the given range from min:max and search 0XFFFFFFFFFFFFFF values then again take a new random", action="store_true")
parser.add_argument("-rand1", help = "First Start from a random value, then go fully sequential, in the given range from min:max", action="store_true")
parser.add_argument("-ntu", help = "Stop Update of the Tame DP File: HashTable.ice. Default is Always Update.", action="store_true")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

###############################################################################
ss = args.keyspace if args.keyspace else '1:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140'
flag_random = True if args.rand else False
flag_random1 = True if args.rand1 else False
tame_update_file = False if args.ntu else True
ncore = int(args.ncore) if args.ncore else platform.os.cpu_count() - 1
increment = int(args.n) if args.n else 72057594037927935
public_key = args.pubkey    # '02CEB6CBBCDBDF5EF7150682150F4CE2C6F4807B349827DCDBDD1F2EFA885A2630'
if flag_random1: flag_random = True

a, b = ss.split(':')
a = int(a, 16)
if a == 0: a = 1
b = int(b, 16)
lastitem = 0
if increment > b-a: increment = b-a

###############################################################################
if platform.system().lower().startswith('win'):
    dllfile = 'Kangaroo_CPU.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
        sys.exit()
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows] is working')
    sys.exit()
    
ice.run_cpu_kangaroo.argtypes = [ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p] # ntu,st,en,dp,ncpu,mx,pvk,upub
ice.get_reduced_upub.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # stkey, upub, res
ice.init_kangaroo_lib()

###############################################################################
def run_cpu_kangaroo(tame_update_file, start_range_int, end_range_int, dp, ncpu, mx, upub_bytes):
    st_hex = hex(start_range_int)[2:].encode('utf8')
    en_hex = hex(end_range_int)[2:].encode('utf8')
    res = (b'\x00') * 32
    ice.run_cpu_kangaroo(tame_update_file, st_hex, en_hex, dp, ncpu, mx, res, upub_bytes)
    return res

def pub2upub(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:],16)
	return bytes.fromhex('04'+ hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

def randk(a, b):
	if flag_random:
		random.seed(random.randint(1,2**256))
		return random.SystemRandom().randint(a, b)
	else:
		if lastitem == 0:
			return a
		elif lastitem > b:
			print('[+] Range Finished')
			exit()
		else:
			return lastitem + 1

def get_reduced_upub(range_st, upub):
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    res = (b'\x00') * 65
    if range_st < 0: range_st = N + range_st
    k = bytes.fromhex(hex(range_st)[2:].zfill(64))
    ice.get_reduced_upub(k, upub, res)
    return bytes(bytearray(res))

# =============================================================================
# def reduced_key(range_st, upub):
#     modulo = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
#     k1G = bit.Key.from_int(range_st)._pk.public_key.format(compressed=False)
#     nk1G = PublicKey.from_point( int(k1G.hex()[2:66], 16), (-(int(k1G.hex()[66:], 16)))%modulo )
#     PP = PublicKey.from_point(int(upub.hex()[2:66], 16), int(upub.hex()[66:], 16))
#     RR = PublicKey.combine_keys([PP, nk1G])
#     RRx, RRy = RR.point()
#     return bytes.fromhex('04' + hex(RRx)[2:].zfill(64) + hex(RRy)[2:].zfill(64))
# =============================================================================

def fix_pvk(pvk_found, range_st):
    order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    return hex( (int(pvk_found.hex(), 16) + range_st ) % order )

def write_keys(pvk_found, range_st):
    pvk_fix = fix_pvk(pvk_found, range_st)
    print('\n============== KEYFOUND ==============')
    print('Kangaroo FOUND PrivateKey : '+pvk_fix)
    print('======================================')
    with open('KEYFOUNDKEYFOUND.txt','a') as fw:
        fw.write('Kangaroo FOUND PrivateKey : '+pvk_fix+'\n')
            
def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
    exit(0)
###############################################################################
print('[+] Starting CPU Kangaroo.... Please Wait     Version [', parser.version,']')

dp = 10 # -1 for automatic value
mx = 2 # 0 for Endless

upub = pub2upub(public_key)

###############################################################################
if flag_random1 == True:
    print('[+] Search Mode: Random Start then Continuous Range Search from it')
elif flag_random == True:
    print('[+] Search Mode: Random Start after every Range 0XFFFFFFFFFFFFFF key search')
else:
    print('[+] Search Mode: Range search Continuous in the given range')
###############################################################################
range_st = randk(a, b) # start from
range_en = range_st + increment

# Reset the flag after getting 1st Random Start Key
if flag_random1 == True: flag_random = False

print('[+] Working on Pubkey:',upub.hex())
print('[+] Using  [Number of CPU Threads: {}] [DP size: {}] [MaxStep: {}]'.format(ncore, dp, mx))

###############################################################################
print('[+] ............................................', end='\r')
while True:
    # Tell Python to run the handler() function when SIGINT is recieved
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    print(f'{" "*100}\r[+] Scanning Range          {hex(range_st)} : {hex(range_en)}')
#    pvk_found = run_cpu_kangaroo(range_st, range_en, dp, ncore, mx, upub)
#    rpub = reduced_key(range_st, upub)
    rpub = get_reduced_upub(range_st, upub)
    print('[+] Reduced Pubkey:', rpub.hex())
    if int(rpub.hex()[2:], 16) == 0: 
        write_keys((b'\x00') * 65, range_st)
        break
    pvk_found = run_cpu_kangaroo(tame_update_file, 0, range_en-range_st, dp, ncore, mx, rpub)
    if int(pvk_found.hex(),16) != 0: 
        write_keys(pvk_found, range_st)
        break
    lastitem = range_en
    range_st = randk(a, b)
    range_en = range_st + increment
    print('',end='\r')
print('[+] Program Finished')