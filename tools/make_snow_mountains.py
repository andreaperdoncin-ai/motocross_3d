from PIL import Image
import os

def create_snow_mountains(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    width, height = img.size
    
    # We want to make the mountains look snowy.
    # We can desaturate, increase brightness, and tint slightly blue.
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            if a > 0:
                # Luminance
                lum = 0.299*r + 0.587*g + 0.114*b
                
                # Boost brightness for snow effect
                new_lum = min(255, lum * 1.5)
                
                # Tint slightly blue for ice/snow feel
                nr = int(new_lum * 0.9)
                ng = int(new_lum * 0.95)
                nb = int(min(255, new_lum * 1.1))
                
                pixels[x, y] = (nr, ng, nb, a)
                
    img.save(output_path)
    print(f"Saved: {output_path}")

current_dir = os.path.dirname(os.path.abspath(__file__))
input_img = os.path.join(current_dir, "assets", "bg_mountains.png")
output_img = os.path.join(current_dir, "assets", "bg_mountains_snow.png")
create_snow_mountains(input_img, output_img)
