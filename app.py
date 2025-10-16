"""
Desert Kite Detection Web App
Powered by EyePop.ai

A modern Streamlit interface for detecting ancient desert kites from satellite imagery.
"""

import streamlit as st
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
from eyepop import EyePopSdk
from eyepop.worker.worker_types import Pop, InferenceComponent
from PIL import Image, ImageDraw, ImageFont
import json
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Desert Kite Detection | EyePop.ai",
    page_icon="🪁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'eyepop_api_key' not in st.session_state:
    st.session_state.eyepop_api_key = None

# EyePop.ai Cyan Blue Branding
EYEPOP_CYAN = "#00D9FF"
EYEPOP_DARK = "#0A1929"
EYEPOP_LIGHT = "#E7F9FF"

# Custom CSS for modern design
st.markdown(f"""
<style>
    /* Main theme colors */
    :root {{
        --eyepop-cyan: {EYEPOP_CYAN};
        --eyepop-dark: {EYEPOP_DARK};
        --eyepop-light: {EYEPOP_LIGHT};
    }}
    
    /* Hide default Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Page background */
    .main {{
        background-color: #fafbfc;
    }}
    
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Custom header */
    .main-header {{
        background: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 2px solid {EYEPOP_CYAN};
    }}
    
    .main-title {{
        color: #000000;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
        letter-spacing: 2px;
    }}
    
    .sub-title {{
        color: {EYEPOP_CYAN};
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
        opacity: 1;
        font-weight: 500;
    }}
    
    /* Cards */
    .info-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {EYEPOP_CYAN};
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    .result-card {{
        background: {EYEPOP_LIGHT};
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid {EYEPOP_CYAN};
        margin: 1rem 0;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {EYEPOP_CYAN} 0%, #00b8d4 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.625rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 217, 255, 0.2);
        letter-spacing: 0.025em;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 217, 255, 0.25);
        background: linear-gradient(135deg, #00b8d4 0%, {EYEPOP_CYAN} 100%);
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 1px 2px rgba(0, 217, 255, 0.2);
    }}
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {{
        background: white;
        color: #64748b;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: #f8fafc;
        border-color: #cbd5e1;
        color: #475569;
    }}
    
    /* Input fields */
    .stTextInput > div > div > input {{
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        background: white;
    }}
    
    .stTextInput > div > div > input:focus {{
        border: 1px solid {EYEPOP_CYAN} !important;
        box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #94a3b8;
    }}
    
    /* Remove any container borders around inputs */
    .stTextInput > div {{
        border: none !important;
    }}
    
    .stTextInput {{
        border: none !important;
    }}
    
    /* Hide the "Press Enter to apply" message */
    .stTextInput [data-testid="InputInstructions"] {{
        display: none !important;
    }}
    
    /* Alternative: If the above doesn't work, hide by class */
    .stTextInput small {{
        display: none !important;
    }}
    
    /* Stats */
    .stat-box {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border-top: 4px solid {EYEPOP_CYAN};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {EYEPOP_CYAN};
        margin: 0;
    }}
    
    .stat-label {{
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: #f8fafc;
    }}
    
    /* Sidebar text styling */
    section[data-testid="stSidebar"] {{
        background-color: #f8fafc;
    }}
    
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #1e293b !important;
    }}
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li {{
        color: #64748b !important;
    }}
    
    /* Radio buttons */
    .stRadio > label {{
        font-weight: 500;
        color: #1e293b;
    }}
    
    /* Sliders */
    .stSlider > div > div > div > div {{
        background-color: {EYEPOP_CYAN};
    }}
    
    /* Success/Error messages */
    .success-msg {{
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }}
    
    .error-msg {{
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }}
    
    /* Loading animation */
    .loader {{
        border: 4px solid {EYEPOP_LIGHT};
        border-top: 4px solid {EYEPOP_CYAN};
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
</style>
""", unsafe_allow_html=True)


