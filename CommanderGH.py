import streamlit as st
from auth import login, register
from database import load_products, save_order
from utils import calculate_cart_total

st.set_page_config(page_title="CommanderGh Imports", layout="wide")

menu = ["Home", "Login", "Register", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("Welcome to the CommanderGh Imports")
    st.write("Please login or register to start shopping.")

elif choice == "Register":
    register()

elif choice == "Login":
    user = login()
    if user:
        st.success(f"Logged in as {user['username']}!")
        
        products = load_products()
        cart = []
        
        st.subheader("Products")
        for p in products:
            st.write(f"{p['name']} - ${p['price']} - Stock: {p['stock']}")
            qty = st.number_input(f"Qty for {p['name']}", min_value=0, max_value=p['stock'], key=p['id'])
            if qty > 0:
                cart.append({"product": p, "quantity": qty})
        
        if cart:
            st.subheader("Cart")
            for item in cart:
                st.write(f"{item['quantity']} x {item['product']['name']} = ${item['quantity']*item['product']['price']}")
            total = calculate_cart_total(cart)
            st.write(f"**Total: ${total}**")
            if st.button("Checkout"):
                save_order(user['username'], cart, total)
                st.success("Order placed successfully!")

elif choice == "Admin":
    import admin
    admin.dashboard()
