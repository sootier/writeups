## Solution

Original String:
```
n h newuhe eddre nect tota ufyaolim7ter val lcy vsf slAroeeoiroigtatradetlno o pek ?Sl n aee s epeth  atedpairu hsg?Hot oe.wygoelrfo 93aei alsw'e  elntte l o.A eat o,b' by le frnsk,nt tes uv hl o ir lgHayairiteobbaam ibuohlm tursernuuohgteseoob srk    spsrirt1 mdvoho'eI nmpiihi ainuetere susutpa .lwc  dsa   t t,iiorgoguhfecae r tcslhslayhn eseaftaeo peelsantnthu e,nwati  Tetees ecfh ai ofCteb seisn eto potb hyli'rCtirbsx oaego'sbttamt u?Mingfh.e  ev dac cfp  c om  hahh t enm t.esg f ut t  oilso uhao
```




Inside the file where the ciphered string was I found the following:
```
A word of advice for the next one. Don't straddle the fence or you'll end up riding a rail or five. It'll hurt from the bottom up.
```
Reading this I immediately thought of RailFence cipher (aka [ZigZag cipher](https://en.wikipedia.org/wiki/Rail_fence_cipher)), This is a really cool cipher that I like a lot, the decryption takes 3 inputs, a rail number and an encrypted string.

from the hint we can guess that there are 5 rails, and we know the encrypted string, we also get a hint telling us to do the cipher "upside down", which means having an offset of `rails-1`. so all that's left now is coding! for this I made a python script.



Decoded String:
```
Moving right along through a different challenge. How are you at ciphers like these? Solvable by hand and made easier because of the placement of the upper case letters and punctuation throughout the message, no? How about this for a key. The way the goose spells terrific from the 1973 animated movie of Charlotte's web. I've seen a misspelling in the title of a clip on youtube. At the very least it's four Cs, but it's probably six. All lower case for goodness' sake, but not that it matters, oui oui?
```

Finding [the clip](https://youtu.be/Xf5a_F-zNgE?t=71) was easy enough, after a few tries I got the basic spelling down, but it didn't work, so I checked the cipher result again, and was happy to find I only needed to add 2 c's to the end.

At the end the password was:
```
teerrrriiffiicccc
```

And so I used it to unzip `crypto1b.zip` to get to the last part!