import tkinter as tk
from time import time as auth_time
import time, threading, requests
from webbrowser import open
from random import randint
from bs4 import BeautifulSoup
import pyperclip, colorsys

username = ""
session = requests.Session()

removed_error_in_secs = None

def error_remover():
  global removed_error_in_secs
  removed_error_in_secs = None
  while True:
    time.sleep(0.1)
    if removed_error_in_secs != None:
      if removed_error_in_secs == 0:
        main_error_label.config(text="")
        removed_error_in_secs = None
      else:
        time.sleep(1)
        removed_error_in_secs = removed_error_in_secs-1

def clear_text():
  username_entry.delete(0, tk.END)

def paste_latest_item():
  clipboard_content = pyperclip.paste()
  username_entry.delete(0, tk.END)
  username_entry.insert(tk.END, clipboard_content)

def on_join_game(game_name):
  if game_name == "Server":
    global entered_username
    global removed_error_in_secs
    if len(entered_username.get()) == 0:
      main_error_label.config(text="Empty Field")
      removed_error_in_secs = 3
      return
    res = session.post('https://users.roblox.com/v1/usernames/users', json={'usernames': [entered_username.get()], 'excludeBannedUsers': True})
    if len(res.json()['data']) == 0:
      main_error_label.config(text="Invalid Username")
      removed_error_in_secs = 3
      return
    userid = res.json()['data'][0]['id']
    json_data = {'userIds': [int(userid),],}
    status = session.post('https://presence.roblox.com/v1/presence/users', json=json_data).json()
    presType = status['userPresences'][0]['userPresenceType']
    if presType != 2:
      main_error_label.config(text="User is Not In-Game")
      removed_error_in_secs = 3
      return
    res2 = session.get(f"https://www.roblox.com/users/{userid}/profile")
    soup = BeautifulSoup(res2.content, 'html.parser')
    canbefollowed = soup.find('div', {'data-canbefollowed': True})['data-canbefollowed']
    if canbefollowed != "true":
      main_error_label.config(text="User Has Restricted Join Permissions")
      removed_error_in_secs = 3
      return
    authTicketUrl = "https://auth.roblox.com/v1/authentication-ticket/"
    def getAuthTicket():
      return session.post(
        url = authTicketUrl,
        headers = {
          "Referer": "https://www.roblox.com/",
          "X-CSRF-Token": session.post(
            url = authTicketUrl
          ).headers["X-CSRF-Token"],
        }
      ).headers["RBX-Authentication-Ticket"]
    def launchClient(ticket):
      browserTrackerId = randint(10000000000, 99999999999)
      open(
        f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{int(auth_time())}+"\
        f"placelauncherurl:https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestFollowUser&userId={userid}+browsertrackerid:{browserTrackerId}+robloxLocale:en_us+gameLocale:en_us+channel"
      )
    launchClient(getAuthTicket())

  elif game_name == "Adopt Me":
    placeId = "920587237"
    vip_code = "00487294444822772196415533525938"
    authTicketUrl = "https://auth.roblox.com/v1/authentication-ticket/"
    def getAuthTicket():
      return session.post(
        url = authTicketUrl,
        headers = {
          "Referer": "https://www.roblox.com/",
          "X-CSRF-Token": session.post(
            url = authTicketUrl
          ).headers["X-CSRF-Token"],
        }
      ).headers["RBX-Authentication-Ticket"]
    def launchClient(ticket):
      browserTrackerId = randint(10000000000, 99999999999)
      open(
        f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{int(auth_time())}+"\
        f"placelauncherurl:https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestPrivateGame&placeId={placeId}&linkCode={vip_code}+browsertrackerid:{browserTrackerId}+robloxLocale:en_us+gameLocale:en_us+channel"
      )
    launchClient(getAuthTicket())

# Function to check if the entered cookie token is valid
def check_cookie():
    global username
    if len(entered_cookie.get()) == 0:
      error_label.config(text="Empty field. Please try again.")
      return
    entered_token = entered_cookie.get()
    session.cookies[".ROBLOSECURITY"] = entered_token
    res = session.get('https://users.roblox.com/v1/users/authenticated')
    if res.status_code != 200:
      error_label.config(text="Invalid cookie. Please try again.")  # Set error message text
      return
    username = res.json()['name']
    login_window.destroy()
    open_main_app()

