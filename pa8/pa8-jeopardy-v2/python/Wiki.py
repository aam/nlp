import sys, traceback
import re
from xml.dom.minidom import parse
import string
import collections
import xml

class Wiki:
    
    # reads in the list of wives
    def addWives(self, wivesFile):
        try:
            input = open(wivesFile)
            wives = input.readlines()
            input.close()
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            sys.exit(1)    
        return wives
    
    # read through the wikipedia file and attempts to extract the matching husbands. note that you will need to provide
    # two different implementations based upon the useInfoBox flag. 
    def processFile(self, f, wives, useInfoBox):
        
        husbands = [] 
        
        # TODO:
        # Process the wiki file and fill the husbands Array
        # +1 for correct Answer, 0 for no answer, -1 for wrong answers
        # add 'No Answer' string as the answer when you dont want to answer

        if useInfoBox:
            for wife in wives:
                husbands.append('No Answer')
            dom = parse(f)
            for t in dom.getElementsByTagName("text"):
                for c in t.childNodes:
                    if c.nodeType == c.TEXT_NODE:
                        s = c.data.encode("utf-8")
                        mName = re.search("\|\s*name\s*=\s*(.+)\n", s, re.IGNORECASE)
                        mSpouse = re.search("\|\s*spouse\s*=\s*(.*)\s*\n", s, re.IGNORECASE)

                        if mName <> None and mSpouse <> None:
                            if len(mName.groups()) > 0 and len(mSpouse.groups()) > 0:
                                husband = string.split(mName.group(1), "|")[0]
                                if husband.startswith("General "):
                                    husband = husband[len("General "):]
#                            wife = string.split(mSpouse.group(1), "|")[0].strip()
                                wife = mSpouse.group(1)
                                mSquareBrackets = re.search("\[\[([^\]]*)\]\]", wife)
                                if mSquareBrackets <> None and len (mSquareBrackets.groups()) > 0:
                                    wife = mSquareBrackets.group(1)
                                wife = string.split(wife, "(")[0].strip()
                                wife = re.sub("\"[^\"]*\" ", "", wife)
                                print "Looking for ", wife
                                for ndxQ, wifeQ in enumerate(wives):
                                    if wife.startswith(wifeQ.strip()):
                                        print husband, "-", wife, "-", ndxQ
#                                    ndxWife = mapWifeToIndex[wife] 
                                        ndxWife = ndxQ
                                        if ndxWife >= 0:
                                            husbands[ndxWife] = "Who is " + husband + "?"
        else:
            dom = parse(f)
            for wife in wives:
                found = False
                for eTitle in dom.getElementsByTagName("title"):
                    husband = eTitle.firstChild.nodeValue.encode("utf-8")
                    print "husband ", husband
                    parent = eTitle.parentNode
                    fulltext = parent.toxml().encode("utf-8")
                    if string.find(fulltext, wife.strip()) <> -1:
                        husbands.append("Who is " + husband + "?")
                        found = True
                        break
                if not found:
                    husbands.append("No Answer")
            
        f.close()
        print wives
        print husbands
        return husbands
    
    # scores the results based upon the aforementioned criteria
    def evaluateAnswers(self, useInfoBox, husbandsLines, goldFile):
        correct = 0
        wrong = 0
        noAnswers = 0
        score = 0 
        try:
            goldData = open(goldFile)
            goldLines = goldData.readlines()
            goldData.close()
            
            goldLength = len(goldLines)
            husbandsLength = len(husbandsLines)
            
            if goldLength != husbandsLength:
                print('Number of lines in husbands file should be same as number of wives!')
                sys.exit(1)
            for i in range(goldLength):
                if husbandsLines[i].strip() in set(goldLines[i].strip().split('|')):
                    correct += 1
                    score += 1
                elif husbandsLines[i].strip() == 'No Answer':
                    noAnswers += 1
                else:
                    wrong += 1
                    score -= 1
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
        if useInfoBox:
            print('Using Info Box...')
        else:
            print('No Info Box...')
        print('Correct Answers: ' + str(correct))
        print('No Answers: ' + str(noAnswers))
        print('Wrong Answers: ' + str(wrong))
        print('Total Score: ' + str(score)) 

if __name__ == '__main__':
    wikiFile = '../data/small-wiki.xml'
    wivesFile = '../data/wives.txt'
    goldFile = '../data/gold.txt'
    useInfoBox = False;
    wiki = Wiki()
    wives = wiki.addWives(wivesFile)
    husbands = wiki.processFile(open(wikiFile), wives, useInfoBox)
    wiki.evaluateAnswers(useInfoBox, husbands, goldFile)
