import streamlit as st
import pickle
import pandas as pd
import base64

# Load the trained model
with open(r"pro3\Scripts\Demo3.pkl", "rb") as f:
    model = pickle.load(f)

# Set page configuration
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"C:\Users\sayas\Downloads\Project3\pro3\Scripts\CR1.jpg")

st.title("🚗 Car Price Prediction App")
st.write("Fill in the details below to estimate the car's price.")

# Encoding mappings (must match training data)
city_mapping = {
    "Kolkata": 0, "Jaipur": 1, "Hyderabad": 2, "Delhi": 3, "Chennai": 4, "Bangalore": 5
}

body_type_mapping = {
    "Sedan": 0, "Hatchback": 1, "SUV": 2, "MUV": 3, "Coupe": 4, "Convertibles": 5,
    "Minivans": 6, "Pickup Trucks": 7, "Wagon": 8, "Hybrids": 9
}

oem_mapping = {oem: idx for idx, oem in enumerate([
    'Toyota', 'Datsun', 'Renault', 'Hyundai', 'Audi', 'Maruti', 'Tata', 'Jeep',
    'Land Rover', 'Honda', 'Mercedes-Benz', 'Mahindra', 'Skoda', 'BMW', 'Fiat',
    'Ford', 'Hindustan Motors', 'Volvo', 'Chevrolet', 'Kia', 'MG', 'Volkswagen',
    'Porsche', 'Nissan', 'Jaguar', 'Mahindra Ssangyong', 'Mahindra Renault',
    'Mitsubishi', 'Isuzu', 'Citroen', 'Lexus', 'Mini', 'Opel'
])}

