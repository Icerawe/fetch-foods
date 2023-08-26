import streamlit as st
from menu import Menu
from datetime import date, timedelta

class Delivery:
    def __init__(self, name: str, phone_number: str, key: str) -> None:
        self.name = name
        self.phone = phone_number
        self.key = key

    def select_location(self):
        location = st.text_input(
            label="ระบุสถานที่จัดส่ง", 
            placeholder="กรณีมารับที่บ้าน พิมพ์ว่าบ้านครูอายได้เลย")
        if len(location)>0:
            self.location = location
        

    def select_date(self):
        todayDate = date.today()
        nextDate = todayDate + timedelta(days=-todayDate.weekday()-1, weeks=1)
        _TH_FULL_MONTHS = [
            "มกราคม",
            "กุมภาพันธ์",
            "มีนาคม",
            "เมษายน",
            "พฤษภาคม",
            "มิถุนายน",
            "กรกฎาคม",
            "สิงหาคม",
            "กันยายน",
            "ตุลาคม",
            "พฤศจิกายน",
            "ธันวาคม",
        ]
        month_th = _TH_FULL_MONTHS[nextDate.month-1]
        self.order_date = st.selectbox(
            label="วันที่ จัดส่ง",
            options=[f'วันอาทิตย์ ที่ {nextDate.strftime(f"%d {month_th} %Y")}'],
            key=self.key
        )
        

    def conclude(self):
        if self.role=='นักเรียน':
            st.info(body="😄 รับได้ที่ร้านนม Beyond ช่วงเวลาพักเบรค \nสามารถแจ้งชื่อกับพี่พนักงานได้เลยค่ะ")
        elif self.role=='คุณครู':
            st.info(body=f"""😄 คุณครู {self.name} สามารถโยเกิร์ตได้ที่ "{self.location}" ใน {self.order_date}""")

def main(tab: str):
    name = st.text_input(label="ชื่อ", key=tab)
    phone_number = st.text_input(label="เบอร์โทร", key=tab)

    delivery = Delivery(name=name, phone_number=phone_number, key=tab)
    delivery.select_date()
    delivery.select_location()

    menu = Menu(key=f"{tab}_delivery")
    menu.show_menu()
    menu.add_bucket()
    menu.summary_order()
    menu.reset_order()
    if len(st.session_state.orders) > 0:
        menu.payment(name=name, phone_number=phone_number, method="full")  