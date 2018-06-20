#!/usr/bin/env python
#Ben Sherington
#CS 427: Security Project 2

import sys
import os
import random

def modulation(base, power, modulation):
    f = 1
    while power > 0:
        if(power %2) == 1:
            f = (f * base) % modulation
        power = power >> 1
        base = (base * base) % modulation    
    return f

def miller_rabin(n):
    #This Miller-Rabin Code was brought to you by Rosettacode.org
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)
 
    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n is definitely composite
 
    for i in range(10):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
 
    return True
            
def padder(text, x):
    while x > 0:
        text += '0' * x
        x = len(text) % 4
    return text


def key_gen(randomizer):
    random.seed(randomizer)
    while(True):
        optimus = random.randint(0x80000000, 0xffffffff) | 0x80000001
        for i in range(0, 10):
            hot_rod = miller_rabin(optimus)

            if(hot_rod == False):
                break

        if(hot_rod):
            if(optimus % 12 == 5):
                p = 2 * optimus + 1
                for i in range(0, 10):
                    ultra_magnus = miller_rabin(p)
                    if(not ultra_magnus):
                        break
                if ultra_magnus:
                    break
        else:
            continue
    d = random.randint(1, p-2)
    generator = random.randint(1, p-1)
    #generator = 2
    e2 = modulation(generator, d, p)
    return generator, e2, p, d

def encrypt(generator, e2, p, plaintext):
    cipher = open("ciphertext.txt", "w+")
    #diff = len(plaintext) % 4 
    #if(diff != 0):
        #padder(plaintext, diff)
    slices = slicer(plaintext, 4)
    for piece in slices:
        r  = random.randint(1, p-1)
        c1 = modulation(generator,r, p)
        sliced_string = " "
        for char in piece:
            sliced_string += format(ord(char), '08b')
            
        encrypting_string = int(sliced_string,2)
        c2 = ((encrypting_string % p) * modulation(e2, r, p) % p)
        cipher.write(str(c1))
        cipher.write(" ")
        cipher.write(str(c2) + '\n')
        cipher.write("")
    cipher.close()

    return cipher

def decrypt(d, p, c1, c2):
    #this decrypts
    message = (modulation(c1,(p-1-d),p) * (c2 % p)) % p
    # print("message = {}".format(message))
    return message


def slicer(text, slice_size):
    return [text[i:i+slice_size] for i in range(0, len(text),slice_size)]


def console():
    commands = ['1', '2', '3', '4']
    while True:
        print("\nWelcome to Pub_Crypto. Please make a selection: \n")
        print("1) Key Generation\n")
        print("2) Encryption\n")
        print("3) Decryption\n")
        print("4) Quit\n")
        commandline = input("Enter Command: ")
        if commandline not in commands:
            print("Invalid Selection please try again\n")
        
        if commandline == '1':
            
            private_writer = open("prikey.txt" ,"w+")
            public_writer = open("pubkey.txt", "w+")
            prompt = input("Enter a number: ")
            seed = int(prompt)
            gen, e2, p, d = key_gen(seed)
            
            public_writer.write(str(p))
            public_writer.write(" ")
            public_writer.write(str(gen))
            public_writer.write(" ")
            public_writer.write(str(e2))
            public_writer.close()

            private_writer.write(str(p))
            private_writer.write(" ")
            private_writer.write(str(gen))
            private_writer.write(" ")
            private_writer.write(str(d))
            private_writer.close()
        
        if commandline == '2':

            
            plaintext = open("testfile.txt").read()
            public_reader = open("pubkey.txt", "r")
            public_key = public_reader.read()
            p, gen, e2 = public_key.split(" ")
            encrypt(int(gen), int(e2), int(p), plaintext)
            
            public_reader.close()
        
        if commandline == '3':

            decipher = open("translated.txt", "w+")
            private_reader = open("prikey.txt", "r")
            private_key = private_reader.read()
            p, gen, d = private_key.split(" ")
            cipher_reader = open("ciphertext.txt", "r")
            for line in cipher_reader:
                c1, c2 = line.split(" ")
                message = decrypt(int(d),int(p),int(c1),int(c2))
                decryptedmessage = format(message, '032b')
                first_char = chr(int(decryptedmessage[0:8], 2))
                second_char = chr(int(decryptedmessage[8:16], 2))
                third_char = chr(int(decryptedmessage[16:24], 2))
                fourth_char = chr(int(decryptedmessage[24:], 2))
                decipher.write(first_char)
                decipher.write(second_char)
                decipher.write(third_char)
                decipher.write(fourth_char)
            decipher.close()
            private_reader.close()

        elif commandline == '4':
            print("Thank you for using Pub_Crypto. Have a nice day\n")
            exit()
        # pubkey.txt (p, gen, e2)
        # prikey.txt (p, gen, d)
    

if __name__ == "__main__":
    #this runs it
    console()