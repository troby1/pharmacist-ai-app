import streamlit as st
import openai
import os

# Set your OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App Title
st.set_page_config(page_title="ASK A PHARMACIST", layout="centered")
st.title("💊 ASK A PHARMACIST")
st.markdown("This tool helps pharmacists review patient information and receive AI-supported treatment suggestions.")

# Input: Patient Info
st.subheader("Patient Information")

# Age and Sex
age = st.number_input("Patient Age", min_value=0, max_value=120)
sex = st.selectbox("Sex", ["Male", "Female", "Other"])

# Height in feet and inches
height_ft = st.number_input("Height (feet)", min_value=1, max_value=8)
height_in = st.number_input("Additional Inches", min_value=0, max_value=11)
total_height_cm = round((height_ft * 12 + height_in) * 2.54, 2)

# Weight in lbs
weight_lbs = st.number_input("Weight (lbs)", min_value=1, max_value=700)
weight_kg = round(weight_lbs * 0.453592, 2)

# Allergies
st.subheader("Allergy Information")
common_allergies = ["Penicillin", "Sulfa drugs", "Aspirin", "Ibuprofen", "Latex"]
selected_allergies = st.multiselect("Select Known Allergies", common_allergies)
custom_allergies = st.text_input("Other Allergies (comma-separated)")
allergy_list = selected_allergies + [a.strip() for a in custom_allergies.split(",") if a.strip() != ""]

# Ailment
ailment_description = st.text_area("Describe the patient's condition or symptoms")

# Submit Button
if st.button("Generate Recommendation"):
    if not ailment_description.strip():
        st.warning("Please describe the ailment.")
    else:
        with st.spinner("🧪 Collecting data 🟡🔵🟢 Analyzing 🧠 Generating insights..."):
            # Construct prompt
            prompt = f"""
You are a highly experienced pharmacist AI assistant. A patient presents with the following:
- Age: {age} years
- Sex: {sex}
- Height: {total_height_cm} cm
- Weight: {weight_kg} kg
- Allergies: {', '.join(allergy_list) if allergy_list else 'None'}
- Ailment: {ailment_description}

Please:
1. Suggest a list of possible medications or treatments.
2. Check for any allergy conflicts.
3. Summarize your recommendations as if writing for a licensed pharmacist.
4. Mention drug classes and typical dosages.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=1000
                )
                result = response.choices[0].message.content
                st.success("✅ Recommendation Ready")
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
