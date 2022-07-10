enc = "n h newuhe eddre nect tota ufyaolim7ter val lcy vsf slAroeeoiroigtatradetlno o pek ?Sl n aee s epeth  atedpairu hsg?Hot oe.wygoelrfo 93aei alsw'e  elntte l o.A eat o,b' by le frnsk,nt tes uv hl o ir lgHayairiteobbaam ibuohlm tursernuuohgteseoob srk    spsrirt1 mdvoho'eI nmpiihi ainuetere susutpa .lwc  dsa   t t,iiorgoguhfecae r tcslhslayhn eseaftaeo peelsantnthu e,nwati  Tetees ecfh ai ofCteb seisn eto potb hyli'rCtirbsx oaego'sbttamt u?Mingfh.e  ev dac cfp  c om  hahh t enm t.esg f ut t  oilso uhao"
rails = 5
offset = rails-1

def railNumber(position, rails, offset):
    position = (position + offset) % (rails * 2 - 2)
    if (position < rails):
        return position
    else:
        return 2*rails-position-2

def decrypt(enc, rails, offset):
    result = ['+'] * len(enc)
    k = 0
    for i in range(rails):
        for j in range(len(enc)):
            if (railNumber(j, rails, offset) == i):
                result[j] = enc[k]
                k+=1
    return "".join(result)


print(decrypt(enc,rails,offset))