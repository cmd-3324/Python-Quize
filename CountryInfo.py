from tkinter import *
from requests import get, exceptions
import re
from PIL import Image, ImageTk
import io


class IPInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Country Info Checker")
        self.root.geometry("480x720")
        self.root.resizable(True, True)
        self.dark_mode = True
        self.themes = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#f0f0f0",
                "fgtrans": "f0f0f0",
                "trans": "1e1e1e",
                "accent": "#4CAF50",
                "text_bg": "#2b2b2b",
                "text_fg": "#ffffff",
                "border": "#3f3f3f",
                "secondary": "#cccccc",
            },
            "light": {
                "fgtrans": "1c1c1c",
                "trans": "f7f9fc",
                "bg": "#f7f9fc",
                "fg": "#1c1c1c",
                "accent": "#1976D2",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "border": "#cccccc",
                "secondary": "#555555",
            },
        }
        self.transparencyBtn = Button(
            root,
            relief=FLAT,
            bg=self.colors["trans"],
            fg=self.colors["fgtrans"],
            font=("Segoe UI", 20, "bold"),
            text="Set",
            textvariable="transparencyBtn",
        ).pack()
        self.apply_theme()
        self.my_api_key_alpha = "https://restcountries.com/v3.1/alpha/{code}"
        self.my_api_key_name = "https://restcountries.com/v3.1/name/{name}"
        self.COUNTRY_CODES = {
            "iran": "IR",
            "united states": "US",
            "france": "FR",
            "germany": "DE",
            "japan": "JP",
            "china": "CN",
        }

        header = Frame(self.root, bg=self.colors["bg"])
        header.pack(fill=X, pady=(10, 0))
        Label(header, text="Set Transparency", font=("Segoe UI", 14, "italic")).pack(side=RIGHT,padx=(20,10))

        Label(
           
            text="🔎 Country Info Finder",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
        ).pack(side=LEFT, padx=(20, 0))

        self.toggle_btn = Button(
            header,
            text="🌙",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["accent"],
            relief=FLAT,
            bd=0,
            cursor="hand2",
            command=self.toggle_theme,
        )
        self.toggle_btn.pack(side=RIGHT, padx=20)

        Label(
            self.root,
            text="Enter Country Name:",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
        ).pack(pady=(5, 0))

        entry_frame = Frame(self.root, bg=self.colors["bg"])
        entry_frame.pack(pady=10)

        self.entry_var = StringVar()
        self.entry_var.trace("w", self.on_ip_change)

        self.entry_term = Entry(
            entry_frame,
            textvariable=self.entry_var,
            font=("Consolas", 14),
            justify="center",
            relief=FLAT,
            width=26,
            bg=self.colors["text_bg"],
            fg=self.colors["text_fg"],
            insertbackground=self.colors["fg"],
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["accent"],
            highlightthickness=1.5,
        )
        self.entry_term.pack(ipady=8)
        self.entry_var.set("Iran")

        Label(
            self.root,
            text="Choose details to display:",
            font=("Segoe UI", 10, "italic"),
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
        ).pack(pady=(5, 2))

        checkbox_frame = Frame(self.root, bg=self.colors["bg"])
        checkbox_frame.pack(padx=18, pady=(5, 15), fill=X)

        self.fields = {
            "country": IntVar(value=1),
            "Capital": IntVar(value=1),
            "timezone": IntVar(value=1),
            "countryCode": IntVar(value=1),
            "official": IntVar(value=0),
            "continentCode": IntVar(value=1),
        }

        col1 = Frame(checkbox_frame, bg=self.colors["bg"])
        col2 = Frame(checkbox_frame, bg=self.colors["bg"])
        col1.pack(side=LEFT, fill=BOTH, expand=True)
        col2.pack(side=LEFT, fill=BOTH, expand=True)

        self.check_buttons = []
        for i, (key, var) in enumerate(self.fields.items()):
            parent = col1 if i % 2 == 0 else col2
            label_text = "Government" if key == "official" else key.capitalize()
            chk = Checkbutton(
                parent,
                text=label_text,
                variable=var,
                bg=self.colors["bg"],
                fg=self.colors["fg"],
                activebackground=self.colors["bg"],
                activeforeground=self.colors["accent"],
                selectcolor=self.colors["text_bg"],
                font=("Segoe UI", 9),
                anchor="w",
                cursor="hand2",
            )
            chk.pack(fill=X, padx=8, pady=2)
            self.check_buttons.append(chk)

        self.check_btn = Button(
            self.root,
            text="Check Country Info",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["accent"],
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=FLAT,
            width=20,
            cursor="hand2",
            command=self.check_ip,
        )
        self.check_btn.pack(pady=(5, 12))
        self.flag_label = Label(self.root, bg=self.colors["bg"])
        self.flag_label.pack(pady=10)

        result_frame = Frame(self.root, bg=self.colors["bg"])
        result_frame.pack(padx=15, fill=BOTH, expand=True)

        scrollbar = Scrollbar(result_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.result_box = Text(
            result_frame,
            font=("Consolas", 11),
            height=14,
            wrap=WORD,
            relief=FLAT,
            bg=self.colors["text_bg"],
            fg=self.colors["text_fg"],
            padx=10,
            pady=10,
            insertbackground=self.colors["fg"],
            yscrollcommand=scrollbar.set,
        )

        self.result_box.insert(END, "ℹ️ Result will appear here.")
        self.result_box.config(state=DISABLED)
        self.result_box.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.result_box.yview)

        Label(
            self.root,
            text="Powered by restcountries.com And Junior-PRogrammer Me!😏",
            font=("Segoe UI", 8),
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
        ).pack(pady=(6, 10))

    def apply_theme(self):
        mode = "dark" if getattr(self, "dark_mode", True) else "light"
        self.colors = self.themes[mode]
        self.root.config(bg=self.colors["bg"])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        new_icon = "🌞" if not self.dark_mode else "🌙"
        self.toggle_btn.config(
            text=new_icon, fg=self.colors["accent"], bg=self.colors["bg"]
        )
        for widget in self.root.winfo_children():
            try:
                widget.config(bg=self.colors["bg"], fg=self.colors["fg"])
            except:
                pass
        for chk in getattr(self, "check_buttons", []):
            chk.config(
                bg=self.colors["bg"],
                fg=self.colors["fg"],
                selectcolor=self.colors["text_bg"],
                activebackground=self.colors["bg"],
                activeforeground=self.colors["accent"],
            )
        self.entry_term.config(
            bg=self.colors["text_bg"],
            fg=self.colors["text_fg"],
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["accent"],
            insertbackground=self.colors["fg"],
        )
        self.result_box.config(
            bg=self.colors["text_bg"],
            fg=self.colors["text_fg"],
            insertbackground=self.colors["fg"],
        )
        self.check_btn.config(bg=self.colors["accent"])

    def formatErrormessage(self, message, phrase1, phrase2):
        foramted = str(message).replace(phrase1, phrase2)
        return foramted

    def on_ip_change(self, *args):
        pass

    def get_data(self, country_input: str):
        try:
            country_input = country_input.strip().lower()
            country_code = self.COUNTRY_CODES.get(country_input, None)
            if country_code:
                url = self.my_api_key_alpha.format(code=country_code)
                res = get(url, timeout=8)
                res.raise_for_status()
                data = res.json()[0]
            else:
                url = self.my_api_key_name.format(name=country_input)
                res = get(url, timeout=8)
                res.raise_for_status()
                data = res.json()[0]

            return {
                "country": data.get("name", {}).get("common", "N/A"),
                "Capital": data.get("capital", ["N/A"])[0],
                "continentCode": data.get("region", "N/A"),
                "countryCode": data.get("cca2", "N/A"),
                "timezone": data.get("timezones", ["N/A"])[0],
                "official": data.get("name", {}).get("official", "N/A"),
            }

        except exceptions.RequestException as e:
            formated = self.formatErrormessage(
                f"404 Client Error: Not Found for url: https://restcountries.com/v3.1/name/'{country_input}'",
                "Not Found for url: https://restcountries.com/v3.1/name/",
                "",
            )
            return {"error": f"🚫 Network Error:\n{formated}"}

        except IndexError:
            return {"error": "❌ Country not found"}
        except exceptions.RequestException as e:
            return {"error": f"❌⚠️Requset error :\n {e}"}
        except Exception as e:
            return {"error": f"⚠️ Error:\n{e}"}
        # flag finding system

    def getflag(self, countryCode):
        try:
            if not countryCode:
                return None

            code = countryCode.strip().lower()
            url = f"https://flagcdn.com/w320/{code}.png"

            response = get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))

            img = img.resize((150, 90), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            return photo

        except exceptions.RequestException as e:
            print(f"Network error while fetching flag: {e}")
            return None
        except Exception as e:
            print(f"Flag error: {e}")
            return None

    def check_ip(self):
        country = self.entry_var.get().strip()
        if not re.match(r"^[A-Za-z\s\-]{1,50}$", country):
            self.update_result("⚠️ Please enter a valid Country name or code(e.g-Iran-IR)")
            return

        data = self.get_data(country)
        if "error" in data:
            self.update_result(data["error"])
            return

        field_map = {
            "country": "🏳 Country",
            "Capital": "🗺 Capital",
            "timezone": "🕓 Timezone",
            "countryCode": "🌐 Country Code",
            "continentCode": "🌎 Continent Code",
            "official": "🏛️Govermnet-Type",
        }

        output_lines = [f"🌍 Info Of: {country}", ""]
        for key, var in self.fields.items():
            if var.get():
                output_lines.append(f"{field_map[key]}: {data.get(key, 'N/A')}")

        self.flag_photo = self.getflag(data.get("countryCode"))
        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)
        for line in output_lines:
            self.result_box.insert(END, line + "\n")

        if self.flag_photo:
            self.result_box.insert(END, "\n")
            self.result_box.image_create(END, image=self.flag_photo)
            self.result_box.insert(END, "\n")
        else:
            self.result_box.insert(END, "\nNo flag available\n")

        self.result_box.config(state=DISABLED)

    def update_result(self, text):
        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)
        self.result_box.insert(END, text)
        self.result_box.config(state=DISABLED)


# if __name__ == "__main__":
root = Tk()
app = IPInfoApp(root)
root.mainloop()
