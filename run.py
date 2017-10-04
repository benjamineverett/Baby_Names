from tune import Tune
import os
import pandas as pd
from analysis_plotting import Analyze
import numpy as np
import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import pdb

#initialize figure with better font sizes
def _initialize_figure():
    #Respect
    mpl.rcParams.update({
        'font.size'           : 16.0,
        'axes.titlesize'      : 'large',
        'axes.labelsize'      : 'medium',
        'xtick.labelsize'     : 'small',
        'ytick.labelsize'     : 'small',
        'legend.fontsize'     : 'small',
    })
    fig = plt.figure(figsize=(15,8))
#pickle the files
def pickle_data(self, directory,extension_lst):
    '''
    Pickle the files to allow faster access
    INPUT:
    directory: directory of files to pickle
    extension_lst: extensions which to pickle
    OUTPUT:
    pickled files saved in directory
    '''
    peter_piper = Pickle()
    peter_piper.pickle_folder(directory, extension_lst)
#insert columns for original data
def tune_all_years_with_column_names():
    cols = ['names','gender','num_occurences']
    for year in range(1880,2014):
        Baby = Tune()
        Baby.file_to_tune('Data/names/yob{}.txt.pkl'.format(year))
        Baby.create_column_names(cols)
    print("You're tuned baby!")
#insert total_rank,gender_rank,name_density
def tune_all_years_with_added_columns():
    for year in range(1880,2014):
        Baby = Tune()
        Baby.file_to_tune('Data/names/yob{}.pkl.pkl'.format(year))
        Baby.add_columns()
    print("You're tuned baby!")
#create graph of density of names
def density_for_years(yr_start,yr_end):
    years = list(range(yr_start,yr_end+1))
    lst = []
    for year in years:
        Data = Analyze(year)
        F,M,Total = Data.get_density()
        lst.append([year,F,M,Total])
    df = pd.DataFrame(data=lst,columns=['Year','F', 'M', 'Total'])
    return df
def unique_names_for_year(yr_start,yr_end):
    years = list(range(yr_start,yr_end+1))
    lst = []
    for year in years:
        Data = Analyze(year)
        #obtains tuple of births - F,M,Total
        F_names,M_names,T_names = Data.get_number_of_names()
        F_babies,M_babies,T_babies = Data.get_number_of_babies()
        lst.append([year,F_names,M_names,T_names, F_babies, M_babies, T_babies])
    df = pd.DataFrame(data=lst,columns=['Year','F_names','M_names','T_names', 'F_babies', 'M_babies', 'T_babies'])
    return df

def get_total_of_top_names_for_each_year(yr_start,yr_end,rank_st,rank_end):
    years = list(range(yr_start,yr_end+1))
    lst = []
    for year in years:
        Data = Analyze(year)
        #obtain sum of top 10 names
        lst.append([year, Data.get_totals_for_specific_subset_of_rank(rank_st,rank_end)])
    df = pd.DataFrame(data=lst,columns=['Year','top_10'.format(rank_end)])
    return df



def create_pickled_df(yr_start,yr_end,filename):
    df = unique_names_for_year(yr_start, yr_end)
    df.to_pickle('{}.pkl'.format(filename))
    print('Data successfully pickled')


def births_for_years(yr_start,yr_end):
    years = range(yr_start,yr_end+1)
    pop_dict = {}
    for year in years:
        Data = Analyze(year)
        #obtains tuple of births - F,M,Total
        pop_dict[year] = (Data.total_babies_F(),Data.total_babies_M(),Data.total_babies_ALL())
    return pop_dict

def plot_density(yr_start,yr_end):
    '''
    INPUT:
    yr_start = year to start analysis
    yr_end = year to end analysis(analysis is inclusive)
    OUTPUT:
    Number of babies per each unique name
    '''
    fig = plt.figure(figsize=(15,8))
    sns.set_style('darkgrid')
    yrs_dict = density_for_years(yr_start,yr_end)

    x = []
    y = []
    for year, density in yrs_dict.items():
        x.append(year), y.append(1/density[2])
    x = np.array(x)
    y = np.array(y)
    ax = fig.add_subplot(111)
    ax.plot(x,y)
    ax.invert_yaxis()
    ax.set_ylabel('Number of Babies')
    ax.set_xlabel('Year')
    ax.set_title('number of babies per unique name')
    plt.show()

