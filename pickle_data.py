import os
import pandas as pd
import pdb

class Pickle(object):
    '''
    This class will pickle
        1 - a directory of files - Pickle.pickle_folder
        2 - individual files - Pickle.pickle_file
    '''
    def __init__(self):
        self.pickled = []
        self.not_pickled = []

    def pickle_file(self, filename, print=True):
        '''
        INPUT:
        filename: filename, as string, to pickle
        print = True: Calls _print()
        OUTPUT:
        prints title of successfully pickled file
        '''
        try:
            df = pd.read_csv('{}'.format(filename))
        except pd.errors.EmptyDataError:
            self.not_pickled.append(filename)
        else:
            df = pd.read_csv('{}'.format(filename))
            df.to_pickle('{}.pkl'.format(filename))
            self.pickled.append(filename)
        if print:
            self._print()

    def _print(self):
        if len(self.not_pickled) == 0 and len(self.pickled) > 0:
            print('\n')
            print('Congrats!! Your barrel contains the following pickles:')
            print(', '.join(self.pickled))
            print('\n')

        elif len(self.not_pickled) > 0 and len(self.pickled) > 0:
            print('\n')
            print("Your barrel contains these pickles:")
            print(', '.join(self.pickled))
            print('\n')
            print('Unfortunately these guys did not make it:')
            print(', '.join(self.not_pickled))
            print('\n')

        else:
            print('\n')
            print('hum.....seems we pickled nothing.')
            print('\n')

    def pickle_folder(self, directory, extension_lst):
        '''
        INPUT:
        directory: directory, as str, in which to pickle files
            e.g. I'm in main directory, data is in sub folder 'data'
            <directory = 'data'>

        extension_lst: extension(s) as a list to pickle.
            e.g. <['csv', 'txt']>
        OUTPUT:
        string of pickled files
        string of files that had correct extension but were not pickled due to pandas error
            e.g. default setting is that if file has no data to read it will pass it over
        '''
        dir_as_str = directory
        directory = os.fsencode(directory)
        for ext in extension_lst:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".{}".format(ext)):
                    full_file_name = '{}/{}'.format(dir_as_str,filename)
                    self.pickle_file(full_file_name,print=False)
        return self._print()
