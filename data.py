from pandas import DataFrame
import pandas as pd


class SanderDataModel:
    """
    Class to resemble App-Data
    """

    def __init__(self, df_tec: DataFrame, df_1: DataFrame, df_2: DataFrame):
        self.df_tec = df_tec
        self.df_1 = df_1
        self.df_2 = df_2
        self.df_changes = df_1.merge(df_2, how='right', indicator=True)
        self.cleaned = False

    def clean_all_df(self):
        """
        Remove rows with only NaN-values
        """
        self.df_tec = self.df_tec.dropna(how='all')
        self.df_1 = self.df_1.dropna(how='all')
        self.df_2 = self.df_2.dropna(how='all')
        self.df_changes = self.df_changes.dropna(how='all')
        self.cleaned = True

    def crunch_all_df(self):
        """
        Crunch Item-Tables
        """
        if not self.cleaned:
            self.clean_all_df()

        self.df_1 = self.df_1.drop_duplicates(ignore_index=True)
        self.df_2 = self.df_2.drop_duplicates(ignore_index=True)
        self.df_changes = self.df_changes[self.df_changes['_merge']
                                          == 'right_only']
