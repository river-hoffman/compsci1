"""
    CSCI 141 Project
    Task 0
    file: indexTools.py
    author: River Hoffman (rhb4900@g.rit.edu)
"""

from rit_lib import *

class QuaterHPI(struct):
    _slots = ((int,"year"),(int,"qtr"),(float,"index"))

class AnnualHPI (struct):
    _slots = ((int,"year"),(float,"index"))

def read_state_house_price_data (filepath):
    """
        Returns a dictionary mapping state abbreviations to lists of QuarterHPI objects.
        For every state, there is exactly one list of QuarterHPI objects.
        It sends a warning message when a data value is unavailable.
        The message contains the text “data unavailable:”.
        Then it prints the line content.
    """
    newdict = {}
    for x in open(filepath):
        line = x.strip()
        line = line.split()
        if line[0] == '.' or line[1] == '.' or line[3] == '.' or line[2] == '.':
            print("data unavailable:")
            print(x)
        elif line[0] == 'state':
            pass
        elif line[0] in newdict:
            newdict[line[0]].append(QuaterHPI((int(line[1])),(int(line[2])),(float(line[3]))))
        else:
            newdict[line[0]] = [QuaterHPI((int(line[1])),(int(line[2])),(float(line[3])))]
    return newdict

def read_zip_house_price_data(filepath):
    """
        Returns a dictionary, like the previous function, mapping zip codes to lists of AnnualHPI objects.
        For every zip code, there is exactly one list of AnnualHPI objects.
        It's expected to print a count of lines read and lines uncounted due to unavailable or
        incomplete values.
    """
    dict2={}
    counted = 0
    uncounted = 0
    for z in open(filepath):
        line = z.strip()
        line = line.split()

        if line[0] == '.' or line[1] == '.' or line[3] == '.':
            uncounted +=1
        elif line[0] == "Five-Digit":
            pass
        elif line[0] in dict2:
            dict2[line[0]].append(AnnualHPI(int(line[1]),float(line[3])))
            counted+=1
        else:
            dict2[line[0]] = [AnnualHPI(int(line[1]),float(line[3]))]
            counted+=1
    print("count: " + str(counted) + " uncounted: " + str(uncounted))
    return dict2

def index_range(data,region):
    """
        The function takes a dictionary mapping regions to lists of *HPI objects and a region name. The
        objects may be either QuarterHPI or AnnualHPI objects.
        Will return a tuple of the minimum and maximum index values of the *HPI objects.
    """
    minindex= data[region][0]
    maxindex = data[region][0]
    for y in data[region]:
        if y.index < minindex.index:
            minindex = y
        elif y.index > maxindex.index:
            maxindex = y
    return (minindex, maxindex)

def print_range(data,region):
    """
        The function uses a dictionary mapping regions to lists of *HPI objects and a region name.
        It should not return anything, but it will print the low and high values (range) of the house price index for
        a specified region.
    """
    p = index_range(data,region)
    print("Region: " + region)
    if isinstance(p[0],AnnualHPI):
        print("Low: year/index: " + str(p[0].year) + " / "  + str(p[0].index))
        print("High: yearindex: " + str(p[1].year) + " / "  + str(p[1].index))
    else:
        print("Low: year/quarter/index: " + str(p[0].year) + " / " + str(p[0].qtr) + " / " + str(p[0].index))
        print("High: year/quarter/index: " + str(p[1].year) + " / " + str(p[1].qtr) + " / " + str(p[1].index))

def print_ranking(data, heading="Ranking"):
    """
        The function uses data, which is a sorted list of objects, and the heading is a text message whose
        default value is “Ranking”. It will produce a printed Table of the processed data.
    """
    print(heading)
    print("The Top 10: ")
    for n in range(0,10):
        print(str(n+1) + " : " + str(data[n]) )
    print("The Bottom 10: ")
    for m in range(len(data)-10,len(data)):
        print(str(m + 1) + " : " + str(data[m]))

def annualize(data):
    """
        The function uses a dictionary mapping regions to lists of QuarterHPI objects.
        It will return a dictionary mapping regions to lists of AnnualHPI objects.
        This function operates only on a dictionaries whose value type is list of QuarterHPI objects.
        It averages those objects to create the lists of AnnualHPI objects.

        *Since some quar- terly data may be unavailable, it averages whatever ones actually exist, whether that be one,
        two, three or four items per year.
    """
    dict3 = {}
    for x in data.keys():
        numqtr = 0
        sum = 0
        current = 0
        dict3[x] = []

        for b in data[x]:
            if b.year != current:
                if numqtr != 0:
                    dict3[x].append(AnnualHPI(current,sum/numqtr))
                sum = 0
                numqtr = 0
                current = b.year
            sum+= b.index
            numqtr+=1
        dict3[x].append(AnnualHPI(current, sum / numqtr))
    return dict3

if __name__ == '__main__':
    filepath = input("Enter house price index file: " )
    newlst= []
    annual = 0
    quarterly = 0
    if "ZIP" in filepath:
        annual = read_zip_house_price_data('data/' + filepath)
    else:
        quarterly = read_state_house_price_data('data/' + filepath)
    while True:
        next = input("Next region of interest( Hit ENTER to stop): ")
        if next == "":
            break
        else:
            newlst.append(next.strip())
    for h in newlst:
        print("=======================================================")
        if quarterly != 0:
            print_range(quarterly,h)
            annual = annualize(quarterly)
        print_range(annual,h)
        for u in annual[h]:
            print(u)