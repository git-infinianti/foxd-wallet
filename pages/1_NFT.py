# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import streamlit as st
from streamlit.logger import get_logger
import streamlit_option_menu as stom
import streamlit_tags as stt

from json import load
from httpx import Client

LOGGER = get_logger(__name__)
with open('emoji.json') as f: emoji = load(f)
ipfs_endpoint = r'https://ipfs.io/ipfs'
api_endpoint = st.secrets['BASEAPI']
api = Client(base_url=api_endpoint)


def api_interface(): pass


@st.cache_data
def search_nft(asset='A'):
    return api.post('/nft', params={'asset': f'{asset}*', 'verbose': True}).json()


def setup():
    st.set_page_config(page_title='NFT', page_icon=emoji[100])
    st.write(f'# NFT {emoji[100]}')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    
    
def nft():
    setup()
    api_interface()
    with st.sidebar: selected = stom.option_menu(None, ['Browse', 'Buy', 'Sell'])
    def browse():
        nft = st.sidebar.text_input('Search for NFT')
        csens = st.sidebar.checkbox('Case Sensitive', True)
        if not csens: nft = nft.upper()
        if nft: data = search_nft(nft)
        else: data = search_nft()
        for d in data.values():
            if d['has_ipfs']: st.image(f"{ipfs_endpoint}/{d['ipfs_hash']}")
    if selected == 'Browse': browse()
    def buy(): st.write('What would you like to buy?')
    if selected == 'Buy': buy()
    def sell(): st.write('What would you like to sell?')
    if selected == 'Sell': sell()
    
nft()