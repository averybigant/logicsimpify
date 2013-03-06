#!/usr/bin/python
#coding=utf-8
import functools
from pprint import pprint
#import copy

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
            if self._current[i] != minterm2._current[i] and "x" not in (self._current[i], minterm2._current[i]):
                if diff:
                    return ()
                diff = True
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
        return "".join(showchar)

    def __eq__(self, mt2):
        s1 = "".join(self._current)
        s2 = "".join(mt2._current)
        return s1 == s2

    def __hash__(self):
        s = "".join(self._current)
        return s.__hash__()

def con_all(l, isset=True):
    ll = l[:]
    reduce(lambda l1,l2: l1.extend(l2), ll, [])
    if len(ll) == 1 and type(ll) == list:
        ll = ll[0]
    if isset:
        return set(ll)
    else:
        return ll

def get_sublist(minterm, nlist):
    rset = set()
    for minterm2 in nlist:
        r = minterm - minterm2
        if r:
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
    while 1:
        if len(lists) > 1:
            for i in xrange(1, len(lists)):
                clist = []
                get_sublist4mt = functools.partial(get_sublist, nlist=lists[i])
                for mt in lists[i-1]:
                    rmts = get_sublist4mt(mt)
                    if len(rmts) == 0:
                        finalmts.append(mt)
                    else:
                        clist.extend(rmts)
                clist = list(set(clist))
                lists[i-1] = clist
                if i == len(lists) - 1:
                    del lists[-1]
                print "cuurent"
                pprint(lists)
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
    pprint(diclists)
    splists = split_conti(diclists, len(minterms[0]))
    pprint(splists)
    for l in splists:
        print "<<<<<<<"
        pprint(reduce_single_conti(l))
        print "<<<<<<<"
    #pprint(map(reduce_single_conti, splists))
    return con_all(map(reduce_single_conti, splists), False)

def fastprint(finalmts):
    print "====================="
    #print finalmts
    for fmt in finalmts:
        print str(fmt)

def main():
    #mts = ["101", "001", "100", "111"]
    mts = ["001", "011", "100", "101", "111", "110"]
    #mts = ["0000", "0010", "1000", "1010"]
    mts = map(lambda x: Minterm(x), mts)
    fastprint(get_finalmts(mts))

if __name__ == '__main__':
    main()

