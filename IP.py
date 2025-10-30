from tkinter import *
from requests import get, exceptions


class IPInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 IP Info Checker")
        self.root.geometry("380x640")
        self.root.config(bg="#e9eef5")
        self.root.resizable(TRUE, TRUE)
        self.my_api_key = "http://ip-api.com/json/{ip}"

        # Dark/Light mode colors
        self.light_mode = {
            "bg": "#e9eef5",
            "fg": "#2b2b2b",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
            "button_bg": "#4CAF50",
            "button_fg": "white",
            "checkbox_bg": "#e9eef5",
            "checkbox_fg": "#222",
            "text_bg": "#2f284b",
            "text_fg": "#e3e3e3",
        }

        self.dark_mode = {
            "bg": "#2e2e2e",
            "fg": "#e0e0e0",
            "entry_bg": "#3b3b3b",
            "entry_fg": "#ffffff",
            "button_bg": "#555555",
            "button_fg": "#ffffff",
            "checkbox_bg": "#2e2e2e",
            "checkbox_fg": "#ffffff",
            "text_bg": "#1c1c1c",
            "text_fg": "#e0e0e0",
        }

        self.current_colors = self.light_mode.copy()

        # Icon setup
        try:
            pageicon = PhotoImage(file="C:\\Users\\Rayan_Svc\\Pictures\\code.png")
            self.root.iconphoto(True, pageicon)
        except Exception:
            pass

        # Labels
        self.title_label = Label(
            self.root,
            text="IP Information Finder",
            font=("Segoe UI", 14, "bold"),
            bg=self.current_colors["bg"],
            fg=self.current_colors["fg"],
        )
        self.title_label.pack(pady=(18, 6))

        self.instruction_label = Label(
            self.root,
            text="Enter an IPv4 address (auto-format):",
            font=("Segoe UI", 13),
            bg=self.current_colors["bg"],
            fg=self.current_colors["fg"],
        )
        self.instruction_label.pack()

        # Entry
        entry_frame = Frame(self.root, bg=self.current_colors["bg"])
        entry_frame.pack(pady=10)
        self.entry_var = StringVar()
        self.entry_var.set(self.get_own_ip())

        self.entry_term = Entry(
            entry_frame,
            textvariable=self.entry_var,
            font=("Consolas", 14),
            width=22,
            justify="center",
            relief=FLAT,
            bg=self.current_colors["entry_bg"],
            fg=self.current_colors["entry_fg"],
            highlightbackground="#cdd3db",
            highlightcolor="#4CAF50",
            highlightthickness=1,
        )
        self.entry_term.pack(ipady=8, pady=3)
        self.entry_term.bind("<KeyRelease>", self.on_key_release)

        # Checkboxes
        self.fields = {
            "country": IntVar(value=1),
            "regionName": IntVar(value=1),
            "city": IntVar(value=1),
            "timezone": IntVar(value=1),
            "isp": IntVar(value=1),
            "countryCode": IntVar(value=0),
            "continentCode": IntVar(value=0),
            "lat": IntVar(value=0),
            "lon": IntVar(value=0),
        }

        checkbox_frame = Frame(self.root, bg=self.current_colors["bg"])
        checkbox_frame.pack(pady=(9, 13), padx=18, fill=X)

        col1 = Frame(checkbox_frame, bg=self.current_colors["bg"])
        col2 = Frame(checkbox_frame, bg=self.current_colors["bg"])
        col1.pack(side=LEFT, fill=BOTH, expand=True)
        col2.pack(side=LEFT, fill=BOTH, expand=True)

        self.checkbox_widgets = []
        items = list(self.fields.items())
        for i, (key, var) in enumerate(items):
            parent = col1 if i % 2 == 0 else col2
            cb = Checkbutton(
                parent,
                text=key,
                variable=var,
                bg=self.current_colors["checkbox_bg"],
                fg=self.current_colors["checkbox_fg"],
                font=("Segoe UI", 9),
                selectcolor="#d7ead7",
                activebackground=self.current_colors["bg"],
                anchor="w",
            )
            cb.pack(fill=X, padx=6, pady=2)
            self.checkbox_widgets.append(cb)

        # Buttons
        self.check_button = Button(
            self.root,
            text="Check IP Info",
            font=("Segoe UI", 11, "bold"),
            bg=self.current_colors["button_bg"],
            fg=self.current_colors["button_fg"],
            activebackground="#45a049",
            activeforeground="white",
            relief=FLAT,
            width=18,
            command=self.check_ip,
        )
        self.check_button.pack(pady=(10, 14))

        # Dark mode toggle
        self.darkmode_button = Button(
            self.root,
            text="🌙 Dark Mode",
            font=("Segoe UI", 10),
            bg=self.current_colors["button_bg"],
            fg=self.current_colors["button_fg"],
            command=self.toggle_dark_mode,
        )
        self.darkmode_button.pack(pady=(0, 10))

        # Result Text
        result_frame = Frame(self.root, bg=self.current_colors["text_bg"])
        result_frame.pack(padx=15, fill=BOTH, expand=True)
        scrollbar = Scrollbar(result_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.result_box = Text(
            result_frame,
            font=("Consolas", 13),
            height=14,
            wrap=WORD,
            relief=FLAT,
            bg=self.current_colors["text_bg"],
            fg=self.current_colors["text_fg"],
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set,
        )
        self.result_box.insert(END, "ℹ️ Result will appear here.")
        self.result_box.config(state=DISABLED)
        self.result_box.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.result_box.yview)

        self.footer_label = Label(
            self.root,
            text="Powered by ip-api.com",
            font=("Segoe UI", 8),
            bg=self.current_colors["bg"],
            fg=self.current_colors["fg"],
        )
        self.footer_label.pack(pady=(8, 10))

    # ----------------- Dark Mode Toggle -----------------
    def toggle_dark_mode(self):
        if self.current_colors == self.light_mode:
            self.current_colors = self.dark_mode.copy()
            self.darkmode_button.config(text="🌞 Light Mode")
        else:
            self.current_colors = self.light_mode.copy()
            self.darkmode_button.config(text="🌙 Dark Mode")

        # Update all widgets colors
        self.root.config(bg=self.current_colors["bg"])
        self.title_label.config(
            bg=self.current_colors["bg"], fg=self.current_colors["fg"]
        )
        self.instruction_label.config(
            bg=self.current_colors["bg"], fg=self.current_colors["fg"]
        )
        self.footer_label.config(
            bg=self.current_colors["bg"], fg=self.current_colors["fg"]
        )
        self.entry_term.config(
            bg=self.current_colors["entry_bg"], fg=self.current_colors["entry_fg"]
        )
        for cb in self.checkbox_widgets:
            cb.config(
                bg=self.current_colors["checkbox_bg"],
                fg=self.current_colors["checkbox_fg"],
                activebackground=self.current_colors["bg"],
            )
        self.check_button.config(
            bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"]
        )
        self.darkmode_button.config(
            bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"]
        )
        self.result_box.config(
            bg=self.current_colors["text_bg"], fg=self.current_colors["text_fg"]
        )

    # ---------- Input formatting helper ----------
    def on_key_release(self, event=None):
        # raw = self.entry_var.get()
        # filtered = "".join(ch for ch in raw if ch.isdigit() or ch == "-")
        # parts = filtered.split("-")
        # parts = [p[:4] for p in parts if p]
        # while len(parts) < 4:
        #     parts.append("")
        # formatted = "-".join(parts[:4])
        # self.entry_var.set(formatted)
        # try:
        #     self.entry_term.icursor(END)
        # except Exception:
            pass

    # ---------- Core network methods ----------
    def get_data(self, ip: str):
        try:
            url = self.my_api_key.format(ip=ip)
            res = get(url, timeout=8)
            res.raise_for_status()
            return res.json()
        except exceptions.RequestException as e:
            return {"error": f"🚫 Network Error:\n{e}"}
        except Exception as e:
            return {"error": f"⚠️ Error:\n{e}"}

    def get_own_ip(self):
        try:
            res = get("https://api.ipify.org?format=json", timeout=5)
            res.raise_for_status()
            return res.json().get("ip", "")
        except Exception:
            return ""

    def check_ip(self):
        ip = self.entry_var.get().strip()
        parts = [p for p in ip.split(".") if p != ""]
        if (
            len(parts) == 0
            or len(parts) > 4
            or any(not p.isdigit() or len(p) > 3 for p in parts)
        ):
            self.update_result(
                "⚠️ Please enter a valid IPv4 address (e.g. 8.8.8.8 or 208.67.222.222)."
            )
            return

        data = self.get_data(ip)
        if "error" in data:
            self.update_result(data["error"])
            return
        if data.get("status") != "success":
            self.update_result("❌ Invalid IP or data unavailable.")
            return

        output_lines = [f"🌍 IP: {ip}", ""]
        field_map = {
            "country": "🏳 Country",
            "regionName": "🗺 Region",
            "city": "🏙 City",
            "timezone": "🕓 Timezone",
            "isp": "💻 ISP",
            "countryCode": "🌐 Country Code",
            "continentCode": "🌎 Continent Code",
            "lat": "📍 Latitude",
            "lon": "📍 Longitude",
        }
        for key, var in self.fields.items():
            if var.get():
                value = data.get(key, "N/A")
                output_lines.append(f"{field_map[key]}: {value}")

        self.update_result("\n".join(output_lines))

    def update_result(self, text):
        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)
        self.result_box.insert(END, text)
        self.result_box.config(state=DISABLED)


# ---------- Run the App ----------
if __name__ == "__main__":
    page = Tk()
    app = IPInfoApp(page)
    page.mainloop()
