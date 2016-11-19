import Util
import matplotlib.pyplot as plt

dictates = Util.getAllDictates()

#porovna vyskyt chyb v prvni a posledni casti diktatu, pokud je liche delky vyrovna pocet slov
def start(fraction):
    long = []
    short = []
    first_fraction = []
    second_fraction = []
    out = []
    length = []
    for d in dictates:
        words = Util.getMostWrongWords(d.id).values()
        first = words[:len(words)/fraction]
        second = words[-len(words)/fraction:]
        if len(second) > len(first):
            first = (words[:(len(words) / fraction) + 1])
        if sum(second) !=0:
            out.append(sum(second)/float(sum(first)))
            #print "Dict: " " "+ str(d.id)+" " + str(len(words))+" " +str(sum(first)) + " "+str(sum(second)) + " "+ str(sum(second)/float(sum(first)))
        else:
            out.append(0)
        first_fraction.append(sum(first))
        second_fraction.append(sum(second))

        length.append(len(words))
        if len(words) > 25:
            long.append(d.id)
        if len(words) < 15:
            short.append(d.id)
        #out = sum(second)/float(sum(first))
        #plt.plot(len(words), out,'ro')
        #plt.plot(len(words), second, 'bo')
    print short
    print long

    for l in long:
        words = Util.getMostWrongWords(l).values()
        first = words[:len(words)/fraction]
        second = words[-len(words)/fraction:]
        if len(second) > len(first):
            first = (words[:(len(words) / fraction) + 1])
        if sum(second) !=0:
            print "L: " + str(sum(first)) + " " + str(sum(second)) + " " + str(sum(second)/float(sum(first)))

    for s in short:
        words = Util.getMostWrongWords(s).values()
        first = words[:len(words)/fraction]
        second = words[-len(words)/fraction:]
        if len(second) > len(first):
            first = (words[:(len(words) / fraction) + 1])
        if sum(second) !=0:
            print "S: " + str(sum(first)) + " " + str(sum(second)) + " " + str(sum(second)/float(sum(first)))
    plt.plot(length, out, 'ro')
    #plt.plot(length, second_fraction , 'bo')
    plt.show()

start(3)

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


def newOne():
    for d in dictates:
        words = Util.getMostWrongWords(d.id).values()
        print words
newOne()