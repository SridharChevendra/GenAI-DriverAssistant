import streamlit as st
import json
import boto3
import requests
from vin_decoder_nhtsa.decoder import Vin
# https://pypi.org/project/vin-decoder-nhtsa/
# pip install vin-decoder-nhtsa
# from pyvin import VIN
# https://pypi.org/project/pyvin/

#########################
# variables
# Replace the below with your own values

s3_bucket = '<<S3 BUCKET NAME>>'
s3_prefix = 'images/'

api_gw_url = 'https://<<API END POINT>>/dev/claims'
api_gw_url1 = 'https://<API END POINT>>/dev/carinfo'


# Functions
# s3 upload function
def s3_upload(file, bucket, prefix):
    prefix_path = prefix + file.name
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(
            file,
            bucket,
            prefix_path
            )
        return prefix_path
    except:
        return None


# ask genAI model
def ask_model(source_img, input_query):
    url = api_gw_url
    params = {'source_img': source_img, 'input_query': input_query}
    response = requests.get(url, params)
    return st.write(f"Assistant: {response.json()}")

def car_info(input_query):
    url = api_gw_url1
    params = {'input_query': input_query}
    response = requests.get(url, params)
    return response.text


######################################    

# unique key generation for widgets
widget_id = (id for id in range(1, 100_00))

st.header("Digital Driver Assistance")
    
tab1,tab2,tab3,tab4 = st.tabs(["Overview","Roadside Assistance","Accident Management", "Providerclaim Management"])
    
with tab1:
        # st.header("Digital Driver Assistance")
        st.write("When you are on the Road, you need a piece of mind. Handle the wheel and leave rest to us.")
        images = ['Images/incident.png', 'Images/accident.png', 'Images/claims.png']
        captions = ['Roadside Assistance', 'Accident Management', 'Process Claims']
        cols = st.columns(len(images))
        for col in range(len(images)):
            with cols[col]:
                st.image(images[col], width=200, caption=captions[col])
        # st.image(images, width=200, caption=['Roadside Assistance', 'Accident Management', 'Process Claims'])
        st.write("Trusted by our customers 24x7, 365 days.")
        
with tab2:
        # text box to collect user input
        data = ''
        vin = st.text_input("VIN: ")
        
        st.write("Vehicle Info:")
        vehicleInfo = ["Fuel", "TowCapacity", "Coolant", "Battery"]
        cols = st.columns(len(vehicleInfo))
        for col in range(len(vehicleInfo)):
            with cols[col]:
                # cols[col] = st.checkbox(vehicleInfo[col])
                checkboxName = vehicleInfo[col]
                checkboxName = st.checkbox(vehicleInfo[col], key=vehicleInfo[col])

        st.write("Choice of language:")
        langs = ["English", "Spanish", "French", "German"]
        selected_lang = st.radio("", langs, key="language_radio")
        st.write(selected_lang)


        submitted = st.button("Submit")
        # fetch Vehicle data using VIN module
        if submitted:
            # Get the selected vehicle info options

            selected_vehicle_info = [vehicleInfo[i] for i in range(len(vehicleInfo)) if st.session_state.get(vehicleInfo[i], False)]
                        
            data = Vin(vin)
            st.write(selected_vehicle_info)
            st.subheader("Vechicle Details")
        if data:
            make = st.write("Make: ", data.Make)
            model = st.write("Model: ", data.Model)
            year = st.write("Model Year: ", data.ModelYear)
            hp = st.write("EngineHP: ", data.EngineHP)
            cylinders = st.write("EngineCylinders: ", data.EngineCylinders)
            fuelPrimary = st.write("FuelTypePrimary: ", data.FuelTypePrimary)
            fuelSecondary = st.write("FuelTypeSecondary: ", data.FuelTypeSecondary)
            tpms = st.write("TPMS: ", data.TPMS)
            battery = st.write("Battery Info: ", data.BatteryInfo)
            

            
            # Perform actions based on the selected options
            if "Fuel" in selected_vehicle_info:
                # Fetch fuel-related data or perform fuel-related actions
                st.write("Fetching fuel-related data...")
                st.write(car_info(f"What type of fuel for {data.Make} {data.Model} {data.ModelYear}? provide response in {selected_lang}"))
            if "TowCapacity" in selected_vehicle_info:
                # Fetch tow capacity-related data or perform tow capacity-related actions
                st.write("Fetching tow capacity-related data...")
                st.write(car_info("What are tow guidelines for {data.Make} {data.Model} {data.ModelYear}? provide response in {selected_lang}"))
            if "Coolant" in selected_vehicle_info:
                # Fetch coolant-related data or perform coolant-related actions
                st.write("Fetching coolant-related data...")
                st.write(car_info(f"What coolant specification for {data.Make} {data.Model} {data.ModelYear}? provide response in {selected_lang}"))
            if "Battery" in selected_vehicle_info:
                # Fetch battery-related data or perform battery-related actions
                st.write("Fetching battery-related data...")
                st.markdown(car_info(f"What are supported battery models for {data.Make} {data.Model} {data.ModelYear}? provide response in {selected_lang}"))
