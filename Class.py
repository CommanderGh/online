import streamlit as st


st.title("Login")
username= st.text_input("enter username")
password= st.text_input("enter password")
if st.button("login"):
	st.success(f"hello {username}")
