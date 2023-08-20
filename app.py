import streamlit as st
import pandas as pd
from PIL import Image 

import requests
import notify
import time
import io

import school
import delivery

st.image('image/banner.jpg')
st.text('เลือกวิธีการจัดส่ง ⤵️')
tabs = st.tabs(["❤️‍🔥 มงฟอร์ตโรงเรียนที่เรา รัก!", "🚕 จัดส่งถึงที่ Delivery ทันใจ"])
for tab in tabs:
    with tab:
        if tab==tabs[0]:
            school.main(tab=tab)
        elif tab==tabs[1]:
            delivery.main(tab=tab)