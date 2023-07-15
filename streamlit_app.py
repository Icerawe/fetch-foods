import streamlit as st
import pandas as pd
from PIL import Image 

import notify
import time
import json
import io




if 'selected_value' not in st.session_state:
    st.session_state.selected_item = None
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'qr_code' not in st.session_state:
    st.session_state.qr_code = True


st.image('image/banner.jpeg')
if st.secrets['is_open']:
    st.text(f"""
        ลูกค้าสามารถสั่ง และ ชำระเงินได้ผ่านเว็บไซต์
        โดยสามารถรออาหารรับได้ที่ร้าน หจก.มีดีกรี/ร้านก๋วยเตี๋ยวลุง
        ติดต่อร้านค้า โทร. {st.secrets['phone']}""")

    menu = st.secrets['menu']
    st.write("\n")

    menu_list = [f"{key}: {value}฿" for key,value in menu.items()]
    selected_item = st.selectbox(label="รายการอาหาร",options=["เลือกเมนู"]+menu_list, index=0)
    selected_item = selected_item.split(":")[0]
    topping = ""
    if "กรีกโยเกิร์ต + ท๊อปปิ้ง + ผลไม้"==selected_item:
        topping = st.multiselect(
            label="เลือกท็อปปิ้งได้ 3 อย่าง",
            options=st.secrets['topping'],
            max_selections=3,
        )
        topping = ','.join(topping)

    if "กรีกโยเกิร์ต" in selected_item:
        sauce = st.radio(
            label="เลือกซอส",
            options=st.secrets['sauce'],
        )
        if sauce == 'ไม่ใส่':
            sauce = ""
        else:
            sauce = f"ราด{sauce}"
        order_name = f"{selected_item} {topping} {sauce}"
    else:
        order_name = selected_item

    quantity = st.number_input("จำนวน", min_value=1, value=1)
    add_to_cart = st.button("✅  เพิ่มรายการ")

    # add_to_cart = st.button("เพิ่มรายการอาหาร")
    if add_to_cart and selected_item != "เลือกเมนู":
        price = menu[selected_item] * quantity
        st.success(f"""* สั่งอาหารเพิ่มสามารถเลือกรายการใหม่ได้เลย""")

        st.session_state.orders.append({
            "รายการ": order_name,
            "จำนวน": quantity,
            "ราคา": price
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
        total_price = df['ราคา'].sum()
        st.info(f"รายการอาหาร {len(df)} รายการ ทั้งหมด {total_price} บาทครับ")
        remark = st.text_input(label="หมายเหตุ (ถ้ามี)")

        name = st.text_input("ชื่อลูกค้า :", )
        phone = st.text_input(label="เบอร์ติดต่อกลับ (กรณีทางร้านหาลูกค้าไม่เจอ)")
        qr_code = st.button("💰 ชำระเงิน")
        qr_code = True
        if qr_code and len(name.strip())>0:
            st.image(f"image/prompt_pay.png",width=250)
            st.image(f"https://promptpay.io/{st.secrets['prompt_pay']}/{total_price}.png", width=250)
        else:
            st.warning(f"กรุณากรอกชื่อ และ เบอร์โทร")

        uploaded_file = st.file_uploader("อับโหลด")

        done = st.button("เสร็จสิ้น")
        if done and (uploaded_file is not None):
            st.info(f"ออเดอร์ถูกส่งเรียบร้อย กรุณารออาหารสักครู่นะครับ")
            image = Image.open(uploaded_file)
            # width, height = 1290, 2134
            # image = image.resize((width, height))
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            menu_message = ""
            for order, quantity in zip(df['รายการ'], df['จำนวน']):
                menu_message += f"{order}: \t[{quantity}]\n"

            order_name = f"*คุณ {name}*"
            order_contact = f"ติดต่อ: {phone}"
            order_price = f"ยอดชำระ:{total_price} บาท"
            order_list = f"รายการอาหาร \n```{menu_message}```"
            order_remark = f"หมายเหตุ: `{remark}`"
            notify.send_message(
                message=f"{order_name}\n{order_contact}\n{order_price}\n{order_list}\n{order_remark}",
                files={"imageFile": image_bytes.getvalue()},
                token=st.secrets['token']
            )

            name = ""
            st.session_state.orders = []
            df = pd.DataFrame(st.session_state.orders)
            df.index = range(1,len(df)+1)
            time.sleep(2)
            st.experimental_rerun()
        elif uploaded_file is None:
            st.warning("กรุณาอับโหลด สลิปชำระเงินเพื่อยืนยันออเดอร์")
else:
    st.header("ขออภัยวันนี้ร้านปิดให้บริการ ขอบคุณครับ 🙏")


