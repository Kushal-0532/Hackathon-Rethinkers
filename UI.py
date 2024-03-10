import streamlit as st

def authenticate(username, password):
    if username == "user" and password == "password":
        return True
    else:
        return False

def app():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate(username, password):
            # Successful login, redirect to the main application page
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        app()
    else:
        # Import the main application page
        import Main
        Main.app()