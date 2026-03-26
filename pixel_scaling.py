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
        background.configure(bg="#2e2e44")
else:
    background.configure(bg="#2e2e44")

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

    path = filedialog.askopenfilename(title="Select Pixel-Art", filetypes=[("PNG Images", "*.png"),("All Files","*.png *.gif *.bmp")])
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

        show_preview(img)

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

        text = f"{w}x{h} ({i}x)"
        
        options.append(text)
    
    return options

def options_int(options: str) -> int:
        scaling_part = options.split("(")[1]
        i = scaling_part.replace("x)", "")
        return int(i)

def pixel_scaling(img: Image.Image, img_scale: int) -> Image.Image:
   
    new_width = img.width * img_scale
    new_height = img.height * img_scale
    scaled_img = img.resize((new_width, new_height), resample=Image.NEAREST)
    
    return scaled_img

def pixel_scaling_call():
    global img_path, img_og

    if img_og is None:
        messagebox.showwarning("Open an Image first! ʕ•ᴥ•ʔ")
        return
    
    options = drop_scaling.get()
    scaling = options_int(options)

    scaled_img = pixel_scaling(img_og, scaling)
    before_name = os.path.splitext(os.path.basename(img_path))[0]
    after_name = f"{before_name}_{scaling}x.png"
    save_file = filedialog.asksaveasfilename( title="Save Image...", initialfile=after_name, defaultextension=".png", filetypes=[("PNG","*.png")])

    if not save_file:
        return
    
    scaled_img.save(save_file, format="PNG")
    label_status.configure( text=f" Saved! ʕ^ᴥ^ʔ ", foreground="green")


def show_preview(img: Image.Image):
    preview_size = 256
    preview_scaling = preview_size // max(img.width, img.height)
    preview_scaling = max(preview_scaling, 1)
    img_preview = img.resize((img.width * preview_scaling, img.height * preview_scaling), resample=Image.NEAREST)
    show_img = ImageTk.PhotoImage(img_preview)

    preview.delete("all")
    preview.create_image( 
        preview_size // 2, preview_size // 2, 
        image=show_img, anchor="center")
    preview.tk_img = show_img


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

preview = tk.Canvas( mainframe, width=256, height=256, bg="#e0d6d6", borderwidth=1, relief="sunken")
preview.grid(row=2, column=0, columnspan=3, pady=(15,0))
preview.create_text(128, 128, text="Nothing Yet ʕ◉ᴥ◉ʔ", fill="#7A7979", font=("Arial", 13), justify="center")

b_frame = ttk.Frame(mainframe)
b_frame.grid(row=3, column=0, columnspan=3, pady=(15,0))
scale_button = ttk.Button(b_frame, text="Scale!", command=pixel_scaling_call)
scale_button.pack(side="left", padx=(0, 10))    
button_stat = ttk.Label(b_frame, text="Select your pixel-art.", foreground="gray")
button_stat.pack(side="left")

mainframe.columnconfigure(1, weight=1)

window.mainloop()