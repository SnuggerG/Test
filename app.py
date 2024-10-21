import streamlit as st
from max_total_calculator import run_max_total_calculator  # Import the max total calculator

# Function to calculate cabin baggage capacity
def calculate_cabin_baggage_capacity(
    current_occupation, max_cabin_baggage, 
    max_hand_luggage, max_loose_items, 
    cabin_baggage_input, hand_luggage_input, 
    loose_items_input, pct_hand_luggage_chairs, 
    pct_loose_items_chairs):

    # Calculate cabin baggage on board
    cabin_baggage_on_board = cabin_baggage_input

    # Calculate hand luggage on board
    hand_luggage_on_board = hand_luggage_input

    # Calculate loose items on board
    loose_items_on_board = loose_items_input

    # Calculate space occupied by each type of baggage in the overhead bins
    cabin_baggage_space_used = cabin_baggage_on_board
    hand_luggage_space_used = (
        hand_luggage_on_board 
        - (hand_luggage_on_board * pct_hand_luggage_chairs / 100)
    )
    loose_items_space_used = (
        loose_items_on_board 
        - (loose_items_on_board * pct_loose_items_chairs / 100)
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

# Streamlit app for Cabin Baggage Calculator
def run_cabin_baggage_calculator():
    st.title('Cabinebagage Calculator')
    st.write("_Korte uitleg: Dit is een rekentool die de praktische maximale te verkopen cabinebagage uitrekent._")
    st.markdown("---")  # Separator line

    # Predefined Conditions Section
    st.subheader("Vooraf gedefinieerde waardens:")
    st.write("_Vooraf gedefinieerde waardens: Dit zijn de totale capaciteiten, uitgedrukt in cabinebagage, handbagage en losse items. "
              "De waardens zijn standaardinstellingen die kunnen worden aangepast om te zien hoeveel van elk type bagage in de overhead bins past._")


    # Retrieve maximum baggage capacities from session state or set defaults
    max_cabin_baggage = st.session_state.get('max_cabin_baggage', 242)
    max_hand_luggage = st.session_state.get('max_hand_luggage', 342)
    max_loose_items = st.session_state.get('max_loose_items', 683)

    # Display fixed maximum baggage capacities
    st.write(f"Maximale cabinebagage (items): **{max_cabin_baggage}**")
    st.write(f"Maximale handbaggage (items): **{max_hand_luggage}**")
    st.write(f"Maximale losse items (items): **{max_loose_items}**")

    # Adjust Predefined Parameters Note
    st.markdown("_Als u de vooraf gedefinieerde waardens wilt wijzigen, bezoek dan de (Maximale Capaciteit Calculator) pagina._")
    st.markdown("---")  # Separator line

    # Input Parameters Section
    st.subheader("Invoerparameters:")
    st.write("_Uitleg over parameters: De parameters die invloed hebben op het algoritme kunnen hieronder worden aangepast. "
              "Door deze waarden te wijzigen, kun je de resultaten van de rekentool beïnvloeden en zo de maximale capaciteit voor verschillende soorten bagage berekenen._")
    
    # Fixed maximum passenger capacity
    MAX_PASSENGER_CAPACITY = 232

    # Only input for exact number of passengers
    current_occupation = st.number_input("Huidig aantal passagiers (exact aantal)", min_value=0, max_value=MAX_PASSENGER_CAPACITY, value=197)

    # Input for cabin baggage (maximum sold cabin baggages only)
    st.subheader("Cabinebagage:")
    cabin_baggage_input = st.number_input("Maximaal verkochte cabinebagages (items)", min_value=0, value=70)  # Ensure min_value is integer

    # Input for hand luggage (exact number or percentage)
    st.subheader("Handbaggage & Loose items:")
    st.markdown("_Uitleg voor Handbaggage en Losse Items:_")
    st.markdown("_De termen 'bij de gate' verwijzen naar het totale aantal items dat alle passagiers met zich meenemen. "
                "Ruwweg neemt ongeveer 80% van de passagiers handbaggage mee. "
                "Hetzelfde geldt voor losse items._")
    
    hand_luggage_input_type = st.radio("Wilt u handbaggage invoeren als percentage of als exact aantal?", ["Percentage", "Exact aantal"])
    if hand_luggage_input_type == "Percentage":
        pct_hand_luggage_gate = st.number_input("Handbaggage bij de gate (%)", min_value=0.0, max_value=100.0, value=80.0)
        hand_luggage_input = current_occupation * pct_hand_luggage_gate / 100
    else:
        hand_luggage_input = st.number_input("Exact aantal handbaggage (items)", min_value=0.0)

    # Input for loose items (exact number or percentage)
    loose_items_input_type = st.radio("Wilt u losse items invoeren als percentage of als exact aantal?", ["Percentage", "Exact aantal"])
    if loose_items_input_type == "Percentage":
        pct_loose_items_gate = st.number_input("Losse items bij de gate (%)", min_value=0.0, max_value=100.0, value=5.0)
        loose_items_input = current_occupation * pct_loose_items_gate / 100
    else:
        loose_items_input = st.number_input("Exact aantal losse items (items)", min_value=0.0)

    # New input fields for percentages of hand luggage and loose items under the chairs
    st.subheader("Bagage Onder Stoelen:")
    st.markdown("_Uitleg voor Baggage onder de Stoelen:_")
    st.markdown("_Dit percentage geeft aan hoeveel handbaggage en losse items passagiers onder hun stoel plaatsen. "
                "Het overige deel van de bagage gaat in de bovenliggende vakken._")

    pct_hand_luggage_chairs = st.number_input("Percentage van handbaggage onder stoelen (%)", min_value=0.0, max_value=100.0, value=10.0)
    pct_loose_items_chairs = st.number_input("Percentage van losse items onder stoelen (%)", min_value=0.0, max_value=100.0, value=0.0)
    st.markdown("---")  # Separator line

    # Button to calculate cabin baggage capacity
    if st.button("Bereken cabinebagagecapaciteit"):
        results = calculate_cabin_baggage_capacity(
            current_occupation, max_cabin_baggage, 
            max_hand_luggage, max_loose_items, 
            cabin_baggage_input, hand_luggage_input, 
            loose_items_input, pct_hand_luggage_chairs, 
            pct_loose_items_chairs
        )
        
        # Title for the results section
        st.markdown("## Resultaten:")

        # Create a container for organized layout
        with st.container():
            # Create two columns for input parameters and results
            col1, col2 = st.columns(2)

            # Left Column: Omrekende Parameters
            with col1:
                st.write("Omrekende Parameters:")
                st.write("**Gegeven maximale te verkopen Cabine baggage:**")
                st.write(f"{results[0]} items")
                st.write("**Gegeven handbaggage komt aan boord:**")
                st.write(f"{results[1]} items")
                st.write("**Gegeven losse items komt aan boord:**")
                st.write(f"{results[2]} items")
                st.write("**Aantal cabine baggage in overheadbins:**")
                st.write(f"{results[3]} items")
                st.write("**Aantal handbaggage in overheadbins:**")
                st.write(f"{results[4]} items")
                st.write("**Aantal losse items in overheadbins:**")
                st.write(f"{results[5]} items")

            # Right Column: Uitkomsten
            with col2:
                st.write("Uitkomsten:")
                st.write(f"**Bezettingsgraad overhead bins:** {results[6] * 100:.2f}%")
                beschikbare_ruimte = round(results[7], 1)  # Available cabin baggage space
                totaal_te_verkopen = round(results[8], 1)  # Total to sell

                # Calculate the 10% correction factor
                correction_factor = 0.10  # 10%
                totaal_te_verkopen_corrected = round(totaal_te_verkopen * (1 - correction_factor), 1)

                st.write(f"**Dit is wat je nog in totaal zou kunnen verkopen:** {beschikbare_ruimte} items")
                st.write(f"**Dit is de theoretische maximale capaciteit die je kunt verkopen:** {totaal_te_verkopen} items")
                st.write(f"**Dit is de praktische maximale capaciteit die je kunt verkopen (10% correctie):** {totaal_te_verkopen_corrected} items")
                

# Main function to run the app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigatie")
    page = st.sidebar.radio("Selecteer een pagina:", ["Cabinebagage Calculator", "Maximale Capaciteit Calculator"])

    if page == "Cabinebagage Calculator":
        run_cabin_baggage_calculator()
    elif page == "Maximale Capaciteit Calculator":
        run_max_total_calculator()  # Call the separate calculator

if __name__ == "__main__":
    main()