model_mapping = {model: idx for idx, model in enumerate([
    'Toyota Camry', 'Datsun RediGO', 'Renault Kiger', 'Hyundai i20', 'Audi Q3',
    'Maruti Wagon R', 'Hyundai Santro', 'Renault KWID', 'Maruti Swift Dzire',
    'Maruti Swift', 'Hyundai i10', 'Tata Harrier', 'Maruti Baleno',
    'Toyota Fortuner', 'Jeep Compass', 'Land Rover Range Rover Evoque',
    'Maruti Alto K10', 'Tata Nexon', 'Maruti Ciaz', 'Honda City',
    'Hyundai Grand i10 Nios', 'Hyundai Creta', 'Hyundai Verna', 'Maruti Celerio',
    'Hyundai Grand i10', 'Mercedes-Benz E-Class', 'Toyota Yaris',
    'Mahindra Marazzo', 'Honda Civic', 'Tata Tiago', 'Honda Amaze', 'Skoda Rapid',
    'Hyundai Santro Xing', 'BMW 3 Series', 'Fiat Linea', 'BMW 5 Series',
    'Jeep Wrangler', 'Honda BR-V', 'Ford Ecosport', 'Honda Jazz', 'Honda WR-V',
    'Honda Brio', 'Audi A6', 'Ambassador', 'Hyundai Elantra',
    'Mercedes-Benz C-Class', 'Maruti Ertiga', 'Maruti Alto',
    'Mahindra KUV 100 NXT', 'Tata Altroz', 'Skoda Laura', 'Maruti Zen Estilo',
    'Audi Q5', 'Maruti A-Star', 'Toyota Innova', 'Toyota Corolla Altis',
    'Tata New Safari', 'Mahindra XUV500', 'Hyundai i20 Active',
    'Volvo S60 Cross Country', 'Volvo XC60', 'Chevrolet Tavera',
    'Renault Duster', 'Kia Seltos', 'Jeep Compass Trailhawk',
    'Land Rover Range Rover Velar', 'MG Gloster', 'MG Hector', 'Hyundai EON',
    'Chevrolet Spark', 'Maruti Ritz', 'Maruti Alto 800', 'Tata Tigor',
    'Maruti Wagon R Stingray', 'Volkswagen Ameo', 'Mahindra Scorpio',
    'Maruti XL6', 'Maruti SX4 S Cross', 'Mahindra TUV 300', 'Renault Scala',
    'Hyundai i20 N Line', 'Mahindra KUV 100', 'Maruti Ignis',
    'Toyota Innova Crysta', 'Tata Sumo Victa', 'BMW 6 Series', 'Hyundai Alcazar',
    'Volkswagen Polo', 'Maruti Vitara Brezza', 'Skoda Fabia', 'Maruti S-Presso',
    'Porsche Macan', 'BMW X3', 'Tata Manza', 'Renault Captur', 'Volkswagen Jetta',
    'Chevrolet Sail', 'Kia Sonet', 'Honda New Accord', 'Toyota Urban cruiser',
    'Nissan Micra Active', 'Mercedes-Benz GLC', 'Volvo V40', 'Skoda Kushaq',
    'Mercedes-Benz GLA Class', 'BMW X1', 'MG Hector Plus', 'Hyundai Xcent',
    'Jaguar XJ', 'Porsche Panamera', 'Mercedes-Benz GLE', 'Mahindra Bolero',
    'Hyundai Sonata', 'Audi Q2', 'Volkswagen Vento', 'Mahindra Thar',
    'Hyundai Venue', 'Mahindra XUV300', 'Toyota Etios Liva', 'Ford Endeavour',
    'Toyota Etios', 'Nissan Micra', 'Tata Zest', 'Mercedes-Benz AMG GT',
    'Mahindra Alturas G4', 'Ford Figo', 'Chevrolet Beat', 'Maruti Brezza',
    'Nissan Terrano', 'Mercedes-Benz CLA', 'Datsun GO', 'Tata Indica',
    'Tata Indigo', 'Ford Aspire', 'Land Rover Freelander 2', 'Audi A4',
    'Tata Hexa', 'BMW 3 Series Gran Limousine', 'Audi S5 Sportback',
    'Chevrolet Aveo', 'Hyundai Accent', 'Renault Pulse', 'Audi A3',
    'Mahindra Ssangyong Rexton', 'Maruti Zen', 'Tata Punch', 'BMW 3 Series GT',
    'Ford Fiesta', 'Nissan Magnite', 'Maruti Celerio X', 'Mahindra XUV700',
    'Mahindra Renault Logan', 'Honda Mobilio', 'Tata Tiago NRG',
    'Mercedes-Benz GL-Class', 'Kia Carens', 'Mahindra Bolero Neo',
    'Jeep Meridian', 'Skoda Superb', 'Hyundai Aura', 'Ford Fiesta Classic',
    'Chevrolet Cruze', 'Mahindra Scorpio N', 'Toyota Etios Cross', 'MG Astor',
    'Datsun GO Plus', 'Jaguar F-TYPE', 'Maruti Eeco', 'Toyota Fortuner Legender',
    'Mahindra Xylo', 'Toyota Glanza', 'Land Rover Discovery Sport',
    'Mercedes-Benz M-Class', 'Fiat Grande Punto', 'Hyundai Xcent Prime',
    'Maruti 800', 'BMW 7 Series', 'Skoda Kodiaq', 'BMW X5', 'Tata Nano',
    'Skoda Slavia', 'Maruti SX4', 'Skoda Octavia', 'Volkswagen Taigun',
    'Mitsubishi Pajero', 'Honda CR-V', 'Audi Q7', 'Mercedes-Benz GLS',
    'Jaguar XF', 'Mercedes-Benz AMG GLC 43', 'Chevrolet Aveo U-VA',
    'Mercedes-Benz A Class', 'Isuzu D-Max', 'Tata Safari Storme', 'Hyundai Getz',
    'Hyundai Santa Fe', 'Mahindra Bolero Camper', 'Mahindra Bolero Power Plus',
    'Maruti Omni', 'Chevrolet Optra', 'Maruti Esteem', 'Citroen C3',
    'Maruti Baleno RS', 'Mahindra Quanto', 'Maruti Swift Dzire Tour',
    'Jaguar XE', 'Fiat Avventura', 'Volkswagen Passat', 'Volkswagen CrossPolo',
    'Maruti Jimny', 'Fiat Punto EVO', 'Volvo S60', 'Nissan Kicks',
    'Ford Freestyle', 'Citroen C5 Aircross', 'Maruti Gypsy',
    'Mercedes-Benz S-Class', 'Chevrolet Enjoy', 'Nissan Sunny', 'BMW 1 Series',
    'Land Rover Range Rover Sport', 'Volkswagen Virtus',
    'Land Rover Range Rover', 'Renault Triber', 'Honda City Hybrid',
    'Fiat Punto', 'Tata Indica V2', 'Tata Aria', 'Volvo XC 90', 'Kia Carnival',
    'Tata Bolt', 'Mahindra E Verito', 'Fiat Abarth Avventura',
    'Tata Yodha Pickup', 'Tata Indigo Marina', 'Chevrolet Captiva',
    'Mahindra Bolero Pik Up Extra Long', 'Ford Ikon', 'Mercedes-Benz B Class',
    'Jaguar F-Pace', 'Toyota Qualis', 'Toyota Corolla', 'Isuzu MU-X',
    'Land Rover Defender', 'Mercedes-Benz GLC Coupe', 'Lexus RX',
    'Mitsubishi Outlander', 'Mercedes-Benz CLS-Class', 'Mini Cooper Clubman',
    'Land Rover Discovery', 'Mercedes-Benz AMG A 35', 'Porsche Cayenne',
    'Mercedes-Benz AMG G 63', 'BMW X7', 'Volvo XC40', 'BMW X4',
    'Mercedes-Benz GLA', 'Mercedes-Benz G', 'Mini Cooper Convertible',
    'Mini Cooper', 'Toyota Land Cruiser 300', 'Mahindra Scorpio Classic',
    'Hyundai Tucson', 'Volvo S90', 'Mercedes-Benz SLC',
    'Mercedes-Benz A-Class Limousine', 'Maruti Grand Vitara', 'Toyota Hyryder',
    'Mini Cooper Countryman', 'Maruti FRONX', 'Lexus ES', 'Maruti Ertiga Tour',
    'Isuzu MU 7', 'Renault Fluence', 'Mitsubishi Cedia', 'Mini 5 DOOR',
    'Maruti Versa', 'Mitsubishi Lancer', 'Fiat Punto Pure', 'Volvo S 80',
    'Skoda Yeti', 'Audi A8', 'Mercedes-Benz AMG GLA 35', 'Mahindra TUV 300 Plus',
    'Volkswagen Tiguan', 'Mini 3 DOOR', 'Renault Lodgy', 'Volkswagen T-Roc',
    'Mahindra Verito', 'Mahindra e2o Plus', 'Fiat Punto Abarth', 'OpelCorsa',
    'Volkswagen Tiguan Allspace', 'Tata Sumo', 'Fiat Palio', 'Audi A3 cabriolet'
])}

