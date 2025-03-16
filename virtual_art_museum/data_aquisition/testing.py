import streamlit as st
import requests

import asyncio
import aiohttp

import requests
import pandas as pd 
from tqdm import tqdm
import numpy as np
import async_utils
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
# st.image('https://images.metmuseum.org/CRDImages/ad/original/204788.jpg')
# st.image('https://www.dropbox.com/s/u2xvcw1ev2pt32c/DK_Slott%20Moeller_Sankt%20Hans%20Aften_VejleMuseerne.jpg?raw=1')


# def check_dropbox_content(content: bytes):
#     content = content[:9]
#     if content == b'<!DOCTYPE': # if it is a valid dropbox url it will return hexxcode, not html
#         return False
#     else:
#         return True
    
# bad_url = 'https://www.dropbox.com/s/qxn33ysbrazbxru/Ireland_Dorothy%20Cross%2C%20Saddle.JPG?raw=1'
# response = requests.get(bad_url)
# print(async_utils.check_dropbox_content(response.content))
session = requests.Session()
retries = Retry(total=5, 
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

headers = {
    'User-Agent': 'PostmanRuntime/7.43.2',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Postman-Token': '00b71906-b3b0-4373-9996-561e894a2816',
    'Host': 'images.metmuseum.org',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'incap_ses_1544_1661977=A4jfEAEi3AaUeeEOGmRtFfQi12cAAAAAVrE917tEXBu40KAuVbNfmQ==; visid_incap_1661977=6VISR2CoSjWg6AK/v5X352SD1mcAAAAAQUIPAAAAAAA6O5/aY5xz4wvFD0QkgJn5; visid_incap_1662004=kamgr9t+TBioZFjTpRe90F/rs2cAAAAAQUIPAAAAAAAOKfci+zafcJu2COA1oWt/'
}

try:
    # Use session instead of direct requests
    response = session.get('https://images.metmuseum.org/CRDImages/ad/original/204788.jpg', 
                         headers=headers, 
                         timeout=30,
                         allow_redirects=True)
    print(response.status_code)
except Exception as e:
    print(e)