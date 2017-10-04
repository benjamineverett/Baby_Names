from tune import Tune
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pdb

class Analyze(object):
    def __init__(self, year):
        self.year = year
        self.df = self._get_data_for_year()
        self.fig = None
        self.ax = None

    def get_totals_for_specific_subset_of_rank(self,rank_st,rank_end):
        '''
        Get total number of babies from <year>.pkl files pertaining to a specific name rank
            e.g. Return total sum of babies ranked with names that ranked 10-15 for the year
        INPUT:
        rank_st: int of rank for where to begin search
        rank_end: int of rank for where to end search (inclusive)
        OUTPUT:
        total sum of babies with specific name rank
        '''
        df = self.df[(self.df['total_rank']>=rank_st) & (self.df['total_rank']<=rank_end)]
        return df['num_occurences'].sum()

    def get_density(self):
        '''
        INPUT: None. Called by other functions
        OUTPUT: get the density of names for entire population
            e.g. number of names / number of babies
        '''
        F = self.get_number_of_names()[0] / self.get_number_of_babies()[0]
        M = self.get_number_of_names()[1] / self.get_number_of_babies()[1]
        Total = self.get_number_of_names()[2] / self.get_number_of_babies()[2]
        return F,M,Total

    def get_number_of_names(self):
        '''
        INPUT: None, calls self.df
        OUTPUT: Counts of the number of names by gender
            F = female
            M = male
            Total = total names
        '''
        #total number of female names
        F = self.df[self.df['gender']=='F'].shape[0]
        #total number of male names
        M = self.df[self.df['gender']=='M'].shape[0]
        #total number of names
        Total = F+M
        return F,M,Total

    def get_number_of_babies(self):
        '''
        INPUT: None, calls self.df
        OUTPUT: Number of babies born by gender
            F = female
            M = male
            Total = total babies
        '''
        #total number female babies
        F = self.df[self.df['gender']=='F'].sum()[2]
        #total number male babies
        M = self.df[self.df['gender']=='M'].sum()[2]
        #total number of babies
        Total = F+M
        return F,M,Total

    def get_name_data(self,names):
        '''
        INPUT:
        names = names and gender (dict)
                e.g. {'John','M'}
        OUTPUT: pandas DataFrame of of requested name
        '''
        new_df = pd.DataFrame()
        for name, gender in names.items():
            new_df = pd.concat([new_df,self.df[(self.df['names'] == name) & (self.df['gender']==gender)]],axis=0)
        return(new_df)

    def initialize_plot(self,fig_size=(15,8)):
        '''
        INPUT:
        fig_size = figure size, default set to (15,8)
        OUTPUT:
        Initialized plot
        '''
        self.fig = plt.figure(figsize=fig_size)
        self._respect()

    def plot(self,xaxis,yaxis,line_name='Insert Line Name',xlabel='Insert xlabel',ylabel='Insert ylabel',
            axes=(111),xlims=(0,10),ylims=(0,10),color=None):
        '''
        INPUT:
        Only following two required:
            xaxis = x values
            yaxis = y values
        OUPUT:
        Plots onto axes
        '''
        ax = self.fig.add_subplot(axes)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        ax.plot(xaxis,yaxis,label=line_name,color=color)

    def show_plot(self,plot_title='Insert Plot Title',save_fig=False):
        '''
        INPUT:
        plot_title = Title for figure
        save_fig = Set to false, insert title as string to save as title
        '''
        plt.title(plot_title)
        plt.legend()
        if save_fig:
            plt.savefig('{}.png'.format(save_fig))
        return plt.show()

    '''
    All hidden functions below
    '''
    def _get_data_for_year(self):
        '''
        INPUT: Initialized at instantiation
        OUTPUT: Pandas Data Frame of year = year
        '''
        return pd.read_pickle('Data/names/yob{}.pkl'.format(self.year))

    def _respect(self):
        mpl.rcParams.update({
            'font.size'           : 16.0,
            'axes.titlesize'      : 'large',
            'axes.labelsize'      : 'medium',
            'xtick.labelsize'     : 'small',
            'ytick.labelsize'     : 'small',
            'legend.fontsize'     : 'small',
        })

class Bayes(object):
    # Bayes:
    # P(A|B) = P(B|A)*P(A) / P(B)
    #
    # P(A|B) -> Posterior
    # P(B|A) -> Likelihood
    # P(A) -> Prior
    # P(B) -> Normalizing constant
    #
    # Given it is year 2011 what is probabily Kit is baby name?

    #P(Name|Year) = P(Year|Name)*P(Name) / P(Year)

    #P(Year) = P()


    '''
    INPUT:
        prior (dict): key is the value (e.g. 4-sided die),
                      value is the probability

        likelihood_func (function): takes a new piece of data and the value and
                                    outputs the likelihood of getting that data
    '''
    def __init__(self, prior, likelihood_func):
        self.prior = prior
        self.likelihood_func = likelihood_func

    def normalize(self):
        '''
        INPUT: None
        OUTPUT: None

        Makes the sum of the probabilities equal 1.
        '''
        total = float(sum(self.prior.values()))
        for key in self.prior:
            self.prior[key] /= total

    def update(self, data):
        '''
        INPUT:
            data (int or str): A single observation (data point)

        OUTPUT: None

        Conduct a bayesian update. Multiply the prior by the likelihood and
        make this the new prior.
        '''
        for key in self.prior:
            self.prior[key] *= self.likelihood_func(data, key)
        self.normalize()

    def print_distribution(self):
        '''
        Print the current posterior probability.
        '''
        sorted_keys = sorted(self.prior.keys())
        for key in sorted_keys:
            print("{}:{}".format(str(key), str(self.prior[key])))

