#!/opt/bin/python3
import os
import sys
import re

MAGIC=[0xfa,0xce,0xfa,0xdf]

class Error(Exception):
    def __init__(self):
        print("Something went wrong")



#This function encodes a .txt using mtf coding and then outputs to a .mtf file
#Note: No compression will be achieved if the file has no repeated words
def encode_main(textfile):
    original_size=os.fstat(textfile.fileno()).st_size
    
    name=textfile.name.split(".")
    name[-1]="mtf"
    name=".".join(name)
    print("Writing to: ",name)
    outfile=open(name,"wb")
    outfile.write(bytearray(MAGIC))
    
    output=[]
    pile=[]
    codeLength=1
    for line in textfile:
        if len(line)>1:
            line=line.split(" ")
            line[-1] = line[-1][:-1]
            for word in line:
                if word not in pile:
                    #print("Adding %s to pile" % word)
                    pile.append(word)
                    if len(pile)<=120:
                        output.append(chr(len(pile)+128))
                    elif len(pile)<=375:
                        output.append(chr(121+128) + chr(len(pile)-121))
                    elif len(pile)<=65912:
                        output.append(chr(122+128) + chr((len(pile)-376)//256) + chr((len(pile)-376)%256))
                    else:
                        print("Too many unique words in the file")
                        raise Error
                    output.append(word)
                else:
                    index=pile.index(word)
                    pile.append(pile.pop(index))
                    if len(pile)-index<=120:
                        output.append(chr(len(pile)-index+128))
                    elif len(pile)-index<=375:
                        output.append(chr(121+128) + chr(len(pile)-index-121))
                    else:
                        output.append(chr(122+128) + chr((len(pile)-376-index)//256) + chr((len(pile)-376-index)%256))
        output.append("\n")
    output="".join(output)
    outfile.write(bytes(output,'latin-1'))
    
    compressed_size=len(bytearray(MAGIC)) + len(bytes(output,'latin-1'))
    print("Size of original file: ", original_size)
    print("Size of compressed file: ", compressed_size)
    print("Filesize has been reduced by %.2f%%" % ((original_size-compressed_size)/original_size*100))


    
#This function finds the next word in the string after the given index
#by finding the next chr with a value above 0x80
#It is used in the decode function because the words are separated by
#various code values rather than a consistent character such as space
def get_word(f):
    string=""
    newline=False                       #Due to the way this function is called,
    while True:                         #any newlines encountered are actual newlines
        ch=f.read(1)                    #rather than part of a code
        if ord(ch)>0x80 or ch=='\n':
            f.seek(f.tell()-1)         
            break                       
        string=string + ch
    #print("String found: ",string)
    return string
#This function decodes a .mtf file and outputs the plaintext to a .txt file
def decode_main(mtffile):
    magic=mtffile.read(4)
    if(not re.match('úÎúß',magic) and not re.match('úÎúÞ',magic)):
        raise Error
    
    output=[]
    pile=[]
    while True:
        ch=mtffile.read(1)
        if ch=='': break
        if ch=='\n':    output.append('\n')
        elif ord(ch)>0x80:
            if ord(ch)<=0xf8:
                code=ord(ch)-0x80
                if code>len(pile):
                    word=get_word(mtffile)
                    pile.append(word)
                else:
                    word=pile.pop(len(pile)-code)
                    pile.append(word)
            elif ord(ch)==0xf9:
                ch=mtffile.read(1)
                code=ord(ch)+121
                if code>len(pile):
                    word=get_word(mtffile)
                    pile.append(word)
                else:
                    word=pile.pop(len(pile)-code)
                    pile.append(word)
            elif ord(ch)==0xfa:
                ch=mtffile.read(1)
                ch2=mtffile.read(1)
                code=ord(ch)*256+ord(ch2)+376
                if code>len(pile):
                    word=get_word(mtffile)
                    pile.append(word)
                else:
                    word=pile.pop(len(pile)-code)
                    pile.append(word)
            else:
                raise Error
            if mtffile.read(1)=='\n':                     
                output.append(word + "\n")
            else:
                output.append(word + " ")
                mtffile.seek(mtffile.tell()-1)                
    name=mtffile.name.split(".")
    name[-1]="txt"
    name=".".join(name)
    output="".join(output)
    print("Outputting to: ",name)
    with open(name,'wb') as f:
        f.write(bytes(output,'latin-1'))

def encode(filename):
    with open(filename, encoding="latin-1") as f: 
        encode_main(f)    
def decode(filename):
    with open(filename, encoding="latin-1",newline="") as f:
        decode_main(f)    
