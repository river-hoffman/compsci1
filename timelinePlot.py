"""
    CSCI 141 Project
    Task 4
    file: timelinePlot.py
    author: River Hoffman (rhb4900@g.rit.edu)
"""

import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
from indexTools import *

def build_plottable_array(xyears, regiondata):
    """
     For the Parameters:
        xyears is a list of integer year values, and regiondata is a list of AnnualHPI
        objects.

    Returns:
        An array suitable for plotting with the matplotlib module.
        The build_plottable_array function exists because the available dataset may have gaps or
        holes in its available data.
    """
    newmask = ma.masked_all(len(xyears))
    counter = 0
    for i in range(len(xyears)):
        if xyears[i] == regiondata[counter].year:
            newmask[i] = regiondata[counter].index
            counter+=1
    return  newmask

def filter_years(data, year0, year1):
    """
     For the Parameters:
        When given a dataset and a pair of years (earlier, then later),
        the filter_years function filters the AnnualHPI values for all regions so that each list of values contains data
         for only the span of the given years.

    Returns:
        A dictionary mapping regions to lists of HPI values that are within the year0 to year1 inclusive range.
        Each list of HPI values is sorted in ascending order by year.
    """
    for k in data:
        newlst= []
        for m in data[k]:
            if year0 <= m.year and m.year  <= year1:
                newlst.append(m)
        data[k] = newlst
    return data

def find_years(data):
    year0 = -1
    year1 = -1
    for y in data:
        if data[y] != []:
            if year0 ==-1:
                year0 = data[y][0].year
                year1 = data[y][-1].year
            if data[y][0].year <= year0:
                year0 = data[y][0].year
            if data[y][-1].year >= year1:
                year1 = data[y][-1].year
    return (year0,year1)

def plot_HPI(data, regionList):
    """
         For the Parameters:
            data is a dictionary mapping a state or zip code to a list of AnnualHPI objects.
            regionList is a list of key values whose type isstring.

        Prints:
            The plot_HPI function plots a timeline from point to point over
            the time period of the data.
    """
    plt.figure()
    x, y = find_years(data)
    plt.title('Home Price Indies:' + str(x) + '-' + str(y))
    tmplst=[]
    lst = [i for i in range(x,y+1)]
    for o in regionList:
        b=build_plottable_array(lst, data[o])
        tmplst.append(b)
        plt.plot(lst, b,marker='*',linestyle= "-")
    plt.legend(regionList,loc=2)
    plt.show()

def plot_whiskers(data, regionList):
    """
         For the Parameters:
            data is a dictionary mapping a state or zip code to a list of AnnualHPI objects.
            regionList is a list of key values whose type isstring.

        Prints:
            The whiskers plotted output is found in the accompanying file of
            graph outputs.
    """
    dc = dict(marker ='D', markeredgecolor='black',markerfacecolor='red')
    plt.figure()
    x, y = find_years(data)
    plt.title('Home Price Index Comparison. Median is a line. Mean is a diamond.')
    tmplst = []
    lst = [i for i in range(x, y + 1)]
    for o in regionList:
        b = build_plottable_array(lst, data[o])
        tmplst.append(b.compressed())
    plt.boxplot(tmplst,0,meanprops=dc,meanline=False,showmeans=True,labels=regionList)
    plt.show()

def main():
    filepath = input("Enter house price index filename: ")
    year0 = int(input("Enter the start year of the range to plot: "))
    year1 = int(input("Enter the end year of the range to plot: "))

    annual = 0
    quarterly = 0
    regionList=[]

    while True:
        next = input("Enter next region for plots (<ENTER> to stop): ")
        if next == "":
            break
        else:
            regionList.append(next.strip())
    if "ZIP" in filepath:
        annual = read_zip_house_price_data('data/' + filepath)
    else:
        quarterly = read_state_house_price_data('data/' + filepath)
        for r in regionList:
            print_range(quarterly, r)
        annual = annualize(quarterly)


    annual = filter_years(annual, year0, year1)
    print('Close display window to continue')
    plot_HPI(annual,regionList)
    print('Close display window to continue')
    plot_whiskers(annual,regionList)

if __name__ == '__main__':
    main()
