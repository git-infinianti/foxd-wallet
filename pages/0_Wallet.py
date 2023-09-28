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

from json import dumps, load, loads
from base64 import b64encode, b64decode


LOGGER = get_logger(__name__)
with open(f'emoji.json') as f: emoji = load(f)


def hierarchical_deterministic_wallet(symbol): return HDWallet(symbol, get_cryptocurrency(symbol))


def mnemonic_phrase():
    lang = st.sidebar.text_input('Language', 'english', key='language').lower()
    strength = st.sidebar.select_slider('Security Strength', (128, 256), 128)
    mnemonic = utils.generate_mnemonic(lang, strength)
    st.code(mnemonic)
    st.divider()
    return mnemonic


def load_wallet():
    wallet = st.file_uploader('Open Wallet', type=emoji[126])
    if wallet: 
        decoded_data = b64decode(wallet.read())
        st.session_state['loadwallet'] = loads(decoded_data); return False
    return True 
 
def display_wallet():
    if load_wallet(): 
        addr = st.sidebar.number_input('Address', 0, None, 'min', 1)
        mnemonic = st.sidebar.text_input('Secret Words')
    else: 
        addr = str(st.session_state['loadwallet']['path']).split('/')
        addr = st.sidebar.number_input('Address', 0, None, int(addr[-1]), 1)
        mnemonic = st.session_state['loadwallet']['mnemonic']
    if not mnemonic: 
        st.sidebar.divider()
        mnemonic = mnemonic_phrase()
        st.session_state['loadwallet'] = {'mnemonic': mnemonic}
    derivation = Derivation(f"m/44'/0'/0'/0/{addr}")
    hdwallet = hierarchical_deterministic_wallet('FOXD')
    password = st.sidebar.text_input('Passphrase')
    hdwallet = hdwallet.from_mnemonic(mnemonic, passphrase=password)
    address = hdwallet.from_path(derivation).dumps()
    number_emotes = [emoji[287], emoji[286], emoji[285], emoji[284], emoji[283], emoji[282], emoji[281], emoji[272], emoji[273], emoji[274]]
    addr_emote = ''.join([number_emotes[int(a)] for a in str(addr)])
    filename = st.text_input('File Name', f'{emoji[768]+emoji[289]+addr_emote}')
    data_string = dumps(address)
    st.download_button('Download', b64encode(bytes(data_string, 'utf-8')), f'{filename}.{emoji[126]}')
    st.divider()
    st.write(address)
    

def setup():
    st.set_page_config(page_title='Wallet', page_icon=emoji[126])
    st.write(f'# Wallet {emoji[126]}')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    display_wallet()


def wallet():
    setup()
wallet()