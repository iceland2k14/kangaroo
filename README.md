# kangaroo
Find PrivateKey of corresponding Pubkey(s) using Pollard Kangaroo algo 

## Info
- Precomputation could help in search of a pubkey by overall Number of jumps required for collision during runtime.
- Instead of running 2 times for each pubkey search (1 for precompute and 1 for run) an option of saving the Tames Kangaroo DP could be usefull.
- By changing the pubkey range and therefore range in which search is happening the kangaroo will become not useful for other pubkey.
- To overcome this issue Pubkey Search is reduced in the given range of start:end so that the DP search is always in the 1:number range for any pubkey
- The DP collected during runtime is saved to a fixed binary file HashTable.ice and only tames kangaroo are retained.
- The option "ntu" controls whethere you would like to update this file in each run or not.
- __Tips__ 
  - always try to keep a reasonable range (max-min) to search. Kangaroo search is not sequential. Very small range will also takes few seconds to find key.
  - If very large range (max-min) is given program will break it into segments of 72000 trillion range each and run in them one by one till range is finished.
  - Speed shown is equal to the range coverage using formula 2.08 * sqrt(N) based on number of group operations jumps of kangaroos
  - Script has fixed DP of 10 but can be edited manually if needed. Those who know what they are doing.
  - mx = 2 is default. its a reasonable approximation for time and work. It gives us ~70% probability for the key to be in the given range. mx can be used till 6.
  - As we are searching in reduced range the pubkey even slightly outside the min:max range can be found if they are close to these limits.
  - Don't try to change the interval too much. the tames DP found in all previous runs are most usefull if the interval is very similar in search all the time.

## Usage
- python kangaroo.py [-h] -p PUBKEY [-keyspace min:max] [-ncore NCORE] [-n N] [-rand] [-rand1] [-ntu]

```
(base) C:\anaconda3>python kangaroo.py -p 0352b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e -keyspace 935da71d7350734c3472fe305fef82ab8aca644fc:935da71d7350734c3472fe305fff82ab8aca644f9
[+] Starting CPU Kangaroo.... Please Wait     Version [ 10052022 ]
[+] Search Mode: Range search Continuous in the given range
[+] Working on Pubkey: 0452b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e2d22dceb73a2648739bfc45c9a305e385a5c1fbeea35a8f946fd78c9fc67a615
[+] Using  [Number of CPU Threads: 7] [DP size: 10] [MaxStep: 2]
[+] Scanning Range          0x935da71d7350734c3472fe305fef82ab8aca644fc : 0x935da71d7350734c3472fe305fff82ab8aca644f9
[+] Reduced Pubkey: 0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798b7c52588d95c3b9aa25b0403f1eef75702e84bb7597aabe663b82f6f04ef2777
[+] Loading: [HashTable 0.9/1.0GB]
[+] [67.73 TeraKeys/s][Kang 7168][Count 2^28.30/2^29.07][Elapsed 19s][Dead 0][RAM 1089.2MB/44.9MB]
============== KEYFOUND ==============
Kangaroo FOUND PrivateKey : 0x935da71d7350734c3472fe305fef82ab8aca644fb
======================================
[+] Program Finished


```
