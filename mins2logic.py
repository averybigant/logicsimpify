#!/usr/bin/python
#coding=utf-8
#license: GPLv3
#author: yurenbi
import functools
from pprint import pprint
import logging
logging.basicConfig(level=logging.WARN)

import sys
from os import linesep

FILENAME = "./s.txt"

class Minterm(object):
    @staticmethod
    def _default_char_show(num):
        return chr(num+97).upper()
        #return chr(num+97).upper() + str(num)

    def __init__(self, m, show=None):
        self._raw = list(m)
        self._current = self._raw
        self._count1 = None
        self.charshow = show if show else Minterm._default_char_show
        self._batch = -1

    def count1(self):
        if not self._count1:
            self._count1 = self._current.count("1")
        return self._count1

    def __len__(self):
        assert self._raw == self._current
        return len(self._raw)

    def __sub__(self, minterm2):
        rmt = Minterm([], self.charshow)
        diff = False
        assert len(minterm2) == len(self)
        for i in xrange(len(self._current)):
            if self._current[i] != minterm2._current[i] :
                if diff:
                    return ()
                diff = True
                if "x" not in (self._current[i], minterm2._current[i]):
                    rmt._current.append("x")
            else:
                rmt._current.append(self._current[i])
        return rmt

    def __repr__(self):
        return "< %s.%s object %s at %s >" % (__name__, "Minterm", "".join(self._current), id(self))

    def __str__(self):
        showchar = []
        for i, c in enumerate(self._current):
            if c == "x":
                continue
            thischar = self.charshow(i)
            if c == "0":
                thischar = "!" + thischar
            showchar.append(thischar)
        return "&".join(showchar)

    def __eq__(self, mt2):
        s1 = "".join(self._current)
        s2 = "".join(mt2._current)
        return s1 == s2


    def __hash__(self):
        s = "".join(self._current)
        return s.__hash__()

def con_all(l, isset=True):
    ll = l[:]
    reduce(lambda l1,l2: l1 + l2, ll, [])
    if len(ll) == 1 and type(ll) == list:
        ll = ll[0]
    if isset:
        return set(ll)
    else:
        return ll

def expand_list(l):
    l = list(l)
    if not l:
        return []
    if type(l[0]) == list:
        return expand_list(l[0]) + expand_list(l[1:])
    else:
        return [ l[0] ] + expand_list(l[1:])

def get_sublist(minterm, nlist, current_batch):
    rset = set()
    for minterm2 in nlist:
        r = minterm - minterm2
        #if r and not r == minterm:
        if r:
            minterm2._batch = current_batch
            rset.add(r)
    return list(rset)

def get_init_diclists(minterms):
    rdic = {}
    for mt in minterms:
        l = rdic.get(mt.count1(), [])
        if not l:
            rdic[mt.count1()] = l
        l.append(mt)
    return rdic

def split_conti(diclists, length):
    rlist = []
    maxx = -1
    for i in xrange(0, length+1):
        if i <= maxx:
            continue
        srlist = []
        if i in diclists:
            srlist.append(diclists[i])
        for j in xrange(i+1, length+1):
            if j in diclists:
                srlist.append(diclists[j])
                maxx = j
            else:
                break
        if(srlist):
            rlist.append(srlist)
    return rlist

