import streamlit as st
import matplotlib.pyplot as plt

# Function to run the cabin baggage tab
def run_cabin_baggage_tab():
    # Function to calculate cabin baggage capacity
    def bereken_te_verkopen_cabinebagage(max_bezetting, bezetting, max_cabinebagage, max_handbagage, max_lose_items,
                                         cabinebagage_input, handbagage_input, lose_items_input, 
                                         pct_handbagage_onder_stoel, pct_lose_items_onder_stoel):
        
        cabinebagage_aan_boord = cabinebagage_input if cabinebagage_input is not None else bezetting * pct_cabinebagage_gate / 100
        handbagage_aan_boord = handbagage_input if handbagage_input is not None else bezetting * pct_handbagage_gate / 100
        lose_items_aan_boord = lose_items_input if lose_items_input is not None else bezetting * pct_lose_items_gate / 100
        
        ruimte_cabinebagage = cabinebagage_aan_boord  
        ruimte_handbagage = handbagage_aan_boord - (handbagage_aan_boord * pct_handbagage_onder_stoel / 100)
        ruimte_lose_items = lose_items_aan_boord - (lose_items_aan_boord * pct_lose_items_onder_stoel / 100)
        
        bezetting_overhead_bins = (ruimte_cabinebagage / max_cabinebagage) + \
                                  (ruimte_handbagage / max_handbagage) + \
                                  (ruimte_lose_items / max_lose_items)
        
        beschikbare_ruimte_cabinebagage = max_cabinebagage * (1 - bezetting_overhead_bins)
        
        te_verkopen_cabinebagage = beschikbare_ruimte_cabinebagage + ruimte_cabinebagage
        
        return (cabinebagage_aan_boord, handbagage_aan_boord, lose_items_aan_boord,
                ruimte_cabinebagage, ruimte_handbagage, ruimte_lose_items,
                bezetting_overhead_bins, beschikbare_ruimte_cabinebagage, te_verkopen_cabinebagage)

    # Title for this tab
    st.title('Cabin Baggage Calculator')

    # Maximum baggage inputs
    st.subheader("Maximale aantallen:")
    max_cabinebagage = st.number_input("Maximale cabinebagage (stuks)", min_value=0, value=242)
    max_handbagage = st.number_input("Maximale handbagage (stuks)", min_value=0, value=432)
    max_lose_items = st.number_input("Maximale losse items (stuks)", min_value=0, value=683)

    # Passenger capacity input
    max_bezetting = st.number_input("Maximale passagierscapaciteit", min_value=1, value=232)

    # Input options for occupancy
    st.subheader("Bezettingsgraad:")
    bezetting_optie = st.radio("Wil je de bezettingsgraad als percentage of het exacte aantal passagiers invoeren?", ["Percentage", "Exact aantal"])
    if bezetting_optie == "Percentage":
        bezettingsgraad_pct = st.number_input("Bezettingsgraad (%)", min_value=0.0, max_value=100.0, value=85.0)
        bezetting = bezettingsgraad_pct / 100 * max_bezetting
    else:
        bezetting = st.number_input("Exact aantal passagiers", min_value=0.0, max_value=float(max_bezetting), value=200.0)
        bezettingsgraad_pct = None

    # Input for baggage
    st.subheader("Cabinebagage bij de gate:")
    cabinebagage_optie = st.radio("Wil je een percentage of een exact aantal invullen?", ["Percentage", "Exact aantal"])
    if cabinebagage_optie == "Percentage":
        pct_cabinebagage_gate = st.number_input("Percentage cabinebagage bij de gate (%)", min_value=0.0, max_value=100.0, value=10.0)
        cabinebagage_input = None
    else:
        cabinebagage_input = st.number_input("Exact aantal cabinebagage bij de gate (stuks)", min_value=0.0, value=10.0)
        pct_cabinebagage_gate = None

    st.subheader("Handbagage bij de gate:")
    handbagage_optie = st.radio("Wil je een percentage of een exact aantal invullen?", ["Percentage", "Exact aantal"], key="handbagage")
    if handbagage_optie == "Percentage":
        pct_handbagage_gate = st.number_input("Percentage handbagage bij de gate (%)", min_value=0.0, max_value=100.0, value=5.0)
        handbagage_input = None
    else:
        handbagage_input = st.number_input("Exact aantal handbagage bij de gate (stuks)", min_value=0.0, value=5.0)
        pct_handbagage_gate = None

    st.subheader("Losse items bij de gate:")
    lose_items_optie = st.radio("Wil je een percentage of een exact aantal invullen?", ["Percentage", "Exact aantal"], key="lose_items")
    if lose_items_optie == "Percentage":
        pct_lose_items_gate = st.number_input("Percentage losse items bij de gate (%)", min_value=0.0, max_value=100.0, value=2.0)
        lose_items_input = None
    else:
        lose_items_input = st.number_input("Exact aantal losse items bij de gate (stuks)", min_value=0.0, value=2.0)
        pct_lose_items_gate = None

    st.subheader("Percentages for under-seat storage:")
    pct_handbagage_onder_stoel = st.number_input("Percentage handbagage onder de stoel (%)", min_value=0.0, max_value=100.0, value=50.0)
    pct_lose_items_onder_stoel = st.number_input("Percentage losse items onder de stoel (%)", min_value=0.0, max_value=100.0, value=1.0)

    # Perform calculations
    resultaten = bereken_te_verkopen_cabinebagage(max_bezetting, bezetting, max_cabinebagage, max_handbagage, max_lose_items,
                                                  cabinebagage_input, handbagage_input, lose_items_input, 
                                                  pct_handbagage_onder_stoel, pct_lose_items_onder_stoel)

    # Display results
    st.subheader("Resultaten")
    resultaten_labels = [
        "Cabinebagage aan boord", "Handbagage aan boord", "Lose items aan boord",
        "Cabinebagage in bins", "Handbagage in bins", "Losse items in bins",
        "Bezettingsgraad overhead bins", "Beschikbare ruimte over voor cabinebagage", "Totaal te verkopen cabinebagage"
    ]
    for label, resultaat in zip(resultaten_labels, resultaten):
        st.write(f"{label}: {resultaat:.1f}")

    # Plotting a graph
    st.subheader("Grafiek van Ruimte en Bezettingsgraad")
    plt.figure(figsize=(10, 6))
    plt.bar(['Cabinebagage', 'Handbagage', 'Lose items'], resultaten[:3], color=['blue', 'green', 'orange'])
    plt.title('Aantal items aan boord')
    plt.ylabel('Aantal')
    plt.grid(True)
    st.pyplot(plt)
