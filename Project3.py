import random
import os.path


# A global constant defining the alphabet. 
LETTERS = "abcdefghijklmnopqrstuvwxyz"

def isLegalKey( key ):
    # A key is legal if it has length 26 and contains all letters.
    # from LETTERS.
    key = key.lower()
    return ( len(key) == 26 and all( [ ch in key for ch in LETTERS ] ) )

def makeRandomKey():
    # A legal random key is a permutation of LETTERS.
        lst = list( LETTERS )    # Turn string into list of letters
        random.shuffle( lst )    # Shuffle the list randomly
        return ''.join( lst )    # Assemble them back into a string

def makeConversionDictionary( key1, key2 ):
    key1 = key1.lower()
    key2 = key2.lower()
    dictkeys1 = {}
    dictkeys2 = {}
    for i in range(len(key1)):
        dictkeys1[key1[i]] = key2[i]
        dictkeys2[key2[i]] = key1[i]
    return dictkeys1, dictkeys2

def convertCharacter(ch,d):
    """convertCharacter takes a single character and encrypts/decrypts 
    it using the dictionary d. Recall that you have to treat the cases 
    of lowercase, uppercase, non-letter all separately, so it's a good 
    idea to have this separate function to deal with that.""" 
    if not ch.isalpha():
        converted = ch
    elif ch.islower():
        key = ch
        converted = (d[key])
    elif not ch.islower():
        ch = ch.lower()
        key = ch
        converted = ((d[key])).capitalize()
    return (converted)

def convertText( text, d ):
    """converts a string, basically by calling convertCharacter for each 
    character in it, and assembling the result."""
    fixed = ''
    for i in range(len(text)):
        value = convertCharacter(text[i], d)
        fixed = fixed + value
    return fixed

class SubstitutionCipher:
    def __init__ (self, key = makeRandomKey()):
        """Create an instance of the cipher with stored key, which
        defaults to a randomly generated key."""
        self.__key = key

    def getKey(self):
        """Getter for the stored key."""
        if isLegalKey(self.__key):
            return self.__key

    def setKey( self, newKey):
        """Setter for the stored key.  Check that it's a legal
        key."""
        if isLegalKey(newKey):
            self.__key = newKey.lower()

    def encryptFile( self, inFile, outFile ):
        """Encrypt the contents of inFile using the stored key
        and write the results into outFile.  Assume inFile exists.
        """
        INFILE = open(inFile, "r")
        #OUTFILE = open(outFile, "w")
        # find out the outputfile name
        extension = "-Enc"                  # or "-Dec"
        if INFILE.endswith(".txt"):
            outFile = inFile[:-4] + extension + ".txt"
        else:
            outFile = inFile + extension  
        for i in INFILE.readlines():
            #print(i)
            encdict, decdict = makeConversionDictionary(LETTERS, self.__key)
            values = convertText(i, encdict)
            OUTFILE.write(values)
        INFILE.close()
        OUTFILE.close()
        return (OUTFILE)

    def decryptFile( self, inFile, outFile ):
        """Encrypt the contents of inFile using the stored key
        and write the results into outFile.  Assume inFile exists.
        """
        INFILE = open(inFile, "r")
        OUTFILE = open(outFile, "w")
        for i in INFILE.readlines():
            #print(i)
            encdict, decdict = makeConversionDictionary(LETTERS, self.__key)
            values = convertText(i, decdict)
            OUTFILE.write(values)
        INFILE.close()
        OUTFILE.close()
        return (outFile)


def main():
    """ This implements the top level command loop.  It
    creates an instance of the SubstitutionCipher class and allows the user
    to invoke within a loop the following commands: getKey, changeKey,
    encryptFile, decryptFile, quit."""
    cipher = SubstitutionCipher()
    message = "\nEnter a command (getKey, changeKey, encryptFile, decryptFile, quit): "
    command = input(message)
    while command.lower() != "quit":
        if command.lower() == "getkey":
            print("  Current cipher key:", cipher.getKey())
        elif command.lower() == "decryptfile":
            filename = input("  Enter a filename: ")
            if os.path.exists(filename): #check that file exists 
                out_file = cipher.decryptFile(filename, "/Users/pg/cselements/blankfile.txt") #if so, take input filename and generate output filename
                print("The encrypted output filename is", out_file)
            else:
                print("File does not exist") #if not, print and continue 
        elif command.lower() == "encryptfile":
            filename = input("  Enter a filename: ")
            if os.path.exists(filename): #check that file exists 
                out_file = cipher.encryptFile(filename, "/Users/pg/cselements/blankfile.txt") #if so, take input filename and generate output filename
                print("The decrypted output filename is", out_file)
            else:
                print("File does not exist") #if not, print and continue 
        elif command.lower() == "changekey": #allows user to change stored key
            inner_command = input("  Enter a valid cipher key, 'random' for a random key, or 'quit' to quit: ")
            while inner_command.lower() != "quit":
                if inner_command == "random": #random (generate and store a new random key)
                    newkey = makeRandomKey()
                    cipher.setKey(newkey)
                    print("    New cipher key:", cipher.getKey())
                    inner_command = "quit"
                elif isLegalKey(inner_command): #gather a new key, check if it is valid, if valid then set the stored key to input
                    cipher.setKey(inner_command)
                    print("New cipher key:", cipher.getKey())
                    inner_command = "quit"
                else:
                    print("    Illegal key entered. Try again!")
                    inner_command = input("  Enter a valid cipher key, 'random' for a random key, or 'quit' to quit: ") 
                    cipher.setKey(inner_command)
                    print("New cipher key:", cipher.getKey())
                    inner_command = "quit"          
        else:
            print("  Command not recognized. Try again!")
        command = input(message) 
    if command.lower() == "quit":
        print("Thanks for visiting!\n")


main()






