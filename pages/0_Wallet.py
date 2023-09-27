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


LOGGER = get_logger(__name__)


def hierarchical_deterministic_wallet(symbol): return HDWallet(symbol, get_cryptocurrency(symbol))


def mnemonic_phrase():
    lang = st.sidebar.text_input('Language', 'english')
    str = st.sidebar.select_slider('Security Strength', (128, 256), 128)
    mnem = utils.generate_mnemonic(lang, str)
    mnemonic = st.text_input('Secret Words', mnem)
    st.divider()
    return mnemonic


def display_wallet():
    mnemonic = st.sidebar.text_input('Secret Words')
    if not mnemonic: mnemonic = mnemonic_phrase()
    addr = st.sidebar.number_input('Address', 0, None, 0, 1)
    st.sidebar.divider()
    derivation = Derivation(f"m/44'/0'/0'/0/{addr}")
    hdwallet = hierarchical_deterministic_wallet('FOXD')
    hdwallet = hdwallet.from_mnemonic(mnemonic)
    st.write(hdwallet.from_path(derivation).dumps())


def setup():
    st.set_page_config(page_title='Wallet', page_icon='💳')
    st.write('# Wallet 💳')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    display_wallet()


def wallet():
    setup()
wallet()