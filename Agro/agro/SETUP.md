# Quick Setup Guide

## Prerequisites
- Python 3.8+
- MongoDB installed and running
- Bhashini API credentials

## Step-by-Step Setup

### 1. Activate Virtual Environment
```bash
cd G:\agro
.\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB
- Make sure MongoDB is running on `localhost:27017`
- The database `agro-db` will be created automatically
- Weather data will be stored in the `agro-collection` collection

### 4. Configure APIs
Create a `.env` file in the project root and add:
- **Bhashini API**: Get your API key from https://bhashini.gov.in/
  ```env
  BHASHINI_API_KEY=your_actual_bhashini_api_key
  BHASHINI_URL=https://dhruva-api.bhashini.gov.in/services/inference/pipeline
  ```
- **OpenWeather API**: Get a free API key from https://openweathermap.org/api
  ```env
  OPENWEATHER_API_KEY=your_openweather_api_key
  ```

### 5. Seed Sample Data (Optional)
```bash
python manage.py seed_data
```

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Access the Application
Open your browser and go to: `http://localhost:8000`

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB service is running
- Check connection string in `settings.py`
- Verify MongoDB is accessible on port 27017

### Voice Recognition Not Working
- Use Chrome or Edge browser for best support
- Allow microphone permissions in browser
- Check Bhashini API credentials in `.env` file are correct
- Ensure `BHASHINI_API_KEY` and `BHASHINI_URL` are set in `.env`

### Static Files Not Loading
- Run: `python manage.py collectstatic` (if needed)
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings.py

### CORS Errors
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py

## Testing the Application

1. **First Visit**: You'll see two popups asking about crops
2. **Voice Input**: Click microphone icon in any input field
3. **Chatbot**: Type or speak questions in the chatbot
4. **Availability**: Check the three availability cards on the right

## Next Steps

- Add more availability data through MongoDB
- Customize chatbot responses
- Integrate additional Bhashini API features (multiple languages, etc.)
- Add user authentication if needed

