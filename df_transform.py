import pandas as pd
import numpy as np
import streaming_chat
from os import listdir


class ChatDataFrame:

    def __init__(self, log_dir='./'):
        '''
        Given the directory of the chat logs, create a pandas dataframe with the all the chat logs
        '''
        self.chat_logs = listdir(log_dir)
        chat_logs = [log_dir + file for file in self.chat_logs]
        data = streaming_chat.combine_chat_logs(chat_logs)
        self.df = pd.DataFrame(data)


    # mark all empty messages as NaN
    def _clean_empty_messages(self):
        self.df.loc[self.df.message.apply(len) == 0, 'message'] = np.NaN
    

    # mark all channels that are not in the list of streamers as NaN (due to weird glitch in data collection)
    def  _clean_streamer_names(self):
        streamers = set()
        for log in self.chat_logs:
            streamers.add(log.split('.log')[0])
        self.df.loc[self.df['channel'].apply(lambda row: row not in streamers), 'message'] = np.NaN
    

    def clean_data(self):
        '''
        Calls all private data cleaning methods and then drops all NaN values
        Return DataFrame Object     
        '''
        cleaning_methods= [method for method in dir(self) if callable(getattr(self, method)) if method.startswith('_clean')]
        for method in cleaning_methods:
            getattr(self, method)()
        self.df.dropna(inplace=True)
        return self.df
    

    def calculated_columns(self):
        self.df['command_message'] = self.df.apply(lambda row: row['message'].startswith('!'), axis = 1)
    