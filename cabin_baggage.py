import streamlit as st
import matplotlib.pyplot as plt

# Function to run the Cabin Baggage Calculator tab
def run_cabin_baggage_tab():
    """
    This function handles the logic for calculating cabin baggage capacity
    based on user inputs and displays the results in a Streamlit interface.
    """
    
    def calculate_cabin_baggage_capacity(
        max_passenger_capacity, current_occupation, max_cabin_baggage, 
        max_hand_luggage, max_loose_items, cabin_baggage_input, 
        hand_luggage_input, loose_items_input, pct_hand_luggage_under_seat, 
        pct_loose_items_under_seat):
        """
        This function calculates the total available cabin baggage capacity 
        and the space used by different types of baggage on board the aircraft.
        """
        
        # Calculate cabin baggage on board
        cabin_baggage_on_board = (
            cabin_baggage_input 
            if cabin_baggage_input is not None 
            else current_occupation * pct_cabin_baggage_gate / 100
        )

        # Calculate hand luggage on board
        hand_luggage_on_board = (
            hand_luggage_input 
            if hand_luggage_input is not None 
            else current_occupation * pct_hand_luggage_gate / 100
        )

        # Calculate loose items on board
        loose_items_on_board = (
            loose_items_input 
            if loose_items_input is not None 
            else current_occupation * pct_loose_items_gate / 100
        )

        # Calculate space occupied by each type of baggage in the overhead bins
        cabin_baggage_space_used = cabin_baggage_on_board
        hand_luggage_space_used = (
            hand_luggage_on_board 
            - (hand_luggage_on_board * pct_hand_luggage_under_seat / 100)
        )
        loose_items_space_used = (
            loose_items_on_board 
            - (loose_items_on_board * pct_loose_items_under_seat / 100)
        )

        # Calculate the total occupancy rate of the overhead bins
        overhead_bin_occupancy = (
            (cabin_baggage_space_used / max_cabin_baggage) 
            + (hand_luggage_space_used / max_hand_luggage) 
            + (loose_items_space_used / max_loose_items)
        )

        # Calculate available space for additional cabin baggage
        available_cabin_baggage_space = max_cabin_baggage * (1 - overhead_bin_occupancy)

        # Total cabin baggage to sell (available + space already used)
        total_cabin_baggage_to_sell = available_cabin_baggage_space + cabin_baggage_space_used

        # Return all calculated values
        return (
            cabin_baggage_on_board, hand_luggage_on_board, loose_items_on_board,
            cabin_baggage_space_used, hand_luggage_space_used, loose_items_space_used,
            overhead_bin_occupancy, available_cabin_baggage_space, total_cabin_baggage_to_sell
        )

    # Streamlit Title and Subheaders
    st.title('Cabin Baggage Calculator')

    # Input for maximum baggage capacities
    st.subheader("Maximum Baggage Quantities:")
    max_cabin_baggage = st.number_input("Maximum cabin baggage (items)", min_value=0, value=242)
    max_hand_luggage = st.number_input("Maximum hand luggage (items)", min_value=0, value=432)
    max_loose_items = st.number_input("Maximum loose items (items)", min_value=0, value=683)

    # Input for maximum passenger capacity
    max_passenger_capacity = st.number_input("Maximum passenger capacity", min_value=1, value=232)

    # Input for current passenger occupancy
    st.subheader("Occupancy Rate:")
    occupancy_input_type = st.radio(
        "Would you like to enter the occupancy rate as a percentage or exact number of passengers?", 
        ["Percentage", "Exact number"]
    )

    # Depending on input type, get the occupancy either as percentage or exact number
    if occupancy_input_type == "Percentage":
        occupancy_percentage = st.number_input("Occupancy rate (%)", min_value=0.0, max_value=100.0, value=85.0)
        current_occupation = occupancy_percentage / 100 * max_passenger_capacity
    else:
        current_occupation = st.number_input(
            "Exact number of passengers", 
            min_value=0.0, max_value=float(max_passenger_capacity), 
            value=200.0
        )
        occupancy_percentage = None

    # Input for cabin baggage
    st.subheader("Cabin Baggage at the Gate:")
    cabin_baggage_input_type = st.radio("Would you like to enter a percentage or an exact number?", ["Percentage", "Exact number"])
    if cabin_baggage_input_type == "Percentage":
        pct_cabin_baggage_gate = st.number_input("Percentage of cabin baggage at the gate (%)", min_value=0.0, max_value=100.0, value=10.0)
        cabin_baggage_input = None
    else:
        cabin_baggage_input = st.number_input("Exact number of cabin baggage at the gate (items)", min_value=0.0, value=10.0)
        pct_cabin_baggage_gate = None

    # Input for hand luggage
    st.subheader("Hand Luggage at the Gate:")
    hand_luggage_input_type = st.radio("Would you like to enter a percentage or an exact number?", ["Percentage", "Exact number"], key="hand_luggage")
    if hand_luggage_input_type == "Percentage":
        pct_hand_luggage_gate = st.number_input("Percentage of hand luggage at the gate (%)", min_value=0.0, max_value=100.0, value=5.0)
        hand_luggage_input = None
    else:
        hand_luggage_input = st.number_input("Exact number of hand luggage at the gate (items)", min_value=0.0, value=5.0)
        pct_hand_luggage_gate = None

    # Input for loose items
    st.subheader("Loose Items at the Gate:")
    loose_items_input_type = st.radio("Would you like to enter a percentage or an exact number?", ["Percentage", "Exact number"], key="loose_items")
    if loose_items_input_type == "Percentage":
        pct_loose_items_gate = st.number_input("Percentage of loose items at the gate (%)", min_value=0.0, max_value=100.0, value=2.0)
        loose_items_input = None
    else:
        loose_items_input = st.number_input("Exact number of loose items at the gate (items)", min_value=0.0, value=2.0)
        pct_loose_items_gate = None

    # Input for under-seat storage percentages
    st.subheader("Under-seat Storage Percentages:")
    pct_hand_luggage_under_seat = st.number_input("Percentage of hand luggage stored under the seat (%)", min_value=0.0, max_value=100.0, value=50.0)
    pct_loose_items_under_seat = st.number_input("Percentage of loose items stored under the seat (%)", min_value=0.0, max_value=100.0, value=1.0)

    # Perform calculations based on inputs
    results = calculate_cabin_baggage_capacity(
        max_passenger_capacity, current_occupation, max_cabin_baggage, max_hand_luggage, max_loose_items,
        cabin_baggage_input, hand_luggage_input, loose_items_input, 
        pct_hand_luggage_under_seat, pct_loose_items_under_seat
    )

    # Display results
    st.subheader("Results")
    result_labels = [
        "Cabin baggage on board", "Hand luggage on board", "Loose items on board",
        "Cabin baggage in overhead bins", "Hand luggage in overhead bins", "Loose items in overhead bins",
        "Overhead bin occupancy rate", "Available space for cabin baggage", "Total cabin baggage to sell"
    ]
    
    # Loop through each result and display it with its corresponding label
    for label, result in zip(result_labels, results):
        st.write(f"{label}: {result:.1f}")