def bar_plot_1(yr_start,yr_end):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(15, 8))
    df = pd.read_pickle('name_data.pkl')
    df = df[(df['Year']>=yr_start) & (df['Year']<=yr_end)]
    # Plot the total babies born
    sns.set_color_codes("pastel")
    sns.barplot(y=df['F_babies']/1000000, x=df['Year'],label="total births\n(1,000,000s)", color="b", ax=ax)
    # Plot the total number of names
    sns.set_color_codes("muted")
    sns.pointplot(y=df['F_names']/10000, x=df['Year'],label="unique names\n(10,000s)",color="b", ax=ax)

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="upper right", frameon=True)
    #turn x-axis lines off
    ax.grid('off', axis='x')
    #set x-ticks to every ten years
    ax.set_xticklabels([yr if yr%10==0 else '' for yr in list(range(yr_start,yr_end+1))],rotation=45)
    ax.set(ylabel="",
           xlabel=""
           )
    # ax.set_title('Growth of unique names in the United States\n| 1920 - 2016 |')
    sns.despine(left=True, bottom=True)
    # plt.savefig('Growth of unique names in the United States')
    plt.show()

def bar_plot_2(yr_start,yr_end):
    df_top_10 = get_total_of_top_names_for_each_year(yr_start,yr_end,1,10)
    sns.set(style="whitegrid")
    # pdb.set_trace()
    fig, ax = plt.subplots(figsize=(15, 8))
    df = pd.read_pickle('name_data.pkl')
    df = df[(df['Year']>=yr_start) & (df['Year']<=yr_end)]
    # Plot the total babies born
    sns.set_color_codes("pastel")
    sns.barplot(y=df['T_babies']/1000000, x=df['Year'],label="total births\n(1,000,000s)", color="b", ax=ax)
    # Plot the total number of top 10 names
    sns.set_color_codes("muted")
    sns.barplot(y=df_top_10['top_10']/1000000, x=df_top_10['Year'],label="top 10 names\n(1,000,000s)",color="r", ax=ax)
    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="upper right", frameon=True)
    #turn x-axis lines off
    ax.grid('off', axis='x')
    #set x-ticks to every ten years
    ax.set_xticklabels([yr if yr%10==0 else '' for yr in list(range(yr_start,yr_end+1))],rotation=45)
    ax.set(ylabel="",
           xlabel=""
           )
    ax.set_title('Decline of top 10 names in the United States\n| 1920 - 2016 |')
    sns.despine(left=True, bottom=True)
    plt.savefig('Decline of top 10 names in the United States')
    plt.show()

def bar_plot_3(yr_start,yr_end):
    df_top_10 = get_total_of_top_names_for_each_year(yr_start,yr_end,1,10)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(15, 8))
    df = pd.read_pickle('name_data.pkl')
    df = df[(df['Year']>=yr_start) & (df['Year']<=yr_end)]
    # Plot the total babies born
    sns.set_color_codes("pastel")
    sns.barplot(y=df['T_babies']/1000000, x=df['Year'],label="total births\n(1,000,000s)", color="b", ax=ax)
    # Plot the total number of names
    sns.set_color_codes("muted")
    sns.barplot(y=df['T_names']/10000, x=df['Year'],label="unique names\n(10,000s)",color="b", ax=ax)
    # Plot the total number of top 10 names
    sns.set_color_codes("muted")
    sns.barplot(y=df_top_10['top_10']/1000000, x=df_top_10['Year'],label="top 10 names\n(1,000,000s)",color="r", ax=ax)
    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="upper right", frameon=True)
    #turn x-axis lines off
    ax.grid('off', axis='x')
    #set x-ticks to every ten years
    ax.set_xticklabels([yr if yr%10==0 else '' for yr in list(range(yr_start,yr_end+1))],rotation=45)
    ax.set(ylabel="",
           xlabel=""
           )
    ax.set_title('Growth of unique names in the United States\n| 1920 - 2016 |')
    sns.despine(left=True, bottom=True)
    plt.savefig('Growth of unique names in the United States all')
    plt.show()



if __name__ == '__main__':
    # tune_all_years_ with_column_names()
    # tune_all_years_with_added_columns()
    # print(density_for_years(1990,1995))
    # print(df.head(25))
    # plot_density(1900,2016)
    bar_plot_1(1920,2016)
    # bar_plot_2(1920,2016)
    # bar_plot_3(1920,2016)
    # create_pickled_df(1880,2016,'name_data')
    # get_total_of_top_names_for_each_year(1920,1930,1,10)
