import streamlit as st
import sqlite3
import pandas as pd
def read(selected_table, db):
    if selected_table == "DEALER":
        cursor = db.cursor()
        # Fetch data 
        cursor.execute("SELECT * FROM DEALER")
        data = cursor.fetchall()
        cursor.close()

        # Display the data in a Streamlit table
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        #st.markdown(df.to_html(index=False), unsafe_allow_html=True)
        st.write(df)

    elif selected_table == "MEDICINE":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM MEDICINE")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)

    elif selected_table == "QUANT":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM QUANT")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)

    elif selected_table == "STORES":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM STORES")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "HOSPITAL":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM HOSPITAL")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "RETAIL":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM RETAIL")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "TREATMENT":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM TREATMENT")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "TRANSACTIONS":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM TRANSACTIONS")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "DOCTOR":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM DOCTOR")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif selected_table == "PATIENT":
        cursor = db.cursor()
        cursor.execute("SELECT * FROM PATIENT")
        data = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.write(df)