class GetYearlyTotals(object):

    def __init__(self,year_start, year_end):
        self.year_start = year_start
        self.year_end = year_end
        self.info_dict = {}
        self.names_dict = {}
        self.years = list(range(self.year_start,self.year_end+1))
        self.names = None
        self.fig = None

    def get_name_data(self,names_dict):
        info_dict = {}
        for year in self.years:
            for name, gender in names_dict.items():
                if year in info_dict:
                    info_dict[year].update(self._fetch_name_data_for_year(name,gender,year))
                else:
                    info_dict[year]=self._fetch_name_data_for_year(name,gender,year)
        self.info_dict = info_dict
        self.names = list(names_dict.keys())

    def _fetch_name_data_for_year(self,name,gender,year):
        df = self._get_pickle_for_names(year)
        # return {name:list(df[(df['names']==name) & (df['gender']==gender)])}
        try:
            df[(df['names']==name) & (df['gender']==gender)].iloc[0,2:]
        except IndexError:
            return {name:[9999,9999,9999,9999,9999,9999]}
        else:
            return {name:list(df[(df['names']==name) & (df['gender']==gender)].iloc[0,2:])}

    def plot_name_rank(self,plot_title,save_fig=False):
        self._initialize_plot()
        for name in self.names:
            rank_info = self._fetch_name_rank(name)
            self._fetch_plot(xaxis=self.years, yaxis=rank_info,line_name=name,xlims=(self.year_start,self.year_end),ylims=(0,1000),xlabel="Year",ylabel='Rank')
        self._show_plot(plot_title=plot_title,save_fig=save_fig)

    def _fetch_name_rank(self,name):
        return [self.info_dict[year][name][2] for year in self.years]

    def _fetch_plot(self,xaxis,yaxis,line_name='Insert Line Name',xlabel='Insert xlabel',ylabel='Insert ylabel',
            axes=(111),xlims=(0,10),ylims=(0,10)):
        '''
        INPUT:
        Only following two required:
            xaxis = x values
            yaxis = y values
        OUPUT:
        Plots onto axes
        '''
        ax = self.fig.add_subplot(axes)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        ax.plot(xaxis,yaxis,label=line_name)
        sns.set()

    def _show_plot(self,plot_title='Insert Plot Title',save_fig=False):
        '''
        INPUT:
        plot_title = Title for figure
        save_fig = Set to false, insert title as string to save as title
        '''
        plt.style.use('ggplot')
        plt.title(plot_title)
        plt.legend()
        plt.gca().invert_yaxis()
        if save_fig:
            plt.savefig('{}.png'.format(save_fig))
        return plt.show()

    def _initialize_plot(self,fig_size=(15,8)):
        '''
        INPUT:
        fig_size = figure size, default set to (15,8)
        OUTPUT:
        Initialized plot
        '''
        self.fig = plt.figure(figsize=fig_size)
        self._respect()

    def _respect(self):
        mpl.rcParams.update({
            'font.size'           : 16.0,
            'axes.titlesize'      : 'large',
            'axes.labelsize'      : 'medium',
            'xtick.labelsize'     : 'small',
            'ytick.labelsize'     : 'small',
            'legend.fontsize'     : 'small',
        })

    def _get_pickle_for_names(self,year):
        return pd.read_pickle('/Users/benjaminreverett/Dropbox/Personal_Projects/Baby_Names/Data/names/yob{}.pkl'.format(year))

if __name__ == "__main__":
    # d2000 = Analyze(2000)
    # new_df = d2000.get_name_data({'Kit':'M', 'Emilia':'F', 'Benjamin': 'M'})
    # d2000.initialize_plot()
    # d2000.plot(xaxis=[1,2,3,4],yaxis=[4,8,12,16])
    # d2000.show_plot()
    d2016 = GetYearlyTotals(1915,2015)
    # print(d2016._fetch_name_data_for_year(year=1900,name='Taryn',gender='F'))
    # d2016.get_name_data({'Frank':'M','Taryn':'F', 'Adam': 'M', 'John':'M'})
    # d2016.plot_name_rank('Cohort Instructors')
    d2016.get_name_data({'':''})
    d2016.plot_name_rank('')
