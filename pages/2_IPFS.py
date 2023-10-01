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
from ipfs_api import publish, pin
from json import load, loads
from PIL import Image


LOGGER = get_logger(__name__)
with open('emoji.json') as f: emoji = load(f)



api_key = st.secrets['DBTOKEN']
h = {
    'Authorization': f'Bearer {api_key}', 
    'accept': 'application/json'
}
endpoint = 'https://api.web3.storage'
client = Client(base_url=endpoint, headers=h)


def encode_image():
    pass


def asset(ftype:list[str]): return {
		'name': st.text_input('Name'),
		'description': st.text_area('Description'),
		'asset_type': st.selectbox('Asset Type', ['Main', 'Sub', 'Unique'], 2),
		'permissions': stt.st_tags(label='Permissions', text='Press Enter After Each Tag'),
        'restrictions': stt.st_tags(label='Restrictions', text='Press Enter After Each Tag'),
        'image': st.file_uploader('Image', ftype)
	}


def tag_info(label, sstate, asset_data):
    tag_desc = []
    if tags := asset_data[label]:
        st.sidebar.title(label.upper())
        for t in tags: tag_desc.append(st.sidebar.text_input(t))
        st.sidebar.divider()
    st.session_state[f'{sstate}_description'] = tag_desc


def upload_nft():
    filetypes, c = ['jpeg', 'jpg', 'png'], 'cid'
    asset_data = asset(filetypes)
    tag_info('permissions', 'permission', asset_data)
    tag_info('restrictions', 'restriction', asset_data)

    loaded_file = asset_data['image']
    if loaded_file: 
        st.success(f'Image Loaded Successfully {emoji[296]}')
        st.image(Image.open(BytesIO(loaded_file.read())))
    if st.sidebar.button('UPLOAD') and loaded_file:
        with st.spinner():
            try:
                cid = publish(loaded_file)
                st.success(f'Uploaded Successfully {emoji[296]}')
                st.session_state[c] = cid
                pin(cid)
                st.code(cid)
                return cid
            except:
                try:
                    ret = client.post('/upload', files={'file': loaded_file})
                    st.success(f'Uploaded Successfully {emoji[296]}')
                    st.session_state[c] = loads(ret.text)
                    if c in (cid := st.session_state[c]).keys(): st.code(cid[c])
                    return cid
                except: st.error(f'File Failed to Upload {emoji[292]}')


def setup():
    st.set_page_config(page_title='IPFS', page_icon=emoji[79])
    st.write(f'# IPFS {emoji[79]}')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    

def setup_session_state():
    st.session_state['cid'] = ''


def ipfs():
    setup()
    setup_session_state()
    upload_nft()
ipfs()