with tab3:
        # upload pictures
        st.write("Auto accident picture(s)")
        st.write("press upload button once the pictures are added.")
        documentImage = st.file_uploader("image(s): ", key=next(widget_id))

        if documentImage: 
            bytes_data = documentImage.getvalue()
            st.image(documentImage)
    
        documentImageUploaded = st.button("upload", key=next(widget_id))
        if documentImage is not None:
            if documentImageUploaded:
                response = s3_upload(documentImage, s3_bucket, s3_prefix)
                st.write(response)
        # Define the options for the radio buttons
        options = ["None","Initial assessment","Interactive mode"]

        # Create a radio button for each option
        selected_option = st.radio("Select an option", options)

        # unique key generation for widgets
        # widget_id = (id for id in range(1, 100_00))
        
        # Handle the selected option
        if selected_option == "Initial assessment":
            # Initial assessment
            st.subheader("Initial assessment")
            st.write("Generting the scene & damage assessment")
            source_img = s3_prefix + documentImage.name
            input_query = 'Describe car color, impacted parts, damage description, accuracy score in json format'
            ask_model(source_img, input_query)
    
        elif selected_option == "Interactive mode":
            # Interactive mode
            st.subheader("Interactive mode")
            st.write("Use the chat option to interact with AI assistant")
            # prompt = st.chat_input("What's up?", key=next(widget_id))
            prompt = st.text_area("What's up?", key="chat_input", height=100)
            if prompt:
                st.write("Agent:", prompt)
                source_img = s3_prefix + documentImage.name
                input_query = prompt
                response = ask_model(source_img, input_query)
        else:
            # please select an option
            st.write("Select one of the above options")
        
with tab4:
        # upload pictures
        st.write("Auto accident picture(s)")
        st.write("press upload button once the pictures are added.")
        documentImage = st.file_uploader("image(s): ", key=next(widget_id))

        if documentImage: 
            bytes_data = documentImage.getvalue()
            st.image(documentImage)
    
        documentImageUploaded = st.button("upload", key=next(widget_id))
        if documentImage is not None:
            if documentImageUploaded:
                response = s3_upload(documentImage, s3_bucket, s3_prefix)
                st.write(response)
        # st.subheader("Validate Claims")
        st.write("Validate claim description with image and generate confidence score")
        # prompt = st.chat_input("provide claim text", key=next(widget_id))
        prompt = st.text_area("provide claim text", key="claim_input", height=100)
        if prompt:
            st.write("Agent:", prompt)
            source_img = s3_prefix + documentImage.name
            input_query = prompt
            response = ask_model(source_img, input_query)

        
            

        


           



        
        
                 
    