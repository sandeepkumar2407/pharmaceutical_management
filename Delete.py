import streamlit as st
import sqlite3

def delete(selected_table, db):
    if selected_table == "HOSPITAL":
        
        cursor = db.cursor()
        # Fetch data from the HOSPITAL table
        cursor.execute("SELECT * FROM HOSPITAL")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a record to delete
        hospital_options = [f"{hospital[0]} - {hospital[1]}" for hospital in data]
        selected_hospital_option = st.selectbox("Select HOSPITAL Record to Delete", hospital_options)

        # Extract hos_id from the selected option
        selected_hospital_parts = selected_hospital_option.split('-')
        hos_id = selected_hospital_parts[0].strip()

        if st.button("Delete HOSPITAL Record"):
            # Perform the delete operation in the database
            cursor = db.cursor()
            cursor.execute("DELETE FROM HOSPITAL WHERE hos_id=%s", (hos_id,))
            db.commit()
            cursor.close()
            st.success("HOSPITAL Record deleted successfully")

    elif selected_table == "DEALER":
        
        cursor = db.cursor()
        # Fetch data from the DEALER table
        cursor.execute("SELECT * FROM DEALER")
        data = cursor.fetchall()
        cursor.close()

        dealer_options = [f"{dealer[0]} - {dealer[1]}" for dealer in data]
        selected_dealer_option = st.selectbox("Select DEALER Record to Delete", dealer_options)

        selected_dealer_parts = selected_dealer_option.split('-')
        dealer_id = int(selected_dealer_parts[0].strip())

        if st.button("Delete DEALER Record"):
            # Perform the delete operation in the database
            cursor = db.cursor()
            cursor.execute("DELETE FROM DEALER WHERE dealer_id=%s", (dealer_id,))
            db.commit()
            cursor.close()
            st.success("DEALER Record deleted successfully")

    elif selected_table == "STORES":

        cursor = db.cursor()
        cursor.execute("SELECT * FROM STORES")
        data = cursor.fetchall()
        cursor.close()

        store_options = [f"{stores[0]}-{stores[1]}" for stores in data]
        selected_stores_option = st.selectbox("SELECT STORE Record to Delete", store_options)

        selected_store_parts = selected_stores_option.split('-')
        store_id = selected_store_parts[0].strip()

        if st.button("Delete STORE Record"):
            try:
                # Check for foreign key constraints and delete related records in the CONTRACT table
                cursor = db.cursor()
                cursor.execute("DELETE FROM CONTRACT WHERE store_id = %s", (store_id,))
                db.commit()

                # Now you can delete the record from the STORES table
                cursor.execute("DELETE FROM STORES WHERE store_id = %s", (store_id,))
                db.commit()
                cursor.close()
                st.success("STORES Record deleted successfully")
            except sqlite3.Error as e:
                st.error(f"Error deleting record: {str(e)}")

    elif selected_table == "TREATMENT":

        cursor = db.cursor()
        # Fetch data from the TREATMENT table
        cursor.execute("SELECT * FROM TREATMENT")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a record to delete
        treatment_options = [f"{treatment[0]} - {treatment[1]} - {treatment[2]} - {treatment[3]} - {treatment[4]}" for treatment in data]
        selected_treatment_option = st.selectbox("Select TREATMENT Record to Delete", treatment_options)

        # Extract treat_id from the selected option
        selected_treatment_parts = selected_treatment_option.split('-')
        treat_id = selected_treatment_parts[0].strip()

        if st.button("Delete TREATMENT Record"):
            # Perform the delete operation in the database
            cursor = db.cursor()
            cursor.execute("DELETE FROM TREATMENT WHERE treat_id=%s", (treat_id,))
            db.commit()
            cursor.close()
            st.success("TREATMENT Record deleted successfully")

    elif selected_table == "DOCTOR":

        cursor = db.cursor()
        # Fetch data from the DOCTOR table
        cursor.execute("SELECT * FROM DOCTOR")
        data = cursor.fetchall()
        cursor.close()

        # Display a dropdown to select a record to delete
        doctor_options = [f"{doctor[0]} - {doctor[1]} - {doctor[2]}" for doctor in data]
        selected_doctor_option = st.selectbox("Select DOCTOR Record to Delete", doctor_options)

        # Extract doc_id from the selected option
        selected_doctor_parts = selected_doctor_option.split('-')
        doc_id = selected_doctor_parts[0].strip()

        if st.button("Delete DOCTOR Record"):
            # Perform the delete operation in the database
            cursor = db.cursor()
            cursor.execute("DELETE FROM DOCTOR WHERE doc_id=%s", (doc_id,))
            db.commit()
            cursor.close()
            st.success("DOCTOR Record deleted successfully")