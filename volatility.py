"""
    CSCI 141 Project
    Task 3
    file: volatility.py
    author: River Hoffman (rhb4900@g.rit.edu)
"""
from indexTools import *

def average(nums):
    """
       For the Parameters:
           A list of float values to average together.
       Returns:
           A float representing the average value of the given numeric dataset.
    """
    sum = 0
    for x in nums:
        sum += x
    return sum/len(nums)

def deviation_squared(nums, avg):
    """
       For the Parameters:
           The nums is a list of numeric values, and the avg is the average of those values.
       Returns:
           An array of float values representing the square of the deviations of the data from
           the data average.
    """
    sum= 0
    for x in nums:
        sum += (x - avg)**2
    return sum/len(nums)

def slst(lst):
    return lst[1]

def measure_volatility(data):
    """
       For the Parameters:
           The data is a dictionary from region to list of AnnualHPI values.
       Returns:
           A list of (region, standard_deviation) tuples sorted from high value to low value.
           The measure_volatility function computes standard deviations using these values as the measure of volatility
           The calculation steps are as follows to compute the measure:
               Calculate the average index for the number of observations.
               Determine each period’s deviation.
               Square each period’s deviation.
               Sum the squares of the deviations.
               Divide this sum by the number of observations.
               The standard deviation, (stdev) is the square root of that number.
   """
    returnlst= []
    for m in data:
        templst=[]
        for n in data[m]:
            templst.append(n.index)
        aver= average(templst)
        devi=deviation_squared(templst,aver)
        devi = (devi)**.5
        returnlst.append((m,devi))
    returnlst.sort(key=slst, reverse=True)
    return returnlst

def main():
    filepath = input("Enter region-based house price index filename: ")
    data = input('Enter the region of interest: ')

    if 'state' in filepath:
        oen = read_state_house_price_data('data/' + filepath)
        annual = annualize(oen)
    elif 'ZIP' in filepath:
        annual = read_zip_house_price_data('data/' + filepath)
    else:
        print('Not vaild file name')
        return
    annual = measure_volatility(annual)
    print_ranking(annual, heading='Annualized Price Standard Deviation, High to Low')

    print('Note: Absence of data can increase the apparent variation.')
    for y in annual:
        if y[0] == data:
            print('Standard deviation for ' + data + ' is ' + str(y[1]))

if __name__ == '__main__':
    main()