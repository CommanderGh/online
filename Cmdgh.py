import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import time

# Set page configuration
st.set_page_config(
    page_title="CommanderGH Shopping Center",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'users' not in st.session_state:
    st.session_state.users = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Sample product data
def load_products():
    products = [
        {"id": 1, "name": "Wireless Headphones", "price": 100.00, "category": "Electronics", "stock": 50, "image": "🎧"},
        {"id": 2, "name": "Smartphone", "price": 1500.00, "category": "Electronics", "stock": 30, "image": "📱"},
        {"id": 3, "name": "Running Shoes", "price": 150.00, "category": "Fashion", "stock": 100, "image": "👟"},
        {"id": 4, "name": "Shirts Unisex", "price": 49.00, "category": "Fashion", "stock": 40, "image": "👕"},
        {"id": 5, "name": "Water Bottle", "price": 30.00, "category": "Home", "stock": 200, "image": "💧"},
        {"id": 6, "name": "Ladies pouches", "price": 50.00, "category": "Fashion", "stock": 75, "image": "🎒"},
        {"id": 7, "name": "Fitness Tracker", "price": 90.00, "category": "Electronics", "stock": 60, "image": "⌚"},
        {"id": 8, "name": "Juice Extractor", "price": 470.00, "category": "Home", "stock": 45, "image": "🍹"}
    ]
    return products

# User authentication functions
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def initialize_users():
    if not st.session_state.users:
        # Add default admin user
        st.session_state.users.append({
            "username": "admin",
            "password": make_hashes("admin123"),
            "email": "admin@example.com",
            "role": "admin",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Add default customer user
        st.session_state.users.append({
            "username": "customer",
            "password": make_hashes("customer123"),
            "email": "customer@example.com",
            "role": "customer",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Initialize users
initialize_users()

# Authentication UI
def authentication_page():
    st.title("🛒 CommanderGH online Shopping")
    
    auth_option = st.radio("Select Option", ["Login", "Register"])
    
    if auth_option == "Login":
        login_form()
    else:
        register_form()

def login_form():
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = next((u for u in st.session_state.users if u["username"] == username), None)
            if user and check_hashes(password, user["password"]):
                st.session_state.logged_in = True
                st.session_state.user_role = user["role"]
                st.session_state.user_id = username
                st.success(f"Logged in successfully as {username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")

def register_form():
    with st.form("Register"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif any(u["username"] == username for u in st.session_state.users):
                st.error("Username already exists")
            else:
                st.session_state.users.append({
                    "username": username,
                    "password": make_hashes(password),
                    "email": email,
                    "role": "customer",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Registration successful! Please login.")
                time.sleep(1)
                st.rerun()

# Navigation
def navigation():
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.user_id}!")
        
        if st.session_state.user_role == "admin":
            menu_options = ["Home", "Products", "Cart", "Admin Dashboard", "Reports", "Logout"]
        else:
            menu_options = ["Home", "Products", "Cart", "My Orders", "Logout"]
        
        selected = st.radio("Navigation", menu_options)
        
        if selected == "Logout":
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.session_state.cart = []
            st.rerun()
        else:
            st.session_state.page = selected

# Home page
def home_page():
    st.title("🛒 CommanderGH online Shopping")
    st.subheader("Welcome to our Online Store!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Browse Products**
        
        Explore our wide range of products across different categories.
        """)
    
    with col2:
        st.success("""
        **Easy Checkout**
        
        Add items to your cart and complete your purchase in just a few clicks.
        """)
    
    with col3:
        st.warning("""
        **Fast Delivery**
        
        We deliver to your doorstep within 2-3 business days.
        """)
    
    # Show featured products
    st.subheader("Featured Products")
    products = load_products()
    featured_products = products[:4]  # First 4 products as featured
    
    cols = st.columns(4)
    for idx, product in enumerate(featured_products):
        with cols[idx]:
            st.markdown(f"### {product['image']} {product['name']}")
            st.markdown(f"**${product['price']}**")
            if st.button("Add to Cart", key=f"home_{product['id']}"):
                add_to_cart(product)
                st.success(f"Added {product['name']} to cart!")

# Products page
def products_page():
    st.title("Products")
    
    products = load_products()
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        categories = ["All"] + list(set([p["category"] for p in products]))
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        sort_option = st.selectbox("Sort by", ["Price: Low to High", "Price: High to Low", "Name"])
    
    # Apply filters
    if selected_category != "All":
        filtered_products = [p for p in products if p["category"] == selected_category]
    else:
        filtered_products = products
    
    # Apply sorting
    if sort_option == "Price: Low to High":
        filtered_products.sort(key=lambda x: x["price"])
    elif sort_option == "Price: High to Low":
        filtered_products.sort(key=lambda x: x["price"], reverse=True)
    elif sort_option == "Name":
        filtered_products.sort(key=lambda x: x["name"])
    
    # Display products
    cols = st.columns(4)
    for idx, product in enumerate(filtered_products):
        col_idx = idx % 4
        with cols[col_idx]:
            st.markdown(f"### {product['image']} {product['name']}")
            st.markdown(f"**Category:** {product['category']}")
            st.markdown(f"**Price:** ${product['price']}")
            st.markdown(f"**Stock:** {product['stock']}")
            
            if st.button("Add to Cart", key=f"prod_{product['id']}"):
                add_to_cart(product)
                st.success(f"Added {product['name']} to cart!")

# Cart functions
def add_to_cart(product):
    for item in st.session_state.cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            return
    
    product_copy = product.copy()
    product_copy["quantity"] = 1
    st.session_state.cart.append(product_copy)

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item["id"] != product_id]

def cart_page():
    st.title("Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        return
    
    total = 0
    for item in st.session_state.cart:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**{item['image']} {item['name']}**")
        with col2:
            st.markdown(f"${item['price']}")
        with col3:
            st.markdown(f"Qty: {item['quantity']}")
        with col4:
            item_total = item['price'] * item['quantity']
            st.markdown(f"${item_total}")
            if st.button("Remove", key=f"remove_{item['id']}"):
                remove_from_cart(item['id'])
                st.rerun()
        total += item_total
    
    st.markdown(f"### Total: ${total}")
    
    if st.button("Proceed to Checkout"):
        checkout()

def checkout():
    if not st.session_state.cart:
        st.error("Your cart is empty!")
        return
    
    st.title("Checkout")
    
    with st.form("checkout_form"):
        st.subheader("Shipping Information")
        name = st.text_input("Full Name")
        address = st.text_area("Shipping Address")
        city = st.text_input("City")
        state = st.text_input("State")
        zip_code = st.text_input("ZIP Code")
        
        st.subheader("Payment Information")
        card_number = st.text_input("Card Number")
        exp_date = st.text_input("Expiration Date (MM/YY)")
        cvv = st.text_input("CVV", type="password")
        
        if st.form_submit_button("Complete Purchase"):
            # Process order
            order_id = len(st.session_state.orders) + 1
            order = {
                "order_id": order_id,
                "user_id": st.session_state.user_id,
                "items": st.session_state.cart.copy(),
                "total": sum(item['price'] * item['quantity'] for item in st.session_state.cart),
                "shipping_info": {
                    "name": name,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip_code": zip_code
                },
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Processing"
            }
            
            st.session_state.orders.append(order)
            st.session_state.cart = []
            
            st.success(f"Order placed successfully! Your order ID is #{order_id}")
            time.sleep(2)
            st.rerun()

# Orders page for customers
def orders_page():
    st.title("My Orders")
    
    user_orders = [order for order in st.session_state.orders if order["user_id"] == st.session_state.user_id]
    
    if not user_orders:
        st.info("You haven't placed any orders yet.")
        return
    
    for order in user_orders:
        with st.expander(f"Order #{order['order_id']} - {order['order_date']} - Total: ${order['total']} - Status: {order['status']}"):
            st.write("**Items:**")
            for item in order["items"]:
                st.write(f"{item['name']} - ${item['price']} x {item['quantity']} = ${item['price'] * item['quantity']}")
            
            st.write("**Shipping Address:**")
            st.write(f"{order['shipping_info']['name']}")
            st.write(f"{order['shipping_info']['address']}")
            st.write(f"{order['shipping_info']['city']}, {order['shipping_info']['state']} {order['shipping_info']['zip_code']}")

# Admin dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    
    # Key metrics
    total_orders = len(st.session_state.orders)
    total_revenue = sum(order["total"] for order in st.session_state.orders)
    total_users = len(st.session_state.users)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", total_orders)
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Total Users", total_users)
    col4.metric("Average Order Value", f"${avg_order_value:,.2f}")
    
    # Order trend chart
    st.subheader("Order Trends")
    if st.session_state.orders:
        orders_df = pd.DataFrame(st.session_state.orders)
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        orders_by_date = orders_df.groupby(orders_df['order_date'].dt.date).size().reset_index(name='count')
        
        fig = px.line(orders_by_date, x='order_date', y='count', title='Orders Over Time')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No orders data available for visualization.")
    
    # Recent orders
    st.subheader("Recent Orders")
    if st.session_state.orders:
        recent_orders = st.session_state.orders[-5:]  # Last 5 orders
        for order in reversed(recent_orders):
            st.write(f"**Order #{order['order_id']}** - {order['order_date']} - ${order['total']} - {order['status']}")
    else:
        st.info("No recent orders.")
    
    # User management
    st.subheader("User Management")
    users_df = pd.DataFrame(st.session_state.users)
    users_df = users_df[['username', 'email', 'role', 'created_at']]
    st.dataframe(users_df, use_container_width=True)

# Reports page
def reports_page():
    st.title("Reports")
    
    # Sales report
    st.subheader("Sales Report")
    if st.session_state.orders:
        orders_df = pd.DataFrame(st.session_state.orders)
        
        # Expand items
        items_list = []
        for order in st.session_state.orders:
            for item in order["items"]:
                item_copy = item.copy()
                item_copy["order_id"] = order["order_id"]
                item_copy["order_date"] = order["order_date"]
                items_list.append(item_copy)
        
        items_df = pd.DataFrame(items_list)
        
        # Sales by product
        product_sales = items_df.groupby('name').agg({
            'quantity': 'sum',
            'price': 'mean',
            'id': 'count'
        }).rename(columns={'id': 'orders_count'})
        
        product_sales['revenue'] = product_sales['quantity'] * product_sales['price']
        product_sales = product_sales.sort_values('revenue', ascending=False)
        
        st.write("**Top Selling Products by Revenue**")
        st.dataframe(product_sales, use_container_width=True)
        
        # Sales by category
        products_df = pd.DataFrame(load_products())
        items_with_cat = items_df.merge(products_df[['id', 'category']], left_on='id', right_on='id')
        category_sales = items_with_cat.groupby('category').agg({
            'quantity': 'sum',
            'price': 'mean'
        })
        category_sales['revenue'] = category_sales['quantity'] * category_sales['price']
        category_sales = category_sales.sort_values('revenue', ascending=False)
        
        st.write("**Sales by Category**")
        fig = px.pie(category_sales, values='revenue', names=category_sales.index, title='Revenue by Category')
        st.plotly_chart(fig, use_container_width=True)
        
        # Export options
        st.download_button(
            label="Download Sales Report (CSV)",
            data=product_sales.to_csv(),
            file_name="sales_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No sales data available for reporting.")
    
    # Inventory report
    st.subheader("Inventory Report")
    products_df = pd.DataFrame(load_products())
    st.dataframe(products_df[['name', 'category', 'price', 'stock']], use_container_width=True)
    
    low_stock = products_df[products_df['stock'] < 10]
    if not low_stock.empty:
        st.warning("**Low Stock Alert**")
        st.dataframe(low_stock[['name', 'category', 'stock']], use_container_width=True)

# Main app logic
def main():
    if not st.session_state.logged_in:
        authentication_page()
    else:
        navigation()
        
        if st.session_state.page == "Home":
            home_page()
        elif st.session_state.page == "Products":
            products_page()
        elif st.session_state.page == "Cart":
            cart_page()
        elif st.session_state.page == "My Orders":
            orders_page()
        elif st.session_state.page == "Admin Dashboard":
            if st.session_state.user_role == "admin":
                admin_dashboard()
            else:
                st.error("You don't have permission to access this page.")
        elif st.session_state.page == "Reports":
            if st.session_state.user_role == "admin":
                reports_page()
            else:
                st.error("You don't have permission to access this page.")

if __name__ == "__main__":

    main()
