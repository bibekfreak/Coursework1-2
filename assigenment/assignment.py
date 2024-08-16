import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
import webbrowser

class WebCrawler:
    def __init__(self, url):
        self.url = url if url.startswith("http://") or url.startswith("https://") else "http://" + url

    def fetch_links(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            return [link.get('href') for link in links if link.get('href')]
        except requests.exceptions.RequestException as e:
            return str(e)

class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler")

        # URL input
        self.url_label = ttk.Label(root, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Crawl button
        self.crawl_button = ttk.Button(root, text="Crawl", command=self.start_crawl)
        self.crawl_button.grid(row=0, column=2, padx=10, pady=10)

        # Search input
        self.search_label = ttk.Label(root, text="Search:")
        self.search_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.search_entry = ttk.Entry(root, width=50)
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)
        self.search_button = ttk.Button(root, text="Search", command=self.search_links)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

        # Result display
        self.result_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.result_text.tag_configure("link", foreground="blue", underline=True)
        self.result_text.bind("<Button-1>", self.on_click)

        # Status bar
        self.status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        self.progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def start_crawl(self):
        self.result_text.delete(1.0, tk.END)
        self.status_bar.config(text="Crawling...")
        self.progress_bar.start()
        self.root.update_idletasks()
        url = self.url_entry.get()
        self.root.after(100, self.crawl, url)

    def crawl(self, url):
        crawler = WebCrawler(url)
        links = crawler.fetch_links()
        self.progress_bar.stop()
        self.status_bar.config(text="Ready")

        if isinstance(links, str):  # Error message
            self.result_text.insert(tk.END, f"Error: {links}")
        else:
            self.result_text.insert(tk.END, f"Found {len(links)} links:\n\n")
            self.links = links  # Store links for search
            for link in links:
                self.result_text.insert(tk.END, link + "\n", "link")

    def search_links(self):
        search_term = self.search_entry.get().lower()
        self.result_text.delete(1.0, tk.END)
        if hasattr(self, 'links'):
            filtered_links = [link for link in self.links if search_term in link.lower()]
            self.result_text.insert(tk.END, f"Found {len(filtered_links)} matching links:\n\n")
            for link in filtered_links:
                self.result_text.insert(tk.END, link + "\n", "link")

    def on_click(self, event):
        index = self.result_text.index("@%s,%s" % (event.x, event.y))
        tags = self.result_text.tag_names(index)
        if "link" in tags:
            clicked_link = self.result_text.get("insert linestart", "insert lineend").strip()
            webbrowser.open(clicked_link)

def main():
    root = tk.Tk()
    app = WebCrawlerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
