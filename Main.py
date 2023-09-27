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

# import torch
# import torchvision
import tempfile
import zipfile
import numpy as np

import utils
import streamlit as st
from streamlit.logger import get_logger

import uuid
from io import BytesIO
from PIL import Image

import torch
from torchvision import transforms

LOGGER = get_logger(__name__)


def image_to_tensor(image): 
    if torch.cuda.is_available(): return torch.tensor(
        image.getdata(), 
        dtype=torch.uint8, 
        device=torch.cuda.current_device()
    )
    return torch.tensor(image.getdata(), dtype=torch.uint8)


def items_from_tensor(tensor):
    for t in tensor:
        if t: yield t.item()


def setup():
    session_id = str(uuid.uuid4())
    if 'key' not in st.session_state: st.session_state['key'] = session_id
    st.set_page_config(page_title='Foxdcoin Wallet', page_icon='👋', initial_sidebar_state='expanded')
    st.write('# Welcome to Foxdcoin! 👋')
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)

    fname = ''
    utils.load_script(fname)
    if st.sidebar.button('CLEAR'):
        st.session_state['key'] = session_id
        st.experimental_rerun()
    st.sidebar.divider()


def run():
    allowed_filetypes = ['png', 'jpg', 'jpeg']
    uploaded_files = st.sidebar.file_uploader('Upload File(s)', allowed_filetypes, True, st.session_state['key'])
    for f in uploaded_files:
        data = BytesIO(f.read())
        im = Image.open(data)
        r = im.getchannel('R')
        g = im.getchannel('G')
        b = im.getchannel('B')
        a = im.getchannel('A')
        st.image(chan := [r,g,b,a])
        itensors = (image_to_tensor(img) for img in chan)
        tensors = (items_from_tensor(tensor) for tensor in itensors)
        # for t in itensors:
        #     with open(f'dataset/{f.name}_tensor.tnsr', "wb") as f:
        #         f.write(bytes(t))
        #         st.success("Image converted successfully!")


if __name__ == "__main__":
    setup()
    run()
