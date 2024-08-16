import tkinter as tk
from tkinter import scrolledtext
import nmap

class NmapGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nmap Scanner")
        self.geometry("600x400")

        # Target IP input
        self.target_label = tk.Label(self, text="Target IP or Hostname:")
        self.target_label.pack(pady=5)
        self.target_entry = tk.Entry(self, width=50)
        self.target_entry.pack(pady=5)

        # Port range input
        self.ports_label = tk.Label(self, text="Ports (e.g., 22-80):")
        self.ports_label.pack(pady=5)
        self.ports_entry = tk.Entry(self, width=50)
        self.ports_entry.pack(pady=5)

        # Scan button
        self.scan_button = tk.Button(self, text="Scan", command=self.scan)
        self.scan_button.pack(pady=10)

        # Output area
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=15)
        self.output_text.pack(pady=10)

    def scan(self):
        # Clear previous output
        self.output_text.delete(1.0, tk.END)

        target = self.target_entry.get()
        ports = self.ports_entry.get()

        if not target or not ports:
            self.output_text.insert(tk.END, "Please enter both target and port range.\n")
            return

        # Initialize the Nmap object
        try:
            nm = nmap.PortScanner()
            self.output_text.insert(tk.END, f"Initialized Nmap PortScanner.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Failed to initialize Nmap PortScanner: {e}\n")
            return

        try:
            # Perform the scan
            self.output_text.insert(tk.END, f"Scanning {target} on ports {ports}...\n\n")
            nm.scan(target, ports)
            self.output_text.insert(tk.END, f"Scan completed.\n")

            # Print results
            for host in nm.all_hosts():
                self.output_text.insert(tk.END, f"Host: {host} ({nm[host].hostname()})\n")
                self.output_text.insert(tk.END, f"State: {nm[host].state()}\n")
                for proto in nm[host].all_protocols():
                    self.output_text.insert(tk.END, f"Protocol: {proto}\n")
                    ports = nm[host][proto].keys()
                    for port in sorted(ports):
                        state = nm[host][proto][port]['state']
                        self.output_text.insert(tk.END, f"Port {port}: {state}\n")
                self.output_text.insert(tk.END, "\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred during the scan: {e}\n")

if __name__ == "__main__":
    app = NmapGUI()
    app.mainloop()
