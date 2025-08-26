import streamlit as st


st.title("Login")
username= st.text_input("Enter username")
password= st.text_input("Enter Password")
if st.button("Login"):
	st.success(f"Hello {username}")