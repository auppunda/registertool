#!/usr/bin/python
from docx import Document
from docx import table

def makefile():
    #gets the name of the file you want to read
    docName = input("Enter the path of the docs: ")
    doc = Document(docName)
    #gets the name of the file you want to write it to
    fileName = input("Enter the name of the file u want it saved to:")
    #get tables from document
    listOfTables = doc.tables
    file = open(fileName + "_register.txt", "w")
    #loop through all registers
    for register in listOfTables:
        rowsforTable = register.rows
        registerName = rowsforTable[0].cells[3].text
        
        registerAddress = rowsforTable[1].cells[3].text

        numChar = ""
        i = 0
        #get registerAddress from table
        for char in registerAddress:
            if (char > '0' and char <='9') or (char >= 'A' and char <= 'Z'):
                j = i
                for char in registerAddress[i:len(registerAddress)]:
                    if (char < '0' or char > '9') and (char < 'A' or char >'Z'):
                        numChar = registerAddress[i:j]
                        break;
                    j = j+1
                if(j == len(registerAddress)):
                    numChar = registerAddress[i:len(registerAddress)]
                break;
            i = i+1
        if numChar == "":
            numChar = "0x0:0x0"
        else:
            numChar = "0x" + numChar + ":0x0"
        #read the format string, read write, and descriptor from table
        regDescriptor = rowsforTable[2].cells[3].text

        formatString = rowsforTable[3].cells[3].text

        readWrite = rowsforTable[5].cells[1].text
        readchar = ' '
        if(len(readWrite) > 1):
            readchar = readWrite[1]
        if readchar == 'W':
            readWrite = "read-write"
        else:
            readWrite = "read-only"
        j = 0
        #gets the register string from the format string, this is used to assign which bits
        numberString = ""
        charString = ""
        for char in formatString:
            if char == '\n':
                numberString = formatString[0:j]
                print(numberString)
                i = j + 1
                for charr in formatString[i:len(formatString)]:
                    if charr != " ":
                        charString = formatString[i:i+j]
                        break
                    i = i+1
                #charString = formatString[j+1:j+1+j]
                print(charString)
                break
            j = j+1

        resetChar = rowsforTable[5].cells[3].text
        if resetChar == "All one register":
            resetChar = "0xffffffffffffffff:0xffffffffffffffff"
        else:
            resetChar = "0x0000000000000000:0xffffffffffffffff"

        #write to file, write register name, addressoffset, size, access, and reset
        file.write("register:" + registerName + "\n")
        file.write("addressoffset:" + numChar + "\n")
        file.write("size:64" + "\n")
        file.write("access:" + readWrite + "\n")
        file.write("reset:" + resetChar + "\n")
        #gets the fields from the format string and writes it to file
        k=0
        amountWhiteSpace = 0
        amountUnused = 1
        reset = rowsforTable[5].cells[3].text
        if reset != "All one register" and reset != "All zero register":
            while k < len(charString):
                #checks if field is unused
                if charString[k] == '.' or charString[k] == '0':
                    for s in range(k,len(numberString)):
                        if charString[s] != '.' and charString[s] != '0' and charString[s] != ' ' or s == len(numberString) - 1:
                            if s == len(numberString) - 1:
                                if amountUnused == 1:
                                    file.write("field:UNUSED:" + str(s-k + 1 - amountWhiteSpace) + "\n")
                                else:
                                    file.write("field:UNUSED" + str(amountUnused) +  ":" + str(s-k + 1 - amountWhiteSpace) + "\n") 
                                k = s
                            else:
                                if amountUnused == 1:
                                    file.write("field:UNUSED:" + str(s-k - amountWhiteSpace) + "\n")
                                else:
                                    file.write("field:UNUSED" + str(amountUnused) +  ":" + str(s-k - amountWhiteSpace) + "\n") 
                                k = s - 1
                            amountUnused += 1
                            amountWhiteSpace = 0
                            break
                        if charString[s] == ' ':
                            amountWhiteSpace = amountWhiteSpace + 1
                #ignores if blank space    
                elif charString[k] != ' ':        
                    for s in range(k,len(charString)):
                        #finds when the character is not repeated, and a new field starts, but ignores blank spaces
                        if (charString[s] != charString[k] and charString[s] != ' '):
                                file.write("field:" + charString[k] + ":" + str(s-k - amountWhiteSpace) + "\n")
                                k = s - 1
                                amountWhiteSpace = 0
                                break
                        if s == len(charString) - 1:
                                print(charString[len(charString) - 1])
                                file.write("field:" + charString[k] + ":" + str(s-k  + 1 - amountWhiteSpace) + "\n")
                                k = s
                                break
                        if charString[s] == ' ':
                            amountWhiteSpace = amountWhiteSpace + 1
                k= k+1
        #finishes up the register
        file.write("vendorExtensions:NULL" + "\n")
        file.write("\n")

    file.close()
    return None

