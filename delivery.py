import streamlit as st
from menu import Menu
from datetime import date, timedelta

class Delivery:
    def __init__(self, name: str, phone_number: str, key: str) -> None:
        self.name = name
        self.phone = phone_number
        self.key = key

    def select_location(self):
        self.location = st.text_input(
            label="ระบุสถานที่จัดส่ง", 
            placeholder="กรณีมารับที่บ้าน พิมพ์ว่าบ้านครูอายได้เลย")
        

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
        order_date = st.selectbox(
            label="วันที่ จัดส่ง",
            options=[f'วันอาทิตย์ ที่ {nextDate.strftime(f"%d {month_th} %Y")}'],
            key=self.key
        )
        self.order_date = order_date
        

    def conclude(self):
        st.info(body=f"""😄 คุณ {self.name} รับโยเกิร์ตได้ที่ >{self.location}< {self.order_date}""")
        message = f"*{self.name}*\nส่ง`{self.order_date}`\n{self.location}"
        return message

def main(tab: str):
    name = st.text_input(label="ชื่อ", key=tab)
    phone_number = st.text_input(label="เบอร์โทร", key=tab)
    
    if len(name)>0 and len(phone_number)==10:
        delivery = Delivery(name=name, phone_number=phone_number, key=tab)
        delivery.select_date()
        delivery.select_location()
        _name = delivery.conclude()

        menu = Menu(key=f"{tab}_delivery")
        menu.show_menu()
        menu.add_bucket()
        menu.summary_order()
        menu.reset_order()
        if len(st.session_state.orders) > 0:
            menu.payment(name=_name, phone_number=phone_number, method="full")  