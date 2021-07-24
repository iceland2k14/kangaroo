# -*- coding: utf-8 -*-
"""
Usage :
 > python kangaroo_cpu

@author: iceland
"""
import bit
import ctypes
import platform

###############################################################################
ice = ctypes.CDLL('Kangaroo_CPU.dll')
    
ice.run_cpu_kangaroo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p] # st,en,dp,ncpu,mx,pvk,upub

ice.init_kangaroo_lib()
###############################################################################
def run_cpu_kangaroo(start_range_int, end_range_int, dp, ncpu, mx, upub_bytes):
    st_hex = hex(start_range_int)[2:].encode('utf8')
    en_hex = hex(end_range_int)[2:].encode('utf8')
    res = (b'\x00') * 32
    ice.run_cpu_kangaroo(st_hex, en_hex, dp, ncpu, mx, res, upub_bytes)
    return res

def pub2upub(pub_hex):
	x = int(pub_hex[2:66],16)
	if len(pub_hex) < 70:
		y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
	else:
		y = int(pub_hex[66:],16)
	return bytes.fromhex('04'+ hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

###############################################################################
print('[+] Starting CPU Kangaroo.... Please Wait')

ncore = platform.os.cpu_count() - 1 # Leave 1 thread open
dp = 10 # -1 for automatic value
mx = 1 # 0 for Endless
pubkey_hex = '0352b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e'

upub = pub2upub(pubkey_hex)
increment = 72057594037927935 # fix value dont change. Ctrl ^C handler not passed.
range_st = 0x935da71d7350734c3472fe305fef82ab8aca644fb
range_en = range_st + increment

print('[+] Working on Pubkey:',upub.hex())
print('[+] Using  [Number of CPU Threads: {}] [DP size: {}] [MaxStep: {}]'.format(ncore, dp, mx))
###############################################################################
print('[+] ............................................', end='\r')
while True:
    print('\n[+] Scanning Range ',hex(range_st),':', hex(range_en))
    pvk_found = run_cpu_kangaroo(range_st, range_en, dp, ncore, mx, upub)
    if int(pvk_found.hex(),16) != 0: 
        print('\n============== KEYFOUND ==============')
        print('Kangaroo FOUND PrivateKey : 0x'+pvk_found.hex())
        print('======================================')
        break
    range_st = range_en
    range_en = range_st + increment
print('Program Finished')