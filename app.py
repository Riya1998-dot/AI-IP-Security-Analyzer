import streamlit as st
import requests

st.set_page_config(
    page_title="AI IP Security Analyzer",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ AI IP Security Analyzer")
st.caption("Live IP Intelligence and Security Risk Analysis")

st.divider()

if st.button("🔍 Analyze My IP", use_container_width=True):

    try:
        # Step 1: Get public IP
        ip_response = requests.get(
            "https://api.ipify.org?format=json",
            timeout=10
        )

        ip = ip_response.json()["ip"]

        # Step 2: Get IP location and network information
        url = f"http://ip-api.com/json/{ip}"

        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") != "success":
            st.error("Unable to retrieve IP location information.")
            st.write(data)
            st.stop()

        city = data.get("city", "Unknown")
        region = data.get("regionName", "Unknown")
        country = data.get("country", "Unknown")
        isp = data.get("isp", "Unknown")

        # Risk calculation
        risk_score = 20

        # Example rule-based analysis
        if not city or city == "Unknown":
            risk_score += 20

        if not isp or isp == "Unknown":
            risk_score += 20

        if risk_score <= 35:
            status = "🟢 LOW RISK"
            message = "Network appears normal."

        elif risk_score <= 65:
            status = "🟡 MEDIUM RISK"
            message = "Some network characteristics require attention."

        else:
            status = "🔴 HIGH RISK"
            message = "Potentially suspicious network characteristics detected."

        # Display results
        st.success("IP Analysis Completed!")

        st.subheader("🌐 Network Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("IP Address", ip)
            st.write("📍 **City:**", city)
            st.write("🌍 **Country:**", country)

        with col2:
            st.write("🏢 **ISP:**", isp)
            st.write("🗺️ **Region:**", region)

        st.divider()

        st.subheader("🤖 Security Analysis")

        st.metric("Security Risk Score", f"{risk_score}/100")
        st.progress(risk_score)

        st.subheader(status)
        st.write(message)

        st.divider()

        st.caption("AI IP Security Analyzer | Python + Streamlit")

    except Exception as e:
        st.error("Error connecting to the IP detection service.")
        st.write(e)
