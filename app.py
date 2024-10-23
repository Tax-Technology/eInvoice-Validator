import streamlit as st
import requests

# Streamlit app to replicate the Invoice Validator Tool
st.title("Invoice Validator")

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
        # Prepare the payload based on user input
        input_data = None
        if file_to_validate is not None:
            # Read the content of the uploaded file
            input_data = file_to_validate.getvalue().decode("utf-8")
        elif uri_to_validate:
            input_data = uri_to_validate  # Assuming this will be processed by the API
        elif string_to_validate:
            input_data = string_to_validate

        if input_data is None:
            st.error("Please provide input for validation.")
            st.stop()

        # Prepare the payload for the API request
        payload = {
            "contentToValidate": input_data,
            "validationType": validation_type,  # This might need to match the API's expected format
            # You can add other parameters like externalSchemas, locale, etc. if required
        }

        # Perform the API request
        try:
            api_url = "https://www.itb.ec.europa.eu/vitb/rest/api/validate"  # Correct API endpoint for validation
            with st.spinner('Validating invoice...'):
                response = requests.post(api_url, json=payload)

            # Display the result
            if response.status_code == 200:
                st.success("Invoice successfully validated!")
                validation_results = response.json()
                st.json(validation_results)  # Show the JSON response
            else:
                st.error(f"Validation failed with status code: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")