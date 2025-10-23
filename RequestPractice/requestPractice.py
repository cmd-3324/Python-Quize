import requests as rq
# user_id = int(input("Enter UserID :"))
# base_url = "https://reqres.in/api/users/{user_id}"
base_url = "https://reqres.in/api/users"
api_key = "reqres-free-v1"


# def getTestdata():
#     try:
#         # First GET request without parameters (page 1)
#         response = rq.get(base_url)
#         statusCode = response.status_code

#         if statusCode == 200:
#             data = response.json()  # Correct way to get JSON

#             # Print all users on page 1
#             print(f"Page: {data.get('page')}")

#             # 'data' key holds a list of users
#             users = data.get('data', [])

#             for user in users:
#                 print(
#                     f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']} \t Email: {user['email']}"
#                 )
#         else:
#             print(f"Failed to retrieve data. Status code: {statusCode}")

#         # Now get users on page 2 with params
#         response = rq.get(base_url, params={"page": 2})
#         print("\nSecond request (page 2):")
#         print("Status Code:", response.status_code)
#         # print("Response JSON:", response.json())
#         print("Data retrieved successfully.")

#     except Exception as e:
#         print("An error occurred:", e)

#     finally:
#         print("Function execution completed.")

# def firstTime():
#     searchTerm  = "amazon.com.uk"
#     test_url = f"https://google.com/search?q={searchTerm}"
#     response = rq.get(test_url)
#     if (response.status_code == 200):
#         print("Data retirved Succesfully")
#         info = response.json()
#         print(info)
#     else:
#         print("Can't retrive data!")
# firstTime()
# data = response.json() e
# print(data)
# def get_weather(self):
#     api_key = "0e4a5d4aa42ea9d02953ce3697f105e6"
#     city = self.city_input.text()
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         if data["cod"] == 200:
#             self.display_weather(data)

#     except requests.exceptions.HTTPError as http_error:
#         match response.status_code:
#             case 400:
#                 self.display_error("Bad request:\nPlease check your input")
#             case 401:
#                 self.display_error("Unauthorized:\nInvalid API key")
#             case 403:
#                 self.display_error("Forbidden:\nAccess is denied")
#             case 404:
#                 self.display_error("Not found:\nCity not found")
#             case 500:
#                 self.display_error("Internal Server Error:\nPlease try again later")
#             case 502:
#                 self.display_error("Bad Gateway:\nInvalid response from the server")
#             case 503:
#                 self.display_error("Service Unavailable:\nServer is down")
#             case 504:
#                 self.display_error("Gateway Timeout:\nNo response from the server")
#             case _:
#                 self.display_error(f"HTTP error occurred:\n{http_error}")

#     except requests.exceptions.ConnectionError:
#         self.display_error("Connection Error:\nCheck your internet connection")
#     except requests.exceptions.Timeout:
#         self.display_error("Timeout Error:\nThe request timed out")
#     except requests.exceptions.TooManyRedirects:
#         self.display_error("Too many Redirects:\nCheck the URL")
#     except requests.exceptions.RequestException as req_error:
#         self.display_error(f"Request Error:\n{req_error}")

# f = br(res.content,features="lxml")
# print(col.Fore.RED + str(f.find("a")))
# -------------------------------------
import requests
from bs4 import BeautifulSoup

url = "https://google.com"
response = requests.get(url)
html = response.text  # or response.content for bytes

soup = BeautifulSoup(html, "html.parser")

# find all <a> tags with href attribute
links = soup.find_all("a", href=True)

for link in links:
    href = link.get("href")
    text = link.get_text().strip()
    print(f"Link text: {text} -> URL: {href}")
