## Solution

Original String (cut for comfort):
```
1112211214131111212313122221112162121112411221322111216211211311416311321142112113222162222241132131133161122112141311112123131222211121632212141212331222211....
```
Hint:
```
Last one of the basic batch. But is it compression, encoding, or encryption?
```

This one definetly took the longest of the crypto1 series, and I needed lots of help with it, but I did manage to get it eventually, the hint was pretty unhelpful, so I went on my own and tried all I could think of, my first attempt was base7 encoding, but it failed, after that I remembered the hint given in the challenge description, it was ``For crypto1c, start with "0" not "1".``   , rereading that helped me realize, it had to be Binary, so I thought of as many ways to get binary from this string.

|Method|
|:-----|
|Assigning each number in the string a binary value|
|Assigning each number in the string a binary value AND repeating the binary value number times|
|Summing up all the repeating numbers (ie. 11111 = 5) and applying the earlier methods to it|
|LITERALLY ANYTHING THAT CAN BE FUCKING DONE|


After doing everything that is shown above, I asked around, I ended up finding someone who was willing to help, we talked and I got some hints, over and over again, until I got *The Hint*.


After *The Hint* I started coding instantly! creating a the simplest script I made so far, I can't find a way to easily explain the script without the code so I will show you the code here, with explainations for each part.


Just import a function and define some vars, I'll explain why the huge number is a string later.
```
from Crypto.Util.number import long_to_bytes

enc = "(HUGE DAMN NUMBER)"
result = ""
```
This is the interesting part, I prefer the individually explain everything
```
for i in range(len(enc)):               # Looping through the big number, this is the reason I made it a
                                        # string, since it's easier to iterate over it this way.
    binary = '0' if i % 2 == 0 else '1' # Now the cool stuff starts! here I used a one liner to check
                                        # if the i (the index) is odd or even, this determines if our
                                        # binary number will be a 1 or a 0.
    result+=binary*int(enc[i])          # Now for the end, we append the binary number
                                        # to the string n times (n being our number)
```



Decoding the binary we found by making it an integer and running the imported `long_to_bytes` to convert the number to a bytes sequence, then decoding the byte sequence to get rid of that pesky b!

```
flag = long_to_bytes(int(result, 2)).decode("ASCII") 

print(flag)
```

I'm not sure how well I explained the actual decryption process so I'll do a runtime chart (Don't worry I'm getting High-School flashbacks too).

```
i = for loop iteration, integer.
n = enc[i], character.
b = 1 or 0, character.
r = result of this iteration, string.
f = full result, string.
enc = "122223111114111", string.
```

|i|n|b|r|f|
|:-:|:-:|:-:|:-:|:-|
|0|1|0|0|0|
|1|2|1|11|011|
|2|2|0|00|01100|
|3|2|1|11|0110011|
|4|2|0|00|011001100|
|5|3|1|111|011001100111|
|6|1|0|0|0110011001110|
|7|1|1|1|01100110011101|
|8|1|0|0|011001100111010|
|9|1|1|1|0110011001110101|
|10|1|0|0|01100110011101010|
|11|4|1|1111|011001100111010101111|
|12|1|0|0|0110011001110101011110|
|13|1|1|1|01100110011101010111101|
|14|1|0|0|011001100111010101111010|


This binary translates to an acronym for a close friend of mine, He'll understand it <3