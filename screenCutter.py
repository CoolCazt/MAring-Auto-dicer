import os
import uuid
import tkinter as tk
from PIL import ImageGrab
from tkinter import messagebox
from screeninfo import get_monitors
from tkinter import filedialog

class ScreenCaptureApp:
    def __init__(self, root):
      self.root = root
      self.x = self.y = 0
      self.start_x = None
      self.start_y = None

      self.rect = None

      self.root.geometry('720x480')  # Set the window size
      self.root.title('Screen Capture')

      self.button = tk.Button(root, text='Capture', command=self.capture)
      self.button.place(relx=0.5, rely=0.5, anchor='center')

    def capture(self):
      if hasattr(self, 'screen'):
        self.screen.destroy()  # Destroy the old Toplevel window
      self.root.withdraw()  # Hide the main window
      self.root.after(100, self.start_capture)  # Start capturing after 100ms

    def start_capture(self):
      self.screen = tk.Toplevel(self.root)
      self.screen.attributes('-fullscreen', True)
      self.screen.attributes('-alpha', .3)
      self.canvas = tk.Canvas(self.screen)
      self.canvas.pack(fill="both", expand=True)
      self.canvas.bind('<ButtonPress-1>', self.on_button_press)
      self.canvas.bind('<B1-Motion>', self.on_move_press)
      self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
      self.start_x = event.x
      self.start_y = event.y

    def on_move_press(self, event):
      self.curX = event.x
      self.curY = event.y

      width, height = self.curX - self.start_x , self.curY - self.start_y

      if not self.rect:
          self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x + width, self.start_y + height, outline='red')
      else:
          self.canvas.coords(self.rect, self.start_x, self.start_y, self.start_x + width, self.start_y + height)

    def on_button_release(self, event):
      self.screen.withdraw()
      self.root.deiconify()  # Show the main window
      x1 = min(self.start_x, self.curX)
      y1 = min(self.start_y, self.curY)
      x2 = max(self.start_x, self.curX)
      y2 = max(self.start_y, self.curY)

      # Adjust for monitor resolution and position
      monitors = get_monitors()
      for m in monitors:
          if x1 >= m.x and x2 <= m.x + m.width and y1 >= m.y and y2 <= m.y + m.height:
              x1 -= m.x
              x2 -= m.x
              y1 -= m.y
              y2 -= m.y
              break

      self.root.after(100, self.capture_screenshot, x1, y1, x2, y2)
      self.rect = None  # Reset the rectangle

    def capture_screenshot(self, x1, y1, x2, y2):
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.save_screenshot(img)

    def save_screenshot(self, img):
        # Create a new Toplevel window
        self.save_window = tk.Toplevel(self.root)
        self.save_window.title('Select directory')
        self.save_window.geometry('720x480')

        # Increase the font size
        font_size = 20  # Change this value to adjust the font size

        # Create buttons for each directory
        dirs = ['negativeDice', 'negativeEffect', 'positiveDice', 'positiveEffect']
        for dir_name in dirs:
            button = tk.Button(self.save_window, text=dir_name, font=('TkDefaultFont', font_size),
                               command=lambda d=dir_name: self.save_to_directory(img, d))
            button.pack(padx=10, pady=30)  # Add padding around the button

    def save_to_directory(self, img, dir_name):
        # Generate a unique file name
        file_name = str(uuid.uuid4()) + '.png'
        file_path = os.path.join('.', 'imgs', dir_name, file_name)

        # Save the image
        img.save(file_path)

        # Close the save window
        self.save_window.destroy()

        messagebox.showinfo('Success', 'Image saved successfully')

root = tk.Tk()
root.geometry('3840x2160')
app = ScreenCaptureApp(root)
root.mainloop()