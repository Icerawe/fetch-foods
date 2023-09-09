import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime

import school
import delivery
import market

st.image('image/banner.jpg')
st.text('เลือกวิธีการจัดส่ง ⤵️')

list_menu = [
    "🚚 ตลาดนัด",
    "❤️‍🔥 มงฟอร์ตโรงเรียนที่เรา รัก!", 
    "🚕 จัดส่งถึงที่ Delivery ทันใจ", 
    "📄 ตรวจสอบคำสั่งซื้อ"
    ]
if (datetime.now() + timedelta(days=-7)).weekday()!=5:
    list_menu.pop(0)

tabs = st.tabs(list_menu)
for tab, menu in zip(tabs, list_menu):
    with tab:
        if menu=="🚚 ตลาดนัด":
            market.main(tab=tab)
        elif menu=="❤️‍🔥 มงฟอร์ตโรงเรียนที่เรา รัก!":
            school.main(tab=tab)
        elif menu=="🚕 จัดส่งถึงที่ Delivery ทันใจ":
            delivery.main(tab=tab)
        elif menu=="📄 ตรวจสอบคำสั่งซื้อ":
            st.subheader('ประวัติการสั่งซื้อ')
            show_log = pd.read_csv('log.csv')
            show_log['วันที่สั่ง'] = pd.to_datetime(show_log['วันที่สั่ง'])
            show_log = show_log.loc[show_log['วันที่สั่ง'].dt.date > (date.today() + timedelta(days=-7))]
            st.table(show_log.set_index('วันที่สั่ง').sort_index(ascending=False))
            show_log.to_csv('log.csv', index=False, encoding='utf-8-sig')