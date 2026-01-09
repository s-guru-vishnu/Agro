
let map = null;
let marker = null;
let selectedLocation = null;


function hidePopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = 'none';
    }
}

function showPopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.style.display = 'flex';
    }
}


function handleLocationChoice(isOnLand) {
    if (isOnLand) {
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    
                    localStorage.setItem('userLatitude', latitude);
                    localStorage.setItem('userLongitude', longitude);
                    
                    
                    hidePopup('popupLocation');
                    showPopup('popupPlanting');
                },
                function(error) {
                    console.error('Error getting location:', error);
                    
                    hidePopup('popupLocation');
                    showMapPopup();
                }
            );
        } else {
            console.warn('Geolocation is not supported by your browser. Showing map selection.');
            hidePopup('popupLocation');
            showMapPopup();
        }
    } else {
        
        hidePopup('popupLocation');
        showMapPopup();
    }
}


function showMapPopup() {
    showPopup('popupMap');
    
    setTimeout(function() {
        initializeMap();
    }, 100);
}

function initializeMap() {
    
    if (typeof L === 'undefined') {
        console.error('Leaflet library is not loaded');
        return;
    }
    
    const mapContainer = document.getElementById('mapContainer');
    if (!mapContainer) return;
    
    
    if (map) {
        map.remove();
        map = null;
        marker = null;
    }
    
    
    const defaultLat = 20.5937;
    const defaultLon = 78.9629;
    
    
    map = L.map('mapContainer').setView([defaultLat, defaultLon], 5);
    
    
    L.tileLayer('https:
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    
    const confirmBtn = document.getElementById('confirmMapBtn');
    if (confirmBtn) {
        confirmBtn.disabled = true;
    }
    selectedLocation = null;
    
    
    const locationText = document.getElementById('selectedLocationText');
    if (locationText) {
        locationText.textContent = 'Click on the map to select';
    }
    
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                map.setView([lat, lon], 13);
                
                
                if (marker) {
                    map.removeLayer(marker);
                }
                marker = L.marker([lat, lon]).addTo(map);
                selectedLocation = { lat: lat, lon: lon };
                updateLocationText(lat, lon);
                if (confirmBtn) {
                    confirmBtn.disabled = false;
                }
            },
            function(error) {
                console.log('Could not get location for map center:', error);
                
            }
        );
    }
    
    
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        
        
        if (marker) {
            map.removeLayer(marker);
        }
        
        
        marker = L.marker([lat, lon]).addTo(map);
        selectedLocation = { lat: lat, lon: lon };
        
        
        updateLocationText(lat, lon);
        
        
        const confirmBtn = document.getElementById('confirmMapBtn');
        if (confirmBtn) {
            confirmBtn.disabled = false;
        }
    });
    
    
    setTimeout(function() {
        if (map) {
            map.invalidateSize();
        }
    }, 200);
}

