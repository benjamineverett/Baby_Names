import pandas as pd
import numpy as np
import pdb
import json

class Tune(object):
    def __init__(self):
        pass

        #pickle the files
    def _pickle_data(directory,extension_lst):
        peter_piper = Pickle()
        peter_piper.pickle_folder(directory, extension_lst)

    def to_csv(self):
        df = self.fetch_name_data()
        df.to_csv('results/{}_{}_{}.csv'.format(self.title,self.year_start,self.year_end))
        self.new_paragraph()
        print('Successfully ported to CSV titled: "{}_{}_{}.csv"'.format(self.title,self.year_start,self.year_end))
        self.new_paragraph()

    def column_names(self,num):
        if num == 1:
            return ['names','gender','num_occurences']
        if num == 2:
            return ['year','names','gender','num_occurences','rank']

    def create_new_df(self):
        cols = self.column_names(2)
        change_types = ['year','num_occurences','rank']
        df = pd.DataFrame(columns=cols)
        for col in change_types:
            df[col] = df[col].astype(np.int64)
        return df

    def get_years(self):
        return list(range(self.year_start, self.year_end + 1))

    def get_data(self,year):
        cols = self.column_names(1)
        filename = '/Users/benjaminreverett/Dropbox/5-Data/names/yob{}.txt'.format(year)
        df = pd.read_csv(filename, names=cols)
        df.insert(0,'year',year)
        df.insert(4, 'rank', [n for n in range(1,df.shape[0]+1)])
        return df



    def new_paragraph(self):
        print('\n')



class GetYearlyTotals(object):

    def __init__(self,year_start, year_end):
        self.year_start = year_start
        self.year_end = year_end
        self.totals = {}
        self.get_totals()

    def get_totals(self):
        totals = {}
        cols = ['names','gender','num_occurences']
        for year in list(range(self.year_start,self.year_end + 1)):
            filename = '/Users/benjaminreverett/Dropbox/5-Data/names/yob{}.txt'.format(year)
            df = pd.read_csv(filename, names=cols)
            df_M = df[df['gender'] == 'M']
            df_F = df[df['gender'] == 'F']
            totals[year] = {'F':df_F.iloc[:,2].sum(), 'M':df_M.iloc[:,2].sum(),'all':df.iloc[:,2].sum()}
        self.totals = totals
        json.dump(self.totals, open('/Users/benjaminreverett/Dropbox/Personal_Projects/Baby_Names/results/yearly_totals.txt', 'w'))
