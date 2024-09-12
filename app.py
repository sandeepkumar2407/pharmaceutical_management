import streamlit as st
from Create import create
from Read import read
from Update import update
from Delete import delete
from connection import fun
import pandas as pd

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.allowed_tables = []

store_user = User(username="store", password="store", role="store")
store_user.allowed_tables = ["MEDICINE", "HOSPITAL", "QUANT", "DEALER", "STORES", "RETAIL"]

hospital_user = User(username="hospital", password="hospital", role="hospital")
hospital_user.allowed_tables = ["HOSPITAL", "PATIENT", "DOCTOR", "TREATMENT", "TRANSACTIONS","MEDICINE","QUANT"]

doctor_user = User(username="doctor", password="doctor", role="doctor")
doctor_user.allowed_tables = ["DOCTOR", "PATIENT", "TREATMENT"]

user_managed_tables = {
    "MEDICINE": ["Read", "Create"],
    "HOSPITAL": ["Read", "Delete"],
    "QUANT": ["Read", "Update"],
    "DEALER": ["Read", "Create", "Update", "Delete"],
    "STORES": ["Read", "Create", "Delete"],
    "RETAIL": ["Read","Create"],
    "PATIENT": ["Read", "Create", "Update"],
    "DOCTOR": ["Read", "Create", "Delete"],
    "TREATMENT": ["Read", "Create", "Delete"],
    "TRANSACTIONS": ["Read","Create","Update"],
    "TREATMENT":["Read","Create"]
}

db = fun()
st.set_page_config(
    page_title="Pharmaceutical Management System",
    page_icon="🌿",
    layout="wide"
)

# Add to the top of your script
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.login_button_clicked = False

# Check if user is not logged in
if st.session_state.user is None:

    st.markdown(
    '<p style="color: #FFDAB9; font-size: 36px; font-family: Cambria, serif;"><i>DATURA ENTERPRISES</i></p>',
    unsafe_allow_html=True
    )
    image_path = r'D:\Study\SEM-5\DBMS\Project\datura.jpg'  # Replace with your image path
    image = open(image_path, 'rb').read()
    st.image(image, use_column_width=True)

    st.title("Please Login")
    username_input = st.text_input("Username:")
    password_input = st.text_input("Password:", type="password")

    login_button_clicked = st.button("Login")

    if login_button_clicked and not st.session_state.login_button_clicked:
        users = [store_user, hospital_user, doctor_user]
        for user in users:
            if username_input == user.username and password_input == user.password:
                st.session_state.user = user
                st.success(f"Logged in as {user.role} user.")
                st.session_state.login_button_clicked = True
                st.experimental_rerun()  
                break
        else:
            st.error("Invalid username or password.")