variant_mapping = {variant: idx for idx, variant in enumerate([
    'Hybrid', 'T Option', 'RXT AMT', '1.2 V AT i VTEC Privilege', 'Diesel E4',
    '1.4 Asta Dual Tone'
])}

insurance_mapping = {
    "Third Party": 0, "Comprehensive": 1, "Zero Dep": 2, "No insurance": 3,
    "Basic Coverage": 4, "Extended Coverage": 5
}

fuel_mapping = {
    "Petrol": 0, "Diesel": 1, "CNG": 2, "LPG": 3, "Electric": 4
}

ownership_mapping = {
    "First Owner": 0, "Second Owner": 1, "Third Owner": 2,
    "Fourth Owner": 3, "Fifth Owner": 4
}

transmission_mapping = {
    "Automatic": 0, "Manual": 1
}

color_mapping = {color: idx for idx, color in enumerate([
    'White', 'Red', 'Blue', 'Brown', 'Silver', 'Grey', 'Black', 'Gray', 'Green',
    'Others', 'Maroon', 'Golden', 'Foliage', 'Sky Blue', 'Orange', 'Off White',
    'Bronze', 'G Brown', 'Purple', 'Golden Brown', 'Parpel', 'Yellow', 'Cherry Red',
    'Sunset Red', 'Silicon Silver', 'golden brown', 'Dark Blue',
    'Technometgrn+Gryroof', 'Light Silver', 'Gold', 'Out Back Bronze', 'Violet',
    'Bright Silver', 'Porcelain White', 'Tafeta White', 'Coral White',
    'Diamond White', 'Brick Red', 'Carnelian Red Pearl',
    'Urban Titanium Metallic', 'Silky silver', 'Mediterranean Blue',
    'Mist Silver', 'Gravity Gray', 'Candy White', 'Metallic Premium silver',
    'Polar White', 'Glistening Grey', 'Super white', 'Deep Black Pearl',
    'PLATINUM WHITE PEARL', 'Twilight Blue', 'Caviar Black',
    'Pearl Met. Arctic White', 'Superior white', 'Pearl White', 'Sleek Silver',
    'Phantom Black', 'Metallic silky silver', 'Pearl Arctic White', 'Pure white',
    'Smoke Grey', 'Fiery Red', 'StarDust', 'Alabaster Silver Metallic - Amaze',
    'Ray blue', 'Glacier White Pearl', 'OUTBACK BRONZE', 'Granite Grey',
    'Solid Fire Red', 'Daytona Grey', 'Metallic Azure Grey', 'Moonlight Silver',
    'Aurora Black Pearl', 'Fire Brick Red', 'Cashmere', 'Pearl Snow White',
    'Minimal Grey', 'Metallic Glistening Grey', 'Light Orange', 'Hip Hop Black',
    'Nexa Blue', 'Passion Red', 'Cirrus White', 'Arizona Blue', 'Beige',
    'Galaxy Blue', 'Silky Silver', 'Modern Steel Metal', 'GOLDEN BROWN',
    'magma gray', 'CBeige', 'Goldan BRWOON', 'm grey', 'urban titanim', 'g brown',
    'beige', 'Rosso Brunello', 'b grey', 'Radiant Red M', 'c bronze',
    'Champagne Mica Metallic', 'MODERN STEEL METALLIC', 'Bold Beige Metallic',
    'Starry Black', 'Symphony Silver', 'Metallic Magma Grey', 'c brown', 'chill',
    'Modern Steel Metallic', 'Arctic Silver', 'Medium Blue',
    'Alabaster Silver Metallic', 'Carbon Steel', 'Cavern Grey', 'ESPRESO_BRWN',
    'Magma Grey', 'Dark Red', 'Falsa Colour', 'Cherry', 'TAFETA WHITE', 'P Black',
    'Golden brown', 'Star Dust', 'METALL', 'MET ECRU BEIGE', 'COPPER', 'TITANIUM',
    'CHILL', 'TITANIUM GREY', 'Burgundy', 'Lunar Silver Metallic', 'SILKY SILVER',
    'BERRY RED', 'PREMIUM AMBER METALLIC', 'PLATINUM SILVER',
    'ORCHID WHITE PEARL', 'CARNELIAN RED PEARL', 'POLAR WHITE', 'BEIGE',
    'O Purple', 'Other', 'PLATINUM WHITE', 'Flash Red', 'Wine Red',
    'Taffeta White', 'T Wine', 'Prime Star Gaze'
])}


