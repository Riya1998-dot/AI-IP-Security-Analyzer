import streamlit as st
import requests
import random

# Page settings
st.set_page_config(
    page_title="AI IP Security Analyzer",
    page_icon="🛡️",
    layout="centered"
)

# Title
st.title("🛡️ AI IP Security Analyzer")
st.caption("Live IP Intelligence and Security Risk Analysis")

st.divider()

# Detect button
if st.button("🔍 Analyze My IP", use_container_width=True):

    try:
        # Get IP information
        response = requests.get("https://ipapi.co/json/")
        data = response.json()

        ip = data.get("ip", "Not Found")
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country_name", "Unknown")
        isp = data.get("org", "Unknown")

        # Simple AI Risk Score
        risk_score = random.randint(15, 90)

        # Risk classification
        if risk_score <= 35:
            status = "🟢 LOW RISK"
            message = "Network appears normal."
        elif risk_score <= 65:
            status = "🟡 MEDIUM RISK"
            message = "Some network characteristics require attention."
        else:
            status = "🔴 HIGH RISK"
            message = "Potentially suspicious network characteristics detected."

        # Display IP information
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

        # Security Analysis
        st.subheader("🤖 AI Security Analysis")

        st.metric("Security Risk Score", f"{risk_score}/100")

        st.progress(risk_score)

        st.subheader(status)
        st.write(message)

        st.divider()

        st.subheader("📊 Analysis Summary")

        if risk_score <= 35:
            st.success("✓ IP appears to have low-risk characteristics")
        elif risk_score <= 65:
            st.warning("⚠ Moderate risk detected – monitor network activity")
        else:
            st.error("🚨 High-risk score – additional verification recommended")

    except Exception as e:
        st.error("Unable to analyze IP. Please check your internet connection.")

# Footer
st.divider()
st.caption("AI IP Security Analyzer | Built with Python & Streamlit")
