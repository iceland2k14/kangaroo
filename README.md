# kangaroo
Find PrivateKey of corresponding Pubkey(s) using Pollard Kangaroo algo 

# Usage
- python kangaroo.py
```
(base) C:\anaconda3>python kangaroo.py -p 02ca298581993a21f38083092001dfa86a2f4aa06e75867a3fece2b5b96a253e20 -keyspace 1:ffffffffffff -ntu -dispset 1
[+] Starting CPU Kangaroo.... Please Wait     Version [ 02072022 ]
[+] Search Mode: Range search Continuous in the given range
[+] Working on Pubkey: 04ca298581993a21f38083092001dfa86a2f4aa06e75867a3fece2b5b96a253e2065f41e8a3277db35a7bfa0fef5999f2ec76d3477fb668f4fc34188965cf981d8
[+] Using  [Number of CPU Threads: 7] [DP size: 10] [MaxStep: 2]
[+] Scanning Range          0x1 : 0xffffffffffff
[+] Reduced Pubkey: 04a07c1bd42d3edf0bf44074da9cab49875ac9610ce13eeb46ea4aade8b69a033dbe4b28d6e5f101e7fe7df31c553c366126777f964e99acbaf0650f246d923399
[+] Loading: [HashTable 1.3/1.4GB]
[+] Scanning Range          0x1000000000000 : 0x1fffffffffffe
[+] Reduced Pubkey: 046548ef2cb83531d598bfc5d336b741e3ebb5d8d4f40b49c4165305a9056ab09a76eec10541de1ea5bf3210c3a3ff96ecc58b7d1cda067b39801644dbebedff5b
[+] Loading: [HashTable 1.3/1.4GB]

============== KEYFOUND ==============
Kangaroo FOUND PrivateKey : 0xff88ffff9900
======================================
[+] Program Finished
```
