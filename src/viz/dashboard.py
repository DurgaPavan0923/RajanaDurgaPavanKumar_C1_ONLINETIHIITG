"""Streamlit Monitoring Dashboard for Water Potability & Underwater Environmental Telemetry."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# Configure dashboard page
st.set_page_config(
    page_title="Water Environmental Monitor & Potability AI",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 Underwater Environmental Monitoring & Water Potability AI")
st.markdown(
    "**Acyntra AIML Project Cadre** | Real-time Sensor Telemetry, Anomaly Detection & Potability Risk Assessment"
)

# Sidebar track selection
track_choice = st.sidebar.radio(
    "Select Operational Track:",
    ["Track B: Water Potability (Tabular)", "Track A: Underwater Telemetry (Stream)"],
)

if track_choice == "Track B: Water Potability (Tabular)":
    st.header("💧 Track B: Physicochemical Potability Assessment & Outlier Detection")

    data_file = Path("data/01_raw/water_potability.csv")
    if data_file.exists():
        df = pd.read_csv(data_file)
        st.subheader("Raw Water Sample Telemetry (Preview)")
        st.dataframe(df.head(10), use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Water Samples", len(df))
        col2.metric("Features Tracked", len(df.columns) - 1)
        potable_ratio = (df["Potability"] == 1).mean() if "Potability" in df else 0.0
        col3.metric("Empirical Potability Rate", f"{potable_ratio:.1%}")
        col4.metric("Missing pH Records", int(df["ph"].isna().sum()))

        st.subheader("Interactive Sample Inference & Regulatory WHO Check")
        with st.form("potability_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                input_ph = st.number_input("pH (0-14)", min_value=0.0, max_value=14.0, value=7.2)
                input_hardness = st.number_input(
                    "Hardness (mg/L)", min_value=10.0, max_value=500.0, value=190.0
                )
                input_solids = st.number_input(
                    "Solids (ppm)", min_value=100.0, max_value=60000.0, value=21000.0
                )
            with c2:
                input_chlor = st.number_input(
                    "Chloramines (ppm)", min_value=0.0, max_value=20.0, value=6.5
                )
                input_sulfate = st.number_input(
                    "Sulfate (mg/L)", min_value=10.0, max_value=800.0, value=330.0
                )
                input_cond = st.number_input(
                    "Conductivity (uS/cm)", min_value=10.0, max_value=2000.0, value=420.0
                )
            with c3:
                input_org = st.number_input(
                    "Organic Carbon (ppm)", min_value=0.0, max_value=50.0, value=14.0
                )
                input_thm = st.number_input(
                    "Trihalomethanes (ug/L)", min_value=0.0, max_value=250.0, value=65.0
                )
                input_turb = st.number_input(
                    "Turbidity (NTU)", min_value=0.0, max_value=20.0, value=3.8
                )

            submitted = st.form_submit_button("Run Classification & Anomaly Check")

            if submitted:
                # WHO guideline check
                who_violations = []
                if not (6.5 <= input_ph <= 8.5):
                    who_violations.append(f"pH ({input_ph}) outside [6.5, 8.5]")
                if input_turb > 5.0:
                    who_violations.append(f"Turbidity ({input_turb} NTU) exceeds 5.0 limit")
                if input_chlor > 4.0:
                    who_violations.append(f"Chloramines ({input_chlor} ppm) exceeds 4.0 limit")
                if input_sulfate > 250.0:
                    who_violations.append(f"Sulfate ({input_sulfate} mg/L) exceeds 250.0 limit")

                st.markdown("### Decision Results")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    if who_violations:
                        st.error(
                            f"❌ WHO Regulatory Non-Compliant ({len(who_violations)} violations)"
                        )
                        for v in who_violations:
                            st.write(f"- {v}")
                    else:
                        st.success("✅ Fully Compliant with WHO Standards")

                with res_col2:
                    model_path = Path("models/production/water_potability_pipeline_v1.joblib")
                    if model_path.exists():
                        bundle = joblib.load(model_path)
                        clf = bundle.get("classifier")
                        st.info(f"Model Candidate: {bundle.get('model_name')}")
                    else:
                        st.warning(
                            "Production model bundle not yet compiled. Run 'make train' first."
                        )

    else:
        st.error(f"Dataset not found at {data_file}. Verify data/01_raw directory.")

else:
    st.header("🌊 Track A: Underwater Environmental Continuous Stream Monitoring")
    stream_file = Path("data/01_raw/underwater_sensor_stream.csv")
    if stream_file.exists():
        df_stream = pd.read_csv(stream_file)
        df_stream["timestamp"] = pd.to_datetime(df_stream["timestamp"])
        st.subheader("Continuous Stream Timeline")

        sensor_to_view = st.selectbox(
            "Select Sensor Telemetry to Inspect:",
            ["dissolved_oxygen", "temperature", "ph", "turbidity", "conductivity", "pressure"],
        )

        st.line_chart(df_stream.set_index("timestamp")[sensor_to_view])

        st.subheader("Statistical Summary")
        st.write(df_stream.describe())
    else:
        st.error(f"Telemetry stream file not found at {stream_file}.")
