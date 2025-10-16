# Desert Kite Detection

Detect ancient desert kites (prehistoric stone structures) from satellite imagery using AI.

![Desert Kite Detection](https://img.shields.io/badge/Powered%20by-EyePop.ai-00D9FF?style=flat-square)

## What It Does

This app finds ancient desert kites in satellite images. Just enter GPS coordinates, and AI will detect these prehistoric structures for you.

## Quick Start

### 1. Get an EyePop API Token

Sign up at [eyepop.ai](https://eyepop.ai) to get your free API token.

### 2. Install Dependencies

```bash
pip install streamlit pillow python-dotenv eyepop-sdk-python requests
```

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Use the App

1. **Login** - Enter your EyePop API token
2. **Add Coordinates** - Input locations in decimal or DMS format
3. **Process** - Click "Process All Locations" 
4. **View Results** - See detected kites with confidence scores

## Features

✨ **Easy Authentication** - Simple token-based login  
📍 **Flexible Input** - Accepts decimal or DMS coordinates  
🎯 **Batch Processing** - Queue multiple locations at once  
🔍 **Confidence Filter** - Adjust threshold to show/hide detections  
📊 **Visual Results** - Bounding boxes on satellite imagery  
💾 **Export** - Download annotated images

## Coordinate Formats

**Decimal:**
```
31.483472, 38.368028
```

**DMS (Degrees Minutes Seconds):**
```
31°29'00.5"N 38°22'04.9"E
```

## Example Usage

1. Enter coordinates: `25.742162, 39.292586`
2. Click "Add to Queue"
3. Add more locations (optional)
4. Click "Process All Locations"
5. Adjust confidence threshold slider
6. Download results

## Requirements

- Python 3.8+
- EyePop API token (get it at [eyepop.ai](https://eyepop.ai))
- Internet connection (for satellite imagery)

## Technology

- **AI Detection**: EyePop.ai computer vision
- **Satellite Imagery**: Google Maps Static API
- **Interface**: Streamlit

## Support

Need help? 
- Visit [eyepop.ai](https://eyepop.ai)
- Check out [EyePop Documentation](https://docs.eyepop.ai)

## License

MIT License

---

**Built with ❤️ using EyePop.ai**

