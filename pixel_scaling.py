import sys
import os
from PIL import Image

sizes = [8, 16, 32, 64]

scaling = {
    8:  [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 32],
    16: [2, 3, 4, 5, 6, 8, 10, 12, 16, 20],
    32: [2, 3, 4, 5, 6, 8, 10, 12, 16],
    64: [2, 3, 4, 5, 6, 8, 10],
}


def img_validation(img_path: str) -> Image.Image:
    #Returns Image if the size is correctly in range (8 -> 64) or ValueError if it isn't
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"File not found: {img_path}")
    
    img = Image.open(img_path)
    width, height = img.size
    
    if width not in sizes or height not in sizes:
        raise ValueError(
            f"The image size of ({width}x{height}) is not supported.\n"
            f"Supported sizes: {sizes}\n"
        )
    return img

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
        print("Usage: python pixel_scaler.py pixel_art.png 4")
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

if __name__ == "__main__":
    main()