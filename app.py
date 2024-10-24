import streamlit as st
from zeep import Client
from zeep.transports import Transport
import requests
from io import BytesIO
import xml.etree.ElementTree as ET

# SOAP API WSDL URL
wsdl_url = "https://www.itb.ec.europa.eu/invoice/api/validation?wsdl"

# SOAP Client Setup
client = Client(wsdl_url)

# Streamlit App
st.title("eInvoice Validator")

# File or URI or Direct Input selection
validation_method = st.selectbox(
    "Choose validation input method", 
    ["File", "URI", "Direct input"]
)

# File Input
uploaded_file = None
xml_data = None
if validation_method == "File":
    uploaded_file = st.file_uploader("Select the XML file", type="xml")
    if uploaded_file:
        xml_data = uploaded_file.read()
        st.text_area("Uploaded XML Content", xml_data.decode("utf-8"), height=200)

# URI Input
if validation_method == "URI":
    uri = st.text_input("Enter XML URI")
    if uri:
        try:
            response = requests.get(uri)
            if response.status_code == 200:
                xml_data = response.content
                st.text_area("XML Content from URI", xml_data.decode("utf-8"), height=200)
            else:
                st.error("Failed to fetch the XML from the URI.")
        except Exception as e:
            st.error(f"Error fetching URI: {e}")

# Direct Input
if validation_method == "Direct input":
    xml_input = st.text_area("Paste your XML content here", height=200)
    if xml_input:
        xml_data = xml_input.encode("utf-8")

# Validation Type Dropdown
validation_type = st.selectbox(
    "Validate as", 
    ["UBL Invoice XML - release 1.3.13", "CII Invoice XML - release 1.3.13", "UBL Credit Note XML - release 1.3.13"],
    index=0
)

# Map validation types
validation_type_mapping = {
    "UBL Invoice XML - release 1.3.13": "ubl",
    "CII Invoice XML - release 1.3.13": "cii",
    "UBL Credit Note XML - release 1.3.13": "credit"
}

# Checkbox for including external artefacts
include_external = st.checkbox("Include external artefacts (e.g., XML Schema, Schematron)")

# XML Schema and Schematron inputs (conditionally displayed if checkbox is selected)
external_schema = None
external_schematron = None
if include_external:
    st.text("Provide additional artefacts for validation")
    external_schema = st.text_input("XML Schema URL")
    external_schematron = st.text_input("Schematron URL")

# Validate button
if xml_data and st.button("Validate"):
    # Attempt validation if XML is provided
    try:
        # Optional external artefact handling can be added here if needed
        
        # Make SOAP API call
        with st.spinner("Validating..."):
            validation_response = client.service.validate(
                xmlContent=xml_data,
                validationType=validation_type_mapping[validation_type]
            )
        
        # Display validation result
        if validation_response:
            st.success("Validation Successful")
            st.write("Validation Response:", validation_response)
        else:
            st.error("Validation Failed")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

