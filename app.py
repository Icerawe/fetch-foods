import streamlit as st
import pandas as pd
from datetime import date, timedelta

import school
import delivery

st.image('image/banner.jpg')
st.text('เลือกวิธีการจัดส่ง ⤵️')
tabs = st.tabs(["❤️‍🔥 มงฟอร์ตโรงเรียนที่เรา รัก!", "🚕 จัดส่งถึงที่ Delivery ทันใจ", "📄 ตรวจสอบคำสั่งซื้อ"])
for tab in tabs:
    with tab:
        if tab==tabs[0]:
            school.main(tab=tab)
        elif tab==tabs[1]:
            delivery.main(tab=tab)
        elif tab==tabs[2]:
            st.subheader('ประวัติการสั่งซื้อ')
            show_log = pd.read_csv('log.csv')
            show_log['วันที่สั่ง'] = pd.to_datetime(show_log['วันที่สั่ง'])
            show_log = show_log.loc[show_log['วันที่สั่ง'].dt.date > (date.today() + timedelta(days=-7))]
            st.table(show_log.set_index('วันที่สั่ง').sort_index(ascending=False))
            show_log.to_csv('log.csv', index=False, encoding='utf-8-sig')