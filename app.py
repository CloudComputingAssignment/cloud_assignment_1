
from dependancies import *
from home import *
from login import *

from about import *


def main():
    # st.set_page_config(
    #     page_title="Cloud Based Web Storage App",
    #     page_icon="home",
    #     layout="wide",
    # )

    st.title("Cloud Based Web Storage App")


    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox('Get Started:', ['User', 'Home',  'About'])

    if app_mode == 'User':
        login()
        

    elif app_mode == 'About':
        about()
        
        
    else:
        home()

if __name__ == "__main__":
    try:
        main()
    except SystemError:
        pass
