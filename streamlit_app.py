import streamlit as st
import pandas as pd
from PIL import Image 

import requests
import notify
import time
import io


def download_image(url):
    response = requests.get(url)
    return response.content


if 'selected_value' not in st.session_state:
    st.session_state.selected_item = None
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'qr_code' not in st.session_state:
    st.session_state.qr_code = True


st.image('image/banner.jpg')
if st.secrets['is_open']:
    st.text(f"""
        ลูกค้าสามารถสั่ง และ ชำระเงินได้ผ่านเว็บไซต์
        โดยสามารถพิมพ์สถานที่จัดส่งได้ที่ หมายเหตุ
        ติดต่อร้านค้า โทร. {st.secrets['phone']}""")

    menu = st.secrets['menu']
    st.write("\n")

    menu_list = [f"{key}: {value}฿" for key,value in menu.items()]
    selected_item = st.selectbox(label="รายการอาหาร",options=["เลือกเมนู"]+menu_list, index=0)
    selected_item = selected_item.split(":")[0]
    topping = ""
    if "กรีกโยเกิร์ต + ท๊อปปิ้ง + ผลไม้"==selected_item:
        topping = st.multiselect(
            label="เลือกผลไม้ได้ 3 อย่าง",
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

    if selected_item != 'เลือกเมนู':
        quantity = st.number_input("จำนวน", min_value=0, value=0)
        add_to_cart = st.button("🛒 ใส่ตะกร้า")
        if add_to_cart:
            if ("กรีกโยเกิร์ต + ท๊อปปิ้ง + ผลไม้"==selected_item) and len(topping)==0:
                st.error(f"กรุณาเลือก ท๊อปปิ้ง/ผลไม้")
            elif quantity==0:
                st.error(f"กรุณาเลือก ใส่จำนวน")
            else:
                price = menu[selected_item] * quantity
                st.success(f"""* สั่งอาหารเพิ่มสามารถเลือกรายการใหม่ได้เลย""")
                st.session_state.orders.append({
                    "รายการ": order_name,
                    "จำนวน": quantity,
                    "ราคา": price
                })
                # st.experimental_rerun()


    if len(st.session_state.orders) > 0:
        st.markdown("###### รายการอาหารที่สั่ง")
        df = pd.DataFrame(st.session_state.orders)
        df.index = range(1,len(df)+1)
        st.dataframe(df)
        remark = st.text_input(label="หมายเหตุ (ถ้ามี)")
        reset_order = st.button("❌ ยกเลิกรายการ")
        if reset_order:
            name = ""
            st.session_state.orders = []
            st.error(f"ยกเลิกรายการอาหาร เรียบร้อยแล้ว")
            df = pd.DataFrame(st.session_state.orders)
            df.index = range(1,len(df)+1)
            time.sleep(1)
            st.experimental_rerun()
        total_price = df['ราคา'].sum()
        st.info(f"รายการอาหาร {len(df)} รายการ ทั้งหมด {total_price} บาทครับ")


        name = st.text_input("ชื่อลูกค้า")
        phone = st.text_input(label="เบอร์ติดต่อกลับ")
        qr_code = st.button("💰 ชำระเงิน")
        
        if qr_code and len(name.strip())>0:
            # st.image(f"image/prompt_pay.png",width=250)
            st.text("กดค้างที่ QR-code เพื่อบันทึกรูปภาพ\nสำหรับสแกนเพื่อชำระเงิน")
            image_url = f"https://promptpay.io/{st.secrets['prompt_pay']}/{total_price}.png"
            st.image(image_url, width=250)
            # image_bytes = download_image(image_url)
            # st.download_button(label="บันทึก QR-Code", data=image_bytes, file_name="downloaded_image.png", mime="image/png")
        else:
            st.warning(f"กรุณากรอกชื่อลูกค้า")
        uploaded_file = st.file_uploader("อับโหลดสลิปชำระเงิน")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        done = st.button("✅ ยืนยันรายการ")
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


