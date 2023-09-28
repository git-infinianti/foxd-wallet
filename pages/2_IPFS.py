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
from json import loads
from PIL import Image


LOGGER = get_logger(__name__)


api_key = st.secrets['DBTOKEN']
headers = {
    'Authorization': f'Bearer {api_key}', 
    'Content-Type': 'multipart/form-data', 
    'accept': 'application/json'
}
endpoint = r'https://api.web3.storage'
client = Client(headers=headers)


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
        file_type = loaded_file.name.split('.')
    image_type = 'image/png'
    if file_type[-1] == 'jpg' or file_type[-1] == 'jpeg': image_type = 'image/jpeg'
    if st.sidebar.button('UPLOAD') and loaded_file:
        with st.spinner():
            try:
                cid = publish(loaded_file)
                st.session_state['cid'] = cid
                st.write(st.session_state['cid'])
            except:
                ret = client.post(url=endpoint + '/upload', content=loaded_file, params={'file': loaded_file.name, 'type': image_type})
                cid = loads(ret.content)
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