# Function to open the main application window
def open_main_app():
    global app
    app = tk.Tk()
    app.attributes("-topmost", True)
    app.bind("<Map>", lambda event: app.attributes("-topmost", True))
    app.title("Middleman Tool")

    # Set the window size
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 550
    window_height = 160
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Dark theme colors
    background_color = "#121212"
    text_color = "#FFFFFF"
    button_bg_color = "#303030"
    button_fg_color = "#FFFFFF"

    # Set the background color
    app.config(bg=background_color)

    # Placeholder data for the Roblox profile
    roblox_username = username

    join_user_frame = tk.Frame(app, bg=background_color)
    join_user_frame.pack(anchor="w", padx=10, pady=5)
    
    def_font = ("Arial", 10, "bold")

    # Create a label to display the logged username
    username_display = tk.Label(join_user_frame, text=f"Logged as: {roblox_username}", bg=background_color, fg=text_color, font=("Arial", 15, "bold"))
    username_display.pack(anchor="w", padx=10, pady=5)
    def update_rainbow_text():
      hue = 0

      def change_color():
          nonlocal hue
          rgb = colorsys.hsv_to_rgb(hue, 1, 1)
          hex_color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
          username_display.config(fg=hex_color)
          hue = (hue + 0.01) % 1
          app.after(50, change_color)

      change_color()

    # Start the rainbow text effect
    update_rainbow_text()

    # Create a label for the username input field
    username_label = tk.Label(join_user_frame, text="Join a User (Input Username):", bg=background_color, fg=text_color, font=def_font)
    username_label.pack(side="left", anchor="w", pady=5)

    # Create an entry widget for the username input
    global entered_username
    global username_entry
    entered_username = tk.StringVar()
    username_entry = tk.Entry(join_user_frame, textvariable=entered_username, bg=background_color, fg=text_color, font=def_font)
    username_entry.pack(side="left", anchor="w", pady=5)

    # Create a button to join the server using the entered username
    join_button = tk.Button(join_user_frame, text="Join User", bg="green", fg=button_fg_color, command=lambda: on_join_game("Server"), font=def_font)
    join_button.pack(side="left", anchor="w", padx=5, pady=5)
    
    clr_button = tk.Button(join_user_frame, text="CLR", bg=button_bg_color, fg=button_fg_color, command=lambda: clear_text(), font=def_font)
    clr_button.pack(side="left", anchor="w", padx=5, pady=5)

    paste_button = tk.Button(join_user_frame, text="Paste", bg=button_bg_color, fg=button_fg_color, command=lambda: paste_latest_item(), font=def_font)
    paste_button.pack(side="left", anchor="w", padx=5, pady=5)

    join_game_frame = tk.Frame(app, bg=background_color)
    join_game_frame.pack(anchor="w", padx=10, pady=5)

    # Create a label for the game buttons
    games_label = tk.Label(join_game_frame, text="VIP Servers:", bg=background_color, fg=text_color, font=def_font)
    games_label.pack(side="left", anchor="w", pady=5)

    # Create Join Game buttons (placeholders)
    adopt_me_button = tk.Button(join_game_frame, text="Join Adopt Me", bg="green", fg=button_fg_color, command=lambda: on_join_game("Adopt Me"), font=def_font)
    adopt_me_button.pack(side="left", anchor="w", padx=10, pady=5)

    psx_button = tk.Button(join_game_frame, text="Join PSX", bg="green", fg=button_fg_color, command=lambda: on_join_game("PSX"), font=def_font)
    psx_button.pack(side="left", anchor="w", padx=10, pady=5)

    mm2_button = tk.Button(join_game_frame, text="Join MM2", bg="green", fg=button_fg_color, command=lambda: on_join_game("MM2"), font=def_font)
    mm2_button.pack(side="left", anchor="w", padx=10, pady=5)

    global main_error_label
    main_error_label = tk.Label(app, text="", fg="red", bg=background_color)
    main_error_label.pack()

    # Run the main application window
    threading.Thread(target=error_remover).start()
    app.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.attributes("-topmost", True)
login_window.bind("<Map>", lambda event: login_window.attributes("-topmost", True))
login_window.title("Login Page")

# Set the login window size
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
window_width = 250
window_height = 150
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Dark theme colors for the login window
login_background_color = "#1F1F1F"
login_text_color = "#FFFFFF"

# Set the login window background color
login_window.config(bg=login_background_color)

# Create a label for the login prompt
login_label = tk.Label(login_window, text="Enter Roblox Cookie:", bg=login_background_color, fg=login_text_color, font=("Arial", 10, "bold"))
login_label.pack(pady=10)

# Create an entry widget for the cookie token input
entered_cookie = tk.StringVar()
cookie_entry = tk.Entry(login_window, textvariable=entered_cookie, show="*", bg=login_background_color, fg=login_text_color)
cookie_entry.pack(pady=5)

# Create a button to submit the cookie token
login_button = tk.Button(login_window, text="Login", bg="#303030", fg=login_text_color, command=check_cookie, font=("Arial", 10, "bold"))
login_button.pack(pady=10)

error_label = tk.Label(login_window, text="", fg="red", bg=login_background_color)
error_label.pack()

# Run the login window
login_window.mainloop()
