import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import re
import json
import os

CACHE_FILE = "currency_rates_cache.json"
stable_url_path = "https://www.tgju.org/profile/price_"


class Currency:
    url_map = {
        "USD": f"{stable_url_path}dollar_rl",
        "EUR": f"{stable_url_path}eur",
        "GBP": f"{stable_url_path}pound",
        "RUB": f"{stable_url_path}ruble",
        "JPY": f"{stable_url_path}yen",
        "EGP": f"{stable_url_path}egp",
        "IRR": f"{stable_url_path}irr",
        "TRY": f"{stable_url_path}turkish_lira",
        "CAD": f"{stable_url_path}cad",
        "AUD": f"{stable_url_path}aud",
        "CHF": f"{stable_url_path}swiss_franc",
        "CNY": f"{stable_url_path}cny",
        "INR": f"{stable_url_path}inr",
    }

    def __init__(self, currency_name, previous_value=None):
        self.currency_name = currency_name.upper()
        self.value = None
        self.previous_value = previous_value

    def GetValue(self):
        if self.currency_name not in self.url_map:
            print(f"Currency '{self.currency_name}' not supported.")
            return None

        url = self.url_map[self.currency_name]

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        price_span = soup.find("span", class_="value")

        if price_span:
            raw_value = price_span.text.strip()
            sanitized_value = re.sub(r"[^\d.]", "", raw_value.replace(",", ""))
            try:
                self.value = float(sanitized_value)
                return self.value
            except ValueError:
                print("Error converting to float.")
                return None
        else:
            print("Couldn't find the price on the page.")
            return None

    def FormatValue(self, amount=None):
        if self.value is None:
            return "N/A"
        final_value = self.value if amount is None else self.value * amount
        return f"{final_value:,.0f} ﷼"

    def RateChange(self):
        if self.previous_value is None or self.previous_value == 0:
            return "N/A", "gray"
        change = self.value - self.previous_value
        percent_change = (change / self.previous_value) * 100
        if change > 0:
            return f"↑ +{change:,.0f} ({percent_change:.2f}%)", "green"
        elif change < 0:
            return f"↓ {change:,.0f} ({percent_change:.2f}%)", "red"
        else:
            return "No change", "gray"


class CurrencyApp:
    AUTO_REFRESH_INTERVAL_MS = 30_000  # 30 seconds

    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f0f0")

        self.rate_cache = self.load_cache()

        # UI Setup
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=(30, 10))

        # Amount input
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(
            input_frame, textvariable=self.amount_var, font=("Arial", 12), width=15
        )
        self.amount_entry.insert(0, "Enter amount")
        self.amount_entry.bind("<FocusIn>", self.clear_placeholder)
        self.amount_entry.bind("<FocusOut>", self.add_placeholder)
        self.amount_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Currency dropdown
        self.currency_names = list(Currency.url_map.keys())
        self.currency_name = tk.StringVar(value=self.currency_names[0])
        self.currency_menu = ttk.Combobox(
            input_frame,
            textvariable=self.currency_name,
            values=self.currency_names,
            state="readonly",
            font=("Arial", 12),
        )
        self.currency_menu.pack(side=tk.LEFT)

        # Convert button
        self.button = tk.Button(
            root,
            text="Convert",
            command=self.run_currency_methods,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=20,
        )
        self.button.pack(pady=10)

        # Output labels
        self.result_label = tk.Label(
            root, text="", fg="blue", font=("Arial", 14, "bold"), bg="#f0f0f0"
        )
        self.result_label.pack(pady=5)

        self.previous_rate_label = tk.Label(
            root, text="", fg="blue", font=("Arial", 12), bg="#f0f0f0"
        )
        self.previous_rate_label.pack()

        # Loader
        self.loader = ttk.Progressbar(root, mode="indeterminate", length=250)
        self.loader.pack(pady=10)

        self.auto_refresh()

    def clear_placeholder(self, event):
        if self.amount_entry.get() == "Enter amount":
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.config(fg="black")

    def add_placeholder(self, event):
        if not self.amount_entry.get():
            self.amount_entry.insert(0, "Enter amount")
            self.amount_entry.config(fg="grey")

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_cache(self):
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(self.rate_cache, f)
        except Exception as e:
            print(f"Failed to save cache: {e}")

    def run_currency_methods(self):
        try:
            amount = float(self.amount_var.get())
            if amount < 0:
                raise ValueError
        except ValueError:
            self.result_label.config(text="Enter a valid positive amount.", fg="red")
            self.previous_rate_label.config(text="")
            return

        currency_code = self.currency_name.get()
        prev_value = self.rate_cache.get(currency_code)

        currency = Currency(currency_code)  # create first
        currency.previous_value = prev_value  # assign previous_value correctly

        self.loader.start()
        self.root.update_idletasks()

        value = currency.GetValue()
        self.loader.stop()

        if value is None:
            self.result_label.config(
                text=f"Could not get data for {currency_code}.", fg="red"
            )
            self.previous_rate_label.config(text="")
            return

        self.rate_cache[currency_code] = currency.value
        self.save_cache()

        formatted = currency.FormatValue(amount)
        rate_change, color = currency.RateChange()

        self.result_label.config(
            text=f"{amount} {currency_code} = {formatted}", fg=color
        )
        self.previous_rate_label.config(text=f"Rate Change: {rate_change}", fg=color)

    def auto_refresh(self):
        self.run_currency_methods()
        self.root.after(self.AUTO_REFRESH_INTERVAL_MS, self.auto_refresh)


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