else:
    user_role = st.session_state.user.role
    allowed_tables = st.session_state.user.allowed_tables

    st.sidebar.subheader(f"Tables Managed by {st.session_state.user.role}")
    selected_table = st.sidebar.selectbox("Select Table", allowed_tables)

    available_operations = user_managed_tables[selected_table]

    st.sidebar.subheader("Operations")
    operation = st.sidebar.selectbox("Select Operation", available_operations)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.login_button_clicked = False
        st.experimental_rerun() 
        st.info("Logged out successfully. Please log in again.")

    if user_role == "store":
        if selected_table == "RETAIL":
            if operation == "Read" and "Read" in available_operations:
                st.subheader(f"View Details from RETAIL")
                read(selected_table, db)
                if st.button("Major Details"):
                    st.subheader("Bulk Quantity Retail and Dealer")
                    try:
                        cursor = db.cursor()
                        query = """
                        SELECT B.dealer_id, A.name, A.phone, B.retail_id, B.store_id, B.med_id, B.quantity_supplied 
                        FROM RETAIL B, DEALER A
                        WHERE A.dealer_id = B.dealer_id AND EXISTS (
                            SELECT B.dealer_id
                            FROM DEALER A
                            WHERE A.dealer_id = B.dealer_id AND B.quantity_supplied >= 100
                        )
                        ORDER BY A.dealer_id;
                        """
                        cursor.execute(query)
                        query_result = cursor.fetchall()
                        df = pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close()
                if st.button("Unsold Medicines"):
                    st.subheader("List of Unsold Medicies")
                    try:
                        cursor = db.cursor()
                        query1 = """
                        SELECT DISTINCT(A.store_id), A.name, D.med_id, D.quantity
                        FROM STORES A, RETAIL B, TRANSACTIONS C, QUANT D
                        WHERE D.store_id = A.store_id AND A.store_id=B.store_id AND B.store_id NOT IN 
                        (
                            SELECT DISTINCT(C.store_id)
                            FROM TRANSACTIONS C
                        );
                        """
                        cursor.execute(query1)
                        query1_result = cursor.fetchall()
                        df = pd.DataFrame(query1_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close() 
            else:
                create(selected_table,db)
        else:
            if operation == "Create" and "Create" in available_operations:
                st.subheader("Enter Details for {}".format(selected_table))
                create(selected_table, db)
            elif operation == "Read" and "Read" in available_operations:
                st.subheader("View Details from {}".format(selected_table))
                read(selected_table, db)
            elif operation == "Update" and "Update" in available_operations:
                st.subheader('Update Details in {}'.format(selected_table))
                update(selected_table, db)
            elif operation == "Delete" and "Delete" in available_operations:
                st.subheader('Delete Details in {}'.format(selected_table))
                delete(selected_table, db)
            else:
                st.subheader("About Tasks")
        
    elif user_role == "hospital":
        if selected_table == "TRANSACTIONS":
            if operation == "Read" and "Read" in available_operations:
                st.subheader(f"View Details from TRANSACTIONS")
                read(selected_table, db)
                def execute_stored_procedure_for_all():
                    try:
                        if db.is_connected():
                            cursor = db.cursor()
                            cursor.callproc('UpdateTransactionTotalForAll')
                            db.commit()
                            st.success("Total Updated Successfully for all bill_ids.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        if 'cursor' in locals():
                            cursor.close()
                if st.button("Caluculate Bill Total"):
                    execute_stored_procedure_for_all()

                if st.button("STATS"):
                    st.subheader("Display the daily transaction statistics of every store")
                    try:
                        cursor = db.cursor()
                        query = """
                        SELECT ANY_VALUE(a.store_id) as store_id, ANY_VALUE(b.name) as store_name, ANY_VALUE(COUNT(a.store_id)) as No_of_Trancts, ANY_VALUE(AVG(a.total)) as AVG_amt, ANY_VALUE(MIN(a.total)) as MIN_amt, ANY_VALUE(MAX(a.total)) as MAX_amt, ANY_VALUE(a.pur_date)as Purch_Date
                        FROM TRANSACTIONS a JOIN STORES b
                        ON a.store_id = b.store_id
                        GROUP BY(a.pur_date)
                        ORDER BY a.pur_date DESC;
                        """
                        cursor.execute(query)
                        query_result = cursor.fetchall()
                        df = pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close()

                if st.button("Patient Details"):
                    st.subheader("Patient Details Who Bought Medicines")
                    try:
                        cursor = db.cursor()
                        query1 = """
                        SELECT DISTINCT A.pat_id AS patient_id, A.name AS patient_name, A.phone AS patient_phone,
                        C.hos_id AS hospital_id, E.name AS hospital_name, D.store_id AS store_id, F.name AS store_name
                        FROM PATIENT A, TREATMENT B, CONTRACT C, TRANSACTIONS D, HOSPITAL E, STORES F
                        WHERE A.pat_id = D.pat_id AND E.hos_id = C.hos_id AND F.store_id = D.store_id AND (D.pat_id, C.hos_id, D.store_id) IN
                        (
                            SELECT B.pat_id, B.hos_id, C.store_id
                            FROM TREATMENT B, CONTRACT C
                            WHERE B.hos_id = C.hos_id
                        );
                        """
                        cursor.execute(query1)
                        query1_result = cursor.fetchall()
                        df = pd.DataFrame(query1_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close()
            elif operation == "Create" and "Create" in available_operations:
                st.subheader("Enter Details for {}".format(selected_table))
                create(selected_table, db)
            else:
                st.subheader('Update Details in {}'.format(selected_table))
                update(selected_table, db)
        else:
            if operation == "Create" and "Create" in available_operations:
                st.subheader("Enter Details for {}".format(selected_table))
                create(selected_table, db)
            elif operation == "Read" and "Read" in available_operations:
                st.subheader("View Details from {}".format(selected_table))
                read(selected_table, db)
            elif operation == "Update" and "Update" in available_operations:
                st.subheader('Update Details in {}'.format(selected_table))
                update(selected_table, db)
            elif operation == "Delete" and "Delete" in available_operations:
                st.subheader('Delete Details in {}'.format(selected_table))
                delete(selected_table, db)
            else:
                st.subheader("About Tasks")

    else:
        if selected_table == "PATIENT":
            if operation == "Read" and "Read" in available_operations:
                st.subheader(f"View Details from PATIENT")
                read(selected_table, db)
                if st.button("Patient Medicine"):
                    st.subheader("Patient Medicine Details")
                    try:
                        cursor = db.cursor()
                        query = """
                        SELECT  A.store_id, A.med_id, C.name, A.dealer_id, C.exp_date, B.pur_date, B.pat_id
                        FROM MEDICINE C JOIN TRANSACTIONS B JOIN RETAIL A
                        ON B.med_id = A.med_id and C.med_id = B.med_id AND
                        C.med_id = A.med_id and B.store_id = A.store_id
                        ORDER BY A.store_id;
                        """
                        cursor.execute(query)
                        query_result = cursor.fetchall()
                        df = pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close()
                if st.button("Todays Consultants"):
                    st.header("List of Patients Treated Today")
                    try:
                        cursor=db.cursor()
                        query1 = """
                        SELECT DISTINCT(A.pat_id) , name, B.med_id
                        FROM PATIENT A, TRANSACTIONS B, TREATMENT C
                        WHERE A.pat_id = B.pat_id AND B.pur_date = CURRENT_date() AND B.pat_id IN
                        (
                            SELECT C.pat_id
                            FROM TREATMENT C
                            WHERE C.treat_date = CURRENT_date()
                        );
                        """
                        cursor.execute(query1)
                        query1_result = cursor.fetchall()
                        df = pd.DataFrame(query1_result, columns=[desc[0] for desc in cursor.description])
                        st.write(df)
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        cursor.close()
            elif operation == "Create" and "Create" in available_operations:
                st.subheader("Enter Details for {}".format(selected_table))
                create(selected_table,db)
            else:
                st.subheader('Update Details in {}'.format(selected_table))
                update(selected_table, db)
        else:
            if operation == "Create" and "Create" in available_operations:
                st.subheader("Enter Details for {}".format(selected_table))
                create(selected_table, db)
            elif operation == "Read" and "Read" in available_operations:
                st.subheader("View Details from {}".format(selected_table))
                read(selected_table, db)
            elif operation == "Update" and "Update" in available_operations:
                st.subheader('Update Details in {}'.format(selected_table))
                update(selected_table, db)
            elif operation == "Delete" and "Delete" in available_operations:
                st.subheader('Delete Details in {}'.format(selected_table))
                delete(selected_table, db)
            else:
                st.subheader("About Tasks")
            
st.markdown(
    '<div style="position: fixed; bottom: 10px; right: 10px; text-align: right; padding-right: 50px;">'
    '<p style="font-family: Georgia, serif; font-size: 20px; color: red;"><i>Designed by Datura</i></p>'
    '</div>',
    unsafe_allow_html=True
)