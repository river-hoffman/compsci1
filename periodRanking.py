"""
    CSCI 141 Project
    Task 1
    file: periodRanking.py
    author: River Hoffman (rhb4900@g.rit.edu)
"""
from indexTools import *

def slst(lst):
    return lst[1]

def quarter_data(data, year, qtr):
    """
        For the Parameters:
            The data is a dictionary mapping a state region to a list of QuarterHPI instances
            The year is the year of interest
            The qtr is the quarter of interest, expressed as an integer between 1 and 4.
        Returns:
            A list of (region, HPI) tuples sorted from high value HPI to low value HP
    """
    lst = []
    for x in data:
        for l in data[x]:
           if l.year == year and l.qtr == qtr:
               lst.append((x,l.index))
    lst.sort(key= slst, reverse=True)
    return lst

def annual_data(data, year):
    """
        For the Parameters:
            The data is a dictionary mapping a state or zip code to a list of AnnualHPI objects
            The year is the year of interest.
        Returns:
            A list of (region, HPI) tuples sorted from high value HPI to low value HPI.
    """
    lst = []
    for x in data:
        for l in data[x]:
            if l.year == year:
                lst.append((x, l.index))
    lst.sort(key=slst, reverse=True)
    return lst
def main():
    filepath = input("Enter region-based house price index filename: ")
    year = int(input('Enter year of interest for house prices: '))

    if 'state' in filepath:
        oen = read_state_house_price_data('data/' + filepath)
        annual = annualize(oen)
    elif 'ZIP' in filepath:
        annual = read_zip_house_price_data('data/' + filepath)
    else:
        print('Not vaild file name')
        return
    annual = annual_data(annual,year)
    print_ranking(annual,heading= str(year) + 'Annual Ranking')

if __name__ == '__main__':
    main()

