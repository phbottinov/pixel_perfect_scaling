import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Pixel Art Scaler")
width = 608
height = 496
window.geometry(f"{width}x{height}")
window.resizable(False, False)
background = tk.Canvas(window, width=width, height=height)
background.pack(fill="both", expand=True)

background_path = "background.png"
if os.path.exists(background_path):
    try:
        bg_img = Image.open(background_path)
        if bg_img.size != (width, height):
            bg_img = bg_img.resize(
                (width, height),
                resample=Image.NEAREST
            )
        bg_imagem_tk = ImageTk.PhotoImage(bg_img)
        background.create_image(0, 0, image=bg_imagem_tk, anchor="nw")
    except Exception:
        background.configure(bg="#2b2b3d")
else:
    background.configure(bg="#2b2b3d")

sizes = [8, 16, 32, 64]

scaling = {
    8:  [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 32],
    16: [2, 3, 4, 5, 6, 8, 10, 12, 16, 20],
    32: [2, 3, 4, 5, 6, 8, 10, 12, 16],
    64: [2, 3, 4, 5, 6, 8, 10],
}

img_path = None
img_og = None

def img_validation():
    global img_path, img_og

    path = filedialog.askopenfilename(title="Select Pixel-Art", filetypes=["*.png *.gif *.bmp"])
    if not path:
        return
    try:
        img = Image.open(path)
        width, height = img.size
    
        if width not in sizes or height not in sizes:
            messagebox.showerror(
                f"The image size of ({width}x{height}) is not supported!  ʕ◉ᴥ◉ʔ\n"
                f"Supported sizes: {sizes}\n"
            )
            return
        img_og = img
        img_path = path
        file_entry.configure(state="normal")
        file_entry.delete(0, tk.END)
        file_entry.insert(0, os.path.basename(path))
        file_entry.configure(state="readonly")

        label_info.configure(text=f"{width}x{height} ʕっ•ᴥ•ʔっ {img.mode}", foreground="black")

        options = drop_scaling_options(width, height)
        drop_scaling.configure(values=options)
        drop_scaling.set(options[2] if len(options) > 2 else options[0])
        label_status.configure(text="٠࣪⭑⊹ Image Loaded! ₊˚.")


    except:
        messagebox.showerror("ERROR: could not open the image!  ʕ◉ᴥ◉ʔ")

def drop_scaling_options(width: int, height: int) -> list[str]:

    lesser = min(width, height)
    mult = scaling.get(lesser, [2, 4, 8])
    
    options = []
    for i in mult:
        w = width * i
        h = height * i

        if w == h:
            text = f"{w}x{h} ({i}x)"
        else:
            text = f"{w}x{h} ({i}x)"
        
        options.append(text)
    
    return options

def pixel_scaling(img: Image.Image, img_scale: int) -> Image.Image:

    if not isinstance(img_scale, int) or img_scale < 2:
        raise ValueError("Scaling must be at least >= 2")
    
    new_width = img.width * img_scale
    new_height = img.height * img_scale
    scaled_img = img.resize(
        (new_width, new_height),
        resample=Image.NEAREST
    )
    
    return scaled_img

def final_img_name(starting_path: str, img_scale: int) -> str:
    name, extension = os.path.splitext(starting_path)
    return f"{name}_{img_scale}x{extension}"


def main():
    #Terminal-based
    args = sys.argv[1:]
    
    if len(args) < 2:
        print(__doc__)
        print("Usage: python pixel_scaling.py pixel_art.png 4")
        sys.exit(1)
    
    img_path = args[0]
    
    try:
        img_scale = int(args[1])
    except ValueError:
        print(f"'{args[1]}' is not a valid number to scale.")
        sys.exit(1)
    
    user_img_name = None
    if "-o" in args:
        i = args.index("-o")
        if i + 1 < len(args):
            user_img_name = args[i + 1]
        else:
            print("-o needs the full file name.")
            sys.exit(1)
    
    try:
        print(f"Opening: {img_path}")
        img = img_validation(img_path)

        print(f"\nScaling {img_scale}...")
        scaled_img = pixel_scaling(img, img_scale)
        
        if user_img_name is None:
            user_img_name = final_img_name(img_path, img_scale)
        
        scaled_img.save(user_img_name, format="PNG")

        print(f"Saved as: {user_img_name}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

mainframe = ttk.Frame(window, padding=20)
background.create_window(width // 2, height // 2, window=mainframe, anchor="center", width=512, height=400)

file_label = ttk.Label(mainframe, text="File:")
file_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

file_entry = ttk.Entry(mainframe, width=40, state="readonly")
file_entry.grid(row=0, column=1, sticky="we")

open_button = ttk.Button(mainframe, text="Open...", command=img_validation)
open_button.grid(row=0, column=2, padx=(10, 0))

label_scaling = ttk.Label(mainframe, text="Scaling:")
label_scaling.grid(row=1, column=0, sticky="w", pady=(10, 0), padx=(0, 10))

drop_scaling = ttk.Combobox(mainframe, values=["Nothing yet    ʕ-ᴥ-ʔ"], state="readonly", width=22)
drop_scaling.grid(row=1, column=1, sticky="w", pady=(10, 0))
drop_scaling.set("Open a Pixel-Art   •ᴥ•")

label_info = ttk.Label(mainframe, text="", foreground="gray")
label_info.grid(row=1, column=2, pady=(10, 0))

label_status = ttk.Label(text="Select an image to proceed.", foreground="gray")
label_status.pack(side="left")

window.mainloop()