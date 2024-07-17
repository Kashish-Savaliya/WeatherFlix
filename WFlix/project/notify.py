# import required libraries
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

# create an object to ToastNotifier class
n = ToastNotifier()


# define a function
def getdata(url):
    r = requests.get(url)
    return r.text


def scrape_weather_data():
    url = f'http://127.0.0.1:5000/weather_forecast'  # Replace 'example.com' with the actual website URL
    htmldata = getdata(url)

    soup = BeautifulSoup(htmldata, 'html.parser')

    print(soup.prettify())
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract weather data from the page
            temperature = soup.find('span', class_='temperature').text
            humidity = soup.find('span', class_='humidity').text
            condition = soup.find('div', class_='condition').text

            return {'temperature': temperature, 'humidity': humidity, 'condition': condition}
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

def should_send_notification(weather_data):
    # Check if temperature is above a certain threshold
    temperature = int(weather_data['temperature'].split('°')[0])
    if temperature > 30:  # Example threshold
        return True

    # Check if there's a specific weather condition
    condition = weather_data['condition'].lower()
    if 'rain' in condition or 'storm' in condition:
        return True

    return False

def send_notification(user_email, message):
    # Implement your notification logic here (e.g., email, SMS, push notification)
    print(f"Sending notification to {user_email}: {message}")