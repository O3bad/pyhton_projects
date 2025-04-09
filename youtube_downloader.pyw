import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import yt_dlp
import threading
from collections import defaultdict

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced YouTube Downloader")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TEntry', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Enhanced YouTube Downloader", 
            style='Title.TLabel'
        )
        self.title_label.pack(pady=(0, 15))
        
        # URL Entry Section
        self.url_frame = ttk.LabelFrame(self.main_frame, text="Video URL", padding=10)
        self.url_frame.pack(fill=tk.X, pady=5)
        
        self.url_entry = ttk.Entry(self.url_frame)
        self.url_entry.pack(fill=tk.X, padx=5, pady=5, expand=True)
        
        # Fetch Button
        self.fetch_button = ttk.Button(
            self.url_frame,
            text="Get Available Resolutions",
            command=self.fetch_resolutions_threaded
        )
        self.fetch_button.pack(pady=5)
        
        # Resolutions Display
        self.resolutions_frame = ttk.LabelFrame(self.main_frame, text="Available Resolutions", padding=10)
        self.resolutions_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.resolutions_text = scrolledtext.ScrolledText(
            self.resolutions_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.resolutions_text.pack(fill=tk.BOTH, expand=True)
        
        # Resolution Selection
        self.selection_frame = ttk.Frame(self.main_frame)
        self.selection_frame.pack(fill=tk.X, pady=10)
        
        self.resolution_label = ttk.Label(self.selection_frame, text="Select Resolution:")
        self.resolution_label.pack(side=tk.LEFT, padx=5)
        
        self.resolution_var = tk.StringVar()
        self.resolution_combobox = ttk.Combobox(
            self.selection_frame,
            textvariable=self.resolution_var,
            state='readonly',
            width=10
        )
        self.resolution_combobox.pack(side=tk.LEFT, padx=5)
        
        # Download Button
        self.download_button = ttk.Button(
            self.main_frame,
            text="Download Video",
            state=tk.DISABLED,
            command=self.download_threaded
        )
        self.download_button.pack(pady=10)
        
        # Progress/Status Area
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Download Status", padding=10)
        self.status_frame.pack(fill=tk.BOTH, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_text = tk.Text(
            self.status_frame,
            height=4,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 9)
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Initialize variables
        self.available_resolutions = {}
        self.url = ""
        
    def fetch_resolutions_threaded(self):
        self.url = self.url_entry.get().strip()
        if not self.url:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL")
            return
            
        # Disable controls during fetch
        self.toggle_controls(False)
        self.clear_resolutions()
        self.update_status("Fetching available resolutions...", clear=True)
        
        # Start in a separate thread
        threading.Thread(
            target=self.fetch_resolutions,
            daemon=True
        ).start()
    
    def fetch_resolutions(self):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
            resolutions = defaultdict(list)
            for fmt in info.get('formats', []):
                if fmt.get('height') and fmt.get('filesize'):
                    res = fmt['height']
                    size_mb = fmt['filesize'] / (1024 * 1024)
                    resolutions[res].append(size_mb)
            
            # Get average size for each resolution
            self.available_resolutions = {
                res: round(sum(sizes)/len(sizes), 2)
                for res, sizes in resolutions.items()
            }
            
            # Update UI
            self.root.after(0, self.display_resolutions)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch resolutions: {str(e)}"))
            self.root.after(0, self.update_status, f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.toggle_controls(True))
    
    def display_resolutions(self):
        self.resolutions_text.config(state=tk.NORMAL)
        self.resolutions_text.delete(1.0, tk.END)
        
        if not self.available_resolutions:
            self.resolutions_text.insert(tk.END, "No resolutions found for this video.")
            return
            
        sorted_res = sorted(self.available_resolutions.items(), key=lambda x: x[0], reverse=True)
        
        for res, size in sorted_res:
            self.resolutions_text.insert(tk.END, f"{res}p: {size} MB\n")
        
        self.resolutions_text.config(state=tk.DISABLED)
        
        # Update combobox
        self.resolution_combobox['values'] = [f"{res}p" for res in sorted(self.available_resolutions.keys(), reverse=True)]
        if self.resolution_combobox['values']:
            self.resolution_combobox.current(0)
            self.download_button.config(state=tk.NORMAL)
        
        self.update_status("Resolutions fetched successfully. Select a resolution and click Download.")
    
    def download_threaded(self):
        selected_res = self.resolution_var.get()
        if not selected_res or not selected_res[:-1].isdigit():
            messagebox.showwarning("Input Error", "Please select a valid resolution")
            return
            
        resolution = int(selected_res[:-1])
        
        # Disable controls during download
        self.toggle_controls(False)
        self.update_status(f"Starting download at {resolution}p...", clear=True)
        self.progress_var.set(0)
        
        # Start download in separate thread
        threading.Thread(
            target=self.download_video,
            args=(resolution,),
            daemon=True
        ).start()
    
    def download_video(self, resolution):
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [self.progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            self.root.after(0, lambda: self.update_status("Download completed successfully!"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {str(e)}"))
            self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.toggle_controls(True))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', "0%")
            try:
                percent_float = float(percent.strip('%'))
                self.root.after(0, lambda: self.progress_var.set(percent_float))
                
                status_msg = f"Downloading: {percent} complete\n"
                status_msg += f"Speed: {d.get('_speed_str', 'N/A')}\n"
                status_msg += f"ETA: {d.get('_eta_str', 'N/A')}"
                
                self.root.after(0, lambda: self.update_status(status_msg))
            except ValueError:
                pass
    
    def update_status(self, message, clear=False):
        self.status_text.config(state=tk.NORMAL)
        if clear:
            self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def clear_resolutions(self):
        self.resolutions_text.config(state=tk.NORMAL)
        self.resolutions_text.delete(1.0, tk.END)
        self.resolutions_text.config(state=tk.DISABLED)
        self.resolution_combobox.set('')
        self.download_button.config(state=tk.DISABLED)
    
    def toggle_controls(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        self.url_entry.config(state=state)
        self.fetch_button.config(state=state)
        self.resolution_combobox.config(state='readonly' if enable else tk.DISABLED)
        self.download_button.config(state=state if self.available_resolutions else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()