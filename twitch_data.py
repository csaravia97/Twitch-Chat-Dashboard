import pandas as pd
import numpy as np


class TwitchData:
    def __init__(self, data_directory='./'):
        '''
        Given the directory of the data, create the following pandas dataframes
            - chat_df : all chat info
            - emote_df : data pertaining to emotes (name and usage)
            - emote_channel_df : df to figure out which emotes correspond to which channels (use to join)
        '''
        self.chat_df = pd.read_pickle(data_directory + 'chat_data.pkl')
        self.emote_df = pd.read_pickle(data_directory + 'emote.pkl')
        self.emote_channel_df = pd.read_pickle(data_directory + 'emote_channel.pkl')
        self.unique_channels = self.chat_df.channel.unique()
    

    def top_chatters_per_channel(self, n):
        '''
        Return the top n chatters for each channel in the DataFrame 
        ''' 
        return self.chat_df.groupby(['channel', 'username'])['message'].count().sort_values().groupby(level=0).tail(n)
    

    def top_commands_per_channel(self, n):
        '''
        Return the top n commands(!<command>) for each channel in the DataFrame 
        ''' 
        command_count_per_channel = self.chat_df.loc[self.chat_df['command_message'] == True].groupby(['channel','message'])['username'].count()
        top_commands_per_channel = command_count_per_channel.sort_values().groupby(level=0).tail(n)
        return top_commands_per_channel


    def top_emotes_per_channel(self, n):
        '''
        Return the top n used emotes for each channel in chat_df
        '''
        series = []
        channels = self.unique_channels
        for c in channels:
            top_ind = [c] * n
            emotes = self.emote_df[f'{c}_count'].nlargest(n)[::-1]
            multi_index = pd.MultiIndex.from_tuples(list(zip(top_ind, emotes.index)))
            series.append(pd.Series(emotes.values, index=multi_index))
        return pd.concat(series)
    

    def __combine_series(self, v1, v2):
        l = not np.isnan(v1)
        r = not np.isnan(v2)
        
        if l and r:
            return v1 + v2
        elif l:
            return v1
        else:
            return v2


    def emote_type_breakdown(self):
        '''
        Returns a multi-index series containing the amount of emotes per type for each channel in chat_df
        '''
        # Inner join emote & emote_channel_df on 'name' and groupby channel and emote_type
        merged_df = pd.merge(self.emote_df, self.emote_channel_df, left_index=True, right_on='name')
        grouped_emotes = merged_df.groupby(['channel', 'modified_emote_type']).sum()
        series = []
        channels = self.unique_channels

        for c in channels:
            # combines the global emote count with channel emote count using logic from combine_series
            global_channel_combined = grouped_emotes[f'{c}_count'][c].combine(grouped_emotes[f'{c}_count']['global'], self.__combine_series)

            # Subtracts (channel + global emote count) from total count to get # of emotes from other channels
            total_emote_count = global_channel_combined.append(
                pd.Series(self.emote_df[f'{c}_count'].sum() - global_channel_combined.sum(), index=['Other Channel Emotes']))

            # Make MultiIndex series for channel
            top_index = [c] * len(total_emote_count)
            multi_index = pd.MultiIndex.from_tuples(list(zip(top_index, total_emote_count.index)))
            series.append(pd.Series(total_emote_count.values, index=multi_index))
        return pd.concat(series)
    

    def streamer_mention_count(self):
        '''
        Returns a series containing the number of @streamer messages per streamer
        '''
        streamer_mentions = self.chat_df.loc[self.chat_df['is_@_streamer'] == True]
        mentions_by_channel = streamer_mentions.groupby('channel').message.count()
        return mentions_by_channel
    

    def question_mark_count(self):
        '''
        Returns a series containing the number of ??? messages per streamer
        '''
        question_mark_msgs = self.chat_df.loc[self.chat_df['question_mark_messages'] == True]
        question_marks_by_channel = question_mark_msgs.groupby('channel').message.count()
        return question_marks_by_channel
    

    def average_emote_ratio(self):
        '''
        Returns a series containing the average emote ratio per streamer
        '''
        return self.chat_df.groupby('channel')['emote_ratio'].mean()
    

    def highest_emote_count(self, n):
        return self.emote_df.emote_count.nlargest(n)