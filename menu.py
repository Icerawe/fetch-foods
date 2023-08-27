import streamlit as st
import pandas as pd
from PIL import Image 
from typing import Literal

import requests
import notify
import time
import io


class Menu:
    def __init__(self, key:str) -> None:
        self.key = key
        if 'orders' not in st.session_state:
            st.session_state.orders = []

    def show_menu(self):
        col_menu, col_sauce = st.columns(2)
        with col_menu:
            self.menu = st.secrets['menu']
            menu_list = [f"{key}: {value}฿" for key,value in self.menu.items()]
            selected_item = st.radio(
                label="เมนู", options= menu_list, index=0, key=self.key+"col_menu"
            )
            self.selected_item = selected_item.split(":")[0]

        if self.selected_item == 'กรีกโยเกิร์ตล้วนๆ (200g)':
            self.sauce = ""
        else:
            with col_sauce:
                self.sauce = st.radio(
                    label="เลือกซอส",
                    options=st.secrets['sauce'],
                    key=self.key+"col_sauce"
                )

        self.topping = []
        if "กรีกโยเกิร์ต + ท๊อปปิ้ง + ผลไม้" in self.selected_item:
            self.topping = st.multiselect(
                label="เลือกผลไม้ (สูงสุดได้ 3 ชนิด)",
                options=st.secrets['topping'],
                max_selections=3,
                key=self.key
            )

        topping = ','.join(self.topping)
        self.order = f"{self.selected_item} {topping} {self.sauce}"
    
    def add_bucket(self):
        quantity = st.slider("จำนวน", min_value=0, max_value=5, value=1, key=self.key+'quantity')
        add_bucket = st.button("🛒 ใส่ตะกร้า", key=self.key+'bucket')
        if add_bucket:
            if ("กรีกโยเกิร์ต + ท๊อปปิ้ง + ผลไม้" in self.selected_item) and len(self.topping)==0:
                st.error(f"กรุณาเลือก ท๊อปปิ้ง/ผลไม้")
            elif quantity==0:
                st.error(f"กรุณาเลือก ใส่จำนวน")
            else:
                price = self.menu[self.selected_item] * quantity
                st.session_state.orders.append({
                    "รายการอาหารที่สั่ง": self.order,
                    "จำนวน": quantity,
                    "ราคา": price
                })
                st.success(f"""* สั่งอาหารเพิ่มสามารถเลือกรายการใหม่ได้เลยครับ""")

    def reset_order(self):
        reset_order = st.button("❌ ยกเลิกรายการ", key=self.key+'reset')
        if reset_order:
            st.session_state.orders = []
            st.error(f"ยกเลิกรายการอาหาร เรียบร้อยแล้ว")
            time.sleep(1)
            st.experimental_rerun()
    
    def summary_order(self):
        if len(st.session_state.orders) > 0:
            self.df = pd.DataFrame(st.session_state.orders)
            self.df.index = range(1,len(self.df)+1)
            st.subheader("🛒 ตะกร้าของฉัน")
            st.table(self.df)
            self.remark = st.text_input(label="หมายเหตุ (ถ้ามี)", key=self.key+'remark')

            self.total_price = self.df['ราคา'].sum()
            st.info(f"รายการอาหาร {len(self.df)} รายการ ทั้งหมด {self.total_price} บาทครับ")

    def payment(self, name:str, phone_number:str, method:str="full"):
        menu_message = ""
        for order, quantity in zip(self.df['รายการอาหารที่สั่ง'], self.df['จำนวน']):
            menu_message += f"{order}: \t[{quantity}]\n"

        order_name = f"คุณ {name}"
        order_contact = f"ติดต่อ: {phone_number}"
        order_price = f"ยอดชำระ:{self.total_price} บาท"
        order_list = f"รายการอาหาร \n```{menu_message}```"
        order_remark = f"หมายเหตุ: `{self.remark}`"

        qr_code = st.button("💰 ชำระเงิน", key=self.key+'payment')
        if qr_code and len(name.strip())>0:
            st.text("กดค้างที่ QR-code เพื่อบันทึกรูปภาพ\nสำหรับสแกนเพื่อชำระเงิน")
            image_url = f"https://promptpay.io/{st.secrets['prompt_pay']}/{self.total_price}.png"
            st.image(image_url, width=250)
            notify.send_message(
                message=f"{order_name}\n{order_contact}\n{order_price}\n{order_list}\n{order_remark}",
                token=st.secrets['token']
            )
        
        if method=='full':
            uploaded_file = st.file_uploader("อับโหลดสลิปชำระเงิน", key=self.key+'upload')
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            done = st.button("✅ ยืนยันรายการ", key=self.key+'done')
            if done and (uploaded_file is not None):
                st.info(f"ออเดอร์ถูกส่งเรียบร้อย กรุณารอรับสินค้า {name}")
                image = Image.open(uploaded_file)
                scale = int(image.size[1]*1280/image.size[0])
                image = image.resize((1280, scale))
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='PNG')

                notify.send_message(
                    message=f"สลิปยืนยันของ คุณ {name}",
                    files={"imageFile": image_bytes.getvalue()},
                    token=st.secrets['token']
                )
                
                st.session_state.orders = []
                time.sleep(1)
                st.experimental_rerun()
            elif uploaded_file is None:
                st.warning("กรุณาอับโหลด สลิปชำระเงินเพื่อยืนยันออเดอร์")