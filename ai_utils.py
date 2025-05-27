import openai
from PIL import Image
import io
import base64
import os
from config import OPENAI_API_KEY, CONFIDENCE_THRESHOLD

# Initialize OpenAI client with error handling
try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    client = None

def analyze_rooftop_image(image_data):
    """
    Analyze a rooftop image using OpenAI's Vision API.
    
    Args:
        image_data: Image data in bytes or base64 format
        
    Returns:
        dict: Analysis results including roof area, orientation, shading, etc.
    """
    if client is None:
        return {
            'error': 'OpenAI client not initialized. Please check your API key.',
            'confidence_score': 0,
            'is_suitable': False
        }

    try:
        # Convert image to base64 if it's not already
        if isinstance(image_data, bytes):
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        else:
            image_base64 = image_data

        # Prepare the prompt for detailed roof analysis
        prompt = (
            "You are a solar rooftop analysis expert. "
            "Analyze the provided aerial image. "
            "For each rooftop you see, provide: "
            "1. Estimated area in square meters, "
            "2. Orientation (degrees from north), "
            "3. Presence of shading or obstacles (describe), "
            "4. Roof type (flat, pitched, etc.), "
            "5. Available space for solar panels, "
            "6. Any other relevant notes. "
            "Base your answer only on the image content. "
            "Do not provide generic advice."
        )

        # Call OpenAI Vision API with error handling
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert solar rooftop image analysis assistant. Analyze images and provide structured, accurate, and clear information for solar installation assessment."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            # Process and structure the response
            analysis = response.choices[0].message.content
            
            # Extract structured data from the analysis
            structured_analysis = {
                'raw_analysis': analysis,
                'confidence_score': 0.9,  # This would be calculated based on the response
                'is_suitable': True  # This would be determined based on the analysis
            }

            return structured_analysis

        except openai.APIError as e:
            return {
                'error': f'OpenAI API Error: {str(e)}',
                'confidence_score': 0,
                'is_suitable': False
            }
        except Exception as e:
            return {
                'error': f'Unexpected error during API call: {str(e)}',
                'confidence_score': 0,
                'is_suitable': False
            }

    except Exception as e:
        return {
            'error': f'Error processing image: {str(e)}',
            'confidence_score': 0,
            'is_suitable': False
        }

def validate_analysis(analysis):
    """
    Validate the analysis results and ensure they meet confidence thresholds.
    
    Args:
        analysis: Dictionary containing analysis results
        
    Returns:
        bool: Whether the analysis is valid
    """
    if 'error' in analysis:
        print(f"Analysis validation failed: {analysis['error']}")
        return False
    
    return analysis['confidence_score'] >= CONFIDENCE_THRESHOLD

def get_solar_recommendations(analysis):
    """
    Generate solar installation recommendations based on the analysis.
    
    Args:
        analysis: Dictionary containing roof analysis results
        
    Returns:
        dict: Installation recommendations
    """
    try:
        # Parse the raw analysis to extract key information
        raw_analysis = analysis.get('raw_analysis', '')
        
        # Default recommendations
        recommendations = {
            'panel_type': 'standard',
            'estimated_panels': 0,
            'estimated_output': 0,
            'installation_complexity': 'medium',
            'special_considerations': []
        }
        
        # Add special considerations based on analysis
        if 'shading' in raw_analysis.lower():
            recommendations['special_considerations'].append('Potential shading issues')
        if 'obstacles' in raw_analysis.lower():
            recommendations['special_considerations'].append('Roof obstacles present')
        if 'flat' in raw_analysis.lower():
            recommendations['installation_complexity'] = 'low'
        elif 'pitched' in raw_analysis.lower():
            recommendations['installation_complexity'] = 'medium'
        
        return recommendations
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return {
            'panel_type': 'standard',
            'estimated_panels': 0,
            'estimated_output': 0,
            'installation_complexity': 'unknown',
            'special_considerations': ['Error in analysis processing']
        } 