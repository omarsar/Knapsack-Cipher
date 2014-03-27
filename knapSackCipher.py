__author__ = 'Cypher Odyssey'

import argparse
#****************************************
#SuperKnapsack Class
#****************************************
class SuperKnapsack:
    def __init__(self, arr = []):
        self.arr = arr
        i=0
        lent = len(arr)

        #check if superincreasing at index
        for num in range(0,lent):
            if num!=0:
                if (self.arr[num]<=sum(self.arr[0:num])):
                    raise argparse.ArgumentTypeError('Not superincreasing at index "%s"'%(num))


    def getarray(self):
        return self.arr

    def primes(self,m,n):
        state1 = all(m % i for i in range(2,m))
        state2 = all(n % i for i in range(2,n))
        if state1==True and state2==True:
            return True
        else:
            return False

    def to_general(self,m,n):
        if (n<=self.arr[len(self.arr)-1]):
            raise argparse.ArgumentTypeError('"%s" smaller than superincreasing knapsack' % (n))

        if (self.primes(m,n) == False):
            raise argparse.ArgumentTypeError("Arguments must be both Prime")

        hold = list(map((lambda x: (x*m)%n), self.arr))
        return hold

    def inversemod(self,m,n):
        inverse = 1
        val = n+1
        if m>inverse:
            while (val%m)!=0:
                val = (n*inverse)+1
                inverse=inverse+1
            inverse = val/m
        return inverse

    def superPrefixSum(self,val):
        positions = [0]*len(self.arr)
        temp = 0
        i = len(self.arr)
        while i!=0:
            if (self.arr[i-1] + temp)<=val:
                positions[i-1]=1
                temp=temp+self.arr[i-1]
            else:
                positions[i-1]=0
            i=i-1
        return positions
#********************************************
#Knapsack Cipher Class
#********************************************
class KnapsackCipher:
    M = 41
    N = 491
    DEF_SUPER = SuperKnapsack([2,3,7,14,30,57,120])
    DEF_GENERAL = DEF_SUPER.to_general(M,N)

    #In charge of encrypting
    def encrypt(self,plaintext,generalknap=DEF_GENERAL):
        bintext = []
        cipher = []

        i=-1
        pad = len(plaintext)%len(generalknap)
        plaintext = plaintext+("#"*pad)

        plaintext = bytearray(plaintext)
        for c in plaintext:
            i=i+1
            bits = format(c,'b')
            bits = bits.rjust(8,"0")
            for b in bits:
                bintext.append(b)

        value = 0
        i=0
        j=-1
        k= len(generalknap)

        while (i<len(bintext)):
            value = value+int(bintext[i])*generalknap[i%k]
            #print value,
            if ((i+1)%k == 0):
                cipher.append(value)
                value = 0
            i=i+1

        cipher = list(map((lambda x: str(x).rjust(4,"0")), cipher))
        for c in range(0,pad):
            cipher.pop()
        print "CIPHER:",''.join(cipher),"\n"
        return ''.join(cipher)

    #In charge of Decrypting
    def decrypt(self,cipherArray,superknap=DEF_SUPER,m=M,n=N):
        pad = (len(cipherArray)/4)%len(superknap)
        cipherArray = cipherArray+("0334"*pad)
        plaintext = []
        mysuper = SuperKnapsack(superknap)

        if mysuper.primes(m,n):
            inverse = mysuper.inversemod(m,n)
            cipherArray = map(''.join,zip(*[iter(cipherArray)]*int(4)))
            bytevalues = list(map((lambda x: (int(x)*inverse)%n), cipherArray))
            bitvalues = list(map((lambda x: (mysuper.superPrefixSum(x))),bytevalues))

            for b in bitvalues:
                temp=[]
                for bits in b:
                    temp.append(str(bits))
                plaintext.append(chr(int(str(''.join(temp)),2)))
                del temp

            for n in range(0,pad):
                plaintext.pop()

            print "PLAIN:",''.join(plaintext)

        return cipherArray,superknap

#****************************
#MAIN
#****************************

sup = SuperKnapsack([2,3,7,14,30,57,120,251])
newKC = KnapsackCipher()

#Test 1
carray = newKC.encrypt("Pay in \n 1 hour",sup.to_general(41,491))
newKC.decrypt(carray,sup.getarray(),41,491)

#Test 2
carray = newKC.encrypt("Hello World!",sup.to_general(41,491))
newKC.decrypt(carray,sup.getarray())


