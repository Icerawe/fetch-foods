import streamlit as st
from menu import Menu
from datetime import date, timedelta      


def main(tab: str):
    name = st.text_input(label="ชื่อ", key=tab)
    menu = Menu(key=f"{tab}_market")
    menu.show_menu()
    menu.add_bucket()
    menu.summary_order()
    menu.reset_order()
    if len(st.session_state.orders) > 0:
        menu.payment(name=name, method="short")  