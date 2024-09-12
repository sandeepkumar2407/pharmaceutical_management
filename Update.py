import streamlit as st
import sqlite3

def update(selected_table, db):
    if selected_table == "DEALER":
        
        cursor = db.cursor()
        # Fetch data from the DEALER table
        cursor.execute("SELECT * FROM DEALER")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a dealer to update
        dealer_options = [f"{dealer[0]} - {dealer[1]}" for dealer in data]
        selected_dealer = st.selectbox("Select Dealer to Update", dealer_options)

        # Extract dealer ID from the selected option
        dealer_id = int(selected_dealer.split()[0])

        # Fetch existing data for the selected dealer
        cursor = db.cursor()
        cursor.execute("SELECT * FROM DEALER WHERE dealer_id=%s", (dealer_id,))
        existing_data = cursor.fetchone()
        cursor.close()

        # Display the existing data in the form
        updated_name = st.text_input("Updated Dealer Name", value=existing_data[1])
        updated_address = st.text_input("Updated Dealer Address", value=existing_data[2])
        updated_phone = st.text_input("Updated Dealer Phone", value=existing_data[3])

        if st.button("Update Dealer"):
            # Perform the update operation in the database
            cursor = db.cursor()
            cursor.execute("UPDATE DEALER SET name=%s, address=%s, phone=%s WHERE dealer_id=%s",
                        (updated_name, updated_address, updated_phone, dealer_id))
            db.commit()
            cursor.close()
            st.success("Dealer updated successfully")

    elif selected_table == "QUANT":
        
        cursor = db.cursor()
        # Fetch data from the QUANT table
        cursor.execute("SELECT * FROM QUANT")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a record to update
        quant_options = [f"{quant[0]} - {quant[1]}" for quant in data]
        selected_quant_option = st.selectbox("Select QUANT Record to Update", quant_options)

        # Extract med_id and store_id from the selected option
        selected_quant_parts = selected_quant_option.split('-')
        med_id = int(selected_quant_parts[0].strip())
        store_id = selected_quant_parts[1].strip()

        # Fetch existing data for the selected QUANT record
        cursor = db.cursor()
        cursor.execute("SELECT * FROM QUANT WHERE med_id=%s AND store_id=%s", (med_id, store_id))
        existing_data = cursor.fetchone()
        cursor.close()

        # Display the existing data in the form
        updated_quantity = st.number_input("Updated Quantity", value=existing_data[2])

        if st.button("Update QUANT Record"):
            # Perform the update operation in the database
            cursor = db.cursor()
            cursor.execute("UPDATE QUANT SET quantity=%s WHERE med_id=%s AND store_id=%s",
                        (updated_quantity, med_id, store_id))
            db.commit()
            cursor.close()
            st.success("QUANT Record updated successfully")
        
    elif selected_table == "PATIENT":

        cursor = db.cursor()
        # Fetch data from the PATIENT table
        cursor.execute("SELECT * FROM PATIENT")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a patient to update
        patient_options = [f"{patient[0]} - {patient[1]}" for patient in data]
        selected_patient = st.selectbox("Select Patient to Update", patient_options)

        # Extract patient ID from the selected option
        patient_id = int(selected_patient.split()[0])

        # Fetch existing data for the selected patient
        cursor = db.cursor()
        cursor.execute("SELECT * FROM PATIENT WHERE pat_id=%s", (patient_id,))
        existing_data = cursor.fetchone()
        cursor.close()

        # Display the existing data in the form
        updated_name = st.text_input("Updated Patient Name", value=existing_data[1])
        updated_address = st.text_input("Updated Patient Address", value=existing_data[2])
        updated_phone = st.text_input("Updated Patient Phone", value=existing_data[3])

        if st.button("Update Patient"):
            # Perform the update operation in the database
            cursor = db.cursor()
            cursor.execute("UPDATE PATIENT SET name=%s, address=%s, phone=%s WHERE pat_id=%s",
                        (updated_name, updated_address, updated_phone, patient_id))
            db.commit()
            cursor.close()
            st.success("Patient updated successfully")
    
    elif selected_table == "TRANSACTIONS":

        cursor = db.cursor()
        # Fetch data from the TRANSACTIONS table
        cursor.execute("SELECT * FROM TRANSACTIONS")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a transaction to update
        transaction_options = [f"Bill ID: {transaction[0]}, Patient ID: {transaction[1]}, Medicine ID: {transaction[3]}" for transaction in data]
        selected_transaction = st.selectbox("Select Transaction to Update", transaction_options)

        # Extract transaction IDs from the selected option
        transaction_ids = [int(id) for id in selected_transaction.split() if id.isdigit()]

        # Fetch existing data for the selected transaction
        cursor = db.cursor()
        cursor.execute("SELECT * FROM TRANSACTIONS WHERE bill_id=%s AND pat_id=%s AND med_id=%s", tuple(transaction_ids))
        existing_data = cursor.fetchone()
        cursor.close()

        # Display the existing data in the form
        updated_store_id = st.text_input("Updated Store ID", value=existing_data[2])
        updated_quantity = st.number_input("Updated Quantity", value=existing_data[4])
        updated_pur_date = st.date_input("Updated Purchase Date", value=existing_data[5])
        updated_total = st.number_input("Updated Total", value=existing_data[6])

        if st.button("Update Transaction"):
            # Perform the update operation in the database
            cursor = db.cursor()
            cursor.execute("UPDATE TRANSACTIONS SET store_id=%s, quantity=%s, pur_date=%s, total=%s WHERE bill_id=%s AND pat_id=%s AND med_id=%s",
                        (updated_store_id, updated_quantity, updated_pur_date, updated_total, *transaction_ids))
            db.commit()
            cursor.close()
            st.success("Transaction updated successfully")

