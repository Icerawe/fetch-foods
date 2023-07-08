import streamlit as st
import pandas as pd
import io
from PIL import Image 

import notify
import time
from streamlit_image_select import image_select

st.image('image/banner.jpeg')
st.text(f"""
    ลูกค้าสามารถสั่ง และ ชำระเงินได้ผ่านเว็บไซต์
    โดยสามารถรออาหารรับได้ที่ร้าน หจก.มีดีกรี/ร้านก๋วยเตี๋ยวลุง
    ติดต่อร้านค้า โทร. {st.secrets['phone']}""")

st.markdown("###### เมนูอาหาร")
menu = {
    "เอ็นไก่ทอด": 69,
    "เฟรนซ์ฟราย ": 59,
    "กรีกโยเกิร์ต": 50
}

df = pd.DataFrame({
    "รายการอาหาร": menu.keys(),
    "ราคา": menu.values(),
    "ภาพประกอบ": ['image/ch.jpg', 'image/ff.jpg', 'image/yg.jpg']
})
    
# Convert the image paths to HTML with <img> tags
df['ภาพประกอบ'] = df['ภาพประกอบ'].apply(lambda x: f'<img src="{x}">')
df.index = range(1, len(df)+1)
# Display the DataFrame with images in Streamlit
# st.write(df.to_html(escape=False), unsafe_allow_html=True)
st.write("\n")

if 'selected_value' not in st.session_state:
    st.session_state.selected_item = None
if 'orders' not in st.session_state:
    st.session_state.orders = []
    
selected_item = st.selectbox(label="เลือกรายการอาหาร",options=[""]+list(menu.keys()), index=0)
if selected_item == 'กรีกโยเกิร์ต':
    topping = st.multiselect(
        label="เลือกท็อปปิ้งได้ 3 อย่าง",
        options=st.secrets['topping'],
        max_selections=3,
    )

    sauce = st.radio(
        label="เลือกซอส",
        options=st.secrets['sauce'],
    )
    if sauce == 'ไม่ใส่':
        sauce = ""
    else:
        sauce = f"ราด{sauce}"
    order_name = f"{selected_item} {','.join(topping)} {sauce}"
else:
    order_name = selected_item
quantity = st.number_input("จำนวน", min_value=1, value=1)
add_to_cart = st.button("✅  เพิ่มรายการ")

# add_to_cart = st.button("เพิ่มรายการอาหาร")
if add_to_cart and selected_item != "":
    total_price = menu[selected_item] * quantity
    st.success(f"""
               เพิ่ม {selected_item} {quantity} ชุด ราคา: {total_price:.2f} บาท 
               **สั่งอาหารเพิ่มสามารถเลือกรายการใหม่ได้เลย""")

    st.session_state.orders.append({
        "รายการ": order_name,
        "จำนวน": quantity,
        "ราคา": total_price
    })

reset_order = st.button("❌ ยกเลิกรายการ")
if reset_order:
    name = ""
    st.session_state.orders = []
    st.error(f"ยกเลิกรายการอาหาร เรียบร้อยแล้ว")
    df = pd.DataFrame(st.session_state.orders)
    df.index = range(1,len(df)+1)
    time.sleep(1)
    st.experimental_rerun()

if len(st.session_state.orders) > 0:
    st.markdown("###### รายการอาหารที่สั่ง")

    df = pd.DataFrame(st.session_state.orders)
    df.index = range(1,len(df)+1)
    st.dataframe(df)
    price = df['ราคา'].sum()

    with st.form(key='order'):
        name = st.text_input("ชื่อลูกค้า :")
        phone = st.text_input(label="เบอร์ติดต่อกลับ")
        qr_code = st.form_submit_button("ชำระเงิน")

    if qr_code and len(phone)==10 and len(name.strip())>0:
        st.success(f"รายการอาหาร {len(df)} รายการ ทั้งหมด {price} บาทครับ")
        st.image(f"image/prompt_pay.png",width=250)
        st.image(f"https://promptpay.io/{st.secrets['prompt_pay']}/{price}.png", width=250)
    else:
        st.warning(f"กรุณากรอกชื่อ และ เบอร์โทร")

    uploaded_file = st.file_uploader("กรุณาอับโหลด สลิปชำระเงินเพื่อยืนยันออเดอร์")
    if uploaded_file is not None:            
        image = Image.open(uploaded_file)
        width, height = 1290, 2134
        image = image.resize((width, height))
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')

        st.info("กรณีชำระเงินเรียบร้อยแล้ว โปรดรออาหารสักครู่ ขอบคุณครับ")

