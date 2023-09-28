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

import streamlit as st


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


def load_script(filename):
    with open(f'script/{filename}.js') as f:
        st.markdown(f'<script>{f.read()}</script>', True) 


def load_style(filename):
    with open('style/{filename}.css') as f:
        st.markdown(f'<style>{f.read()}</style>', True)

emoji = '''
🪪 🪧 🗿 ⚱️ 🪦 ⚰️ 🚬 🛒 🧯 🧽 🪥 🫧 🧼 🪣 🧻 🧺 🧹 
🧷 🧴 🪒 🪤 🛁 🚿 🪠 🚽 🪑 🛋️ 🛏️ 🪟 🪞 🛗 🚪 🩻 🩺 
🩼 🩹 💊 🩸 💉 📡 🔭 🔬 🧬 🧫 🧪 ⚗️ 🪜 🧲 🧰 🪝 ⛓️ 
🔗 🦯 ⚖️ 🗜️ ⚙️ 🔩 🪛 🔧 🪚 🛡️ 🏹 🪃 🔫 ⚔️ 🗡️ 🛠️ ⚒️ 
⛏️ 🪓 🔨 🗝️ 🔑 🔐 🔏 🔓 🔒 🗑️ 🗄️ 🗃️ ✂️ 📐 📏 🖇️ 🗓️ 
📇 📈 📉 📊 📋 📌 📍 📎 🗒️ 📆 📅 🗂️ 📂 📁 💼 📝 🖍️ 
📬 📭 📮 🗳️ ✏️ ✒️ 🖋️ 🖊️ 🖌️ 📪 📫 📦 📥 📤 📩 📨 📧 
✉️ 🪙 💴 💵 💶 💷 💸 💳 🧾 💹 💰 🏷️ 🔖 📑 🗞️ 📰 📄 
📜 📃 📔 📕 📖 📗 📘 📙 📚 📓 📒 🪔 🏮 🔦 💡 🕯️ 🔎 
🔍 📼 📹 📀 🧮 🎥 🎞️ 📽️ 🎬 📺 📷 📸 💿 💾 💽 🖲️ 🖱️ 
⌨️ 🖨️ 🖥️ 💻 📱 📲 ☎️ 📞 📟 📠 🔋 🪫 🔌 🪘 🥁 🪕 🎻 
🎺 🎹 🎸 🪗 🎷 📻 🎧 🎤 🎛️ 🎚️ 🎙️ 🎶 🎵 🎼 🔇 🔈 🔉 
🔊 📢 📣 📯 🔔 🔕 💎 💍 💄 📿 ⛑️ 🪖 🧢 🎓 🎩 👒 👑 
👢 🩰 👡 👠 🥿 🥾 👟 👞 🩴 🎒 🛍️ 👝 👜 👛 👚 👙 🩳 
🩲 🩱 🥻 👘 👗 🧦 🧥 🧤 🧣 👖 👕 👔 🦺 🥼 🥽 🕶️ 👓
'''
print(emoji.split(' '))