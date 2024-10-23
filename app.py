import streamlit as st
import requests

# Streamlit app to replicate the Invoice Validator Tool

# Title of the app
st.title("Invoice Validator")

# Domain selection
domain = st.selectbox("Select Domain", ("order",))  # Add more domains as needed

# Validation type selection
validation_type = st.selectbox(
    "Validate as",
    ("Select Validation Type", "UBL Invoice XML - release 1.3.13", 
     "CII Invoice XML - release 1.3.13", "UBL Credit Note XML - release 1.3.13")
)

# Choose how to provide input (file, URI, or direct input)
input_method = st.selectbox(
    "Input Method",
    ("Select Input Method", "File Upload", "URI Input", "Direct Input")
)

file_to_validate = None
uri_to_validate = None
string_to_validate = None

# Based on the selected input method, show relevant input fields
if input_method == "File Upload":
    file_to_validate = st.file_uploader("Upload Invoice File", type=["xml"])
elif input_method == "URI Input":
    uri_to_validate = st.text_input("Enter URI of the invoice")
elif input_method == "Direct Input":
    string_to_validate = st.text_area("Paste XML content of the invoice here")

# Button to submit the validation request
if st.button("Validate"):
    if validation_type == "Select Validation Type":
        st.error("Please select a validation type.")
    else:
        # Prepare the payload
        if file_to_validate is not None:
            xml_content = file_to_validate.read().decode('utf-8')  # Read and decode file content
            content_to_validate = xml_content
        elif uri_to_validate:
            content_to_validate = uri_to_validate
        elif string_to_validate:
            content_to_validate = string_to_validate
        else:
            st.error("Please provide input for validation.")
            st.stop()

        # Map validation type to API's expected type
        validation_type_map = {
            "UBL Invoice XML - release 1.3.13": "ubl",
            "CII Invoice XML - release 1.3.13": "cii",
            "UBL Credit Note XML - release 1.3.13": "credit"
        }
        
        selected_validation_type = validation_type_map[validation_type]

        # Prepare the JSON payload
        payload = {
            'contentToValidate': content_to_validate,
            'validationType': selected_validation_type  # Example value for validation type
        }

        # Perform the API request
        try:
            api_url = f"https://www.itb.ec.europa.eu/rest/{domain}/api/validate"  # Correct API URL
            st.write(f"Requesting URL: {api_url}")  # Debug line to check the URL
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=payload, headers=headers)

            # Display the result
            if response.status_code == 200:
                st.success("Invoice successfully validated!")
                st.json(response.json())  # Show the JSON response
            else:
                st.error(f"Validation failed with status code: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")