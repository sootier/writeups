from Crypto.Util.number import long_to_bytes


enc = "(HUGE ASS NUMBER)"
result = ""



for i in range(len(enc)):
    binary = '0' if i % 2 == 0 else '1'
    result+=binary*int(enc[i])

print(result)

flag = long_to_bytes(int(result, 2)).decode("ASCII") # binary to string.




print(flag)