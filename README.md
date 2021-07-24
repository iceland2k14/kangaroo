# kangaroo
Find PrivateKey of corresponding Pubkey(s) using Pollard Kangaroo algo 

# Usage
- python kangaroo.py
```
(base) C:\anaconda3>python kangaroo.py
[+] Starting CPU Kangaroo.... Please Wait
[+] Working on Pubkey: 0452b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e2d22dceb73a2648739bfc45c9a305e385a5c1fbeea35a8f946fd78c9fc67a615
[+] Using  [Number of CPU Threads: 7] [DP size: 10] [MaxStep: 1]
[+] ............................................
[+] Scanning Range  0x935da71d7350734c3472fe305fef82ab8aca644fb : 0x935da71d7350734c3472fe305fff82ab8aca644fa
[+] [646.03 TeraKeys/s][Kang 7168][Count 2^27.34/2^29.07][Elapsed 09s][Dead 0][RAM 19.8MB/44.9MB]
============== KEYFOUND ==============
Kangaroo FOUND PrivateKey : 0x00000000000000000000000935da71d7350734c3472fe305fef82ab8aca644fb
======================================
Program Finished
```
