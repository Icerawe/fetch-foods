import streamlit as st
import pandas as pd
import json

import notify
import time
from streamlit_image_select import image_select

# Menu items
menu = {
    "เอ็นไก่ทอด": 50,
    "เฟรนช์ฟราย": 50,
    "กรีกโยเกิร์ต": 50
}

# Display menu options
st.title("🍟 Jupp Gam")
st.subheader("ยินดีให้บริการค่ะ")
df_menu = pd.DataFrame([menu]).T.reset_index()
df_menu.index = range(1,len(df_menu)+1)
df_menu.columns = ["รายการ", "ราคา(บาท)"]
st.write(df_menu)

# img = image_select("ภาพประกอบ", ["image/ch.jpg", "image/ff.jpg", "image/yg.jpg"],)


# User input
name = st.text_input("ชื่อลูกค้า :")
if len(name.strip())>0:

    if 'selected_value' not in st.session_state:
        # Initialize the 'selected_value' key with the default value
        st.session_state.selected_item = None

    selected_item = st.selectbox(label="เลือกรายการอาหาร",options=[""]+list(menu.keys()))
    quantity = st.number_input("จำนวน", min_value=1, value=1)
    add_to_cart = st.button("ใส่ตะกร้าเลย :basket:")

    # Initialize session state
    if 'orders' not in st.session_state:
        st.session_state.orders = []

    # Process order
    if add_to_cart and selected_item != "":
        total_price = menu[selected_item] * quantity
        st.success(f"เพิ่ม {selected_item} {quantity} ชุด เรียบร้อยแล้ว ราคา: {total_price:.2f} บาท")
        st.session_state.orders.append({
            "รายการ": selected_item,
            "จำนวน": quantity,
            "ราคา": total_price
        })
        st.session_state.selected_item = None
        if st.session_state.selected_item is not None:
            selected_item = st.session_state.selected_item

    if len(st.session_state.orders) > 0:
        st.subheader(f"รายการของคุณ: {name}")
        df = pd.DataFrame(st.session_state.orders)
        df.index = range(1,len(df)+1)
        st.dataframe(df)
        price = df['ราคา'].sum()

        phone = st.text_input(label="เบอร์ติดต่อกลับ")
        if len(phone)==10:
            qr_code = st.button("ชำระเงิน :moneybag:")
            if qr_code:
                st.success(f"รายการอาหารทั้งหมด {len(df)} รายการ ทั้งหมด {price} บาท")

                st.image(f"image/prompt_pay.png",width=250)
                st.image(f"https://promptpay.io/{st.secrets['prompt_pay']}/{price}.png", width=250)
                st.text("กรณีชำระเงินเรียบร้อยแล้ว โปรดรออาหารสักครู่ ขอบคุณครับ")
                notify.send(
                    message=f"คุณ {name}\n {df}\n ยอดชำระ {price} บาท\n ติดต่อ {phone}",
                    token=st.secrets['token']
                )

        reset_order = st.button("ยกเลิกรายการ")
        if reset_order:
            name = ""
            st.session_state.orders = []
            st.error(f"รายการอาหารของคุณ {name} ยกเลิกเรียบร้อยแล้ว ติดต่อร้านค้าโทร: {st.phone}")
            df = pd.DataFrame(st.session_state.orders)
            df.index = range(1,len(df)+1)
            time.sleep(1)
            st.experimental_rerun()
