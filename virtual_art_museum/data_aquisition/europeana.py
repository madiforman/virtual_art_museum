import requests
import random

import pyeuropeana.utils as utils
import pyeuropeana.apis as apis
import pandas as pd

class Europeana:
    # TO DO: bulk download and save data 
    def __init__(self):
        self.df = self.bulk_requests()

    def bulk_requests(self):
        query_terms = pd.read_csv('query_terms.csv', header=None)
        query_terms = query_terms.iloc[:, 0].tolist()
        df_list = []
        for query in query_terms:
            cursor = '*'  # Initial cursor value
            total_results = 0
            max_results = 250  # Set a maximum number of results per query
            
            while cursor and total_results < max_results: 
                response = apis.search(
                    query=query,
                    profile='minimal',
                    cursor=cursor, #pass the cursor to the next page
                    qf='LANGUAGE:en',
                    rows=100  # Maximum allowed per request
                )
                if not response.get('items'): # if no results, break
                    break

                df_new = utils.search2df(response)
                df_list.append(df_new)
    
                cursor = response.get('nextCursor') # move the pointer
                total_results += len(response.get('items', []))
                print(f"Fetched {total_results} results for query: {query}")
            
            break
        self.df = pd.concat(df_list, ignore_index=True)  # Combine all results into single dataframe
        return self.df
    
    def filter_results(self):
        columns_to_translate = self.df[self.df.columns[self.df.columns.str.contains('lang')]]
        print(columns_to_translate)
        
    def write_to_csv(self, filename):
        self.df.to_csv(filename, index=False)


def main():
    key = "etendinfi"
    europeana = Europeana()
    # europeana.df.to_csv('europeana_data.csv', index=False)
    # lang_dict = europeana.df.head(1)['description_lang'][0]
    # for key, value in lang_dict.items():
    #     if key == 'en-US':
    #         print(value)
    europeana.filter_results()
if __name__ == "__main__":
    main()


