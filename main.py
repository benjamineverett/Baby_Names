import pandas as pd
import numpy as np
from data_scrubbing import Scrub
from data_scrubbing import GetYearlyTotals
import pdb
from plot_names import PlotNames
from analysis import Analysis

def stored_names(dict_name):
    name_dicts= {
        'everetts': {'Claude': 'M',
                    'Doris': 'F',
                    'Timothy': 'M',
                    'Leah': 'F',
                    'Claudia': 'F',
                    'Benjamin': 'M',
                    'Meredith': 'F',
                    'Nathaniel': 'M',
                    'Micah': 'M'},
        'baby_names': {'Griffin': 'M',
                    'Sasha': 'M',
                    'Sasha': 'F',
                    'Roy': 'M',
                    'Alexander': 'M',
                    'Alexandra': 'F',
                    'Pepper': 'F',
                    'Magdalena': 'F',
                    'Claude': 'M',
                    'Thomas': 'M'},
        'got_names':{'Peter': 'M',
                    'Tyrion': 'M',
                    'Lena': 'F',
                    'Cersei': 'F',
                    'Emilia': 'F',
                    'Daenerys': 'F',
                    'Kit': 'M',
                    'Jonathan': 'M',
                    'Sophie': 'F',
                    'Sansa': 'F',
                    'Maisie': 'F',
                    'Arya': 'F',
                    'Nikolaj': 'M',
                    'Jaime': 'M'},
        'beckers': {'Thomas': 'M',
                    'Rebecca': 'F',
                    'Katie': 'F',
                    'Eliza': 'F',
                    'Hannah': 'F',
                    'William': 'M',
                    'Magdalena': 'F'},
        'inlaws': {'Jennifer': 'F',
                    'Jerel': 'M',
                    'Michael': 'M',
                    'Katie': 'F',
                    'Timothy': 'M'},
        'leah_requested': {'Linda': 'F',
                    'Donna': 'F',
                    'Bruce': 'M',
                    'Robert': 'M',
                    'William': 'M'},
        'jonas': {'Jonas': 'M',
                    'Meredith': 'M'},
        'martin': {'Martin': 'M'}
                }

    return name_dicts[dict_name]

def scrubbing():
    # beckers = Scrub('beckers',1880,2016, stored_names('beckers'))
    inlaws = Scrub('everett_inlaws',1880,2016, stored_names('inlaws'))

def everett_parents():
    db = 'Everetts_1880_2016.csv'
    parents = ['Claude', 'Doris']
    testing3 = PlotNames(db, parents, set_the_limits=(1000,0), title='Mom & Dad')
    testing3.show_plot(savefig=True, title='everett_parents')

def everett_boys():
    db = 'Everetts_1880_2016.csv'
    boys = ['Timothy','Benjamin','Nathaniel','Micah']
    testing2 = PlotNames(db, boys, set_the_limits=(1000,0), title='The Boys')
    testing2.show_plot(savefig=True, title='everett_boys')

def everett_girls():
    db = 'Everetts_1880_2016.csv'
    girls = ['Leah','Claudia','Meredith']
    testing = PlotNames(db, girls, set_the_limits=(1000,0), title='The Girls')
    testing.show_plot(savefig=True, title='everett_girls')

def inlaws():
    names = ['Jennifer','Jerel','Michael','Katie','Timothy']
    db = 'everett_inlaws_1880_2016.csv'
    testing = PlotNames(db, names, set_the_limits=(1000,0),title='Inlaws')
    testing.show_plot(savefig=True, title='Inlaws')

def becker_sibs():
    sibs = ['Katie', 'Eliza', 'Hannah', 'William', 'Magdalena']
    db = 'beckers_1880_2016.csv'
    testing = PlotNames(db, sibs, set_the_limits=(1000,0),title='Sibbys')
    testing.show_plot(savefig=True, title='becker_sibs')

def becker_parents():
    parents = ['Thomas', 'Rebecca']
    db = 'beckers_1880_2016.csv'
    testing2 = PlotNames(db, parents, set_the_limits=(1000,0),title='Mom & Pops')
    testing2.show_plot(savefig=True,title='becker_parents')

def leah_request():
    # requested = Scrub('requested',1880,2016, stored_names('leah_requested'))
    db = 'requested_1880_2016.csv'
    names = list(stored_names('leah_requested').keys())
    plot = PlotNames(db, names, set_the_limits=(1000,0),title="Leah's Request")
    plot.show_plot(savefig=True,title="Leah_Request")

def jonas():
    jonas = Scrub('jonas',1880,2016,stored_names('jonas'))
    db = 'jonas_1880_2016.csv'
    plot = PlotNames(db, ['Jonas', 'Meredith'], set_the_limits=(1000,0),title="Jonas")
    plot.show_plot(title="Jonas")

def got_names():
    GOT = Scrub('GOT',1880,2016,stored_names('got_names'))

def martin():
    martin = Scrub('martin',1880,2016,stored_names('martin'))
    db = 'martin_1880_2016.csv'
    plot = PlotNames(db, ['Martin'], set_the_limits=(1000,0),title="Martin")
    plot.show_plot(title="Marty")

def test_yearly_totals():
    yr_totals = GetYearlyTotals(1880,2016)
    print(yr_totals.totals)

def test_get_yearly_totals_of_all_names():
    testing = Analysis('/Users/benjaminreverett/Dropbox/Personal_Projects/Baby_Names/results/GOT_1880_2016.csv')
    # testing.describe()
    testing.get_density('Emilia')

if __name__ == '__main__':
    test_get_yearly_totals_of_all_names()
    # test_save_totals()
    # test_yearly_totals()
    # martin()
    # everett_parents()
    # everett_boys()
    # everett_girls()
    # inlaws()
    # becker_sibs()
    # becker_parents()
    # leah_request()
    # jonas()
    # got_names()
