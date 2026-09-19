import tkinter as tk
from tkinter import ttk, messagebox

from wifi_manager import get_wifi_profiles


class WiFiViewer:
    def __init__(self, root):
        self.root = root

        self.root.title("WiFi Viewer")
        self.root.geometry("600x500")
        self.root.minsize(600, 400)

        self.all_profiles = []

        self.create_widgets()
        self.load_profiles()

    # -----------------------------
    # Create GUI
    # -----------------------------

    def create_widgets(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#080808",
            height=80
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="WiFi Viewer",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#111111"
        )

        title.pack(side="left", padx=25, pady=18)

        subtitle = tk.Label(
            header,
            text="Saved Wi-Fi Profiles",
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#111111"
        )

        subtitle.pack(side="left", pady=25)

        # Search section
        search_frame = tk.Frame(self.root)

        search_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            search_frame,
            text="Search:",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11)
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_profiles
        )

        # Buttons
        self.refresh_button = ttk.Button(
            search_frame,
            text="Refresh",
            command=self.load_profiles
        )

        self.refresh_button.pack(side="left")

        # Table
        table_frame = tk.Frame(self.root)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = ("number", "wifi")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "number",
            text="#"
        )

        self.tree.heading(
            "wifi",
            text="Wi-Fi Profile"
        )

        self.tree.column(
            "number",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "wifi",
            width=450
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Bottom buttons
        button_frame = tk.Frame(self.root)

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        ttk.Button(
            button_frame,
            text="Copy Profile Name",
            command=self.copy_profile
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.destroy
        ).pack(side="right")

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 9),
            fg="#224E45"
        )

        self.status_label.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

    # -----------------------------
    # Load Profiles
    # -----------------------------

    def load_profiles(self):

        self.status_label.config(
            text="Loading Wi-Fi profiles..."
        )

        self.root.update_idletasks()

        self.all_profiles = get_wifi_profiles()

        self.display_profiles(self.all_profiles)

        self.status_label.config(
            text=f"{len(self.all_profiles)} Wi-Fi profile(s) found"
        )

    # -----------------------------
    # Display Profiles
    # -----------------------------

    def display_profiles(self, profiles):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, profile in enumerate(profiles, 1):

            self.tree.insert(
                "",
                "end",
                values=(index, profile)
            )

    # -----------------------------
    # Search
    # -----------------------------

    def search_profiles(self, event=None):

        search_text = self.search_var.get().lower().strip()

        if not search_text:
            filtered = self.all_profiles

        else:
            filtered = [
                profile
                for profile in self.all_profiles
                if search_text in profile.lower()
            ]

        self.display_profiles(filtered)

        self.status_label.config(
            text=f"{len(filtered)} profile(s) found"
        )

    # -----------------------------
    # Copy Profile
    # -----------------------------

    def copy_profile(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a Wi-Fi profile first."
            )
            return

        item = self.tree.item(selected[0])

        profile_name = item["values"][1]

        self.root.clipboard_clear()
        self.root.clipboard_append(profile_name)

        messagebox.showinfo(
            "Copied",
            f"Profile name copied:\n{profile_name}"
        )


# -----------------------------
# Start Application
# -----------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = WiFiViewer(root)

    root.mainloop()