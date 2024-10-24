import streamlit as st
from zeep import Client
import xml.etree.ElementTree as ET

# SOAP WSDL URL
WSDL_URL = 'https://www.itb.ec.europa.eu/invoice/api/validation?wsdl'

# Initialize SOAP client
client = Client(wsdl=WSDL_URL)

# App title
st.title("eInvoice Validator")

# Sidebar options for validation type
validation_type = st.sidebar.selectbox(
    "Select Validation Type",
    ("UBL Invoice XML - release 1.3.13", "CII Invoice XML - release 1.3.13", "UBL Credit Note XML - release 1.3.13")
)

# Map validation type to the values expected by the SOAP API
validation_type_map = {
    "UBL Invoice XML - release 1.3.13": "ubl",
    "CII Invoice XML - release 1.3.13": "cii",
    "UBL Credit Note XML - release 1.3.13": "credit"
}
validation_type_value = validation_type_map[validation_type]

# Allow user to upload file, input URL, or paste XML
option = st.selectbox(
    "Choose Input Type",
    ["Upload XML File", "Input URL", "Direct XML Input"]
)

if option == "Upload XML File":
    uploaded_file = st.file_uploader("Choose an XML file to validate", type="xml")
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
elif option == "Input URL":
    file_url = st.text_input("Enter the URL of the XML file to validate")
    if file_url:
        # You may fetch content from the URL if required
        file_content = file_url
elif option == "Direct XML Input":
    file_content = st.text_area("Paste the XML content directly")

# Validate button
if st.button("Validate Invoice"):
    if file_content:
        try:
            # Assuming a SOAP API operation called `validateInvoice` (Check WSDL for exact names)
            response = client.service.validateInvoice(
                validationType=validation_type_value,
                fileContent=file_content
            )

            # Process and display the response
            st.success("Invoice validation successful!")
            st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide the invoice content for validation.")