import streamlit as st
import mysql.connector

def execute_add_quant_trigger(new_med_id, new_store_id, new_quantity_supplied, db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
            INSERT INTO QUANT(med_id, store_id, quantity)
            VALUES({new_med_id}, '{new_store_id}', {new_quantity_supplied})
            ON DUPLICATE KEY UPDATE
            quantity = quantity + {new_quantity_supplied}
        """)
        db.commit()
        cursor.close()
        st.success("add_quant trigger executed successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()

def execute_sub_quant_trigger(med_id, store_id, quantity, db):
    try:
        cursor = db.cursor()
        cursor.execute(f"""
            UPDATE QUANT 
            SET quantity = quantity - {quantity}
            WHERE med_id = {med_id} and store_id = '{store_id}'
        """)
        db.commit()
        cursor.close()
        st.success("sub_quant trigger executed successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()

def create(selected_table, db):
    if selected_table == "DEALER":
        dealer_ID = st.text_input("Dealer ID")
        dealer_name = st.text_input("Dealer Name")
        dealer_address = st.text_input("Dealer Address")
        dealer_phone = st.text_input("Dealer Phone")
        
        if st.button("Add Dealer"):
            cursor = db.cursor()
            # Use %s as placeholders for parameters in MySQL
            cursor.execute("INSERT INTO DEALER (dealer_id, name, address, phone) VALUES (%s, %s, %s, %s)",
                        (dealer_ID, dealer_name, dealer_address, dealer_phone))
            db.commit()
            cursor.close()
            st.success("Dealer created successfully")

    elif selected_table == "MEDICINE":
        med_ID = st.text_input("Medicine Id") 
        med_name = st.text_input("Medicine Name")
        composition = st.text_input("Composition")
        mfg_date = st.date_input("Manufacturing Date")
        exp_date = st.date_input("Expiration Date")
        cost_per_tab = st.number_input("Cost per Tablet")
        
        if st.button("Create Medicine"):
            cursor = db.cursor()
            # Use %s as placeholders for parameters in MySQL
            cursor.execute("INSERT INTO MEDICINE (med_id, name, composition, mfg_date, exp_date, cost_per_tab) VALUES (%s, %s, %s, %s, %s, %s)",
                        (med_ID, med_name, composition, mfg_date, exp_date, cost_per_tab))
            db.commit()
            cursor.execute("INSERT INTO QUANT (med_id, store_id, quantity) SELECT %s, store_id, 0 FROM STORES WHERE store_id NOT IN (SELECT store_id FROM QUANT WHERE med_id = %s)", (med_ID, med_ID))
            cursor.close()
            st.success("Medicine added successfully")
    
    elif selected_table == "STORES":
        store_ID = st.text_input("Store ID")
        store_name = st.text_input("Store Name")
        store_address = st.text_input("Store Address")
        contact_number = st.text_input("Store Number")
        store_man = st.text_input("Owner Name")

        if st.button("Add Store"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO STORES (store_id, name, address, contact, store_man) VALUES (%s, %s, %s, %s, %s)",
                        (store_ID, store_name, store_address, contact_number, store_man))
            db.commit()
            cursor.close()
            st.success("Store added Successfully")
    
    elif selected_table == "DOCTOR":
        doc_ID = st.text_input("Doctor ID")
        hos_ID = st.text_input("Hospital ID")
        doc_name = st.text_input("Doctor Name")

        if st.button("Add Doctor"):
            cursor=db.cursor()
            cursor.execute("INSERT INTO DOCTOR (doc_id, hos_id, doc_name) VALUES (%s, %s, %s)",
                           (doc_ID, hos_ID, doc_name))
            db.commit()
            cursor.close()
            st.success("Doctor added Successfully")

    elif selected_table == "TREATMENT":
        treat_ID = st.text_input("Treatment ID")
        pat_ID = st.text_input("Patient ID")
        hos_Id = st.text_input("Hospital ID")
        doc_Id = st.text_input("Doctor ID")
        treat_date = st.date_input("Date of Treatment")

        if st.button("Add Treatment"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO TREATMENT (treat_id, pat_id, hos_id, doc_id, treat_date) VALUES (%s, %s, %s, %s, %s)",
                           (treat_ID, pat_ID, hos_Id, doc_Id, treat_date))
            db.commit()
            cursor.close()
            st.success("Treatment added Successfully")

    elif selected_table == "PATIENT":
        pat_Id = st.text_input("Patient ID")
        pat_name = st.text_input("Patient Name")
        pat_addr = st.text_input("Patient Address")
        pat_phone = st.text_input("Patient Phone Number")

        if st.button("Add Patient"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO PATIENT (pat_id, name, address, phone) VALUES (%s, %s, %s, %s)",
                           (pat_Id, pat_name, pat_addr, pat_phone))
            db.commit()
            cursor.close()
            st.success("Patient added successfully")

    elif selected_table == "RETAIL":
        retail_id = st.text_input("Retail ID")
        med_id = st.text_input("Medicine ID")
        store_id = st.text_input("Store ID")
        dealer_id = st.text_input("Dealer ID")
        batchno = st.text_input("Batch Number")
        quantity_supplied = st.number_input("Quantity Supplied")

        if st.button("Add Retail"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO RETAIL (retail_id, med_id, store_id, dealer_id, batchno, quantity_supplied) VALUES (%s, %s, %s, %s, %s, %s)",
                        (retail_id, med_id, store_id, dealer_id, batchno, quantity_supplied))
            db.commit()

            # Call 'add_quant' trigger after inserting into RETAIL
            execute_add_quant_trigger(med_id, store_id, quantity_supplied, db)

            cursor.close()
            st.success("Retail entry added successfully")
    
    elif selected_table == "TRANSACTIONS":
        bill_id = st.text_input("Bill ID")
        pat_id = st.text_input("Patient ID")
        store_Id = st.text_input("Store ID")
        med_Id = st.text_input("Medicine ID")
        quantity = st.text_input("Medicine Quantity")
        pur_date = st.date_input("Date of Purchase")
        if st.button("Add Transaction"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO TRANSACTIONS (bill_id, pat_id, store_id, med_id, quantity, pur_date) VALUES (%s, %s, %s, %s, %s, %s)",
                        (bill_id, pat_id, store_Id, med_Id, quantity, pur_date))
            db.commit()

            # Call 'sub_quant' trigger after inserting into TRANSACTIONS
            execute_sub_quant_trigger(med_Id, store_Id, quantity, db)

            update_procedure_query = "CALL UpdateTransactionTotal(%s)"
            cursor.execute(update_procedure_query, (bill_id,))
            db.commit()

            cursor.close()
            st.success("Transaction added successfully")
    
    elif selected_table == "TREATMENT":
        treat_id = st.text_input("Treatment ID")
        pat_iD = st.text_input("Patient ID")
        hos_id = st.text_input("Hospital ID")
        doc_id = st.text_input("Doctor ID")
        treat_date = st.date_input("Treatment Date")

        if st.button("Add Treatment"):
            cursor = db.cursor()
            cursor.execute("INSERT INTO TREATMENT (treat_id, pat_id, hos_id, doc_id, treat_date) VALUES (%s, %s, %s, %s, %s)",
                        (treat_id, pat_iD, hos_id, doc_id, treat_date))
            db.commit()
            cursor.close()
            st.success("Treatment added successfully")
