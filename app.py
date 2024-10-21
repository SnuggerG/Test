import streamlit as st
from max_bin_load import run_bin_total_tab
from cabin_baggage import run_cabin_baggage_tab
from dynamic_bin_calculator import run_dynamic_bin_calculator  # Import the new side program

# Main Streamlit app
def main():
    # Title of the app
    st.title('Optimization and Logistics Tool')

    # Creating tabs
    tab_options = ["Max total Calculator", "Cabin Baggage Calculator"]
    selected_tab = st.radio("Select Functionality", tab_options)

    # Display selected tab based on user choice
    if selected_tab == "Max total Calculator":
        run_bin_total_tab()
    elif selected_tab == "Cabin Baggage Calculator":
        run_cabin_baggage_tab()
   

# Running the app
if __name__ == "__main__":
    main()
