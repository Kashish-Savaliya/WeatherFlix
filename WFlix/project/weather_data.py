import requests

API_KEY = "7cb1f7de7481335e10d504a4dc2aa82c"
base_url = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API_KEY}"

layers = [
    "precipitation_new",
    "pressure_new",
    "clouds_new",
    "temp_new",
    # Add more layers as needed
]

zoom = 1
x = 0
y = 0

for layer in layers:
    url = base_url.format(layer=layer, z=zoom, x=x, y=y, API_KEY=API_KEY)
    response = requests.get(url)
    # Downloaded all the images
    if response.status_code == 200:
        with open(f"static/{layer}.png", "wb") as f:
            f.write(response.content)
            print(f"{layer}.png saved successfully!")
    else:
        print(f"Failed to fetch {layer}.png.")
