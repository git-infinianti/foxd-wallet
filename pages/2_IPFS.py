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
from io import BytesIO
from dotenv import find_dotenv, load_dotenv
import streamlit as st
from streamlit.logger import get_logger
import streamlit_tags as stt
from httpx import post
from ipfs_api import publish
from json import loads
from PIL import Image


if load_dotenv(find_dotenv()): api_key = getenv('DBTOKEN')
else: api_key = st.secrets['DBTOKEN']
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
    filetypes = ['jpeg', 'jpg', 'png', 'gif', 'webp']
    file = st.sidebar.file_uploader('NFT', filetypes)
    if file: st.image(Image.open(BytesIO(file.read())))
    if st.sidebar.button('UPLOAD') and file:
        with st.spinner():
            try:
                cid = publish(file)
                st.session_state['cid'] = cid
                st.write(st.session_state['cid'])
            except:
                cid = post(url=endpoint + '/upload', files=file, headers=auth)
                cid = loads(cid.content)
                st.session_state['cid'] = cid
                st.write(cid)
            return cid


def setup():
    st.set_page_config(page_title='IPFS', page_icon='🗃️')
    st.write('# IPFS 🗃️')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    


def ipfs():
    setup()
    upload_nft()
ipfs()