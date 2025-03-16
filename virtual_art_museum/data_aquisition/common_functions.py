import os # standard libraries
import random
import re
import time
import asyncio
import aiohttp
from math import ceil

import pandas as pd 
from tqdm import tqdm
import numpy as np

def print_example_rows(df, n=5):
    rows = df.head(n)
    for _, row in rows.iterrows():
        for col in rows.columns:
            print(f"{col}: {row[col]}")
        print("--------------------------------")

def century_mapping(year):
    ''' Creates a century value for applicable years '''
    if year != -1: # -1 is a flag for no year found in Europeana search
        if isinstance(year, int):
            century = ceil(abs(year) / 100)
        if year < 0:
            return f"{century}th century BC"
        else:
            if century == 1:
                return f"{century}st century AD"
            elif century == 2:
                return f"{century}nd century AD"
            elif century == 3:
                return f"{century}rd century AD"
            else:
                return f"{century}th century AD"
    return year