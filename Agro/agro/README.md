# Agro Farmer Portal

A comprehensive web application for farmers to manage their farming needs including fertilizer availability, machine rentals, and manpower services. Features an AI-powered chatbot with voice-to-text capabilities using Bhashini API.

## Features

- 🌾 **Crop Management**: Track planted crops with initial popup questionnaires
- 💬 **AI Chatbot**: Interactive chatbot assistant for farming queries
- 🎤 **Voice-to-Text**: Voice input support in all input fields using Bhashini API (Tamil to English translation)
- 🌿 **Fertilizer Availability**: Real-time fertilizer availability tracking
- 🚜 **Machine Availability**: Tractor and farming equipment rental information
- 👥 **Manpower Services**: Connect with skilled farm workers
- 🌤️ **Weather Integration**: Automatic location-based weather data from OpenWeather API
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations

## Tech Stack

### Frontend
- HTML5
- CSS3 (with modern animations and gradients)
- JavaScript (ES6+)
- Font Awesome Icons
- Google Fonts (Poppins)

### Backend
- Django 5.2.8
- MongoDB (using PyMongo)
- Django CORS Headers

### APIs
- Bhashini API (for Tamil/Hindi speech recognition and translation)
- OpenWeather API (for weather data)

## Installation

1. **Clone the repository**
   ```bash
   cd G:\agro
   ```

2. **Activate virtual environment**
   ```bash
   .\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   - Install MongoDB on your system
   - Start MongoDB service
   - Update MongoDB connection in `agro_project/settings.py` if needed:
     ```python
     MONGODB_SETTINGS = {
         'host': 'mongodb://localhost:27017/',
         'db': 'agro-db',
     }
     ```

5. **Configure API Keys**
   - A `.env` file has been created in the project root with all API keys
   - Update the `.env` file with your actual API keys:
     ```bash
     # Bhashini API (for Tamil/Hindi speech recognition)
     BHASHINI_API_KEY=your_bhashini_api_key_here
     Get your API key from: https://bhashini.gov.in/
     
     # OpenWeather API (already configured)
     OPENWEATHER_API_KEY=your_openweather_api_key_here
     Get your API key from: https://openweathermap.org/api
     ```
   - **Note**: The `.env` file is already in `.gitignore` and will not be committed to version control
   - A `.env.example` file is provided as a template

6. **Run migrations** (if needed)
   ```bash
   python manage.py migrate
   ```

7. **Create sample data** (optional)
   - You can add sample data directly to MongoDB or through the admin panel

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`

## Project Structure

```
agro/
├── agro_project/          # Django project settings
│   ├── settings.py       # Main settings file
│   ├── urls.py           # Main URL configuration
│   └── ...
├── farmers_app/          # Main Django app
│   ├── models.py        # MongoDB collection helpers
│   ├── views.py         # API views and endpoints
│   ├── urls.py          # App URL configuration
│   └── db_connection.py # MongoDB connection
├── templates/           # HTML templates
│   └── farmers_app/
│       └── index.html   # Main page template
├── static/              # Static files
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── js/
│       └── main.js     # Main JavaScript file
└── requirements.txt     # Python dependencies
```

## API Endpoints

- `GET /` - Main page
- `POST /api/save-farmer-data/` - Save farmer and crop data
- `GET /api/get-availability/` - Get availability data (fertilizers, machines, manpower)
- `POST /api/chatbot/` - Send message to chatbot
- `POST /api/voice-to-text/` - Convert voice to text using Bhashini NLP
  - Optional parameters: `api` (bhashini/auto), `language` (ta/hi/en), `translate` (true/false)
- `POST /api/get-weather/` - Get weather data for user's location and store in MongoDB

## Usage

1. **First Visit**: Two popups will appear:
   - First popup: Ask if you have planted crops
   - Second popup (if yes): Ask for crop name

2. **Voice Input**: Click the microphone icon in any input field to use voice-to-text

3. **Chatbot**: Type or speak your questions in the chatbot on the right side

4. **Availability**: Check the three availability cards on the right for:
   - Fertilizer availability
   - Machine availability
   - Manpower availability

## MongoDB Collections

- `farmers` - Farmer information
- `crops` - Crop data
- `fertilizers` - Fertilizer availability
- `machines` - Machine availability
- `manpower` - Manpower availability
- `chat_history` - Chatbot conversation history
- `agro-collection` - Weather data and other agricultural information

## Configuration

### Bhashini API Setup

1. Get your API key from [Bhashini](https://bhashini.gov.in/)
2. Add `BHASHINI_API_KEY` to your `.env` file
3. Add `BHASHINI_URL` to your `.env` file (or it will use the default)
4. The voice-to-text endpoint uses Bhashini API for Tamil speech recognition and English translation

### MongoDB Setup

1. Install MongoDB Community Edition
2. Start MongoDB service
3. The application will automatically create the database and collections on first use

## Browser Compatibility

- Chrome/Edge (recommended for best voice recognition support)
- Firefox
- Safari
- Opera

Note: Voice recognition works best in Chrome/Edge browsers with Web Speech API support.

## Development

To add sample data to MongoDB, you can use the MongoDB shell or create a management command:

```python
# Example MongoDB document structure
{
    "name": "NPK Fertilizer",
    "status": "Available",
    "quantity": 100,
    "location": "Warehouse A"
}
```

## License

This project is created for agricultural purposes.

## Support

For issues or questions, please check the documentation or contact the development team.

