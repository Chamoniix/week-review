import random
import time
import math
lettre="aaabcdeeeeefghiiijklmmnnoooppqrsssttuuuvwxyyz"
keyWords = ["Building ", "Compressing", "Exctracting", "Processing", "Debug", "Compiling", "Starting", "Analyzing"]
while(1):
    mot = ""
    l = ""
    phrase = ""
    j = random.randint(0,len(keyWords)-1)
    phrase = keyWords[j]
    for k in range(0,random.randint(3,7)) :
        i = random.randint(0,len(lettre)-1)
        mot = mot + lettre[i]

    phrase = phrase + " " + mot + ".cpp..."
    print(phrase)
    time.sleep(math.log1p(random.randint(0,1000)/1000))