def validate_eyepop_token(api_key):
    """
    Validate EyePop API token by attempting to create a worker endpoint
    Returns (success: bool, error_message: str or None)
    """
    try:
        # Try to create a worker endpoint with the provided key
        with EyePopSdk.workerEndpoint(secret_key=api_key) as endpoint:
            # If we get here without exception, the token is valid
            return True, None
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg or "authentication" in error_msg.lower():
            return False, "Invalid API token. Please check your EyePop API key."
        elif "403" in error_msg or "Forbidden" in error_msg:
            return False, "Access forbidden. Please check your API key permissions."
        else:
            return False, f"Error validating token: {error_msg}"


def parse_dms_coordinate(coord_str):
    """
    Parse DMS (Degrees Minutes Seconds) coordinate string to decimal
    
    Supports formats like:
    - 31°29'00.5"N
    - 31°29'0.5"N
    - 31 29 00.5 N
    """
    coord_str = coord_str.strip().upper()
    
    # Pattern: degrees° minutes' seconds" direction
    pattern = r"(\d+)[°\s]+(\d+)['\s]+([0-9.]+)[\"'\s]*([NSEW])"
    match = re.match(pattern, coord_str)
    
    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        direction = match.group(4)
        
        # Convert to decimal
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        # Apply sign based on direction
        if direction in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    else:
        raise ValueError(f"Could not parse coordinate: {coord_str}")


def convert_coordinates(lat_input, lon_input):
    """
    Convert coordinate inputs to decimal degrees
    Handles both DMS and decimal formats
    """
    try:
        # Try parsing as decimal first
        lat = float(lat_input)
        lon = float(lon_input)
    except ValueError:
        # Try parsing as DMS
        try:
            lat = parse_dms_coordinate(lat_input)
            lon = parse_dms_coordinate(lon_input)
        except:
            raise ValueError("Invalid coordinate format. Use decimal (e.g., 31.483472) or DMS (e.g., 31°29'00.5\"N)")
    
    # Validate ranges
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    
    return lat, lon


