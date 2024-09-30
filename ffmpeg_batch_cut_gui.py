import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font

from moviepy.editor import VideoFileClip

import utils
from ffmpeg_batch_cut import ffmpeg_batch_cut


# Custom class to redirect print output to the GUI
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to the latest log message

    def flush(self):  # Dummy flush method (for Python 3 compatibility)
        pass


class FFMpegBatchCutGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg Batch Cut GUI")

        # GUI elements
        tk.Label(root, text="Input File").grid(row=0, column=0, padx=5, pady=5)
        self.input_file_entry = tk.Entry(root, width=40)
        self.input_file_entry.grid(row=0, column=1, padx=5, pady=5)
        input_file_btn = tk.Button(root, text="Browse", command=self.select_input_file)
        input_file_btn.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Output File").grid(row=1, column=0, padx=5, pady=5)
        self.output_file_entry = tk.Entry(root, width=40)
        self.output_file_entry.grid(row=1, column=1, padx=5, pady=5)
        output_file_btn = tk.Button(root, text="Browse", command=self.select_output_file)
        output_file_btn.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="Mode").grid(row=2, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="Segments (HH:MM:SS)")
        mode_menu = tk.OptionMenu(root, self.mode_var, "Segments (HH:MM:SS)", "Segments (seconds)")
        mode_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Segments (space separated)").grid(row=3, column=0, padx=5, pady=5)
        self.segments_entry = tk.Entry(root, width=40)
        self.segments_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_btn = tk.Button(root, text="Submit", command=self.on_submit)
        submit_btn.grid(row=4, column=1, padx=5, pady=20)

        tk.Label(root, text="Logs").grid(row=5, column=0, padx=5, pady=5)
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.log_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Tags for colored logs
        self.log_text.tag_config('error', foreground="red")
        self.log_text.tag_config('info', foreground="green")

        help_btn = tk.Button(root, text="?", command=self.show_help)
        help_btn.grid(row=4, column=2, padx=5, pady=5)

        # Redirect stdout and stderr to the log window
        log_redirector = RedirectText(self.log_text)
        sys.stdout = log_redirector  # Redirect print statements to log_text
        sys.stderr = log_redirector  # Redirect error messages to log_text

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        self.input_file_entry.delete(0, tk.END)
        self.input_file_entry.insert(0, file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        self.output_file_entry.delete(0, tk.END)
        self.output_file_entry.insert(0, file_path)

    def on_submit(self):
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()
        segments = self.segments_entry.get()
        mode = self.mode_var.get()

        if not input_file or not segments:
            messagebox.showerror("Input Error", "Please fill all required fields")
            return

        self.log_text.insert(tk.END, "Processing...\n", "info")
        self.run_ffmpeg_batch_cut(input_file, segments, output_file, mode)

    def run_ffmpeg_batch_cut(self, input_file, segments, output_file, mode):
        try:
            clip = VideoFileClip(input_file)
            _ = int(clip.duration) + 1
            segments = segments.split(' ')
            if mode == "Segments (HH:MM:SS)":
                segments = utils.time_intervals_converter(segments)

            # in the other mode, time is already in seconds, so no conversion needed
            segments = [list(map(int, seg.split('-'))) for seg in segments]
            # Call the original function without modifying it
            ffmpeg_batch_cut(segments, input_file, output_file)
            self.log_text.insert(tk.END, "Process completed successfully.\n", "info")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error processing/reading video: {str(e)}\n", "error")

    def show_help(self):
        help_message = """
        This tool cuts videos based on input segments. First select the video file you want to cut using the "browse" file
        picker for the Input File. Then click on "browse" for Output File. In the popup window, select the folder and then
        type the name of the output file. Click on "save". The full input and output file paths will be displayed in the
        text fields. You could also directly copy paste the paths for these into the text fields.
        * Then provide undesired segments to cut out or remove from the input video file in the format '10-65 100-120' 
        or '0:10-1:05 1:40-2:00' (space-separated). The first format corresponds to the "Segments (seconds)" mode 
        selected in the "Mode" dropdown menu in the GUI. The second format corresponds to the "Segments (HH:MM:SS)" mode 
        selected in this dropdown element.
        """
        help_message = help_message.replace("\n", " ")
        help_message = help_message.replace("\t", " ")
        help_message = help_message.replace("*", "\n\n")
        help_message = re.sub(' +', ' ', help_message)

        messagebox.showinfo("Help", help_message)


def main():
    root = tk.Tk()
    FFMpegBatchCutGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
