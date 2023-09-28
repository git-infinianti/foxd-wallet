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
from io import BytesIO
import streamlit as st
from streamlit.logger import get_logger
import streamlit_tags as stt
from httpx import Client
from ipfs_api import publish
from json import load, loads
from PIL import Image


LOGGER = get_logger(__name__)
with open('emoji.json') as f: emoji = load(f)



api_key = st.secrets['DBTOKEN']
headers = {
    'Authorization': f'Bearer {api_key}', 
    'accept': 'application/json'
}
endpoint = 'https://api.web3.storage'
client = Client(base_url=endpoint, headers=headers)


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
    
    loaded_file = st.sidebar.file_uploader('NFT', filetypes)
    if loaded_file: 
        st.image(Image.open(BytesIO(loaded_file.read())))
        st.success('Image Loaded Successfully')
    if st.sidebar.button('UPLOAD') and loaded_file:
        with st.spinner():
            try:
                cid = publish(loaded_file)
                st.session_state['cid'] = cid
                st.write(st.session_state['cid'])
                st.success('Uploaded Successfully')
                st.session_state['cid'] = cid
                return st.session_state['cid']
            except:
                try:
                    files = {'file': loaded_file}
                    ret = client.post('/upload', files=files, headers=headers)
                    cid = loads(ret.text)
                    if 'cid' in cid.keys(): st.code(cid['cid'])
                    st.success('Uploaded Successfully')
                    st.session_state['cid'] = cid
                    return st.session_state['cid']
                except: st.error('File Failed to Upload')


def setup():
    st.set_page_config(page_title='IPFS', page_icon=emoji[79])
    st.write(f'# IPFS {emoji[79]}')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    

def ipfs():
    setup()
    upload_nft()
ipfs()