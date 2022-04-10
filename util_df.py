import pandas as pd
import missingno as msno
from matplotlib.pyplot import fill
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

import logging
# format = logging.basicConfig(format=f"[%(level)] %(__file__) (%lineno)s - (%funcName)10s (%message)s")
# logging.basicConfig(format=format)
# logger = logging.getLogger(__file__)
# logger.setLevel(logging.DEBUG)

def missingno_plot_isna(df:pd.DataFrame, is_flexi_figsize=True, title="", is_print_nonzero=True):
    na = df.isna().sum()
    series_na_nonzero = na[na>0].sort_values(ascending=False)    
    df_nonzero = df[series_na_nonzero.index]
        
    if is_print_nonzero:
        na_percent=100*np.array(series_na_nonzero.values)/len(df)
        series_percent_na = pd.Series(np.around(na_percent,decimals=2), index=series_na_nonzero.index)
        print(f"\n{title}\ncolumnns\t% of empty\n{series_percent_na}")        

    if is_flexi_figsize:
        ax_matrix=msno.matrix(df_nonzero, figsize=(min(20,3*df_nonzero.shape[1]), 5))
    else:
        ax_matrix=msno.matrix(df_nonzero)
    
    if len(title):
        ax_matrix.set_title(title, size=20)
    
    plt.show()

    return ax_matrix

class Dfcleaning():
    def __init__(self, df: pd.DataFrame, title=""):
        super().__init__()
        self.df = df    
        self.title = title

    def plot_isna(self):
        missingno_plot_isna(self.df, is_flexi_figsize=True, title=self.title, is_print_nonzero=True)

    # def create_1hot_hierachy_col(self, hierachy_dict: dict):    
    #     def is_intersect(left: list, right: list):
    #         """
    #         Lists are slightly faster than sets when you just want to iterate over the values.
    #         Sets, however, are significantly faster than lists if you want to check if an item is contained within it.             
    #         """
    #         return bool(len(set(left) & set(right)))

    #     self.df.reindex(columns=list(hierachy_dict.values()), fill_value=0)
    #     for t, v in enumerate(hierachy_dict.values()):
    #         self.df[v] = df.
            
    def get_df(self):
        return self.df

    def is_df_series_exist_in_dict_values(df:pd.DataFrame, col_header:str, genre_dict:dict, genre_dict_col_sum:dict, prefix_1hot="_"): 
        lowercase_1space_header = "dummy_header"
        df[lowercase_1space_header] = df[col_header].apply(lambda x : " ".join(x.split()).lower())
        # display(df[["listed_in","listed_in_lowercase_1space"]])
        # print(df["listed_in_lowercase_1space"][:2], type(df["listed_in_lowercase_1space"][0]))       
        col_1hot_list=[]    
        for t, genre in enumerate(genre_dict.keys()):        
            col_1hot = f"{prefix_1hot}{genre.title()}"
            col_1hot_list.append(col_1hot)
            df[col_1hot] = df[lowercase_1space_header].apply(
                lambda x: int(is_in_major_genre(
                            comma_separated_list=x, major_genre=genre, genre_dict=genre_dict))
                )
                    
            if __DEBUG_GENRE__:            
                # print(t, genre, df[col_1hot].sum())        
                assert genre_dict_col_sum[genre] == df[col_1hot].sum(), print(f"column sum of '{genre}' is {df[col_1hot].sum()}, expected {genre_dict_col_sum[genre]}")
            
        # print(genre_dict_col_sum)

        if __DEBUG_GENRE__:
            df["len_listed_in"] = df[lowercase_1space_header].apply(lambda x: len(x.split(",")))
            df["sum_genre"] = df[col_1hot_list].agg("sum", axis=1)
            df["diff"] = (df["len_listed_in"] - df["sum_genre"])    
            print(f"df['diff] {sum(df['diff'])}")

        df.drop(columns=lowercase_1space_header, inplace=True)
        return df


if __name__ == "__main__":
    print(__file__)