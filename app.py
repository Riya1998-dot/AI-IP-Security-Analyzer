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

# Get browser location
location = streamlit_geolocation()

if st.button("📍 Detect My Current Location", use_container_width=True):

    latitude = None
    longitude = None
    accuracy = None

    # Check whether location data exists
    if isinstance(location, dict):
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        accuracy = location.get("accuracy")

    # Check whether coordinates are available
    if latitude is None or longitude is None:

        st.warning(
            "📍 Location not detected yet. Please allow location permission in your browser and click the button again."
        )

    else:

        st.success("Current Location Detected Successfully!")

        st.subheader("📍 Current Coordinates")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Latitude", f"{float(latitude):.6f}")

            if accuracy is not None:
                st.write(
                    "🎯 **Accuracy:**",
                    f"{float(accuracy):.2f} meters"
                )

        with col2:
            st.metric("Longitude", f"{float(longitude):.6f}")

        st.divider()

        # Convert coordinates into location details
        try:

            geo_url = (
                "https://nominatim.openstreetmap.org/reverse"
                f"?lat={latitude}&lon={longitude}&format=json"
            )

            response = requests.get(
                geo_url,
                headers={
                    "User-Agent": "AI-IP-Security-Analyzer"
                },
                timeout=10
            )

            data = response.json()
            address = data.get("address", {})

            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("county")
                or "Unknown"
            )

            state = address.get("state", "Unknown")
            country = address.get("country", "Unknown")

            st.subheader("🌍 Current Location Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("City", city)

            with col2:
                st.metric("State", state)

            with col3:
                st.metric("Country", country)

        except Exception as e:
            st.warning(
                "Coordinates were detected, but address information could not be retrieved."
            )

st.divider()

st.caption(
    "🛡️ AI IP Security Analyzer | Python + Streamlit"
)
