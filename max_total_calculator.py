# max_total_calculator.py

import streamlit as st

# Default predefined conditions
DEFAULT_CABIN_BAGGAGE = 242
DEFAULT_HAND_LUGGAGE = 342
DEFAULT_LOOSE_ITEMS = 683

# Function to calculate total CB, HL, and Loose
def calculate_bin_totals(capacities, quantities):
    total_cb = 0
    total_hl = 0
    total_loose = 0

    # Iterate over each Bin type (A, B, C)
    for bin_type in capacities:
        cb_capacity, hl_capacity, loose_capacity = capacities[bin_type]
        quantity = quantities[bin_type]
        
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
def run_max_total_calculator():
    st.title("Maximale Capaciteit Calculator voor Cabinebagage")

    # Explanation for the Max Total Load Calculator
    st.write("""
    **Toelichting:**
    Deze rekentool berekent de maximale capaciteit van cabinebagage (CB), handbaggage (HL) en losse items voor het hele toestel. 
    Het doel van deze tool is om te bepalen hoeveel cabinebagage er maximaal in de overheadbins past, op basis van de opgegeven capaciteiten per type bin (A, B, C). 
    Worden dit de vooraf gedefinieerde waarden die je zag in hoodprogramma en dienen als basis voor deze die berekening.
    
    U kunt de capaciteiten van de bins en het aantal bins aanpassen om te zien hoe de maximale capaciteiten veranderen.
    """)

    # Input for capacities for each Bin type
    st.subheader("Voer de capaciteiten in voor elke Bin type:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Bin_a_cb = st.number_input("Bin A - Cabine Baggage Capaciteit", min_value=0, value=2)
        Bin_b_cb = st.number_input("Bin B - Cabine Baggage Capaciteit", min_value=0, value=2)
        Bin_c_cb = st.number_input("Bin C - Cabine Baggage Capaciteit", min_value=0, value=5)

    with col2:
        Bin_a_hl = st.number_input("Bin A - Handbaggage Capaciteit", min_value=0, value=3)
        Bin_b_hl = st.number_input("Bin B - Handbaggage Capaciteit", min_value=0, value=4)
        Bin_c_hl = st.number_input("Bin C - Handbaggage Capaciteit", min_value=0, value=7)

    with col3:
        Bin_a_loose = st.number_input("Bin A - Losse Items Capaciteit", min_value=0, value=6)
        Bin_b_loose = st.number_input("Bin B - Losse Items Capaciteit", min_value=0, value=8)
        Bin_c_loose = st.number_input("Bin C - Losse Items Capaciteit", min_value=0, value=13)

    # Define the capacities dictionary
    capacities = {
        'A': (Bin_a_cb, Bin_a_hl, Bin_a_loose),
        'B': (Bin_b_cb, Bin_b_hl, Bin_b_loose),
        'C': (Bin_c_cb, Bin_c_hl, Bin_c_loose)
    }

    # Input for quintet values (quantities for each bin type)
    st.subheader("Voer het aantal in voor elke Bin type:")
    quintet_a = st.number_input("Aantal Bin A", min_value=0, value=4)
    quintet_b = st.number_input("Aantal Bin B", min_value=0, value=2)
    quintet_c = st.number_input("Aantal Bin C", min_value=0, value=46)

    # Define the quantities dictionary
    quantities = {
        'A': quintet_a,
        'B': quintet_b,
        'C': quintet_c
    }

    # Button to save the results and update predefined conditions
    if st.button("Sla nieuwe maximale capaciteit op"):
        # Save the parameters to session state
        st.session_state['max_cabin_baggage'] = calculate_bin_totals(capacities, quantities)['Total CB']
        st.session_state['max_hand_luggage'] = calculate_bin_totals(capacities, quantities)['Total HL']
        st.session_state['max_loose_items'] = calculate_bin_totals(capacities, quantities)['Total Loose']

        # Output the results
        st.write("### Resultaten:")
        st.write(f"**Totale Cabine Baggage (CB):** {st.session_state['max_cabin_baggage']}")
        st.write(f"**Totale Handbaggage (HL):** {st.session_state['max_hand_luggage']}")
        st.write(f"**Totale Losse Items:** {st.session_state['max_loose_items']}")

        # Confirmation message
        st.success("Max load parameters succesvol opgeslagen!")

    # Message for users to reload the page for a reset
    st.write("Als u de parameters wilt resetten naar de standaardwaarden, herlaad dan de pagina.")

# Entry point for the module
if __name__ == "__main__":
    run_max_total_calculator()
