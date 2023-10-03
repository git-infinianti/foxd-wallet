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

import inspect
import textwrap
from json import load, loads
from httpx import Client
from subprocess import run, PIPE
import streamlit as st

RPCUSER = st.secrets['RPCUSER']
RPCPASS = st.secrets['RPCPASS']

with open('emoji.json') as f: emoji = load(f)


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


def load_script(filename):
    with open(f'script/{filename}.js') as f:
        st.markdown(f'<script>{f.read()}</script>', True) 


def load_style(filename):
    with open('style/{filename}.css') as f:
        st.markdown(f'<style>{f.read()}</style>', True)


def get_chain_emoji(symbol):
    if symbol == 'FOXD': e = 768
    elif symbol == 'RVN': e = 708
    elif symbol == 'EVR': e = 312
    elif symbol == 'BTC': e = 120
    elif symbol == 'LTC': e = 524
    elif symbol == 'DOGE': e = 774
    else: e = 307
    return e

CHAINS = 'FOXD', 'RVN', 'EVR', 'BTC', 'LTC', 'DOGE', 'ETH'

def numeric_emoji(account, address, change):
    number_emotes = [
        emoji[287], emoji[286], emoji[285], emoji[284], emoji[283], 
        emoji[282], emoji[281], emoji[272], emoji[273], emoji[274]
    ]
    acc_emote = ''.join([number_emotes[int(a)] for a in str(account)])
    addr_emote = ''.join([number_emotes[int(a)] for a in str(address)])
    chng_emote = ''.join([number_emotes[int(a)] for a in str(change)])
    return acc_emote, addr_emote, chng_emote


def pipe(method: str, *args) -> dict[str] | None:
    APPEXEC = st.secrets['APPEXEC']
    res = run((APPEXEC, f'-rpcuser={RPCUSER}', f'-rpcpassword={RPCPASS}', method, *args), stdout=PIPE)

    ret = res.stdout.strip().decode('utf-8')
    if len(ret) == 0: return
    else: return loads(ret)


class RPC:
    with open('commands.json') as f: commands = load(f)
    def __init__(self, port) -> None:
        cli = Client(
            auth = (RPCUSER, RPCPASS),
            headers = {'content-type': 'application/json'}
        )
        self.__call__: function = lambda method, *params: cli.post(
            f'http://localhost:{port}', 
            json = {
                'jsonrpc': '1.0',
                'id': 'python',
                'method': method,
                'params': list(*params)
            }
        ).json()['result']

    def __dir__(self): return self.commands
    
    def __call__(self, method: str, *args) -> dict:
        return self.__call__(method, *args)
    
    def __getattr__(self, method: str):
        def command(*args): return self(method, *args)
        setattr(self, method, command)
        return lambda *args: self(method, *args)
