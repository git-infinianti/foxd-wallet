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


LOGGER = get_logger(__name__)
ipfs_url = r'https://ipfs.io/ipfs/'


def search_nft(): st.sidebar.text_input('Search for NFT')


def browse(): st.write('You are now Browsing')


def buy(): st.write('What would you like to buy?')


def sell(): st.write('What would you like to sell?')


def setup():
    st.set_page_config(page_title='NFT', page_icon='📝')
    st.write('# NFT 📝')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    search_nft()


def nft():
    setup()
    with st.sidebar: selected = stom.option_menu(None, ['Browse', 'Buy', 'Sell'])
    if selected == 'Browse': browse()
    if selected == 'Buy': buy()
    if selected == 'Sell': sell()
nft()