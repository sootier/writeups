from Crypto.Util.number import bytes_to_long



binary = str(bin(bytes_to_long(input("String To Encode: ").encode())))
enc = ""

i = 0
while (i < len(binary)):
    n = 0
    for j in range(i, len(binary)):
        if binary[i] == binary[j]:
            n+=1
        else:
            break
    i = i+n
    enc+=str(n)
print(enc)
