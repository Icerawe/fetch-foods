import streamlit as st
from menu import Menu
from datetime import date, timedelta

class School:
    def __init__(self, name: str, phone_number: str, key: str) -> None:
        self.name = name
        self.phone = phone_number
        self.key = key

    def select_role(self):
        role = st.radio(
            label="ใครกันน้า ?",
            options=['นักเรียน', 'คุณครู'],
            key=self.key
        )
        if role == 'นักเรียน':
            location = 'ร้านนม Beyond'
        elif role == 'คุณครู':
            location = st.selectbox(
                label="สถานที่จัดส่ง",
                options=[
                    'ห้องพักครู ม.1', 'ห้องพักครู ม.2', 'ห้องพักครู ม.3',
                    'ห้องพักครู ม.4', 'ห้องพักครู ม.5', 'ห้องพักครู ม.6',
                    'ห้องวิชาการ', 'ห้องสมุด', 'อื่นๆ (ระบุ)'
                ]
            )
            if location == 'อื่นๆ (ระบุ)':
                location = st.text_input(label="ระบุสถานที่จัดส่ง")
        self.role = role
        self.location = location
        

    def select_date(self):
        todayDate = date.today()
        nextDate = todayDate + timedelta(days=-todayDate.weekday()+1, weeks=1)
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
            label="วันที่จัดส่ง",
            options=[f'วันอังคาร ที่ {nextDate.strftime(f"%d {month_th} %Y")}'],
            key=self.key
        )
        

    def conclude(self):
        message = f"*{self.name}*\nส่ง`{self.order_date}`"
        if self.role=='นักเรียน':
            st.info(body=f"""
                😄 คุณ {self.name} รับโยเกิร์ตได้ที่ > ร้านนมBeyond (ช่วงพักเบรค) <
                โดยแจ้งชื่อกับพี่พนักงานได้เลยค่ะ 
            """)
        elif self.role=='คุณครู':
            st.info(body=f"""😄 คุณครู {self.name} รับโยเกิร์ตได้ที่ >{self.location}< """)
            message = f"{message}\n{self.location}"
        return message

def main(tab: str):
    name = st.text_input(label="ชื่อ", key=tab)
    phone_number = st.text_input(label="เบอร์โทร", key=tab)
    
    if len(name)>0 and len(phone_number)==10:
        school = School(name=name, phone_number=phone_number, key=tab)
        school.select_role()
        school.select_date()
        _name = school.conclude()
        
        menu = Menu(key=f"{tab}_school")
        menu.show_menu()
        menu.add_bucket()
        menu.summary_order()
        menu.reset_order()
        if len(st.session_state.orders) > 0:
            menu.payment(name=_name, phone_number=phone_number, method="full")  