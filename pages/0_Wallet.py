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
from functools import cache

LOGGER = get_logger(__name__)
with open(f'emoji.json') as f: emoji = load(f)


@cache
def hierarchical_deterministic_wallet(symbol): return HDWallet(symbol, get_cryptocurrency(symbol))


@cache
def mnemonic_phrase():
    lang = st.sidebar.text_input('Language', 'english', key='language').lower()
    strength = st.sidebar.select_slider('Security Strength', (128, 256), 128)
    mnemonic = utils.generate_mnemonic(lang, strength)
    st.code(mnemonic, None)
    st.divider()
    return mnemonic


@cache
def is_new_wallet():
    wallet = st.file_uploader('Open Wallet', type=emoji[126])
    if wallet: 
        decoded_data = b64decode(wallet.read())
        st.session_state['loadwallet'] = loads(decoded_data)
        return False
    return True 



def load_file() -> tuple[str]:
    def _wallet(*args) -> tuple[str]:
        args = (arg for arg in args)
        acc = st.sidebar.number_input('Account', 0, None, next(args), 1)
        addr = st.sidebar.number_input('Address', 0, None, next(args), 1)
        chng = st.sidebar.number_input('Change', 0, None, next(args), 1)
        return acc, addr, chng
    if is_new_wallet(): 
        acc, addr, chng = _wallet(*('min,'*3).split(',')[:-1])
        mnemonic = st.sidebar.text_input('Secret Words')
   
    else: 
        path = str(st.session_state['loadwallet']['path']).split('/')
        emote = [path[3][0], path[4], path[5]]
        acc, addr, chng = _wallet(*emote)
        mnemonic = st.session_state['loadwallet']['mnemonic']
    
    if not mnemonic: 
        st.sidebar.divider()
        mnemonic = mnemonic_phrase()
        st.session_state['loadwallet'] = {'mnemonic': mnemonic}
    return acc, addr, chng, mnemonic


def display_wallet():
    acc, addr, chng, mnemonic = load_file()
    
    password = st.sidebar.text_input('Passphrase')

    hdwallet = hierarchical_deterministic_wallet('FOXD')
    hdwallet = hdwallet.from_mnemonic(mnemonic, passphrase=password)
    
    derivation = Derivation(f"m/44'/175'/{acc}'/{addr}/{chng}")
    address = hdwallet.from_path(derivation).dumps()
    
    number_emotes = [
        emoji[287], emoji[286], emoji[285], emoji[284], emoji[283], 
        emoji[282], emoji[281], emoji[272], emoji[273], emoji[274]
    ]
    acc_emote = ''.join([number_emotes[int(a)] for a in str(acc)])
    addr_emote = ''.join([number_emotes[int(a)] for a in str(addr)])
    chng_emote = ''.join([number_emotes[int(a)] for a in str(chng)])
    filename = st.text_input('File Name', f'{emoji[768]+acc_emote}/{addr_emote}/{chng_emote}')
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