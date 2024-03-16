from dependancies import *
from mysql_connection import *
import logging

logging.basicConfig(filename='activity.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_activity(action, user_id):
    """
    Logs admin activities.

    Args:
        action (str): The action performed by the admin.
        user_id (int): The ID of the admin performing the action.
    """
    log_message = f"Admin with ID {user_id} performed action: {action}"
    logging.info(log_message)


cur.execute("""
CREATE TABLE IF NOT EXISTS users_db (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    dob TEXT,
    email TEXT,
    password TEXT,
    reset_token TEXT,
    reset_expiration TIMESTAMP
)
""")
connection.commit()
result = cur.fetchall()

def get_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

'''def login():
    user_input = st.radio('Please select an option:', options=['Sign In', 'Sign Up'], horizontal=True)
    
    if user_input == 'Sign In':
        sign_in()
        if get_session_state().user:
            user_dashboard()
             # Upload data file section
            st.header('Upload Data File')
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

            if uploaded_file is not None:
                upload_data(uploaded_file)
    
    elif user_input == 'Sign Up':
        sign_up()'''

def login():
    user_input = st.radio('Please select an option:', options=['Sign In', 'Sign Up', 'Admin Sign In'], horizontal=True)
    
    if user_input == 'Sign In':
        sign_in()
        if get_session_state().user:
            if get_session_state().user[4] == 'admin@gmail.com':  # Check if the user is admin
                admin_dashboard()
            else:
                user_dashboard()
                st.subheader("Upload Data File (Limit: 10MB per file)")
                uploaded_file = st.file_uploader("Choose a CSV file (Max 10MB)", type="csv", accept_multiple_files=False)
                



                upload_data(uploaded_file)
    
    elif user_input == 'Sign Up':
        sign_up()
    
    elif user_input == 'Admin Sign In':
        admin_sign_in()

def admin_sign_in():
    st.header('Admin Login')
    email_login = st.text_input('Enter your email:', placeholder="admin@gmail.com")
    password_login = st.text_input('Enter your Password:', placeholder="Password", type="password")
    
    if st.button("Admin Login"):
        # Authenticate admin credentials
        if email_login == 'admin@gmail.com' and password_login == 'malik123':  # Replace with actual admin credentials
            st.success("Admin Login successful.")
            admin_dashboard()
        else:
            st.error("Invalid email or password.")

def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_reset_email(email, token):
    
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "cognimindai@gmail.com"
    smtp_password = ""

    
    sender_email = "cognimindai@gmail.com"
    recipient_email = email
    subject = "Password Reset Request"
    body = f'''
        To reset your password, click the following link:
        [Reset Link](http://localhost:8501/?page=reset&token={token})

        If you did not make this request, please ignore this email.
    '''

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient_email

            server.sendmail(sender_email, recipient_email, msg.as_string())

        st.success("Password reset link sent to your email. Check your inbox or spam.")
    except Exception as e:
        st.error(f"Error sending email: {e}")



def user_dashboard():
    st.title("User Dashboard")
    st.subheader("User Details")

    user = st.session_state.user
    st.write(f"First Name: {user[1]}")
    st.write(f"Last Name: {user[2]}")
    st.write(f"Email: {user[4]}")
    st.write(f"Date of Birth: {user[3]}")

    st.subheader("Update User Details")

    change_first_name = st.checkbox("Want to change your First Name?")

    if change_first_name:
        changefname = st.text_input("Enter your new First Name")
        
        changeb = st.button("Change First Name")
        if changeb:
            cur.execute('''
            UPDATE users_db
            SET first_name = %s
            WHERE id = %s
            ''', (changefname,st.session_state.user[0]))
            connection.commit()
            st.success("Updated Successfully")

    change_last_name = st.checkbox("Want to change your Last Name?")

    if change_last_name:
        changelname = st.text_input("Enter your new Last Name")
        changel = st.button("Change Last Name")
        if changel:
            cur.execute('''
            UPDATE users_db
            SET last_name = %s
            WHERE id = %s
            ''', (changelname,st.session_state.user[0]))
            connection.commit()
            st.success("Updated Successfully")

    change_first_name = st.checkbox("Want to change your DOB?")

    if change_first_name:
        changedob = st.text_input("Enter your new Date of Birth (YYYY-MM-DD)")
        
        changed = st.button("Change DOB")
        if changed:
            cur.execute('''
            UPDATE users_db
            SET dob = %s
            WHERE id = %s
            ''', (changedob,st.session_state.user[0]))
            connection.commit()
            st.success("Updated Successfully")


    st.subheader("Actions")
    passbutton = st.checkbox("Change Password")

    if passbutton:
        oldpass = st.text_input("Enter your old password", type="password")
        newpass = st.text_input("Enter your new password", type="password")
        connpass = st.text_input("Confirm your new password", type="password")
        changep = st.button("Change")
        if changep:
            if hash_password(oldpass) != st.session_state.user[5]:
                st.error("Old password doesn't match")
            else:
                if newpass != connpass:
                    st.error("New and Confirm password don't match")
                else:
                    hashpass = hash_password(newpass)
                    cur.execute('''
                    UPDATE users_db
                    SET password = %s
                    WHERE id = %s
                    ''', (hashpass,st.session_state.user[0]))
                    connection.commit()
                    st.success("Password Updated Successfully")

    # if st.button("Log Out"):
    #     get_session_state().user = None
    #     st.success("Logged out successfully.")
    #     login()
'''def upload_data(file):
    
    #uploaded_file = st.file_uploader("Upload csv file:", type=["csv"], accept_multiple_files=False)

# Check file size
    if file.size > 10*1024*1024:  # 10MB limit
        st.error("File size exceeds the limit (10MB). Please upload a smaller file.")
        return
    
    # Read uploaded file
    df = pd.read_csv(file)
    
    
    df.to_sql('users_data', con=mysql.connector.connect(**config), if_exists='append', index=False)
    
    st.success("Data uploaded successfully!")'''

def upload_data(file):
    # Check if file is uploaded
    if file is None:
        st.error("Please upload a CSV file.")
        return

    # Check file size
    if file.size > 10*1024*1024:  # 10MB limit
        st.error("File size exceeds the limit (10MB). Please upload a smaller file.")
        return
    
    # Read uploaded file
    df = pd.read_csv(file)
    
    # Perform further processing and data upload
    # (Your code for processing and uploading data goes here)

    st.success("Data uploaded successfully!")

def sign_in():
    st.header('User Login')
    email_login = st.text_input('Enter your email:', placeholder="abc123@email.com")
    password_login = st.text_input('Enter your Password:', placeholder="Password", type="password")

    forgot_password = st.checkbox("Forgot Password")

    if forgot_password:
        email_forgot = st.text_input("Enter your registered Gmail account:")
        if st.button("Reset Password"):
            
            cur.execute('SELECT * FROM users_db WHERE email = %s', (email_forgot,))
            user = cur.fetchone()
            # connection.commit()
            if user:
                
                reset_token = generate_reset_token()
                reset_expiration = datetime.now() + timedelta(hours=1)

                cur.execute('''
                    UPDATE users_db
                    SET reset_token = %s, reset_expiration = %s
                    WHERE email = %s
                ''', (reset_token, reset_expiration, email_forgot))
                connection.commit()

                
                send_reset_email(email_forgot, reset_token)

                st.session_state.user = user

            else:
                st.error("Email not found. Please enter a registered Gmail account.")
    else:
        if st.button("Login"):
        
            hashed_login_password = hash_password(password_login)

            cur.execute('SELECT * FROM users_db WHERE email = %s AND password = %s', (email_login, hashed_login_password))
            user = cur.fetchone()

            if user:
                st.session_state.user = user
                st.success("Login successful.")
                return user
            else:
                st.error("Invalid email or password.")
                return None
            
def sign_up():
    st.header('Create a new Account')
    first_name = st.text_input('Enter your First Name:')
    last_name = st.text_input("Enter your Last Name:")
    dob = st.text_input('Enter your DOB(YYYY-MM-DD):', placeholder="01/01/1980")
    email_reg = st.text_input('Enter your email account:', placeholder="abc123@gmail.com")
    password_reg = st.text_input('Enter your password:', type="password")
    confirm_password = st.text_input('Confirm your password:', type="password")
    register=st.button('Register')

    if register == True:
        if password_reg != confirm_password:
            st.error('Passwords do not match. Please try again.')
        
        elif not email_reg.endswith('@gmail.com'):
            st.error('Please register with a Gmail account.')
        else:
            hashed_password = hash_password(password_reg)

            try:
                parameters = (first_name, last_name, dob, email_reg, hashed_password)
                cur.execute("""
                    INSERT INTO users_db (first_name, last_name, dob, email, password)
                    VALUES (%s, %s, %s, %s, %s);
                    """, parameters)
                
                connection.commit()

                st.success(f"Registration successful for {email_reg}!")
            
            except IntegrityError:
                    st.error(f"Email {email_reg} is already registered. Please use a different email.")
def admin_dashboard():
    st.title("Admin Dashboard")
    st.subheader("User Details")

    # Fetch all users from the database
    cur.execute("SELECT * FROM users_db")
    all_users = cur.fetchall()

    # Display user information and allow admin to make changes
    for user in all_users:
        st.write(f"ID: {user[0]}")
        st.write(f"First Name: {user[1]}")
        st.write(f"Last Name: {user[2]}")
        st.write(f"Email: {user[4]}")
        st.write(f"Date of Birth: {user[3]}")

        st.subheader("Update User Details")

        change_first_name = st.checkbox(f"Change First Name for User {user[0]}")

        if change_first_name:
            new_first_name = st.text_input(f"Enter new First Name for User {user[0]}")
            changeb = st.button("Change First Name")
            if changeb:
                cur.execute('''
                UPDATE users_db
                SET first_name = %s
                WHERE id = %s
                ''', (new_first_name, user[0]))
                connection.commit()
                st.success("Updated Successfully")
                log_activity(f"Changed First Name for User {user[0]}")

        change_last_name = st.checkbox(f"Change Last Name for User {user[0]}")

        if change_last_name:
            new_last_name = st.text_input(f"Enter new Last Name for User {user[0]}")
            changel = st.button("Change Last Name")
            if changel:
                cur.execute('''
                UPDATE users_db
                SET last_name = %s
                WHERE id = %s
                ''', (new_last_name, user[0]))
                connection.commit()
                st.success("Updated Successfully")
                log_activity(f"Changed Last Name for User {user[0]}")

        change_dob = st.checkbox(f"Change Date of Birth for User {user[0]}")

        if change_dob:
            new_dob = st.text_input(f"Enter new Date of Birth for User {user[0]} (YYYY-MM-DD)")
            changed = st.button("Change DOB")
            if changed:
                cur.execute('''
                UPDATE users_db
                SET dob = %s
                WHERE id = %s
                ''', (new_dob, user[0]))
                connection.commit()
                st.success("Updated Successfully")
                log_activity(f"Changed Date of Birth for User {user[0]}")

        st.subheader("Actions")
        passbutton = st.checkbox(f"Change Password for User {user[0]}")

        if passbutton:
            oldpass = st.text_input("Enter the old password", type="password")
            newpass = st.text_input("Enter the new password", type="password")
            connpass = st.text_input("Confirm the new password", type="password")
            changep = st.button("Change")
            if changep:
                if hash_password(oldpass) != user[5]:
                    st.error("Old password doesn't match")
                else:
                    if newpass != connpass:
                        st.error("New and Confirm password don't match")
                    else:
                        hashpass = hash_password(newpass)
                        cur.execute('''
                        UPDATE users_db
                        SET password = %s
                        WHERE id = %s
                        ''', (hashpass, user[0]))
                        connection.commit()
                        st.success("Password Updated Successfully")
                        log_activity(f"Changed Password for User {user[0]}")

        # Provide option to deactivate or activate user
        st.subheader("Change User Status")
        toggle_status = st.radio(f"Toggle Status for User {user[0]}", options=["Activate", "Deactivate"])
        if st.button(f"{toggle_status} User {user[0]}"):
            new_status = 1 if toggle_status == "Activate" else 0
            cur.execute('''
            UPDATE users_db
            SET status = %s
            WHERE id = %s
            ''', (new_status, user[0]))
            connection.commit()
            st.success(f"User {user[0]} {toggle_status.lower()}d successfully")
            log_activity(f"{toggle_status} User {user[0]}")

        st.write('---')