def reduce_single_conti(lists, finalmts=None):
    if finalmts==None:
        finalmts = []
    lists = lists[:]
    while 1:
        logging.debug("whilelop>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if len(lists) > 1:
            for i in xrange(1, len(lists)):
                clist = []
                get_sublist4mt = functools.partial(get_sublist, nlist=lists[i])
                for mt in lists[i-1]:
                    rmts = get_sublist4mt(mt, current_batch=i)
                    logging.debug("rmts: %s" % str(rmts) )
                    if len(rmts) == 0 and mt._batch != i-1:
                        logging.debug("add finalmts: %s" % str(mt))
                        finalmts.append(mt)
                    else:
                        clist.extend(rmts)
                clist = list(set(clist))
                lists[i-1] = clist
                if i == len(lists) - 1:
                    del lists[-1]
                logging.debug("lists: %s" % str(lists))
        elif lists:
            finalmts.extend(lists[0])
            break;
        else:
            break;
    return finalmts

def get_finalmts(minterms):
    if not minterms:
        return []
    diclists = get_init_diclists(minterms)
    logging.debug("diclists:")
    logging.debug(str(diclists))
    splists = split_conti(diclists, len(minterms[0]))
    logging.debug("splists:")
    logging.debug(str(splists))
    #for l in splists:
        #print "<<<<<<<"
        #pprint(reduce_single_conti(l))
        #print "<<<<<<<"
    #pprint(map(reduce_single_conti, splists))
    return expand_list(con_all(map(reduce_single_conti, splists), False))

def fastprint(finalmts):
    print "====================="
    #print finalmts
    for fmt in finalmts:
        print str(fmt)

def simple_test():
    #mts = ["101", "001", "100", "111"]
    #mts = ["001", "011", "100", "101", "111", "110"]
    #mts = ["0000", "0001", "0010", "0100", "0011", "0101", "0110", "1100", "0111"]
    #mts = ["000", "001", "011", "100"]
    mts = ["0000", "0010", "1000", "1010"]
    #!B!D
    mts = map(lambda x: Minterm(x), mts)
    fastprint(get_finalmts(mts))


def main():
    global FILENAME
    def alert_and_exit(ustr, linen):
        print ustr
        print "line:", linen+1
        sys.exit(1)

    def getline(line, linen):
        line = line.replace(linesep, "").replace(" ", "")
        for char in line:
            if not (char == "1" or char == "0"):
                alert_and_exit(u"只允许0或者1", linen)
        return line

    Control_bits = None
    currentop = ""
    currentmi = ""
    Oplen = -1
    Milen = -1
    cyn = 1
    Maxcyn = 1
    Status = 0 #0 read OP, #1 read microinstruction

    if len(sys.argv) > 1:
        FILENAME = sys.argv[1]
    with open(FILENAME, "rb") as f:
        currentop = getline(f.readline(), 0)
        Oplen = len(currentop)
        if len(currentop) < 1:
            alert_and_exit(u"不允许空的OP", 0)

        currentmi = getline(f.readline(), 0)
        Milen = len(currentmi)
        if len(currentmi) < 1:
            alert_and_exit(u"不允许空的指令", 1)

        Control_bits = [ [] for i in xrange(Milen) ]

        for i in xrange(Milen):
            if currentmi[i] == "1":
                Control_bits[i].append( (cyn, currentop) )

        Status = 1

        for i, line in enumerate(f, 2):
            if Status == 0:
                currentop = getline(line, i)
                if len(currentop) != Oplen:
                    alert_and_exit(u"OP长度不一致", i)
                cyn = 0
                Status = 1
            else:
                currentmi = getline(line, i)
                if len(currentmi) == 0:
                    if cyn == 0:
                        alert_and_exit(u"不允许空的指令", i)
                    else:
                        Maxcyn = max(Maxcyn, cyn-1)
                        Status = 0
                elif len(currentmi) == Milen:
                    for i in xrange(Milen):
                        if currentmi[i] == "1":
                            Control_bits[i].append( (cyn, currentop) )
                    cyn += 1
                else:
                    alert_and_exit(u"微指令长度不一致", i)

        lencyn = len(bin(Maxcyn)) - 2

        def char_show(num):
            if num < Milen:
                return "O" + str(num)
            else:
                return "Cy" + str(num - Milen)

        for i in xrange(Milen):
            if not Control_bits[i]:
                continue
            minterms = map( lambda tup: Minterm(tup[1] + bin(tup[0])[2:].rjust(lencyn, "0"), char_show), Control_bits[i] )
            print "CONTROL BIT %d:" % i
            print "C%d = %s" % ( i, " + ".join(map(str, minterms)) )
            print "   =", " + ".join( map(str, get_finalmts(minterms)) )

if __name__ == '__main__':
    main()
