
	
 
from PIL import ImageGrab
from pathlib import Path
from io import BytesIO
import win32clipboard
# import pyautogui   # import PyAutoGUI libr
import tkinter as tk  # import tkinter library


screen1size = (3840,2160)
screen2size = (1920,1080)    
save_folder = 'saved_images'

def get_next_filename():
    folder = Path(save_folder)
    folder.mkdir(exist_ok=True)
    files = list(folder.glob("*.png"))
    idx =  len(files)
    filename = f"{idx}.png"
    return folder/filename

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def crop_to_screen2(image):
    # left, upper, right, and lower pixel  
    sz = image.size
    image = image.crop((screen1size[0],0,sz[0],sz[1]))
    return image

def crop_to_video_location(image):
    sz = image.size
    shift_up = 70
    horizontal_squeeze = 320
    vertical_squeeze = 80
    left = screen1size[0]+horizontal_squeeze//2
    upper = sz[1]//3-shift_up+vertical_squeeze//2
    right =  screen1size[0]+3*screen2size[0]//4 -horizontal_squeeze//2
    lower = sz[1]*2//3-shift_up-vertical_squeeze//2
    bb = (left, upper, right , lower)
    print(bb)
    image = image.crop(bb)
    return image

def take_screen_shot():
    #  width, height    
    image = ImageGrab.grab( all_screens = True)
    image = crop_to_video_location(image)

    filename = get_next_filename()
    image.save(filename)
    print(f"Saved to {filename}")
    # print(image.size)
    
    output = BytesIO()
    image2 = image.convert("RGB")
    image2.save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)

 

# # define a method that will call whenever button will be clicked
# def take():
#     image = pyautogui.screenshot("tkscreen.png")
 


if __name__ == '__main__':
    # create main window
    window = tk.Tk()
    # create a button 
    shot_btn = tk.Button(window,text = "Take Screenshot", command= take_screen_shot)
    
    # place the button on the window
    shot_btn.place(x=50, y=50)
    window.mainloop()
 
  