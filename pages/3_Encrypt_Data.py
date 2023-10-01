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
import streamlit_tags as stt
from streamlit.logger import get_logger
from json import load
from gnupg import GPG


gpg = GPG()
LOGGER = get_logger(__name__)
with open('emoji.json') as f: emoji = load(f)

def new_gpg_key(**kwargs): return gpg.gen_key(gpg.gen_key_input(**kwargs))


def get_params():
    stt.st_tags(label='Restrictions', text='Press Enter After Each Tag')


def setup():
    st.set_page_config(page_title='Encrypt Data', page_icon='🔐')
    st.write('# Encrypter 🔏🔐')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    if st.sidebar.button('REFRESH'): st.rerun()
    get_params()


def encrypt_data():
    setup()
encrypt_data()