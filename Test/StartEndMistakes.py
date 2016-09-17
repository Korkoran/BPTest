import Util
import matplotlib as plt

dictates = Util.getAllDictates()

#porovna vyskyt chyb v prvni a posledni casti diktatu, pokud je liche delky vyrovna pocet slov
def start(fraction):
    for d in dictates:
        words = Util.getMostWrongWords(d.id).values()
        first = words[:len(words)/fraction]
        second = words[-len(words)/fraction:]
        if len(second) > len(first):
            first = (words[:(len(words) / fraction) + 1])
        if sum(second) !=0:
            print "Dict: " + str(d.id)+ " " +str(sum(first)) + " "+str(sum(second)) + " "+ str(sum(second)/float(sum(first)))

start(4)

for i in range(94,95):
    words = Util.getMostWrongWords(i).values()
    print words
    first = (words[:len(words) / 4])
    second = (words[-len(words) / 4:])
    if len(second) > len(first):
        first = (words[:(len(words)/4)+1])
    print len(first)
    print len(second)
    print sum(first)
    print sum(second)
    print sum(second) / float(sum(first))
    print sum(first) / float(sum(second))


