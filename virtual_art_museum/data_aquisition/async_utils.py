
"""
This module perfoms the largest data aquisition task of the project.

It is responsible for fetching the image urls from the source and filtering
out any objects that do not have a valid image url. This process is slightly different
for the MET and Europeana sources, however this script is designed to handle both

References
----------
    https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    https://pro.europeana.eu/page/apis
    https://github.com/europeana/rd-europeana-python-api

Functions
----------
    check_dropbox_content: Checks if dropbox content is an image 
    check_europeana_response: Checks if europeana response is a valid image url
    fetch: Fetches the image url from the source
    bound_fetch: Fetches the image url from the source with rate limiting
    run: Runs the fetch function on the dataframe
    filter_objects: Filters the dataframe based on the source

Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""
import time

import asyncio
import aiohttp

from tqdm.asyncio import tqdm_asyncio

def check_dropbox_content(content: bytes):
    """
    Checks if the first 9 bytes of content from Europeana is a valid image url.

    In the Europeana API, some links are to a dropbox page. This can return status 200,
    even though it is just linking you to a bad dropbox page. This function checks if the first
    9 bytes of content are the html code for a dropbox page. If they are, it returns False,
    indicating that the url is not a valid image url. It assumes that if it is not html code,
    then it will be hexcode. I am doubtful that this is a safe assumption always.

    Parameters
    ----------
    content (bytes): The first 9 bytes of content from Europeana image_url

    Returns
    -------
    bool: True if the url is a valid image url, False otherwise
    """
    content = content[:9]
    if content == b'<!DOCTYPE': # if it is a valid dropbox url it will return hexxcode, not html
        return False
    return True

def check_europeana_response(url: str, content: bytes) -> str:
    """
    Checks if the url is a valid image url.

    Parameters
    ----------
    url (str): The url to check
    content (bytes): The first 9 bytes of content from Europeana image_url

    Returns
    -------
    str: The url if it is a valid image link, an empty string otherwise
    """
    if url.startswith('https://www.dropbox.com'):
        if check_dropbox_content(content):
            return url
        return ""
    return url

async def fetch(session:aiohttp.ClientSession, url:str, flag:str) -> str: # pylint: disable=too-many-return-statements
    """
    Fetches the image url using the session object.

    This function is designed to be used with the MET data and Europeana data.
    There are two different cases that must be addressed for each.

    Parameters
    ----------
    session (aiohttp.ClientSession): The session object
    url (str): The url to fetch
    flag (str): The flag to determine the source

    Returns
    -------
    str: The image url if it is a valid image link, an empty string otherwise
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                if flag == "MET":
                    data = await response.json()
                    if 'primaryImage' in data and data['primaryImage']:
                        return data['primaryImage']
                    return ""

                if flag == "EUROPEANA":
                    content = await response.content.read(9)
                    if url.startswith('https://www.dropbox.com'):
                        if check_dropbox_content(content):
                            return url
                        return ""
                    return url
                raise ValueError(f"Invalid source given: {flag}. Must be either MET or EUROPEANA")
            return ""
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Error fetching {url}: {e}")
        return ""

async def bound_fetch(
    semaphore: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    url: str,
    flag: str
) -> str:
    """
    Fetch URL with rate limiting via semaphore.
    
    Parameters
    ----------
        semaphore: Semaphore for rate limiting requests
        session: aiohttp client session
        url: URL to fetch
        flag: Source flag ('MET' or 'EUROPEANA')
        
    Returns:
    -------
        str: The image url if it is a valid image link, an empty string otherwise
    """
    async with semaphore:
        return await fetch(session, url, flag)

async def run(df, flag: str):
    """
    Runs the fetch function on the dataframe.

    This function is designed to be used with the MET data and Europeana data.
    It performs the bulk parallel fetching of the image urls. The function is designed
    to be used with the MET data and Europeana data.It begins by building a dict that maps
    url -> unique id. It then creates a list of tasks where each task is a call to the
    bound_fetch function. It then gathers the results and filters the dataframe based
    on the results.

    Parameters
    ----------
    df (pd.DataFrame): The dataframe to fetch the image urls from
    flag (str): The flag to determine the source
    
    Returns
    -------
    pd.DataFrame: The dataframe with the valid image urls
    """
    url_dict = {}
    col_name = ''
    if flag == "MET":
        base_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        df.dropna(subset=['Object ID'], inplace=True) # just in case
        df.drop_duplicates(subset=['Object ID'], inplace=True)
        url_dict = {f"{base_url}/{obj_id}": obj_id for obj_id in df['Object ID'].tolist()}
        col_name = 'Object ID'

    elif flag == "EUROPEANA":
        url_dict = dict(zip(df['image_url'], df['europeana_id']))
        col_name = 'europeana_id'
    else:
        raise ValueError(f"Invalid source given: {flag}. Must be either MET or EUROPEANA")

    tasks = []
    max_requests = 500
    semaphore = asyncio.Semaphore(max_requests)
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # Create tasks for each URL to fetch in parallel
        tasks = [asyncio.ensure_future(bound_fetch(semaphore, session, url, flag))
                for url in url_dict.keys()]

        total_tasks = len(tasks)
        print(f"All {total_tasks} tasks created, waiting for responses...")
        results = await tqdm_asyncio.gather(*tasks, miniters=50)
        # Create dictionary mapping IDs to valid image URLs (filtering out empty results)
        valid_dictionary = {
                            url_dict[url]: result for url, result in
                            zip(url_dict.keys(), results) if result != ""
                            }
        filtered_df = df[df[col_name].isin(valid_dictionary.keys())].copy()

        if flag == "MET":
            filtered_df['image_url'] = filtered_df['Object ID'].map(valid_dictionary)

        print("All tasks completed.")
        print(f"\tOriginal shape: {df.shape}")
        print(f"\tFiltered shape: {filtered_df.shape}")
        print(f"\tTime taken: {time.time() - start_time} seconds")

    return filtered_df

def filter_objects(df, flag: str):
    """
    Filters the dataframe based on the source. It simply runs the run function. so that asyncio 
    does not need to be imported elsewhere.

    Parameters
    ----------
    df (pd.DataFrame): The dataframe to filter
    flag (str): The flag to determine the source

    Returns
    -------
    pd.DataFrame: The dataframe with the valid image urls
    """
    return asyncio.run(run(df, flag))
