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

from hdwallet import utils, HDWallet
from hdwallet.derivations import Derivation
from hdwallet.cryptocurrencies import get_cryptocurrency

from json import dumps, load


LOGGER = get_logger(__name__)


def hierarchical_deterministic_wallet(symbol): return HDWallet(symbol, get_cryptocurrency(symbol))


def mnemonic_phrase():
    lang = st.sidebar.text_input('Language', 'english', key='language').lower()
    strength = st.sidebar.select_slider('Security Strength', (128, 256), 128)
    mnem = utils.generate_mnemonic(lang, strength)
    mnemonic = st.text_input('Secret Words', mnem)
    st.divider()
    return mnemonic


def load_wallet():
    wallet = st.file_uploader('Open Wallet', type='json')
    if wallet: st.session_state['loadwallet'] = load(wallet); return False
    return True


def display_wallet():
    if load_wallet(): 
        addr = st.sidebar.number_input('Address', 0, None, 'min', 1)
        mnemonic = st.sidebar.text_input('Secret Words', key='mnemonic')
    else: 
        addr = str(st.session_state['loadwallet']['path']).split('/')
        addr = st.sidebar.number_input('Address', 0, None, int(addr[-1]), 1)
        mnemonic = st.session_state['loadwallet']['mnemonic']
    if not mnemonic: st.sidebar.divider(); mnemonic = mnemonic_phrase()
    derivation = Derivation(f"m/44'/0'/0'/0/{addr}")
    hdwallet = hierarchical_deterministic_wallet('FOXD')
    password = st.sidebar.text_input('Passphrase')
    hdwallet = hdwallet.from_mnemonic(mnemonic, passphrase=password)
    address = hdwallet.from_path(derivation).dumps()
    
    filename = st.text_input('File Name', f'foxdwallet-{addr}')
    st.download_button('Download', dumps(address), f'{filename}.json', 'application/json')
    st.write(address)


def setup():
    st.set_page_config(page_title='Wallet', page_icon='💳')
    st.write('# Wallet 💳')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    display_wallet()


def wallet():
    setup()
wallet()