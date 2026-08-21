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

# Get browser/device location
location = streamlit_geolocation()

if st.button("🔍 Analyze My IP & Location", use_container_width=True):

    # ---------------------------------
    # 1. DETECT IP ADDRESS
    # ---------------------------------

    try:
        ip_response = requests.get(
            "https://api.ipify.org?format=json",
            timeout=10
        )

        public_ip = ip_response.json().get(
            "ip",
            "Unknown"
        )

    except Exception:
        public_ip = "Unknown"

    # ---------------------------------
    # 2. GET CURRENT LOCATION
    # ---------------------------------

    latitude = None
    longitude = None
    accuracy = None

    if isinstance(location, dict):
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        accuracy = location.get("accuracy")

    # ---------------------------------
    # DISPLAY IP ADDRESS
    # ---------------------------------

    st.success("Analysis Started Successfully!")

    st.subheader("🌐 IP Information")

    st.metric(
        "Public IP Address",
        public_ip
    )

    st.divider()

    # ---------------------------------
    # CHECK LOCATION
    # ---------------------------------

    if latitude is None or longitude is None:

        st.warning(
            "📍 Location not detected yet. Please allow location permission in your browser and click the button again."
        )

    else:

        st.success("Current Location Detected Successfully!")

        # ---------------------------------
        # COORDINATES
        # ---------------------------------

        st.subheader("📍 Current Coordinates")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Latitude",
                f"{float(latitude):.6f}"
            )

            if accuracy is not None:
                st.write(
                    "🎯 **Accuracy:**",
                    f"{float(accuracy):.2f} meters"
                )

        with col2:
            st.metric(
                "Longitude",
                f"{float(longitude):.6f}"
            )

        st.divider()

        # ---------------------------------
        # CONVERT COORDINATES TO LOCATION
        # ---------------------------------

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

            address = data.get(
                "address",
                {}
            )

            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("county")
                or "Unknown"
            )

            state = address.get(
                "state",
                "Unknown"
            )

            country = address.get(
                "country",
                "Unknown"
            )

            # ---------------------------------
            # DISPLAY LOCATION
            # ---------------------------------

            st.subheader(
                "🌍 Current Location Information"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "City",
                    city
                )

            with col2:
                st.metric(
                    "State",
                    state
                )

            with col3:
                st.metric(
                    "Country",
                    country
                )

        except Exception:

            st.warning(
                "Coordinates were detected, but address information could not be retrieved."
            )

st.divider()

st.caption(
    "🛡️ AI IP Security Analyzer | Python + Streamlit"
)
