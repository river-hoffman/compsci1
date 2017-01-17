"""
    CSCI 141 Project
    Task 2
    file: trending.py
    author: River Hoffman (rhb4900@g.rit.edu)
"""
from indexTools import *

def cagr(idxlist, periods):
    """
        For the Parameters:
            The idxlist is a 2-item list of [HPI0, HPI1], where HPI0 is the index value of the earlier period.
            The periods is the number (N ) of periods (years) between the two HPI values in the list.
        Returns:
            A float representing the compound annual growth rate, CAGR,
            of the index values in the list for the specified period.
            The CAGR value is a floating point number whose formula is this: ((index1/index0)1/N − 1) ∗ 100.
    """
    quotient =(idxlist[1]/idxlist[0])
    return((quotient**(1/periods))-1)*100

def slst(lst):
    return lst[1]

def calculate_trends(data, year0, year1):
    """
        For the Parameters:
            The data is a dictionary from region to a list of AnnualHPI.
            The year0 and year1 specify the periods of interest.
            The year0 is the starting year, year1 is the ending year, and the pre-condition is year0 < year1.

        Returns:
            A list of (region, rate) tuples sorted in descending order by the compound annual growth rate.
            The rate is the compound annual, year-to-year rate of change between the given year0 and the given year1 values.
            If a region lacks an entry for either the year0 or year1, calculate_trends should ignore that region and not include it.
    """
    firstlst = []
    for ctrends in data:
        templst = [0,0]
        for annualh in data[ctrends]:
            if annualh.year == year0:
                templst[0] = annualh.index
            elif annualh.year == year1:
                templst[1] = annualh.index
        if templst[0] != 0 and templst[1] != 0:
            firstlst.append((ctrends,cagr(templst,year1-year0)))
    firstlst.sort(key=slst, reverse=True)
    return firstlst

def main():
    filepath = input("Enter house price index filename: ")
    year0 = int(input('Enter start year of interest: '))
    year1 = int(input('Enter ending year of interest: '))
    if 'state' in filepath:
        oen = read_state_house_price_data('data/' + filepath)
        annual = annualize(oen)
    elif 'ZIP' in filepath:
        annual = read_zip_house_price_data('data/' + filepath)
    else:
        print('Not vaild file name')
        return
    annual = calculate_trends(annual,year0,year1)
    print_ranking(annual, heading=str(year0) + '-' + str(year1) + 'Compound Annual Growth Rate')

if __name__ == '__main__':
    main()