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
import streamlit_tags as stt



LOGGER = get_logger(__name__)


def generate_config():
    testnet = st.sidebar.toggle('Enable Testnet')
    regtest = st.sidebar.toggle('Enable Regtest')
    proxy = f"proxy={st.sidebar.text_input('Enter a Proxy IP Address')}"
    connect = stt.st_tags_sidebar(label='Connections', text="Enter an IP(s)")
    maxconnections = st.sidebar.number_input('Maximum Connections', 0)
    return ''


def download_button():
    config = generate_config()
    st.download_button('Download Config File', config)


def setup():
    st.set_page_config(page_title='Node Config', page_icon='🧰')
    st.write('# Node Configurator 🧰')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    download_button()


def node_config():
    setup()
node_config()