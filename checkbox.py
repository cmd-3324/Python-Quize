from tkinter import *
from requests import get, exceptions
import re


class IPInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 IP Info Checker")
        self.root.geometry("480x720")
        self.root.resizable(True, True)

        # Theme states
        self.dark_mode = True
        self.themes = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#f0f0f0",
                "accent": "#4CAF50",
                "text_bg": "#2b2b2b",
                "text_fg": "#ffffff",
                "border": "#3f3f3f",
                "secondary": "#cccccc",
            },
            "light": {
                "bg": "#f7f9fc",
                "fg": "#1c1c1c",
                "accent": "#1976D2",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "border": "#cccccc",
                "secondary": "#555555",
            },
        }

        self.apply_theme()

        self.my_api_key = "http://ip-api.com/json/{ip}"

        # --- Header with Toggle ---
        header = Frame(self.root, bg=self.colors["bg"])
        header.pack(fill=X, pady=(10, 0))

        Label(
            header,
            text="🔎 IP Information Finder",
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
            text="Enter IP address:",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
        ).pack(pady=(5, 0))

        # --- Input Box ---
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
        self.entry_var.set(self.get_own_ip())

        # --- Checkboxes ---
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
            "regionName": IntVar(value=1),
            "city": IntVar(value=1),
            "timezone": IntVar(value=1),
            "isp": IntVar(value=1),
            "countryCode": IntVar(value=0),
            "continentCode": IntVar(value=0),
            "lat": IntVar(value=0),
            "lon": IntVar(value=0),
        }

        col1 = Frame(checkbox_frame, bg=self.colors["bg"])
        col2 = Frame(checkbox_frame, bg=self.colors["bg"])
        col1.pack(side=LEFT, fill=BOTH, expand=True)
        col2.pack(side=LEFT, fill=BOTH, expand=True)

        self.check_buttons = []
        for i, (key, var) in enumerate(self.fields.items()):
            parent = col1 if i % 2 == 0 else col2
            chk = Checkbutton(
                parent,
                text=key.capitalize(),
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

        # --- Button ---
        self.check_btn = Button(
            self.root,
            text="Check IP Info",
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

        # --- Result Box ---
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
            text="Powered by ip-api.com",
            font=("Segoe UI", 8),
            bg=self.colors["bg"],
            fg=self.colors["secondary"],
        ).pack(pady=(6, 10))

    # ---------- Theme Switch ----------
    def apply_theme(self):
        mode = "dark" if getattr(self, "dark_mode", True) else "light"
        self.colors = self.themes[mode]
        self.root.config(bg=self.colors["bg"])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        new_icon = "🌞" if not self.dark_mode else "🌙"
        self.toggle_btn.config(text=new_icon, fg=self.colors["accent"], bg=self.colors["bg"])
        # Update all widgets' colors
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

    # ---------- Smart IP Formatter ----------
    def on_ip_change(self, *args):
        # current = re.sub(r"[^0-9]", "", self.entry_var.get())
        # groups = []
        # for i in range(0, len(current), 3):
        #     groups.append(current[i:i+3])
        #     if len(groups) == 4:
        #         break
        # formatted = ".".join(groups)
        # if formatted != self.entry_var.get():
        #     self.entry_var.set(formatted)
        pass
    # ---------- Networking ----------
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
        if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
            self.update_result("⚠️ Please enter a valid IPv4 address (e.g. 8.8.8.8)")
            return

        data = self.get_data(ip)
        if "error" in data:
            self.update_result(data["error"])
            return
        if data.get("status") != "success":
            self.update_result("❌ Invalid IP or data unavailable.")
            return

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

        output_lines = [f"🌍 IP: {ip}", ""]
        for key, var in self.fields.items():
            if var.get():
                output_lines.append(f"{field_map[key]}: {data.get(key, 'N/A')}")
        self.update_result("\n".join(output_lines))

    def update_result(self, text):
        self.result_box.config(state=NORMAL)
        self.result_box.delete(1.0, END)
        self.result_box.insert(END, text)
        self.result_box.config(state=DISABLED)


if __name__ == "__main__":
    root = Tk()
    app = IPInfoApp(root)
    root.mainloop()
