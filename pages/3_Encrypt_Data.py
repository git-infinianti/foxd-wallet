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
from json import load, dumps
from gnupg import GPG

from httpx import Client
from binascii import crc32
from hashlib import sha256
from base64 import urlsafe_b64encode

gpg = GPG()
LOGGER = get_logger(__name__)
ENCODE = 'ascii'
CIPHER = 'ECDSA'
CURVE = 'secp256k1'
client = Client()
with open('emoji.json') as f: emoji = load(f)


def sign(metadata): return sha256(bytes(dumps(metadata), 'ascii')).hexdigest()
def p2pkh_chksum(p2pkh): return hex(crc32(bytes(p2pkh, ENCODE)))
def get_pgp_block(fp: str): return gpg.export_keys(fp, expect_passphrase=False)





def gen_key(sym: str, p2pkh:str, password: str):
    def new_gpg_key(**kwargs): return gpg.gen_key(gpg.gen_key_input(**kwargs))
    input_data = {
        'name_real': p2pkh, 
        'name_email': f'{p2pkh}@{str(sym).lower()}.coin',
        'passphrase': password,
        'key_type': CIPHER, 
        'key_curve': CURVE
    }
    gpg.add_subkey(fp := str(new_gpg_key(**input_data)), password, CURVE); return fp


def img_url(url): img = client.get(url).content; return urlsafe_b64encode(img).hex()


def img_file():
    img = st.image()
    with open(img, 'rb') as file: return urlsafe_b64encode(file.read()).hex()


def encrypt_files(fpath, recipients, signer_fingerprint, pw:str, cipher_algorithm): 
    return gpg.encrypt_file(fpath, recipients, signer_fingerprint, passphrase=pw, symmetric=cipher_algorithm) 


def encrypt_img(img, fingerprint, password):
    return gpg.encrypt_file(img, fingerprint, passphrase=password, symmetric=True)


def get_params():
    st.text_input('Name')
    st.text_input('Email')


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