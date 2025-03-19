"""
===============================================
Common Functions - Data Aquisition
===============================================
This module contains the common functions for the data aquisition pipeline.

Functions
----------
    print_example_rows: Prints the first n rows of a dataframe
    century_mapping: Maps a year to a century
    image_processing_europeana: Processes the Europeana data to be compatible with MET
    blend_datasources: Blends the MET and Europeana data
    reorder_columns: Reorders the columns of the two dataframes to be compatible with each other
    main: Main function to run the data aquisition pipeline

Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""
from math import ceil

import pandas as pd

def print_example_rows(df, n=5):
    """
    Prints the first n rows of a dataframe in a readable format.

    Parameters
    ----------
    df (pd.DataFrame): The dataframe to print
    n (int): The number of rows to print

    Returns
    -------
    None
    """
    rows = df.head(n)
    print("--------------------------------")
    for _, row in rows.iterrows():
        for col in rows.columns:
            print(f"\t{col}: {row[col]}")
        print("--------------------------------")

def century_mapping(year):
    """
    Maps a year to a century.

    Parameters
    ----------
    year (int): The year to map

    Returns
    -------
    str: The century of the year
    """
    try:
        # Convert to int if it's a string
        year = int(year)
        
        # Check valid range
        if year > 2015:
            return "Unknown"
            
        # Calculate century
        century = ceil(abs(year) / 100)
        
        # Handle BC years
        if year < 0:
            return f"{century}th century BC"
            
        # Handle AD years with proper suffixes
        if century == 1:
            return f"{century}st century AD"
        elif century == 2:
            return f"{century}nd century AD"
        elif century == 3:
            return f"{century}rd century AD"
        else:
            return f"{century}th century AD"
            
    except (ValueError, TypeError):
        return "Unknown"
        
def image_processing_europeana(met, europeana):
    """
    Transforms the Europeana data to be 
    compatible with MET merge.
    - Reads through the description column
        and tries to match for any Mediums
        or Tags (based on MET)
    - Updates country column to match any
        culture within the MET data
    - Makes a fake column for Artist Bio
    - Replaces 'Unknown' in year column
        with unrealistic value
    - Renames columns to match MET's
    """
    europeana['year'] = europeana['year'].apply(century_mapping)
    europeana['Medium'] = "Medium unknown"
    europeana['Tags'] = "Tags unknown"
    europeana['repository'] = "Europeana"

    tags = met['Tags'].str.split(',').explode().unique()
    cultures = met['Culture'].str.split(',').explode().unique()

    def find_tags(description):
        ''' Searches through the description
        column, finding any Tag matches '''
        tags_match = []

        if description == 'Unknown' or str(description).startswith('warning:'):
            return "Description unknown"

        description = str(description).lower()

        for tag in tags:
            if tag.lower() in description:
                tags_match.append(tag)

        return description

    europeana['description'] = europeana['description'].apply(find_tags)

    for idx, row in europeana.iterrows():
        description = str(row['description']).lower()

        tags_match = [tag for tag in tags if tag and tag.lower() in description]
        if tags_match:
            europeana.at[idx, 'Tags'] = ", ".join(tags_match)

    country_to_culture = {
        'United Kingdom': 'British',
        'England': 'British',
        'Scotland': 'British',
        'Wales': 'British',
        'Ireland': 'Irish',
        'France': 'French',
        'Germany': 'German',
        'Italy': 'Italian',
        'Spain': 'Spanish',
        'Portugal': 'Portuguese',
        'Netherlands': 'Dutch',
        'Belgium': 'Belgian',
        'Switzerland': 'Swiss',
        'Austria': 'Austrian',
        'Greece': 'Greek',
        'Denmark': 'Danish',
        'Sweden': 'Swedish',
        'Norway': 'Norwegian',
        'Finland': 'Finnish',
        'Russia': 'Russian',
        'Poland': 'Polish',
        'Hungary': 'Hungarian',
        'Czech Republic': 'Czech',
        'Romania': 'Romanian',
        'Bulgaria': 'Bulgarian',
        'Turkey': 'Turkish'}

    for culture in cultures:
        country_match = None
        culture = str(culture).strip()

        # Remove suffixes to check for match
        if culture.endswith('ish'):
            country_match = culture[:-3]
        elif culture.endswith('ese'):
            country_match = culture[:-3]
        elif culture.endswith('ian'):
            country_match = culture[:-3]
        elif culture.endswith('ch'):
            country_match = culture[:-2] + 'ce'
        elif culture.endswith('ish'):
            country_match = culture[:-3]

        if country_match and country_match not in country_to_culture.values():
            country_to_culture[country_match] = culture

    def map_countries_to_culture(country):
        ''' Maps countries to respective cultures '''
        if pd.isna(country) or country == 'Unknown':
            return 'Culture unknown'

        country = str(country).strip()

        if country in country_to_culture:
            return country_to_culture[country]

        for known_country, culture in country_to_culture.items():
            if known_country in country:
                return culture

        for culture in cultures:
            culture_lower = culture.lower()
            country_lower = country.lower()
            if culture_lower in country_lower:
                return culture

        return 'Culture unknown'

    europeana['Culture'] = europeana['country'].apply(map_countries_to_culture)

    def clean_title(title):
        ''' Makes a cleaner title to print '''
        if not isinstance(title, str):
            return title

        comma = title.find(',')
        period = title.find('.')

        if comma == -1 and period == -1:
            return title
        elif comma == -1:
            return title[:period].strip()
        elif period == -1:
            return title[:comma].strip()
        else:
            endpoint = min(idx for idx in [comma, period] if idx >= 0)
            return title[:endpoint].strip()

    europeana['title'] = europeana['title'].apply(clean_title)

    def clean_creator(artist):
        if pd.isna(artist) or artist == 'Unknown' or str(artist).startswith('http://'):
            return "Artist unknown"
        return artist

    europeana['creator'] = europeana['creator'].apply(clean_creator)

    europeana['Artist biographic information'] = "Artist biographic information unknown"
    europeana['Dimensions'] = "Dimensions unknown"

    europeana = europeana.rename(columns = {'europeana_id' : 'Object Number',
                                  'title' : 'Title',
                                  'creator' : 'Artist',
                                  'description' : 'Description',
                                  'provider' : 'Department',
                                  'year' : 'Year',
                                  'repository' : 'Repository'})
    europeana = europeana.drop(columns=['country'])

    return europeana, met

def blend_datasources(met, europeana):
    """
    Blends the MET and Europeana dataframes.

    Parameters
    ----------
    met (pd.DataFrame): The MET dataframe
    europeana (pd.DataFrame): The Europeana dataframe

    Returns
    -------
    pd.DataFrame: The blended dataframe
    """
    return pd.concat([met, europeana])

def reorder_columns(df1, df2):
    """
    Reorders the columns of the two dataframes
    to be compatible with each other

    Parameters
    ----------
    df1 (pd.DataFrame): The first dataframe
    df2 (pd.DataFrame): The second dataframe

    Returns
    -------
    pd.DataFrame: The blended dataframe
    """
    first_order = df1.columns.tolist()
    df2 = df2[first_order]
    return df1, df2

def main():
    """
    Main function to run the data aquisition pipeline.
    """
    met = pd.read_csv('../data/MetObjects_final_filtered_processed.csv')
    europeana = pd.read_csv('../data/Europeana_data_processed.csv')
    met, europeana = reorder_columns(met, europeana)

    print_example_rows(met, n=1)
    print_example_rows(europeana, n=1)

    print("Blending dataframes")
    blended = blend_datasources(met, europeana)
    print_example_rows(blended, n=1)
    blended.to_csv('../data/blended_data.csv', index=False)

    print(f"Length of MET: {len(met)}")
    print(f"Length of Europeana: {len(europeana)}")
    print(f"Length of blended: {len(blended)}")

if __name__ == "__main__":
    main()
