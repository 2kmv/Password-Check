import requests
import hashlib
import tkinter as tk

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def check_password():
    password = password_entry.get()
    count = pwned_api_check(password)
    if count:
        result_label.config(text=f'{password} was found to be leaked ({count}). It might be safe to change your password. ')
    else:
        result_label.config(text=f'{password} was NOT found. Your password is secure!')


window = tk.Tk()
window.title("Password Checker")
window.geometry("400x200")

label1 = tk.Label(text="Enter your password:")
label1.pack(pady=10)

password_entry = tk.Entry(show="*")
password_entry.pack()

check_button = tk.Button(text="Check Password", command=check_password)
check_button.pack(pady=10)

result_label = tk.Label(text="")
result_label.pack()

window.mainloop()