function updateLocationText(lat, lon) {
    const locationText = document.getElementById('selectedLocationText');
    if (locationText) {
        locationText.textContent = `Latitude: ${lat.toFixed(6)}, Longitude: ${lon.toFixed(6)}`;
    }
    
    
    fetch(`https:
        .then(response => response.json())
        .then(data => {
            if (data && data.display_name) {
                locationText.textContent = data.display_name;
            }
        })
        .catch(error => {
            console.log('Reverse geocoding failed:', error);
        });
}

function confirmMapLocation() {
    if (selectedLocation) {
        
        localStorage.setItem('userLatitude', selectedLocation.lat);
        localStorage.setItem('userLongitude', selectedLocation.lon);
        
        
        hidePopup('popupMap');
        showPopup('popupPlanting');
    }
}

function goBackToLocationQuestion() {
    hidePopup('popupMap');
    showPopup('popupLocation');
}


function handlePlantingStatus(hasPlanted) {
    
    localStorage.setItem('hasPlanted', hasPlanted);
    
    
    hidePopup('popupPlanting');
    
    
    
    
    
    
    console.log('Planting status:', hasPlanted);
}



function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}


document.addEventListener('DOMContentLoaded', function() {
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    
    
    const hasCompletedLocation = localStorage.getItem('userLatitude') && localStorage.getItem('userLongitude');
    const hasCompletedPlanting = localStorage.getItem('hasPlanted');
    
    if (!hasCompletedLocation) {
        
        showPopup('popupLocation');
    } else if (!hasCompletedPlanting) {
        
        showPopup('popupPlanting');
    }
    

    
    loadAvailabilityCards();
    
    
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});


let recognition = null;
let isListening = false;


const languageMap = {
    'en': 'en-US',
    'hi': 'hi-IN',      
    'bn': 'bn-IN',      
    'te': 'te-IN',      
    'mr': 'mr-IN',      
    'ta': 'ta-IN',      
    'gu': 'gu-IN',      
    'kn': 'kn-IN',      
    'ml': 'ml-IN',      
    'pa': 'pa-IN',      
    'or': 'or-IN',      
    'ur': 'ur-IN',      
    'as': 'as-IN',      
    'ne': 'ne-IN',      
};


function startVoiceInput(inputId) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.error('Input element not found:', inputId);
        return;
    }
    
    
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        console.warn('Speech recognition is not supported in your browser.');
        return;
    }
    
    
    if (isListening && recognition) {
        stopVoiceInput(inputId);
        return;
    }
    
    
    const languageSelect = document.getElementById('languageSelect');
    const selectedLang = languageSelect ? languageSelect.value : 'en';
    const langCode = languageMap[selectedLang] || 'en-US';
    
    
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new Recognition();
    recognition.lang = langCode;
    recognition.continuous = false; 
    recognition.interimResults = false; 
    
    
    recognition.onstart = function() {
        isListening = true;
        updateVoiceButtonState(true, inputId);
        
        
        const originalPlaceholder = input.placeholder;
        input.placeholder = 'Listening... Speak now!';
        
        
        input.dataset.originalPlaceholder = originalPlaceholder;
    };
    
    recognition.onresult = function(event) {
        let transcript = '';
        
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        
        
        if (input.value.trim()) {
            input.value += ' ' + transcript.trim();
        } else {
            input.value = transcript.trim();
        }
        
        
        input.focus();
        
        
        input.setSelectionRange(input.value.length, input.value.length);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        updateVoiceButtonState(false, inputId);
        
        
        if (input.dataset.originalPlaceholder) {
            input.placeholder = input.dataset.originalPlaceholder;
        }
        
        
        let errorMessage = 'Speech recognition error occurred.';
        switch(event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone found. Please check your microphone settings.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow microphone access.';
                break;
            case 'network':
                errorMessage = 'Network error. Please check your internet connection.';
                break;
            case 'aborted':
                
                return;
            default:
                errorMessage = 'An error occurred: ' + event.error;
        }
        
        
        const originalValue = input.value;
        input.value = '';
        input.placeholder = errorMessage;
        setTimeout(() => {
            input.value = originalValue;
            if (input.dataset.originalPlaceholder) {
                input.placeholder = input.dataset.originalPlaceholder;
            } else {
                input.placeholder = 'Type or speak your message...';
            }
        }, 3000);
    };
    
    recognition.onend = function() {
        isListening = false;
        updateVoiceButtonState(false, inputId);
        
        
        if (input.dataset.originalPlaceholder) {
            input.placeholder = input.dataset.originalPlaceholder;
            delete input.dataset.originalPlaceholder;
        } else {
            input.placeholder = 'Type or speak your message...';
        }
    };
    
    
    try {
        recognition.start();
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        alert('Could not start voice input. Please make sure your microphone is connected and permissions are granted.');
        isListening = false;
        updateVoiceButtonState(false, inputId);
    }
}

function stopVoiceInput(inputId) {
    if (recognition && isListening) {
        try {
            recognition.stop();
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    }
    
    const input = document.getElementById(inputId);
    if (input && input.dataset.originalPlaceholder) {
        input.placeholder = input.dataset.originalPlaceholder;
        delete input.dataset.originalPlaceholder;
    }
    
    isListening = false;
    updateVoiceButtonState(false, inputId);
}

function updateVoiceButtonState(isActive, inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    
    const wrapper = input.closest('.voice-input-wrapper');
    const voiceBtn = wrapper ? wrapper.querySelector('.voice-btn') : null;
    
    if (!voiceBtn) {
        console.warn('Voice button not found');
        return;
    }
    
    if (isActive) {
        voiceBtn.classList.add('recording');
        voiceBtn.style.background = '#dc3545'; 
        voiceBtn.title = 'Click to stop recording';
        
        
        const icon = voiceBtn.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-stop';
        }
    } else {
        voiceBtn.classList.remove('recording');
        voiceBtn.style.background = '';
        voiceBtn.title = 'Click to use voice input';
        
        
        const icon = voiceBtn.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-microphone';
        }
    }
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    if (!input || !input.value.trim()) return;
    
    
    if (isListening && recognition) {
        stopVoiceInput('chatInput');
    }
    
    const message = input.value.trim();
    const messagesContainer = document.getElementById('chatbotMessages');
    
    
    addMessageToChat(message, 'user');
    
    
    input.value = '';
    
    
    input.disabled = true;
    
    
    const typingIndicator = addTypingIndicator();
    
    
    let csrfToken = '';
    if (typeof getCSRFToken === 'function') {
        csrfToken = getCSRFToken();
    } else {
        
        csrfToken = getCookie('csrftoken') || '';
    }
    
    
    const userLatitude = localStorage.getItem('userLatitude');
    const userLongitude = localStorage.getItem('userLongitude');
    
    
    const payload = {
        message: message
    };
    
    
    if (userLatitude && userLongitude) {
        payload.latitude = parseFloat(userLatitude);
        payload.longitude = parseFloat(userLongitude);
    }
    
    
    fetch('/api/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        
        removeTypingIndicator(typingIndicator);
        
        if (data.success) {
            
            addMessageToChat(data.response, 'bot');
        } else {
            
            addMessageToChat('Sorry, I encountered an error: ' + (data.error || 'Unknown error'), 'bot');
        }
    })
    .catch(error => {
        
        removeTypingIndicator(typingIndicator);
        
        
        addMessageToChat('Sorry, I couldn\'t connect to the server. Please try again.', 'bot');
        console.error('Error sending message:', error);
    })
    .finally(() => {
        
        input.disabled = false;
        input.focus();
    });
}

function addMessageToChat(message, type) {
    const messagesContainer = document.getElementById('chatbotMessages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const messageText = document.createElement('p');
    messageText.textContent = message;
    contentDiv.appendChild(messageText);
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatbotMessages');
    if (!messagesContainer) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message typing-indicator';
    messageDiv.id = 'typingIndicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const typingText = document.createElement('p');
    typingText.innerHTML = '<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>';
    contentDiv.appendChild(typingText);
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageDiv;
}

function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode) {
        indicator.parentNode.removeChild(indicator);
    } else {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator && typingIndicator.parentNode) {
            typingIndicator.parentNode.removeChild(typingIndicator);
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changeLanguage() {
    
    console.log('Language changed');
}

function requestLocationAndWeather() {
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                console.log('Location:', lat, lon);
                
            },
            function(error) {
                console.error('Error getting location:', error);
            }
        );
    }
}


function loadAvailabilityCards() {
    const sections = [
        { type: 'fertilizer', containerId: 'fertilizerContent' },
        { type: 'machine', containerId: 'machineContent' },
        { type: 'manpower', containerId: 'manpowerContent' },
    ];

    sections.forEach(section => fetchAvailabilitySection(section));
}

function fetchAvailabilitySection({ type, containerId }) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '<div class="loading">Loading...</div>';

    const limit = 3;
    let apiUrl = `/api/get-availability/?type=${type}&limit=${limit}`;
    const userLat = localStorage.getItem('userLatitude');
    const userLon = localStorage.getItem('userLongitude');
    if (userLat && userLon) {
        apiUrl += `&latitude=${userLat}&longitude=${userLon}&radius=100`;
    }

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            const keyMap = {
                fertilizer: 'fertilizers',
                machine: 'machines',
                manpower: 'manpower',
            };
            const list = data[keyMap[type]] || [];
            renderAvailabilityList(container, type, list);
        })
        .catch(error => {
            console.error(`Error loading ${type} availability:`, error);
            container.innerHTML = `<div class="loading">Unable to load ${type} data.</div>`;
        });
}

function renderAvailabilityList(container, type, items) {
    if (!items.length) {
        container.innerHTML = `<div class="loading">No ${type} data found.</div>`;
        return;
    }

    const content = items.map(item => {
        const location = item.location || {};
        const statusClass = item.availability === false ? 'status-unavailable' : 'status-available';
        const statusLabel = item.availability === false ? 'Unavailable' : 'Available';
        const priceText = getAvailabilityPrice(item, type);
        const detailText = getAvailabilityDetail(item, type);
        const distanceText = typeof item.distance_km === 'number'
            ? `${item.distance_km} km away`
            : (location.city || location.state || '').trim();
        const metaParts = [priceText, detailText, distanceText].filter(Boolean);
        const metaLine = metaParts.join(' • ');

        return `
            <div class="availability-item">
                <div>
                    <div class="availability-item-name">${item.name || getDefaultTitle(type)}</div>
                    ${metaLine ? `<div class="availability-meta">${metaLine}</div>` : ''}
                </div>
                <span class="availability-item-status ${statusClass}">${statusLabel}</span>
            </div>
        `;
    }).join('');

    container.innerHTML = content;
}

function getAvailabilityPrice(item, type) {
    const priceValue = type === 'manpower' ? Number(item.rate) : Number(item.price || item.rate);
    if (isNaN(priceValue)) {
        return '';
    }
    const formatter = priceValue.toLocaleString('en-IN');
    if (type === 'manpower') {
        return `₹${formatter}/${item.unit || 'day'}`;
    }
    const unit = item.price_unit || item.unit;
    return `₹${formatter}${unit ? ` ${unit}` : ''}`;
}

function getAvailabilityDetail(item, type) {
    if (type === 'fertilizer') {
        if (item.quantity && item.unit) {
            return `${item.quantity} ${item.unit} available`;
        }
        return item.quantity ? `${item.quantity} units` : '';
    }
    if (type === 'machine') {
        return item.type || '';
    }
    if (type === 'manpower') {
        if (item.skills) return item.skills.split(',').slice(0, 2).join(', ').trim();
        if (item.experience) return `${item.experience} yrs experience`;
    }
    return '';
}

function getDefaultTitle(type) {
    if (type === 'fertilizer') return 'Fertilizer listing';
    if (type === 'machine') return 'Machine listing';
    if (type === 'manpower') return 'Worker listing';
    return 'Listing';
}
