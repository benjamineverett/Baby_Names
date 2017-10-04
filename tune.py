from pickle_data import Pickle
import pandas as pd
import numpy as np

class Tune(object):
    def __init__(self):
        self.df = None
        self.filename = None
        pass

    def file_to_tune(self, filename):
        self.filename = filename
        print('\nGot the file. Lets tune it!\n')

    def create_column_names(self,column_names):
        '''
        Prepare DataFrame with relevent columns
        INPUT:
        column_names: columns to be inserted
        OUTPUT:
        pickled DataFrame with correct columns
        '''
        self.df = pd.read_pickle(self.filename)
        self.df.columns = column_names
        #clean up pickled file extensions
        self.filename = self.filename.replace('.txt','.pkl')
        self.df.to_pickle(self.filename)

    def add_columns(self):
        '''
        Add columns I think will be of interest
        INPUT: None
        OUTPUT:
        pickled DataFrame with additional columns
        '''
        #load DataFrame
        self.df = pd.read_pickle(self.filename)
        #add name rank out of total population
        self._add_total_rank()
        #add name rank for gender
        self._add_rank_for_gender()
        #add density of name for gender(NOT total population)
        self._add_density_of_name()
        #clean up name
        self.filename = self.filename.replace('.pkl.pkl', '.pkl')
        self.df.to_pickle(self.filename)

    def _add_total_rank(self):
        self.df.sort_values('num_occurences',ascending=False,inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        self.df.insert(self.df.shape[1], 'total_rank', self.df.index + 1)

    def _add_rank_for_gender(self):
        self.df.sort_values(['gender','num_occurences'], ascending=False, inplace=True)
        self.df.reset_index(inplace=True,drop=True)
        self.df.insert(self.df.shape[1], 'gender_rank', 0)
        self.df.loc[self.df['gender'] == 'M', 'gender_rank'] = self.df.index + 1
        M = self._get_number_of_names_for_gender()[1]
        self.df.loc[self.df['gender'] == 'F', 'gender_rank'] = self.df.index + 1

    def _get_total_num_for_gender(self):
        #total number female babies
        F = self.df.groupby('gender').sum().iloc[:,0][0]
        #total number male babies
        M = self.df.groupby('gender').sum().iloc[:,0][1]
        return F,M

    def _get_number_of_names_for_gender(self):
        #total number of female names
        F = self.df[self.df['gender']=='F'].count().iloc[0]
        #total number of male names
        M = self.df[self.df['gender']=='M'].count().iloc[0]
        return F,M

    def _add_density_of_name(self):
        #density of name out of gender(NOT total population)
        F,M = self._get_total_num_for_gender()
        self.df.insert(self.df.shape[1], 'name_density', 99)
        self.df.loc[self.df['gender']== 'M', 'name_density'] = self.df['num_occurences'] / M
        self.df.loc[self.df['gender']== 'F', 'name_density'] = self.df['num_occurences'] / F
