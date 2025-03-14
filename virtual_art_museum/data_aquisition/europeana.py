import requests
import random

import pyeuropeana.utils as utils
import pyeuropeana.apis as apis
import pandas as pd

class Europeana:
    def __init__(self):
        self.df = self.bulk_requests()

    def bulk_requests(self):
        query_terms = pd.read_csv('query_terms.csv', header=None)
        query_terms = query_terms.iloc[:, 0].tolist()
        df_list = []
        for query in query_terms:
            cursor = '*'  # Initial cursor value
            total_results = 0
            max_results = 2  # Set a maximum number of results per query
            
            while cursor and total_results < max_results: 
                response = apis.search(
                    query=query,
                    reusability = 'open AND permission', # ensure rights to use the data
                    profile='minimal',
                    cursor=cursor, #pass the cursor to the next page
                    qf='LANGUAGE:en AND TYPE:IMAGE',
                    rows=max_results  # Maximum allowed per request
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
    
    def process_metadata(self, metadata):
        for lang_dict in metadata.values:
            if lang_dict is not None:
                for key, value in lang_dict.items():
                    # print(key)
                    # item = value
                    if key == 'def':
                        return value
                    if key == 'en-US' or key == 'en':
                        return value
        return None

    def get_english_description(self, metadata):
        for lang_dict in metadata.values:
            if lang_dict is not None:
                for key, value in lang_dict.items():
                    if key == 'en-US' or key == 'en':
                        return value
        return None

    def get_english_title(self, metadata):
        for lang_dict in metadata.values:
            if lang_dict is not None:
                for key, value in lang_dict.items():
                    if key == 'def':
                        return value
        return None

    def filter_results(self):
        self.df.pop('uri')
        self.df.pop('description')
        self.df.pop('title')
        self.df.pop('type')
        self.df.pop('concept')
        self.df.pop('concept_lang')
        self.df.fillna('Unknown', inplace=True) # fill missing values with 'Unknown'

        columns_to_translate = ['description_lang', 'title_lang']
        for col in columns_to_translate:
            if col == 'description_lang':
                metadata = self.df[col]
                english_description = self.get_english_description(metadata)
                self.df['description'] = english_description
            if col == 'title_lang':
                metadata = self.df[col]
                english_title = self.get_english_title(metadata)
                self.df['title'] = english_title

        self.df.pop('description_lang')
        self.df.pop('title_lang')
        self.print_example_row()

    def print_example_row(self):
        row = self.df.iloc[0]
        for idx in range(len(self.df.columns)):
            print(f"{self.df.columns[idx]}: {row[idx]}")

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


