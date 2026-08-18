"""AI BioMed Assistant - a simple Streamlit app for biomedical field service."""

import importlib
from pathlib import Path

import streamlit as st

import assistant

importlib.reload(assistant)
from assistant import EQUIPMENT_TYPES, generate_response

ICON_PATH = Path(__file__).parent / "assets" / "multimeter.svg"

st.set_page_config(
    page_title="AI BioMed Assistant",
    page_icon=str(ICON_PATH),
    layout="centered",
)

icon_col, title_col = st.columns([1, 9], vertical_alignment="center")
with icon_col:
    st.image(str(ICON_PATH), width=52)
with title_col:
    st.markdown(
        '<h1 style="color: #004d7a; margin: 0; padding-top: 0.2rem;">AI BioMed Assistant</h1>',
        unsafe_allow_html=True,
    )
st.caption("Enter an equipment problem to receive simulated troubleshooting guidance.")

with st.form("problem_form"):
    equipment_type = st.selectbox(
        "Equipment category",
        EQUIPMENT_TYPES,
        help="Select the type of equipment you are troubleshooting.",
    )
    problem_description = st.text_area(
        "Equipment problem description",
        placeholder=(
            "Example: Detector intermittently loses connection during patient exams."
        ),
        height=150,
    )
    submitted = st.form_submit_button("Get Troubleshooting Help", type="primary")

if submitted:
    if not problem_description.strip():
        st.warning("Please enter a problem description before submitting.")
    else:
        response = generate_response(problem_description, equipment_type)

        st.subheader("Simulated AI Response")
        st.caption(
            f"Equipment: **{response['equipment_type']}** | "
            f"Matched category: **{response['category']}**"
        )
        st.info(
            "This is a simulated response for demo purposes. "
            "Connect a real AI API later to generate live guidance."
        )

        st.markdown("### Possible Cause")
        st.write(response["possible_cause"])

        st.markdown("### Recommended Troubleshooting Steps")
        st.write(response["troubleshooting_steps"])

        st.markdown("### Safety Considerations")
        st.warning(response["safety_considerations"])

st.divider()
st.markdown(
    "**Tip:** Run this app locally with:\n\n"
    "```bash\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py\n"
    "```"
)
