import os,sys,time,re,base64

AllowedB64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def IsValidBase64(StrX):
    BeforeLast = "="
    Last = "="
    if StrX == "":
        return False
    lenX = len(StrX)
    if lenX == 0:
        return False
    i = 0
    while i < lenX:
        if AllowedB64Chars.find(StrX[i])== -1:
            #Only allowed if the filler
            if i != lenX-1 and i != lenX-2:
                return false
            elif i == lenX-2 and StrX[i]!="=":
                BeforeLast = StrX[i]
            elif i == lenX-1 and StrX[i]!="=":
                Last = StrX[i]
        i = i + 1
    if BeforeLast != Last:
       return False
    return True

def DecodeBase64(fCon_n):
    if IsValidBase64(fCon_n)==False:
        print "Not a valid base64 string\r\n"
        return ""
    decX = ""
    try:
        decX = base64.b64decode(fCon_n)
        return decX
    except:
        print "Error: seems like it is not valid base64 string\r\n"
        return ""
    return decX

def RemoveTabsSpacesNewLines(StrX):
    if StrX == 0 or len(StrX)==0:
        return ""
    lenX = len(StrX)
    i = 0
    NewStrX = ""
    while i < lenX:
        if StrX[i]!= "\r" and StrX[i]!="\n" and StrX[i]!="\t" and StrX[i]!=" ":
            NewStrX += StrX[i]
        i = i + 1
    return NewStrX

def FindOffset(Start,HayStack,Needle):
    if HayStack == "" or len(HayStack) == 0 or \
       Needle == "" or len(Needle) == 0:
        return -1
    Off = HayStack.find(Needle,Start)
    return Off

#Finds first single/double quote
def FindFirstQuote(Start,HayStack):
    if HayStack == "" or len(HayStack)==0:
        return -1
    lenHay = len(HayStack)
    if Start >= lenHay:
        return -1
    i_ = Start
    while i_ < lenHay:
        CurrChar = HayStack[i_] 
        if CurrChar =="\"" or CurrChar == "'":
            return i_
        i_ = i_ + 1
    return -1
    

NumArgs = len(sys.argv)


if NumArgs < 2:
    print "Usage: ExtractHTMLDataFiles.py input.html\r\n"
    sys.exit(-1)

inF = sys.argv[1]

if os.path.exists(inF)== False or \
   os.path.getsize(inF) == 0:
    print "File does not exist or empty\r\n"
    sys.exit(-2)


fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()

if fCon.lower().find("data:")==-1:
    print "No embedded data was found\r\n"
    sys.exit(-3)


fCon_no_tab_space_lines = RemoveTabsSpacesNewLines(fCon)
fCon_stripped = fCon_no_tab_space_lines.rstrip().lstrip()
lenX = len(fCon_stripped)

XXxxXX = re.findall("data:((.*?)+);base64,",fCon_stripped,re.IGNORECASE)
if XXxxXX:
    NumBase64 = len(XXxxXX)
    if NumBase64 == 0:
        print "Found no embedded RFC 2397 files"
        sys.exit(0)
    else:
        print "Number of Base64-encoded embedded data files is " + str(NumBase64)
        for ixx in range(0,NumBase64):
            print "Type ==> (" + str(ixx+1) + "): " + XXxxXX[ixx][0]
            
    i = 0
    StartX = 0
    while i < NumBase64:
        if StartX < lenX:
            N = "data:" + XXxxXX[i][0] + ";base64,"
            Offset = fCon_stripped.lower().find(N,StartX)
            #print Offset
            if Offset == -1:
                print "Unexpected error"
                sys.exit(-4)
            Offset += len("data:" + XXxxXX[i][0] + ";base64,")
            End = FindFirstQuote(Offset,fCon_stripped)
            if End == -1:
                print "Unexpected error while trying to find end of Base64 string"
                sys.exit(-5)
            NewBase64 = fCon_stripped[Offset:End]
            #--------------------------------------
            #print NewBase64
            Base64Decoded = DecodeBase64(NewBase64)
            if Base64Decoded == "":
                print "Invalid Base64-encoded string"
            else:
                ext = ".bin"
                if (XXxxXX[ixx][0]).find("icon")!=-1:
                    ext = ".ico"
                elif (XXxxXX[ixx][0]).find("png")!=-1:
                    ext = ".png"
                fOut = open(str(i) + ext,"wb")
                fOut.write(Base64Decoded)
                fOut.close()
            #--------------------------------------
            StartX = End
        i = i + 1