def download_satellite_image(lat, lon, api_key, zoom=17, size="640x640"):
    """Download satellite image from Google Maps"""
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=satellite&key={api_key}"
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Save to temporary file
    os.makedirs('./temp_streamlit', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"./temp_streamlit/satellite_{lat}_{lon}_{timestamp}.png"
    
    with open(image_path, 'wb') as f:
        f.write(response.content)
    
    return image_path

#old 06866d5655967d118000c4c4fca5bd36
def detect_kites(image_path, eyepop_api_key, model_uuid='068e442ce4a4715780004ef18b98aa92'):
    """Run kite detection using EyePop AI"""
    with EyePopSdk.workerEndpoint(secret_key=eyepop_api_key) as endpoint:
        endpoint.set_pop(Pop(
            components=[
                InferenceComponent(
                    modelUuid=model_uuid
                )
            ]
        ))
        
        result = endpoint.upload(image_path).predict()
        return result


def annotate_image(image_path, detections):
    """Draw bounding boxes on detected kites"""
    desert_kites = [obj for obj in detections.get('objects', []) 
                    if obj.get('classLabel') == 'desert kite']
    
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Try to load a nice font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
    
    # Draw bounding boxes
    for i, detection in enumerate(desert_kites):
        x = detection.get('x', 0)
        y = detection.get('y', 0)
        width = detection.get('width', 0)
        height = detection.get('height', 0)
        confidence = detection.get('confidence', 0)
        
        # Draw rectangle (EyePop cyan!)
        draw.rectangle([x, y, x + width, y + height], outline='#00D9FF', width=4)
        
        # Draw label
        label = f"Kite {confidence:.0%}"
        text_bbox = draw.textbbox((x, y), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Background for text
        draw.rectangle([x, y - text_height - 8, x + text_width + 8, y], fill='#00D9FF')
        draw.text((x + 4, y - text_height - 4), label, fill='white', font=font)
    
    return image, desert_kites


def redraw_image_with_threshold(image_path, kites, confidence_threshold):
    """Redraw image with only kites above confidence threshold"""
    # Filter kites by threshold
    filtered_kites = [k for k in kites if k.get('confidence', 0) >= confidence_threshold]
    
    # Open fresh image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Try to load a nice font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
    
    # Draw only filtered bounding boxes
    for detection in filtered_kites:
        x = detection.get('x', 0)
        y = detection.get('y', 0)
        width = detection.get('width', 0)
        height = detection.get('height', 0)
        confidence = detection.get('confidence', 0)
        
        # Draw rectangle (EyePop cyan!)
        draw.rectangle([x, y, x + width, y + height], outline='#00D9FF', width=4)
        
        # Draw label
        label = f"Kite {confidence:.0%}"
        text_bbox = draw.textbbox((x, y), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Background for text
        draw.rectangle([x, y - text_height - 8, x + text_width + 8, y], fill='#00D9FF')
        draw.text((x + 4, y - text_height - 4), label, fill='white', font=font)
    
    return image


def show_auth_screen():
    """Display modern, minimalist authentication screen"""
    
    # Add extra spacing at top for vertical centering effect
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    
    # Center the auth form with more focused layout
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        # Modern minimalist logo/title section
        st.markdown("""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🪁</div>
            <h1 style='color: #000000; font-size: 2.5rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;'>
                Desert Kite Detection
            </h1>
            <p style='color: #64748b; font-size: 1rem; margin-top: 0.5rem; font-weight: 400;'>
                Powered by EyePop.ai
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Label above input
        st.markdown("""
        <p style='color: #64748b; font-size: 0.9rem; margin: 0 0 0.5rem 0;'>
            Enter your API token
        </p>
        """, unsafe_allow_html=True)
        
        # API Token input with clean styling
        api_token = st.text_input(
            "API Token",
            type="password",
            placeholder="xxxxxxxxxxxxxxxx",
            help="Find your token at eyepop.ai/dashboard",
            label_visibility="collapsed"
        )
        
        # Spacer
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Login button - full width, no columns
        login_button = st.button("Continue", use_container_width=True, type="primary")
        
        if login_button:
            if not api_token:
                st.markdown("""
                <div style='background: #fef2f2; color: #991b1b; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.9rem; margin-top: 1rem; border-left: 3px solid #dc2626;'>
                    Please enter your API token
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("Validating..."):
                    is_valid, error_msg = validate_eyepop_token(api_token)
                    
                    if is_valid:
                        st.session_state.authenticated = True
                        st.session_state.eyepop_api_key = api_token
                        st.markdown("""
                        <div style='background: #f0fdf4; color: #166534; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.9rem; margin-top: 1rem; border-left: 3px solid #22c55e;'>
                            ✓ Authentication successful
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown(f"""
                        <div style='background: #fef2f2; color: #991b1b; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.9rem; margin-top: 1rem; border-left: 3px solid #dc2626;'>
                            {error_msg}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Help section with minimalist design
        st.markdown("""
        <div style='margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid #e2e8f0;'>
            <p style='color: #64748b; font-size: 0.9rem; text-align: center; margin: 0 0 1rem 0;'>
                Don't have an API token?
            </p>
            <div style='text-align: center;'>
                <a href='https://eyepop.ai' target='_blank' style='color: #00D9FF; text-decoration: none; font-weight: 500; font-size: 0.95rem;'>
                    Get started at eyepop.ai →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_main_app():
    """Display the main Desert Kite Detection application with modern header"""
    # Top bar with logo and logout
    col_left, col_right = st.columns([6, 1])
    
    with col_left:
        st.markdown("""
        <div style='padding: 0.5rem 0;'>
            <div style='display: flex; align-items: center; gap: 0.75rem;'>
                <span style='font-size: 2rem;'>🪁</span>
                <div>
                    <h1 style='color: #1e293b; font-size: 1.5rem; font-weight: 600; margin: 0; letter-spacing: -0.3px;'>
                        Desert Kite Detection
                    </h1>
                    <p style='color: #64748b; font-size: 0.85rem; margin: 0;'>
                        Powered by EyePop.ai
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("<div style='padding-top: 0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.eyepop_api_key = None
            st.rerun()
    
    # Subtle divider
    st.markdown("""
    <div style='border-top: 1px solid #e2e8f0; margin: 1rem 0 2rem 0;'></div>
    """, unsafe_allow_html=True)


# Main app routing based on authentication status
if not st.session_state.authenticated:
    show_auth_screen()
    st.stop()

# Show main app if authenticated
show_main_app()

# Original sidebar and main content continues here

# Sidebar
with st.sidebar:
    # Modern authentication badge
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); color: #166534; padding: 0.875rem; border-radius: 10px; margin-bottom: 1.5rem; text-align: center; border: 1px solid #bbf7d0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);'>
        <div style='font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px;'>✓ AUTHENTICATED</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #1e293b; font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;'>Settings</h2>", unsafe_allow_html=True)
    
    zoom_level = st.slider(
        "Zoom Level",
        min_value=14,
        max_value=20,
        value=17,
        help="Higher zoom = more detail, lower zoom = wider area"
    )
    
    st.markdown("---")
    
    confidence_threshold_pct = st.slider(
        "Confidence Threshold (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        help="Filter detections below this confidence level"
    )
    
    # Convert percentage to decimal for internal use
    confidence_threshold = confidence_threshold_pct / 100.0
    
    st.info(f"💡 Only showing detections with ≥ {confidence_threshold_pct}% confidence")
    
    st.markdown("""
    <div style='border-top: 1px solid #e2e8f0; margin: 1.5rem 0;'></div>
    """, unsafe_allow_html=True)
    
    st.markdown("### About")
    
    st.markdown("Detect ancient desert kites (prehistoric stone structures) from satellite imagery using AI.")
    
    st.markdown("**Quick Guide:**")
    st.markdown("""
    1. Enter coordinates
    2. Add to queue
    3. Process all locations
    4. View results
    """)
    
    st.markdown("**Coordinate formats:**")
    st.code("""Decimal: 31.483472, 38.368028
DMS: 31°29'00.5"N 38°22'04.9"E""", language=None)
    
    st.markdown("""
    <div style='border-top: 1px solid #e2e8f0; margin: 1.5rem 0;'></div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 0.5rem 0;'>
        <span style='color: {EYEPOP_CYAN}; font-weight: 600;'>EyePop.ai</span>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state for multiple coordinates
if 'coordinate_queue' not in st.session_state:
    st.session_state.coordinate_queue = []
if 'all_detections' not in st.session_state:
    st.session_state.all_detections = []

# Main content
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <h2 style='color: #1e293b; font-size: 1.25rem; font-weight: 600; margin: 0; letter-spacing: -0.3px;'>
        Add Locations
    </h2>
    <p style='color: #64748b; font-size: 0.9rem; margin: 0.25rem 0 0 0;'>
        Enter coordinates to detect ancient desert kites
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    # Coordinate input type selector
    coord_format = st.radio(
        "Format",
        ["Decimal Degrees", "DMS (Degrees Minutes Seconds)"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
    
    if coord_format == "Decimal Degrees":
        st.markdown("<p style='color: #64748b; font-size: 0.85rem; margin: 0 0 0.75rem 0;'>Example: 31.483472, 38.368028</p>", unsafe_allow_html=True)
        lat_input = st.text_input("Latitude", placeholder="31.483472", key="lat_input_field", label_visibility="collapsed")
        lon_input = st.text_input("Longitude", placeholder="38.368028", key="lon_input_field", label_visibility="collapsed")
    else:
        st.markdown("<p style='color: #64748b; font-size: 0.85rem; margin: 0 0 0.75rem 0;'>Example: 31°29'00.5\"N, 38°22'04.9\"E</p>", unsafe_allow_html=True)
        lat_input = st.text_input("Latitude (DMS)", placeholder="31°29'00.5\"N", key="lat_input_field", label_visibility="collapsed")
        lon_input = st.text_input("Longitude (DMS)", placeholder="38°22'04.9\"E", key="lon_input_field", label_visibility="collapsed")
    
    # Add and Clear buttons below text inputs
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    add_col, clear_col = st.columns(2)
    with add_col:
        if st.button("Add to Queue", use_container_width=True, type="primary", key="add_queue"):
            if lat_input and lon_input:
                st.session_state.coordinate_queue.append((lat_input, lon_input))
                st.success("Added to queue")
                st.rerun()
            else:
                st.error("Enter both coordinates")
    
    with clear_col:
        if st.button("Clear Queue", use_container_width=True, key="clear_queue"):
            st.session_state.coordinate_queue = []
            st.session_state.all_detections = []
            st.rerun()
    
    # Quick examples with cleaner styling
    st.markdown("""
    <div style='margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0;'>
        <p style='color: #64748b; font-size: 0.85rem; margin: 0 0 0.75rem 0; font-weight: 500;'>
            Quick Examples
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("Location 1", use_container_width=True, key="ex1"):
            st.session_state.coordinate_queue.append(("25.742162", "39.292586"))
            st.rerun()
    
    with example_col2:
        if st.button("Location 2", use_container_width=True, key="ex2"):
            st.session_state.coordinate_queue.append(("25.867377", "39.240912"))
            st.rerun()
    
    with example_col3:
        if st.button("Location 3", use_container_width=True, key="ex3"):
            st.session_state.coordinate_queue.append(("31.483472", "38.368028"))
            st.rerun()

with col2:
    # Clean queue header
    st.markdown("""
    <h3 style='color: #1e293b; font-size: 1rem; font-weight: 600; margin: 0 0 1rem 0; letter-spacing: -0.2px;'>
        Queue
    </h3>
    """, unsafe_allow_html=True)
    
    # Display queue
    if st.session_state.coordinate_queue:
        st.markdown(f"""
        <p style='color: #64748b; font-size: 0.85rem; margin: 0 0 0.75rem 0;'>
            {len(st.session_state.coordinate_queue)} location(s) queued
        </p>
        """, unsafe_allow_html=True)
        
        for i, (lat, lon) in enumerate(st.session_state.coordinate_queue, 1):
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 0.5rem; border: 1px solid #e2e8f0;'>
                    <p style='color: #64748b; font-size: 0.75rem; margin: 0; font-family: monospace;'>
                        {i}. {lat}, {lon}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button("×", key=f"remove_{i}"):
                    st.session_state.coordinate_queue.pop(i-1)
                    st.rerun()
    else:
        st.markdown("""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center;'>
            <p style='color: #94a3b8; font-size: 0.85rem; margin: 0;'>
                Queue is empty
            </p>
        </div>
        """, unsafe_allow_html=True)

# Process all button with modern styling
st.markdown("""
<div style='border-top: 1px solid #e2e8f0; margin: 2rem 0 1.5rem 0;'></div>
""", unsafe_allow_html=True)

# Center the process button
col_spacer1, col_button, col_spacer2 = st.columns([1, 2, 1])
with col_button:
    detect_button = st.button(
        "Process All Locations", 
        use_container_width=True, 
        type="primary", 
        disabled=len(st.session_state.coordinate_queue) == 0,
        key="process_btn"
    )

if detect_button:
    # Clear previous results
    st.session_state.all_detections = []
    
    # Get API keys
    google_api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyBSb4596aMqgsOzKkjdH2fncNmxyG-52KE')
    eyepop_api_key = st.session_state.eyepop_api_key
    
    if not eyepop_api_key:
        st.error("❌ Authentication error. Please logout and login again.")
        st.stop()
    
    # Process each coordinate
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(st.session_state.coordinate_queue)
    
    for idx, (lat_str, lon_str) in enumerate(st.session_state.coordinate_queue):
        try:
            status_text.write(f"🔄 Processing location {idx + 1} of {total}...")
            
            # Convert coordinates
            lat, lon = convert_coordinates(lat_str, lon_str)
            
            # Download image
            image_path = download_satellite_image(lat, lon, google_api_key, zoom=zoom_level)
            
            # Run detection
            detections = detect_kites(image_path, eyepop_api_key)
            
            # Annotate image
            annotated_img, desert_kites = annotate_image(image_path, detections)
            
            # Store result with original image path for re-drawing
            st.session_state.all_detections.append({
                'image': annotated_img,
                'image_path': image_path,  # Store path for dynamic re-drawing
                'kites': desert_kites,
                'lat': lat,
                'lon': lon,
                'zoom': zoom_level,
                'original_input': (lat_str, lon_str)
            })
            
            # Update progress
            progress_bar.progress((idx + 1) / total)
            
        except Exception as e:
            st.error(f"❌ Error processing {lat_str}, {lon_str}: {str(e)}")
            # Continue with next coordinate
            continue
    
    status_text.write(f"✅ Completed processing {len(st.session_state.all_detections)} of {total} locations!")
    time.sleep(1)
    st.rerun()

# Results section - Display all detections
if st.session_state.all_detections:
    st.markdown("""
    <div style='border-top: 1px solid #e2e8f0; margin: 3rem 0 2rem 0;'></div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 1.5rem; font-weight: 600; margin: 0; letter-spacing: -0.3px;'>
            Results
        </h2>
        <p style='color: #64748b; font-size: 0.9rem; margin: 0.25rem 0 0 0;'>
            Detection analysis for all locations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary stats (with confidence filtering)
    total_locations = len(st.session_state.all_detections)
    
    # Filter kites by confidence threshold
    filtered_detections = []
    for d in st.session_state.all_detections:
        filtered_kites = [k for k in d['kites'] if k.get('confidence', 0) >= confidence_threshold]
        filtered_detections.append({**d, 'filtered_kites': filtered_kites})
    
    total_kites_filtered = sum(len(d['filtered_kites']) for d in filtered_detections)
    locations_with_kites = sum(1 for d in filtered_detections if len(d['filtered_kites']) > 0)
    
    sum_col1, sum_col2, sum_col3 = st.columns(3)
    with sum_col1:
        st.markdown(f"""
        <div style='background: white; padding: 1.75rem; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);'>
            <p style='font-size: 2.5rem; font-weight: 700; color: #00D9FF; margin: 0; letter-spacing: -1px;'>{total_locations}</p>
            <p style='font-size: 0.875rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin: 0.5rem 0 0 0; font-weight: 500;'>Locations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_col2:
        st.markdown(f"""
        <div style='background: white; padding: 1.75rem; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);'>
            <p style='font-size: 2.5rem; font-weight: 700; color: #00D9FF; margin: 0; letter-spacing: -1px;'>{total_kites_filtered}</p>
            <p style='font-size: 0.875rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin: 0.5rem 0 0 0; font-weight: 500;'>Kites Found</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sum_col3:
        st.markdown(f"""
        <div style='background: white; padding: 1.75rem; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);'>
            <p style='font-size: 2.5rem; font-weight: 700; color: #00D9FF; margin: 0; letter-spacing: -1px;'>{locations_with_kites}</p>
            <p style='font-size: 0.875rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin: 0.5rem 0 0 0; font-weight: 500;'>With Detections</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display each location's results
    for idx, filtered_result in enumerate(filtered_detections, 1):
        result = st.session_state.all_detections[idx - 1]
        st.markdown(f"""
        <div style='background: white; padding: 1rem 1.5rem; border-radius: 10px; margin: 1.5rem 0 1rem 0; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);'>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.25rem;'>📍</span>
                <div>
                    <h3 style='color: #1e293b; font-size: 1rem; font-weight: 600; margin: 0; letter-spacing: -0.2px;'>
                        Location {idx}
                    </h3>
                    <p style='color: #64748b; font-size: 0.8rem; margin: 0; font-family: monospace;'>
                        {result['lat']:.6f}, {result['lon']:.6f}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use filtered kites
        filtered_kites = filtered_result['filtered_kites']
        all_kites = result['kites']
        
        # Location stats
        loc_col1, loc_col2, loc_col3, loc_col4 = st.columns(4)
        
        with loc_col1:
            st.metric("Total Detections", len(all_kites))
        
        with loc_col2:
            st.metric("Passing Filter", len(filtered_kites), 
                     delta=f"{len(filtered_kites) - len(all_kites)}" if len(filtered_kites) != len(all_kites) else None)
        
        with loc_col3:
            avg_conf = sum(k.get('confidence', 0) for k in filtered_kites) / len(filtered_kites) if filtered_kites else 0
            st.metric("Avg Confidence", f"{avg_conf:.0%}")
        
        with loc_col4:
            st.metric("Zoom Level", result['zoom'])
        
        # Annotated image and details
        img_col1, img_col2 = st.columns([2, 1])
        
        with img_col1:
            # Redraw image with only filtered bounding boxes
            if 'image_path' in result:
                filtered_image = redraw_image_with_threshold(
                    result['image_path'], 
                    all_kites, 
                    confidence_threshold
                )
                st.image(filtered_image, caption=f"Location {idx} - Detections (≥{confidence_threshold_pct}%)", use_container_width=True)
            else:
                # Fallback to original image if path not available
                st.image(result['image'], caption=f"Location {idx} - All Detections", use_container_width=True)
        
        with img_col2:
            if filtered_kites:
                st.markdown(f"**🪁 {len(filtered_kites)} Kite(s) (≥{confidence_threshold_pct}%):**")
                
                # Show filtered out count if any
                filtered_out = len(all_kites) - len(filtered_kites)
                if filtered_out > 0:
                    st.caption(f"🔽 {filtered_out} detection(s) below threshold (hidden)")
                
                for i, kite in enumerate(filtered_kites, 1):
                    confidence = kite.get('confidence', 0)
                    x = kite.get('x', 0)
                    y = kite.get('y', 0)
                    width = kite.get('width', 0)
                    height = kite.get('height', 0)
                    
                    # Color code the confidence
                    if confidence >= 0.85:
                        conf_color = "🟢"
                    elif confidence >= 0.70:
                        conf_color = "🟡"
                    else:
                        conf_color = "🟠"
                    
                    with st.expander(f"{conf_color} Kite #{i} - {confidence:.1%}"):
                        st.markdown(f"""
                        **Confidence:** {confidence:.2%}  
                        **Position:** ({x:.0f}, {y:.0f})  
                        **Size:** {width:.0f} × {height:.0f} px
                        """)
                
                # Download button for this location
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"./results/detection_loc{idx}_{timestamp}.png"
                os.makedirs('./results', exist_ok=True)
                result['image'].save(output_path)
                
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label=f"💾 Download Location {idx}",
                        data=f,
                        file_name=f"kite_detection_{result['lat']}_{result['lon']}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_{idx}"
                    )
            else:
                if len(all_kites) > 0:
                    st.warning(f"⚠️ {len(all_kites)} detection(s) below {confidence_threshold_pct}% threshold")
                else:
                    st.info("No kites detected at this location.")
        
        # Clean separator between locations
        if idx < len(st.session_state.all_detections):
            st.markdown("""
            <div style='border-top: 1px solid #e2e8f0; margin: 2rem 0;'></div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='border-top: 1px solid #e2e8f0; margin-top: 3rem; padding: 2rem 0; text-align: center;'>
    <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
        Built with Streamlit • Powered by <span style='color: {EYEPOP_CYAN}; font-weight: 600;'>EyePop.ai</span>
    </p>
    <p style='color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
        Detecting ancient structures, one coordinate at a time 🪁
    </p>
</div>
""", unsafe_allow_html=True)

