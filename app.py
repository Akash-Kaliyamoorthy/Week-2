import streamlit as st
from openai import OpenAI
import requests
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="EV Charging Assistant",
    page_icon="⚡",
    layout="wide"
)

# Initialize OpenAI API
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Please add OPENAI_API_KEY in Streamlit secrets!")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_openai_client()

# Get charging stations
def get_charging_stations(latitude, longitude, distance=10):
    """Fetch charging stations from Open Charge Map API"""
    try:
        url = "https://api.openchargemap.io/v3/poi/"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "distance": distance,
            "maxresults": 10,
            "compact": True,
            "verbose": False
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching stations: {str(e)}")
        return []

# Simple ML: Rank stations by distance and charger type
def recommend_stations(stations, preferred_type="Fast"):
    """Simple recommendation based on distance and charger type"""
    scored_stations = []
    
    for station in stations:
        score = 0
        distance = station.get('AddressInfo', {}).get('Distance', 999)
        
        # Score based on distance (closer = better)
        if distance < 5:
            score += 10
        elif distance < 10:
            score += 5
        
        # Score based on charger type
        connections = station.get('Connections', [])
        for conn in connections:
            level = conn.get('Level', {})
            if level and 'Fast' in str(level.get('Title', '')):
                score += 8
        
        # Add availability bonus
        if station.get('StatusType', {}).get('IsOperational'):
            score += 5
            
        scored_stations.append({
            'station': station,
            'score': score,
            'distance': distance
        })
    
    # Sort by score
    scored_stations.sort(key=lambda x: x['score'], reverse=True)
    return scored_stations

# Chat with OpenAI
def chat_with_openai(user_message, context=""):
    """Send message to OpenAI and get response"""
    try:
        system_prompt = f"""You are an EV Charging Assistant. Help users find charging stations and answer EV-related questions.
        
Be friendly, concise, and helpful. If station data is provided, reference it naturally.

Context: {context}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Main UI
def main():
    st.title("⚡ EV Charging Assistant")
    st.markdown("Find charging stations and get answers to your EV questions!")
    
    # Sidebar for location input
    with st.sidebar:
        st.header("📍 Your Location")
        
        # Default to San Francisco
        lat = st.number_input("Latitude", value=37.7749, format="%.4f")
        lon = st.number_input("Longitude", value=-122.4194, format="%.4f")
        distance = st.slider("Search Radius (km)", 5, 50, 10)
        
        st.markdown("---")
        st.markdown("💡 **Tip**: Use your phone's GPS to get exact coordinates")
        
        if st.button("🔍 Find Stations", type="primary"):
            with st.spinner("Searching for charging stations..."):
                stations = get_charging_stations(lat, lon, distance)
                st.session_state['stations'] = stations
                st.session_state['recommendations'] = recommend_stations(stations)
                st.success(f"Found {len(stations)} stations!")
    
    # Chat interface
    st.header("💬 Chat with Assistant")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about EV charging..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare context with station data
        context = ""
        if 'recommendations' in st.session_state and st.session_state['recommendations']:
            top_stations = st.session_state['recommendations'][:3]
            context = "Top 3 recommended stations:\n"
            for i, item in enumerate(top_stations, 1):
                station = item['station']
                addr = station.get('AddressInfo', {})
                context += f"{i}. {addr.get('Title', 'Unknown')} - {item['distance']:.1f}km away\n"
        
        # Get OpenAI's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_openai(prompt, context)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display station recommendations
    if 'recommendations' in st.session_state and st.session_state['recommendations']:
        st.header("🎯 Recommended Stations")
        
        for i, item in enumerate(st.session_state['recommendations'][:5], 1):
            station = item['station']
            addr = station.get('AddressInfo', {})
            
            with st.expander(f"#{i} - {addr.get('Title', 'Unknown Station')} ({item['distance']:.1f} km)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Address**: {addr.get('AddressLine1', 'N/A')}")
                    st.write(f"**Town**: {addr.get('Town', 'N/A')}")
                    st.write(f"**Distance**: {item['distance']:.1f} km")
                
                with col2:
                    st.write(f"**Recommendation Score**: {item['score']}/23")
                    status = station.get('StatusType', {})
                    st.write(f"**Status**: {status.get('Title', 'Unknown')}")
                    
                    # Charger types
                    connections = station.get('Connections', [])
                    if connections:
                        charger_types = [c.get('ConnectionType', {}).get('Title', 'Unknown') 
                                       for c in connections]
                        st.write(f"**Chargers**: {', '.join(set(charger_types))}")

if __name__ == "__main__":
    main()