import random
import time
import math
lettre="eri ieiaaaaaaaeeeeeeeeeuuuuuooooooiiiiiiiiiissssssssssscnr ehlsfqpwqieowe semfpseiuef slajiweucb coeihfsljh feslhf s           "
while(1):
    mot = ""
    l = ""
    phrase = ""
    k = 1
    while k != 0 :
        i = random.randint(0,len(lettre)-1)
        l = lettre[i]
        mot = mot + l
        if l == " " :
            phrase = phrase + mot
            if len(mot) > 4:
                phrase = phrase[0:len(phrase)-1] + ".cpp "
                print(phrase)
                k=0



    time.sleep(math.log1p(random.randint(0,3000)/1000))
