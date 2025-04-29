import streamlit as st
import joblib

# Load the model and encoders
model = joblib.load('fertilizer_recommendation_model.pkl')
le_soil = joblib.load('le_soil.pkl')
le_crop = joblib.load('le_crop.pkl')

# Get class names
soil_colors = list(le_soil.classes_)
crop_names = list(le_crop.classes_)

# App title
st.title("🌾 Fertilizer Recommendation System")
st.write("Provide soil and crop details to get the best fertilizer recommendation for higher yield.")

# Input form
with st.form("fertilizer_form"):
    soil_color = st.radio("Select Soil Color", soil_colors)
    nitrogen = st.number_input("Nitrogen (ppm)", min_value=0)
    phosphorus = st.number_input("Phosphorus (ppm)", min_value=0)
    potassium = st.number_input("Potassium (ppm)", min_value=0)
    ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0)
    temperature = st.number_input("Temperature (°C)", min_value=-10.0)
    crop = st.radio("Select Crop", crop_names)

    submitted = st.form_submit_button("Get Fertilizer Recommendation")

    if submitted:
        # Encode categorical inputs
        soil_encoded = le_soil.transform([soil_color])[0]
        crop_encoded = le_crop.transform([crop])[0]

        # Prepare input data
        input_data = [[soil_encoded, nitrogen, phosphorus, potassium, ph, rainfall, temperature, crop_encoded]]

        # Make prediction
        prediction = model.predict(input_data)
        recommended_fertilizer = prediction[0]

        st.success(f"✅ Recommended Fertilizer: **{recommended_fertilizer}**")

        # 🎯 Fertilizer Tips Section
        st.markdown("---")
        st.subheader("🌟 Fertilizer Usage Tips")

        tips = {
            "Urea": "✔️ Urea is rich in nitrogen. Use it for leafy crops. Avoid overuse to prevent soil acidity.",
            "DAP": "✔️ DAP provides nitrogen and phosphorus. Best during early plant growth stages.",
            "MOP": "✔️ MOP supplies potassium. Ideal for fruiting and flowering crops.",
            "NPK 20:20:20": "✔️ Balanced fertilizer. Perfect for vegetables and cereals.",
            "Compost": "✔️ Organic fertilizer improving soil structure and microbial activity."
        }

        images = {
            "Urea": "images/urea.jpg",
            "DAP": "images/dap.jpg",
            "MOP": "images/mop.jpg",
            "NPK 20:20:20": "images/npk.jpg",
            "Compost": "images/compost.jpg",
        }

        # Display fertilizer tip + image
        if recommended_fertilizer in tips:
            col1, col2 = st.columns([1,3])

            with col1:
                st.image(images[recommended_fertilizer], width=120)

            with col2:
                st.info(tips[recommended_fertilizer])

        else:
            st.info("✅ Apply fertilizer as per recommended dose and monitor soil health regularly.")

