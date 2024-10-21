import streamlit as st
import matplotlib.pyplot as plt

# Function to calculate total CB, HL, and Loose
def calculate_bin_totals(capacities, quantities):
    """
    Calculates the total number of CB, HL, and Loose items that can fit into the given bin with adjustable quantities.

    Parameters:
    capacities (dict): A dictionary where each key is a bin type (A, B, C)
                       and the value is a tuple (CB_capacity, HL_capacity, Loose_capacity).
    quantities (dict): A dictionary containing the number of units for each bin type (A, B, C).

    Returns:
    dict: A dictionary containing the total CB, HL, and Loose items.
    """
    
    # Initialize totals for CB, HL, and Loose
    total_cb = 0
    total_hl = 0
    total_loose = 0

    # Iterate over each Bin type (A, B, C)
    for Bin_type in capacities:
        cb_capacity, hl_capacity, loose_capacity = capacities[Bin_type]
        quantity = quantities[Bin_type]
        
        # Calculate total for current Bin type
        total_cb += cb_capacity * quantity
        total_hl += hl_capacity * quantity
        total_loose += loose_capacity * quantity

    # Return the totals as a dictionary
    return {
        'Total CB': total_cb,
        'Total HL': total_hl,
        'Total Loose': total_loose
    }

# Streamlit app for Max total Calculator
def run_bin_total_tab():
    st.header("Max total Calculator")

    # Input for capacities for each Bin type
    st.subheader("Enter the capacities for each Bin type:")

    col1, col2, col3 = st.columns(3)
    with col1:
        Bin_a_cb = st.number_input("Bin A - CB Capacity", min_value=0, value=2)
        Bin_b_cb = st.number_input("Bin B - CB Capacity", min_value=0, value=2)
        Bin_c_cb = st.number_input("Bin C - CB Capacity", min_value=0, value=5)
    with col2:
        Bin_a_hl = st.number_input("Bin A - HL Capacity", min_value=0, value=3)
        Bin_b_hl = st.number_input("Bin B - HL Capacity", min_value=0, value=4)
        Bin_c_hl = st.number_input("Bin C - HL Capacity", min_value=0, value=7)
    with col3:
        Bin_a_loose = st.number_input("Bin A - Loose Capacity", min_value=0, value=6)
        Bin_b_loose = st.number_input("Bin B - Loose Capacity", min_value=0, value=8)
        Bin_c_loose = st.number_input("Bin C - Loose Capacity", min_value=0, value=13)

    # Define the capacities dictionary
    capacities = {
        'A': (Bin_a_cb, Bin_a_hl, Bin_a_loose),
        'B': (Bin_b_cb, Bin_b_hl, Bin_b_loose),
        'C': (Bin_c_cb, Bin_c_hl, Bin_c_loose)
    }

    # Input for quintet values (quantities for each bin type)
    st.subheader("Enter the number for each Bin type:")
    quintet_a = st.number_input("Number of Bin A", min_value=0, value=4)
    quintet_b = st.number_input("Number of Bin B", min_value=0, value=2)
    quintet_c = st.number_input("Number of Bin C", min_value=0, value=46)

    # Define the quantities dictionary
    quantities = {
        'A': quintet_a,
        'B': quintet_b,
        'C': quintet_c
    }

    # Button to trigger the calculation
    if st.button("Calculate Total CB, HL, and Loose"):
        totals = calculate_bin_totals(capacities, quantities)
        
        # Output the results
        st.write("### Total Calculations:")
        st.write(f"**Total CB**: {totals['Total CB']}")
        st.write(f"**Total HL**: {totals['Total HL']}")
        st.write(f"**Total Loose**: {totals['Total Loose']}")

