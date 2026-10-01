
import os

import requests
import streamlit as st

from dotenv import load_dotenv
from utils.exporters import (
    export_txt,
    export_pdf,
    export_docx
)

load_dotenv()

# PAGE CONFIGURATION
st.set_page_config(
    page_title="LegalEase | AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide"
)

# CUSTOM CSS
st.markdown(
    """
    <style>

    .stApp {
        background-color: #101827;
        color: #edf2f7;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 35px;
        border: 1px solid #34445c;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #172338,
            #243b55
        );
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        color: #b8c7dc;
        font-size: 17px;
    }

    .section-title {
        color: #8fc7ff;
        font-size: 23px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .info-card {
        background: #172338;
        border: 1px solid #34445c;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-color: #1d4ed8;
        color: white;
        border: none;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 25px;
        margin-top: 40px;
        border-top: 1px solid #34445c;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# HEADER
st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p>
            AI-Powered Legal Document Generator
        </p>

        <p>
            Create, customize and download legal document drafts easily.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# WARNING
st.warning(
    "⚠️ LegalEase generates document drafts, not legal advice. "
    "Please review generated documents with a qualified legal professional."
)

# SIDEBAR
with st.sidebar:

    st.title("⚖️ LegalEase")

    st.markdown("---")

    st.subheader("About Project")

    st.write(
        "LegalEase is an AI-powered legal document "
        "generation application."
    )

    st.markdown("---")

    st.subheader("Features")

    st.write("📄 Multiple document types")
    st.write("🤖 AI document generation")
    st.write("✏️ Editable document preview")
    st.write("⬇️ Multiple download formats")

    st.markdown("---")

    st.caption("Version 1.0.0")

# MAIN FORM
st.markdown(
    '<p class="section-title">📝 Create Your Legal Document</p>',
    unsafe_allow_html=True
)

with st.form("document_form"):

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Document Information")

        document_type = st.selectbox(
            "Document Type",
            [
                "Non-Disclosure Agreement (NDA)",
                "Employment Contract",
                "Residential Lease Agreement",
                "Freelance Work Contract",
                "Service Agreement",
                "Employment Offer Letter",
                "General Agreement"
            ]
        )

        parties = st.text_area(
            "Parties Involved",
            placeholder=(
                "Jane Doe (Service Provider), "
                "ABC Company (Client)"
            ),
            height=110
        )

        effective_date = st.text_input(
            "Effective Date",
            placeholder="1 October 2026"
        )

    with col2:

        st.markdown("### Agreement Details")

        jurisdiction = st.text_input(
            "Jurisdiction",
            placeholder="Tamil Nadu, India"
        )

        terms = st.text_area(
            "Terms and Conditions",
            placeholder=(
                "Payment within 30 days; "
                "Confidentiality must be maintained; "
                "Either party may terminate with 15 days notice."
            ),
            height=160
        )

        additional_instructions = st.text_area(
            "Additional Instructions",
            placeholder="Enter any additional requirements...",
            height=110
        )

    submitted = st.form_submit_button(
        "✨ Generate Legal Document",
        use_container_width=True
    )

# GENERATE DOCUMENT
if submitted:

    if (
        not parties.strip()
        or not terms.strip()
        or not effective_date.strip()
    ):

        st.error(
            "Please complete Parties, Terms and Effective Date."
        )

    else:

        backend_url = os.getenv(
            "BACKEND_URL",
            "http://127.0.0.1:8000"
        ).rstrip("/")

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
            "jurisdiction": jurisdiction or "Not specified",
            "additional_instructions": additional_instructions
        }

        try:

            with st.spinner(
                "🤖 Generating your legal document..."
            ):

                response = requests.post(
                    backend_url + "/generate",
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

            if "document" not in data:
                st.error("Backend did not return a document.")
            else:

                st.session_state["document"] = data["document"]

                st.session_state["model"] = data.get(
                    "model",
                    "AI Model"
                )

                st.session_state["demo_mode"] = data.get(
                    "demo_mode",
                    False
                )

                st.session_state["document_type"] = document_type

                st.session_state["edited_document"] = data["document"]

                st.success(
                    "Your document has been generated successfully!"
                )

        except requests.RequestException as error:

            st.error(
                f"Backend connection failed: {error}"
            )

        except (ValueError, KeyError) as error:

            st.error(
                f"Invalid backend response: {error}"
            )

# DOCUMENT PREVIEW
if "document" in st.session_state:

    st.markdown("---")

    st.markdown(
        '<p class="section-title">📄 Generated Document Preview</p>',
        unsafe_allow_html=True
    )

    if st.session_state.get("demo_mode"):

        st.info(
            "Demo mode is active. Add your Gemini API key "
            "to enable AI-powered document generation."
        )

    else:

        st.success(
            f"Generated using {st.session_state.get('model')}"
        )

    # EDITABLE DOCUMENT
    edited_document = st.text_area(
        "Edit Your Document",
        value=st.session_state["document"],
        height=450,
        key="edited_document"
    )

    st.session_state["document"] = edited_document

    filename = "legalease_document"

    doc_title = st.session_state.get(
        "document_type",
        "LegalEase Document"
    )

    # DOWNLOAD SECTION
    st.markdown("---")

    st.markdown(
        '<p class="section-title">⬇️ Download Your Document</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose your preferred format to download the document."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=export_txt(edited_document),
            file_name=filename + ".txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="📝 Download DOCX",
            data=export_docx(
                edited_document,
                doc_title
            ),
            file_name=filename + ".docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )

    with col3:

        st.download_button(
            label="📕 Download PDF",
            data=export_pdf(
                edited_document,
                doc_title
            ),
            file_name=filename + ".pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.success(
        "Your document is ready to download!"
    )

# FOOTER
st.markdown(
    """
    <div class="footer">

        <h4>⚖️ LegalEase</h4>

        <p>
            AI-Powered Legal Document Generator
        </p>

        <p>
            © 2026 LegalEase | Academic Project
        </p>

        <small>
            This application provides document drafts for educational purposes.
        </small>

    </div>
    """,
    unsafe_allow_html=True
)