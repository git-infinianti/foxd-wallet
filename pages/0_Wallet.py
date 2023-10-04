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
from httpx import Client
import pyclip as cb
from utils import CHAINS, get_chain_emoji, numeric_emoji

LOGGER = get_logger(__name__)
client = Client(base_url='https://explorer2.foxdcoin.com')
with open(f'emoji.json') as f: emoji = load(f)

# import subprocess
# subprocess.run('sudo apt install wl-clipboard')

def hdwallet(symbol): return HDWallet(symbol, get_cryptocurrency(symbol))


def mnemonic_phrase():
    lang = st.sidebar.text_input('Language', 'English').lower()
    strength = st.sidebar.select_slider('Security Strength', (128, 256), 128)
    mnemonic = utils.generate_mnemonic(lang, strength)
    st.code(mnemonic, None)
    st.sidebar.divider()
    st.divider()
    return mnemonic


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
        emote = [int(path[3][0]), int(path[4]), int(path[5])]
        acc, addr, chng = _wallet(*emote)
        mnemonic = st.session_state['loadwallet']['mnemonic']
    if not mnemonic: 
        st.sidebar.divider()
        mnemonic = mnemonic_phrase()
        st.session_state['loadwallet'] = {'mnemonic': mnemonic}
    try: cb.copy(mnemonic)
    except: Exception('')
    return acc, addr, chng, mnemonic


def display_wallet():
    # Chain Selection
    symbol = st.sidebar.selectbox('Chain', CHAINS)
    chain = get_chain_emoji(symbol)

    acc, addr, chng, mnemonic = load_file()
    acc_emote, addr_emote, chng_emote = numeric_emoji(acc, addr, chng)
    password = st.sidebar.text_input('Passphrase')


    # Generate Wallet
    hdw = hdwallet(symbol)
    hdw = hdw.from_mnemonic(mnemonic, passphrase=password)
    
    derivation = Derivation(f"m/44'/175'/{acc}'/{addr}/{chng}")
    address = hdw.from_path(derivation).dumps()
    
    
    filename = st.text_input('File Name', f'{emoji[chain]+acc_emote}/{addr_emote}/{chng_emote}')
    data_string = dumps(address)
    st.download_button('Download', b64encode(bytes(data_string, 'utf-8')), f'{filename}.{emoji[126]}')
    st.divider()
    st.image(client.get(f'/qr/{address["addresses"]["p2pkh"]}').content)
    address_info = loads(client.get(f'/ext/getaddress/{address["addresses"]["p2pkh"]}').text)
    if 'error' not in address_info: st.write(address_info)
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