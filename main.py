from datetime import datetime, timedelta
import random
import re
from time import sleep
from sys import argv
from LSL import LSL
import tkinter as tk
from tkinter import font
from os import path, makedirs
from PIL import Image, ImageTk
import config


class Test:
  FW = "forward"
  BW = "backward"
  RT = "right"
  LF = "left"

test_desc = {
  Test.FW: "assets/Up.png",
  Test.BW: "assets/Down.png",
  Test.RT: "assets/Right.png",
  Test.LF: "assets/Left.png",
}


def main():
  try: 
    if argv[1] == "-h" or argv[1] == "--help":
      print("\tusage: uv run main.py <participant name> <trial #> <# of mins>")
  except: pass

  try: participant_name = argv[1]
  except:
    participant_name = input("Enter the participant name (e.g. John Doe): ") or "Participant"
    participant_name = ' '.join(word[0].upper() + word[1:].lower() if len(word) > 0 else word for word in participant_name.split())
    participant_name = re.sub(re.compile(r" "), "_", participant_name)
    participant_name = re.sub(re.compile(r"[^a-zA-Z0-9_]"), "", participant_name)

  try: trial_num = int(argv[2])
  except: trial_num = int(input("Enter the trial number (e.g. 1): "))

  try: mins = int(argv[3])
  except: mins = int(input("Enter the number of minutes you are planning on collecting data: "))

  test_data_path = path.join(config.SAVED_DATA_PATH, participant_name, f"trial{str(trial_num).zfill(2)}.csv")
  makedirs(path.dirname(test_data_path), exist_ok=True)

  print(f"Participant: {participant_name}, Trial: {trial_num}, Duration: {mins} minutes")
  print(f"Data will be saved to: {test_data_path}\n")

  start = datetime.now()
  end = start + timedelta(minutes=mins)

  LSL.init_lsl_stream()
  window = create_fullscreen_window("NXT Data Collector")
  LSL.start_collection()

  # Sleep for five seconds to gather some rest data
  window[0].update()
  sleep(5)

  last_test_name = None
  while datetime.now() < end:
    shuffled_items = list(test_desc.items())
    random.shuffle(shuffled_items)
    shuffled = dict(shuffled_items)

    if last_test_name == shuffled_items[0][0]:
      while last_test_name == shuffled_items[0][0]:
        random.shuffle(shuffled_items)
        shuffled = dict(shuffled_items)

    for name, img_path in shuffled.items():
      print("Collecting data for: " + name)
      LSL.start_label(name)
      add_image_to_window(window[1], img_path)
      window[0].update()
      sleep(10)

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
  root.update()
  return (root, canvas)


def add_image_to_window(canvas: tk.Canvas, img_path: str):
  """
  Displays an image centered on the canvas. Replaces existing image if present.
  """
  canvas.delete("all")
  img = Image.open(img_path)
  img.thumbnail((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)
  photo = ImageTk.PhotoImage(img)
  canvas.image = photo
  canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=photo)
  return canvas



if __name__ == '__main__': main()
