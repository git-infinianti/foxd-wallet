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

import torch
import numpy as np

import streamlit as st
from streamlit.logger import get_logger

import uuid
from io import BytesIO
from PIL import Image

LOGGER = get_logger(__name__)

def setup():
    session_id = str(uuid.uuid4())
    if "key" not in st.session_state: st.session_state["key"] = session_id
    st.set_page_config(
        page_title="Foxdcoin Wallet",
        page_icon="👋",
        initial_sidebar_state="expanded",
    )
    st.write("# Welcome to Foxdcoin! 👋")
    st.markdown(
        "<style> footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>",
        unsafe_allow_html=True,
    )
    if st.sidebar.button('clear'):
        st.session_state["key"] = session_id
        st.experimental_rerun()

def run():
    setup()
    uploaded_files = st.sidebar.file_uploader('Upload File(s)', 'png', True, st.session_state["key"])
    for f in uploaded_files:
        im = Image.open(BytesIO(f.read()))
        r = im.getchannel('R')
        g = im.getchannel('G')
        b = im.getchannel('B')
        a = im.getchannel('A')
        
        channel = []
        def gid(image): return image.getdata()
        for img in (r,g,b,a): 
            channel.append(gid(img))
            st.image(img)
        

if __name__ == "__main__":
    run()
