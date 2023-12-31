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
from utils import CHAINS, FILETYPES, TAGTYPES, get_chain_emoji, numeric_emoji


LOGGER = get_logger(__name__)
client = Client()
with open('emoji.json') as f: emoji = load(f)
gpg = GPG()


def sign(metadata): return sha256(bytes(dumps(metadata), 'ascii')).hexdigest()
def p2pkh_chksum(p2pkh): return hex(crc32(bytes(p2pkh, encode)))
def get_pgp_block(fp: str): return gpg.export_keys(fp, expect_passphrase=False)
def img_url(url): img = client.get(url).content; return urlsafe_b64encode(img).hex()


def gen_key(sym: str, p2pkh:str, password: str):
    def new_gpg_key(**kwargs): return gpg.gen_key(gpg.gen_key_input(**kwargs))
    email = st.text_input('Email', f'{p2pkh}@{sym.lower()}.coin', placeholder='P2PKH Address')
    
    global input_data
    input_data = {
        'name_real': p2pkh, 
        'name_email': email,
        'passphrase': password,
        'key_type': cipher, 
        'key_curve': curve
    }; return new_gpg_key(**input_data)


def encrypt_file():
    file = st.file_uploader('Image to Encrypt', type=FILETYPES)
    if file: return urlsafe_b64encode(file.read()).hex()

def display_encrypted_file():
    data = encrypt_file()
    st.write(data)


def encrypt_files(fpath, recipients, signer_fingerprint, pw:str, cipher_algorithm): 
    return gpg.encrypt_file(fpath, recipients, signer_fingerprint, passphrase=pw, symmetric=cipher_algorithm) 


def encrypt_img(img, fingerprint, password):
    return gpg.encrypt_file(img, fingerprint, passphrase=password, symmetric=True)


def display_encryptor():
    symbol = st.sidebar.selectbox('Chain', CHAINS)
    address = st.text_input('Name', placeholder='P2PKH Address')
    password = st.text_input('Password', type='password', placeholder='Passphrase')
    submit = st.button('Submit')
    if address and password and submit: master_key = gen_key(symbol, address, password)
    if submit and master_key: st.code(master_key, None)
    st.divider()


def setup():
    st.set_page_config(page_title='GnuPG', page_icon='🔐')
    st.write('# GnuPG Encryption 🔏🔐')
    st.divider()
    st.markdown('<style>footer {visibility: hidden;} #MainMenu {visibility: hidden;}</style>', True)
    
    global encode; encode = st.sidebar.selectbox('Encoding', ['ascii', 'utf-8'])
    global cipher; cipher = st.sidebar.selectbox('Cipher', ['RSA', 'DSA', 'ECDH', 'ElGamal', 'EdDSA', 'ECDSA'], 5)
    
    global curve
    bits = st.sidebar.select_slider('bits', [2048, 3072, 4096])
    c = ['nistp256', 'nistp384', 'nistp521', 'brainpoolP256r1', 'brainpoolP384r1', 'brainpoolP512r1', 'secp256k1']
    if cipher == 'ECDSA': curve = st.sidebar.selectbox('Curve', c, 6)
    elif cipher == 'EdDSA': curve = st.sidebar.selectbox('Curve', ['ed25519', 'ed448'])
    else: curve = st.sidebar.selectbox('Curve', c + ['cv25519', 'cv448'])
    
    gpg.encoding = encode
    display_encryptor()
    encrypt_file()


def encrypt_data():
    setup()
encrypt_data()