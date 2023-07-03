import streamlit as st
import pandas as pd

st.title("Food Ordering App")

# Menu items
menu = {
    "Burger": 10.99,
    "Pizza": 12.99,
    "Salad": 8.99
}

# Initialize session state
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Display menu options
st.subheader("Menu:")
for item, price in menu.items():
    st.write(f"{item}: ${price}")

# User input
name = st.text_input("Enter your name:")

st.subheader("Place your order:")
selected_item = st.selectbox("Select an item", list(menu.keys()))
quantity = st.number_input("Quantity", min_value=1, value=1)
add_to_cart = st.button("Add to Cart")

# Process order
if add_to_cart:
    total_price = menu[selected_item] * quantity
    st.success(f"Added {quantity} {selected_item}(s) to the cart. Total: ${total_price:.2f}")
    st.session_state.orders.append({
        "Item": selected_item,
        "Quantity": quantity,
        "Total Price": total_price
    })


reset_order = st.button("Reset Order")
if reset_order:
    st.session_state.orders = []
    st.error(f"reset ")

st.subheader(f"All Orders: {name}")
if len(st.session_state.orders) > 0:
    df = pd.DataFrame(st.session_state.orders)
    st.dataframe(df)
else:
    st.write("No orders yet.")

qr_code = st.button("qr_code")
if qr_code:
    st.image("config/qr_code.png", width=360)