# Input fields with dropdowns
city = st.selectbox("🌍 City", list(city_mapping.keys()))
body_type = st.selectbox("🚙 Body Type", list(body_type_mapping.keys()))
kms_driven = st.number_input("🏁 Kilometers Driven", min_value=0)
oem = st.selectbox("🏭 Manufacturer (OEM)", list(oem_mapping.keys()))
model_name = st.selectbox("🚗 Model Name", list(model_mapping.keys()))
model_year = st.number_input("📅 Model Year", min_value=1998, max_value=2025, step=1)
variant_name = st.selectbox("⚙️ Variant", list(variant_mapping.keys()))
insurance_validity = st.selectbox("🛡️ Insurance Validity", list(insurance_mapping.keys()))
fuel_type = st.selectbox("⛽ Fuel Type", list(fuel_mapping.keys()))
seating_capacity = st.selectbox("🪑 Seating Capacity", [2, 4, 5, 6, 7, 8, 9, 10])
ownership = st.selectbox("🆕 Ownership Type", list(ownership_mapping.keys()))
transmission = st.selectbox("🔀 Transmission Type", list(transmission_mapping.keys()))
color = st.selectbox("🎨 Color", list(color_mapping.keys()))

# Convert categorical values using mappings
input_data = pd.DataFrame(
    [[city_mapping[city], body_type_mapping[body_type], kms_driven, 
      oem_mapping[oem], model_mapping[model_name], model_year, 
      variant_mapping[variant_name], insurance_mapping[insurance_validity], 
      fuel_mapping[fuel_type], seating_capacity, ownership_mapping[ownership], 
      transmission_mapping[transmission], color_mapping[color]]],
    columns=[
        'city', 'body_type', 'Kms_Driven', 'oem', 'model', 'modelYear',
        'variantName', 'Insurance Validity', 'Fuel Type', 'Seating_Capacity',
        'Ownership', 'Transmission', 'Color'
    ]
)

# Predict and format price in Lakhs
if st.button("🔮 Predict Price"):
    try:
        prediction = model.predict(input_data)
        predicted_price = int(prediction[0])  # Convert to integer
        
        # Convert to Lakhs format (₹ X.XX Lakhs)
        price_in_lakhs = predicted_price / 100000
        formatted_price = f"₹{price_in_lakhs:,.2f} Lakhs"
        
        st.success(f"💰Estimated Price: {formatted_price}")
    except Exception as e:
        st.error(f"❌ Error in Prediction: {e}")


st.write("This is a demo app. The predictions depend on the model's training data.")
