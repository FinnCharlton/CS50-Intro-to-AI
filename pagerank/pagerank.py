import os
import random
import re
import sys
from itertools import groupby

DAMPING = 0.85
SAMPLES = 100000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #Initialise variables
    dampingP = round((1-damping_factor)/len(corpus),4)
    nextPageP = {}
    linkCount = len(corpus[page])

    #Loop through corpus, calculating probability
    for pg in corpus.keys():

        #P is at least dampingP
        pgP = dampingP

        #If current page is in links of target page, add probability to dampingP
        if pg in list(corpus[page]):
            pgP += damping_factor/linkCount
        
        #If target page links to nothing, assign equal probability to each other page
        elif len(list(corpus[page])) == 0:
            pgP = 1/len(corpus)

        #Add target page to dictionary
        nextPageP.update({pg:pgP})

    #Return dictionary
    return nextPageP


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Initialise variables
    i=0
    visitedPages = []

    #Find first page randomly and add to list:
    currentPage = random.choice(list(corpus.keys()))
    visitedPages.append(currentPage)

    #Loop through pages, adding random page choice to list
    while i<n:

        #Run transition model to return probablility distribution for next page
        pDistribution = transition_model(corpus,currentPage,DAMPING)

        #Parse distribution in sample and weight lists
        pageList = [x for x in pDistribution.keys()]
        weightList = [x for x in pDistribution.values()]

        #Generate next random page, and add to visited pages list
        currentPage = random.choices(pageList,weightList)[0]
        visitedPages.append(currentPage)

        #Increment i
        i += 1

    #Calculate PageRank from visited pages list
    groupedPages = groupby(sorted(visitedPages))
    pageRanks = {element: len(list(group))/len(visitedPages) for element, group in groupedPages}

    return pageRanks

class Page():
    def __init__(self,pageName,linkList,corpus):
        self.pageName = pageName
        self.linkList = linkList
        self.linkList = linkList
        self.pageRank = 1 / len(corpus)
        #If linkList variable is empty, add one for each page in corpus.
        if len(linkList) == 0:
            for pg in corpus.keys():
                self.linkList.append(pg)

    def updatePageRank(self,corpus,pageList,damping_factor):

        #Calculate sum of pageRank modifiers over i
        self.sum = 0
        for page in pageList:
            self.sum += (page.pageRank/len(page.linkList))
        
        #Set new pageRank
        self.pageRank = ((1-damping_factor)/len(corpus))+(damping_factor*self.sum)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Create list of Page classes
    corpusPageList = []
    for key, value in corpus.items():
        newPage = Page(pageName=key,linkList=list(value),corpus=corpus)
        corpusPageList.append(newPage)

    #Iterate through Pages, updating Page Ranks. Break if checker = True
    checker = False
    while not checker:
        for targetPage in corpusPageList:

            #Set checker to True and record old pageRank
            checker=True
            oldPR = targetPage.pageRank

            #Initalise list of linked pages for pageRank calculation
            listOfLinkedPages = []

            #Iterate through pages again to look for link to the target page
            for checkPage in corpusPageList:
                if targetPage.pageName in checkPage.linkList:

                    #If link is found, add page to list of linked pages
                    listOfLinkedPages.append(checkPage)

            #Call the updatePageRank function with the list of linked pages
            targetPage.updatePageRank(corpus,listOfLinkedPages,damping_factor)

            #Record new pageRank. If difference is more than 0.001, set checker to False
            newPR = targetPage.pageRank
            if abs(oldPR-newPR) > 0.001:
                checker = False

    #Parse finished list of Page objects into pageRank dictionary
    outputDict = {}
    for page in corpusPageList:
        outputDict[page.pageName] = page.pageRank

    return outputDict

if __name__ == "__main__":
    main()
