import streamlit as st
import os
from PIL import Image
import io
from ai_utils import analyze_rooftop_image, validate_analysis, get_solar_recommendations
from config import OPENAI_API_KEY
from rooftop_segmentation import segment_rooftops, draw_rooftop_outlines, mask_area, get_outlined_image_bytes

# Set page config
st.set_page_config(
    page_title="Solar Rooftop Analysis",
    page_icon="☀️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .error-message {
        color: #ff4b4b;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #ffebee;
    }
    .success-message {
        color: #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e8f5e9;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("☀️ Solar Rooftop Analysis")
    st.markdown("""
    Upload a rooftop image to analyze its solar potential. Our AI will assess:
    - Roof area and orientation
    - Shading and obstacles
    - Installation feasibility
    - Estimated solar potential
    """)

    # Check for API key
    if not OPENAI_API_KEY:
        st.error("""
        ⚠️ OpenAI API key not found. Please add your API key to the .env file:
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
        """)
        return

    # File uploader
    uploaded_file = st.file_uploader("Upload a rooftop image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Rooftop Image", use_column_width=True)

            # --- Rooftop Segmentation ---
            mask = segment_rooftops(image)
            outlined_img_buf = get_outlined_image_bytes(image, mask)
            st.image(outlined_img_buf, caption="Detected Rooftop Outlines", use_column_width=True)

            # Calculate rooftop area from mask
            rooftop_area = mask_area(mask)
            st.info(f"Estimated Rooftop Area: {rooftop_area:.2f} m² (demo)")

            # Convert image to bytes for AI analysis
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format)
            img_byte_arr = img_byte_arr.getvalue()

            # Analysis button
            if st.button("Analyze Rooftop"):
                with st.spinner("Analyzing rooftop image and segmentation results..."):
                    # Pass area and image to AI analysis
                    analysis = analyze_rooftop_image(img_byte_arr)
                    analysis['estimated_area'] = rooftop_area

                    if 'error' in analysis:
                        st.error(f"Analysis failed: {analysis['error']}")
                        return

                    # Validate the analysis
                    if not validate_analysis(analysis):
                        st.error("Analysis confidence is too low. Please try with a clearer image.")
                        return

                    # Get recommendations
                    recommendations = get_solar_recommendations(analysis)

                    # Display results
                    st.success("Analysis complete! Here are the results:")

                    # Create columns for results
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Analysis Results")
                        st.markdown(analysis['raw_analysis'])
                        st.markdown(f"**Estimated Rooftop Area:** {rooftop_area:.2f} m² (from segmentation)")

                    with col2:
                        st.subheader("Installation Recommendations")
                        st.markdown(f"""
                        - **Panel Type**: {recommendations['panel_type']}
                        - **Installation Complexity**: {recommendations['installation_complexity']}
                        - **Special Considerations**:
                        """)
                        for consideration in recommendations['special_considerations']:
                            st.markdown(f"- {consideration}")

                    # Additional information
                    st.info("""
                    💡 **Next Steps**:
                    1. Contact a solar installer for a detailed assessment
                    2. Get quotes from multiple providers
                    3. Check local regulations and incentives
                    """)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try uploading a different image or contact support if the issue persists.")

if __name__ == "__main__":
    main() 