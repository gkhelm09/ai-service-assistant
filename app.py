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

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

icon_col, title_col = st.columns([1, 9], vertical_alignment="center")
with icon_col:
    st.image(str(ICON_PATH), width=52)
with title_col:
    st.markdown(
        '<h1 style="color: #004d7a; margin: 0; padding-top: 0.2rem;">AI BioMed Assistant</h1>',
        unsafe_allow_html=True,
    )
st.caption("Enter an equipment problem to receive AI troubleshooting guidance.")
st.info(
    "Privacy notice: Do not enter patient identifiers or PHI, confidential service "
    "information, or other sensitive data. Troubleshooting descriptions are sent "
    "to an external AI service."
)

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
        with st.spinner("Requesting troubleshooting guidance..."):
            response = generate_response(problem_description, equipment_type)

        # Store in conversation history only if no error
        if not response.get("error"):
            st.session_state.conversation_history.append({
                "equipment_type": equipment_type,
                "problem_description": problem_description,
                "response": response,
            })

        st.subheader("AI Response")
        st.caption(f"Equipment: **{response['equipment_type']}**")
        if response.get("error"):
            st.error(response["error"])

        st.markdown("### Possible Cause")
        st.write(response["possible_cause"])

        st.markdown("### Recommended Troubleshooting Steps")
        st.write(response["troubleshooting_steps"])

        st.markdown("### Safety Considerations")
        st.warning(response["safety_considerations"])

# Sidebar: Conversation History
with st.sidebar:
    st.markdown("## Troubleshooting History")
    
    if st.session_state.conversation_history:
        if st.button("🗑️ Clear History", key="clear_history_btn"):
            st.session_state.conversation_history = []
            st.rerun()
        
        st.markdown(f"**{len(st.session_state.conversation_history)} interaction(s)**")
        st.divider()
        
        for i, entry in enumerate(st.session_state.conversation_history, 1):
            with st.expander(
                f"#{i} {entry['equipment_type']} - {entry['problem_description'][:50]}..."
            ):
                st.markdown("**Problem:**")
                st.write(entry["problem_description"])
                st.markdown("**Possible Cause:**")
                st.write(entry["response"]["possible_cause"])
                st.markdown("**First Step:**")
                first_step = entry["response"]["troubleshooting_steps"].split("\n")[0]
                st.write(first_step)
    else:
        st.info("No troubleshooting history yet. Submit a problem to get started!")

st.divider()
st.markdown(
    "**Tip:** Run this app locally with:\n\n"
    "```bash\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py\n"
    "```"
)
