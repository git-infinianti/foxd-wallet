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
from ipfs_api import publish


LOGGER = get_logger(__name__)


def upload_nft():
    filetypes = ['jpeg', 'jpg', 'png']
    file = st.sidebar.file_uploader('NFT', filetypes)
    if st.sidebar.button('UPLOAD') and file:
        with st.spinner():
            cid = publish(file)
            st.text(cid)
        return cid


def setup():
    st.set_page_config(page_title='IPFS', page_icon='🗃️')
    st.write('# IPFS 🗃️')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    if st.sidebar.button('REFRESH'): st.rerun()
    upload_nft()


def ipfs():
    setup()
ipfs()