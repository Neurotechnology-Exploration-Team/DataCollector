import datetime
import random
import re
from time import sleep
from sys import argv
from LSL import LSL
import tkinter as tk
from tkinter import font
from os import path, makedirs
import config


class Test:
  FW = "forward"
  BW = "backward"
  RT = "right"
  LF = "left"

test_desc = {
  Test.FW: "Think about Floating forwards.",
  Test.BW: "Think about Floating backwards.",
  Test.RT: "Think about Floating to the right.",
  Test.LF: "Think about Floating to the left.",
}



def main():
  # Initialize streams & GUI
  LSL.init_lsl_stream()

  if argv[1] == "-h" or argv[1] == "--help":
    print("\tusage: uv run main.py <participant name> <trial #> <# of mins>")

  try: participant_name = argv[1]
  except:
    participant_name = input("Enter the participant name (e.g. John Doe): ")
    participant_name = ' '.join(word[0].upper() + word[1:].lower() if len(word) > 0 else word for word in participant_name.split())
    participant_name = re.sub(re.compile(r" "), "_", participant_name)
    participant_name = re.sub(re.compile(r"[^a-zA-Z0-9_]"), "", participant_name)

  try: trial_num = int(argv[2])
  except: trial_num = input("Enter the trial number (e.g. 1): ")

  try: mins = int(argv[3])
  except: mins = input("Enter the number of minutes you are planning on collecting data: ")

  test_data_path = path.join(config.SAVED_DATA_PATH, participant_name, f"trial{str(trial_num).zfill(2)}.csv")
  makedirs(path.dirname(test_data_path), exist_ok=True)

  print(f"Participant: {participant_name}, Trial: {trial_num}, Duration: {mins} minutes")
  print(f"Data will be saved to: {test_data_path}\n")

  start = datetime.now()
  end = start + datetime.timedelta(minutes=mins)

  window = create_fullscreen_window("NXT Data Collector")
  LSL.start_collection()

  # Sleep for five seconds to gather some rest data
  sleep(5)

  last_test_name = None
  while datetime.now() < end:
    shuffled_items = list(test_desc.items())
    random.shuffle(shuffled_items)
    shuffled = dict(shuffled_items)

    if last_test_name == shuffled[0][0]:
      while last_test_name == shuffled[0][0]:
        random.shuffle(shuffled_items)
        shuffled = dict(shuffled_items)

    for name, text in shuffled.items():
      print("Collecting data for: " + name + " Displaying Text:", text)
      LSL.start_label(name)
      add_text_to_window(window[1], text)
      sleep(15)

    last_test_name = name

  print("Data collection complete. Stopping collection and saving data.")
  LSL.stop_label()
  LSL.stop_collection(test_data_path)
  window[0].destroy()


def create_fullscreen_window(title: str):
  root = tk.Tk()
  root.title(title)
  root.title("NXT Data Collector")
  root.configure(bg='black')
  root.attributes('-fullscreen', True)

  screen_width = root.winfo_vrootwidth()
  screen_height = root.winfo_screenheight()

  root.geometry(f"{screen_width}x{screen_height}+{screen_width}+0")
  root.bind('<Escape>', lambda: root.destroy())

  canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black')
  canvas.pack(expand=True, fill=tk.BOTH)  # Add a black canvas to cover the entire window

  return (root, canvas)


def add_text_to_window(canvas: tk.Canvas, text: str, font_size: int = 40):
  """
  Places text in the middle of the window canvas with the specified font size. replaces text that is there already if it exists.
  """
  canvas.delete("all")  # Clear existing text
  custom_font = font.Font(family="Helvetica", size=font_size, weight="bold")
  canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2, text=text, fill="white", font=custom_font)
  return canvas



if __name__ == '__main__': main()
