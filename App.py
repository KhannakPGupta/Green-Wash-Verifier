import streamlit as st              #Streamlit is used for building web app UI using Python
import plotly.express as px         #Plotly is used to create interactive graphs
import pandas as pd

#Connecting app (frontend) to both APIs
from carbon_engine import CarbonEngine
from route_service import get_distance

#Creating Page Configuration
st.set_page_config(page_title="EcoTrack Supply Chain", layout="wide")
st.title("🚢 Green-Wash Verifier: Supply Chain Auditor")

#Initialising the Engine - Contains emission factors, calculation logic, graph-building logic
engine = CarbonEngine()

#Transport modes supported by climatiq API
TRANSPORT_MODES = [
    "Rail",
    "Cargo Ship",
    "Diesel Truck",
    "Electric Truck",
    "Air Freight"
]

#Inputs for Sidebar
st.sidebar.header("Product Configuration")
prod_name = st.sidebar.text_input("Product Name","Smartphone")
weight = st.sidebar.slider("Product Weight (kg)",0.1,50.0,1.0)

st.sidebar.header('Route Settings')
st.sidebar.info("Define the journey from Raw Material to Customer")

#MAIN INTERFACE - 2 Column system mimics professional BI dashboards
col1, col2 = st.columns([1,2])

#Column 1 is for inputs
with col1:
    st.subheader("1. Define the Journey")

    #Leg 1 - Raw Material to Factory
    st.markdown("---")
    st.markdown("### Source → Factory")

    source_coords = st.text_input("Source Coordinates (lon,lat)", "77.59,12.97")
    factory_coords = st.text_input("Factory Coordinates (lon,lat)", "72.87,19.07")
    
    try:
        source_coords_list = [float(x) for x in source_coords.split(",")]
        factory_coords_list = [float(x) for x in factory_coords.split(",")]

        dist1 = get_distance(source_coords_list, factory_coords_list)
        st.success(f"Distance: {dist1} km")

    except ValueError:
        dist1 = 0
        st.error("Invalid coordinates format. Use: lon,lat")
    except Exception as e:
        dist1 = 0
        st.error(f"API Error calculating distance: {e}")

    mode1 = st.selectbox("Transport Mode 1", TRANSPORT_MODES, index=3)
    #Leg 2 - Factory to Port
    st.markdown("---")
    st.markdown("### Factory → Port")

    dist2 = st.number_input("Factory to Port (km)", value=200)
    mode2 = st.selectbox("Transport Mode 2", TRANSPORT_MODES, index=2)

    #Leg 3 - Port to Retailer
    st.markdown("---")
    st.markdown("### Port → Retailer")

    dist3 = st.number_input("Port to Retailer (km)", value=10000)
    mode3 = st.selectbox("Transport Mode 3", TRANSPORT_MODES, index=0)

#Building the data structure
journey = [
    {"from":"Source","to":"Factory","dist":dist1,"mode":mode1},
    {"from":"Factory","to":"Port","dist":dist2,"mode":mode2},
    {"from":"Port","to":"Retailer","dist":dist3,"mode":mode3}]

#Run Calculation (Calculation using the formula used in Engine.py)
try:
    graph, total_co2 = engine.run_study(weight, journey)
except Exception as e:
    st.error(f"Climatiq API Error: {e}")
    st.stop()

#Column 2 is for results
with col2:
    st.subheader("2. Carbon Audit Results")

    #KPI Metrics
    m1, m2 = st.columns(2)
    m1.metric("Total CO2 Footprint", f"{total_co2} grams")
    m2.metric("Efficiency Score", "High" if total_co2<5000 else "Action Required")

    #Data Visualisation - Converting Graph into DataFrame
    df = pd.DataFrame([
        {"Leg": f"{u} → {v}", "Carbon (g)": data['carbon'], "Mode": data['mode']}
        for u,v,data in graph.edges(data=True)
    ])

    #Interactive Emissions Bar Chart
    fig = px.bar(df, x="Leg", y="Carbon (g)", color = "Mode", title = "Emissions Breakdown by Leg", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    #Educational Table
    st.write("### Detailed Breakdown")
    st.table(df)

#COMPARISON TOOL
st.divider()
st.subheader("3. 'What-If' Simulation")
if st.button("Compare with Greenest Rout (Rail/Electric)"):

    #Mocking a greener route
    green_journey= [
        {'from': 'Source', 'to': 'Factory', 'dist': dist1, 'mode': 'Electric Truck'},
        {'from': 'Factory', 'to': 'Port', 'dist': dist2, 'mode': 'Rail'},
        {'from': 'Port', 'to': 'Retailer', 'dist': dist3, 'mode': 'Cargo Ship'}]
    
    _, green_co2 = engine.run_study(weight, green_journey)
    savings = round(total_co2 - green_co2, 2)
    st.success(f"By switching to the greenest modes, you save **{savings} grams of CO2** per item!")    