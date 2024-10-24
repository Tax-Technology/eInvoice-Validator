import streamlit as st
from zeep import Client
from zeep.transports import Transport
import requests
from io import BytesIO

# SOAP API WSDL URL
wsdl_url = "https://www.itb.ec.europa.eu/invoice/api/validation?wsdl"

# SOAP Client Setup
client = Client(wsdl_url)

# Streamlit App
st.title("eInvoice Validator")

# User File Upload
st.subheader("Upload an eInvoice XML File for Validation")
uploaded_file = st.file_uploader("Choose an XML file", type="xml")

# Validation Type Dropdown
validation_type = st.selectbox(
    "Validate as", 
    ["UBL Invoice XML", "CII Invoice XML", "UBL Credit Note XML"]
)

# Map user-friendly type to API type
validation_type_mapping = {
    "UBL Invoice XML": "ubl",
    "CII Invoice XML": "cii",
    "UBL Credit Note XML": "credit"
}

# If file is uploaded
if uploaded_file is not None and validation_type:
    st.write(f"Validating as {validation_type}...")

    # Convert uploaded file to bytes
    xml_data = uploaded_file.read()

    # Show content of the file
    st.text_area("Uploaded XML Content", xml_data.decode("utf-8"), height=200)

    # Create SOAP API request to validate the file
    if st.button("Validate"):
        try:
            # Make SOAP API call to validate the XML file
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
            st.error(f"An error occurred: {str(e)}")