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
            placeholder="ระบุสถานที่ใกล้เคียง หรือ ระบุชื่ออาคาร ชั้น ห้อง เพิ่มเติม")
        

    def select_date(self):
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
        todayDate = date.today()
        date_options = list()

        for i in st.secrets['delivery_date']:
            _date = todayDate + timedelta(days=-todayDate.weekday()+i, weeks=1)
            str_date = st.secrets['order_date'][str(i)]
            month_th = _TH_FULL_MONTHS[_date.month-1]
            date_options.append(f"""{str_date} ที่ {_date.strftime(f'%d {month_th} %Y')}""")

        self.order_date = st.selectbox(
            label="วันที่จัดส่ง",
            options=date_options,
            key=self.key
        )
        

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

        if len(delivery.location) > 0:
            _name = delivery.conclude()

            menu = Menu(key=f"{tab}_delivery")
            menu.show_menu()
            menu.add_bucket()
            menu.summary_order()
            menu.reset_order()
            try:
                if menu.total_price >= 100:
                    if len(st.session_state.orders) > 0:
                        menu.payment(name=_name, phone_number=phone_number, method="full")
                else:
                    st.error(f"บริการจัดสั่ง ขั้นต่ำ 100 บาทครับ")
            except:
                pass