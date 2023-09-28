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
from os import getenv
from dotenv import find_dotenv, load_dotenv
from base64 import b64encode
import streamlit as st
from streamlit.logger import get_logger
import streamlit_tags as stt
from httpx import post, Headers
from ipfs_api import publish
from json import dumps
Headers()

if load_dotenv(find_dotenv()): api_key = getenv('DBTOKEN')
else: api_key = st.secrets['DBTOKEN']
st.write(api_key)
LOGGER = get_logger(__name__)
auth = {'Authorization': f'Bearer {api_key}'}
endpoint = r'https://api.web3.storage'


def encode_image():
    pass


def asset(): return {
		'icon': st.file_uploader('Icon'),
		'name': st.text_input('name'),
		'description': st.text_input('description'),
		'asset_type': st.selectbox('Asset Type', ['Unique', 'Rare', 'Common']),
		'restrictions': st.multiselect('Restrictions', []),
		'keywords': stt.st_tags()
	}


def upload_nft():
    filetypes = ['jpeg', 'jpg', 'png']
    file = st.sidebar.file_uploader('NFT', filetypes)
    if st.sidebar.button('UPLOAD') and file:
        with st.spinner():
            try:
                cid = publish(file)
                st.write(cid)
            except:
                cid = post(endpoint + '/upload', content=file, headers=auth)
                st.write(cid)
        return cid


def setup():
    st.set_page_config(page_title='IPFS', page_icon='🗃️')
    st.write('# IPFS 🗃️')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    upload_nft()


def ipfs():
    setup()
ipfs()