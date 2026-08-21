import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="AI IP Security Analyzer",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ AI IP Security Analyzer")
st.caption("Live IP Intelligence and Current Location Analysis")

st.divider()

# Get current location from browser
location = streamlit_geolocation()

if st.button("🔍 Analyze My Current Location", use_container_width=True):

    if location and location != "No Location Info":

        latitude = location.get("latitude")
        longitude = location.get("longitude")
        accuracy = location.get("accuracy")

        st.success("Current Location Detected!")

        st.subheader("📍 Current Location")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Latitude", f"{latitude:.6f}")
            st.write("🎯 **Accuracy:**", f"{accuracy:.2f} meters")

        with col2:
            st.metric("Longitude", f"{longitude:.6f}")

        st.divider()

        # Get approximate address from coordinates
        try:
            geo_url = (
                "https://nominatim.openstreetmap.org/reverse"
                f"?lat={latitude}&lon={longitude}&format=json"
            )

            response = requests.get(
                geo_url,
                headers={"User-Agent": "Streamlit Location Analyzer"},
                timeout=10
            )

            data = response.json()
            address = data.get("address", {})

            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or "Unknown"
            )

            state = address.get("state", "Unknown")
            country = address.get("country", "Unknown")

            st.subheader("🌍 Location Information")

            st.write("📍 **City:**", city)
            st.write("🗺️ **State:**", state)
            st.write("🌎 **Country:**", country)

        except Exception:
            st.warning("Location coordinates detected, but address details could not be retrieved.")

    else:
        st.warning("Please click the location button and allow location permission first.")

st.divider()
st.caption("AI IP Security Analyzer | Python + Streamlit")
