from PIL import Image

def update_red_fuji_large():
    base_path = '/Users/nakaneshunsuke/Desktop/antigarvity/work2/assets/symbols.png'
    red_fuji_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/red_fuji_large_1766450522346.png'

    try:
        base_img = Image.open(base_path).convert("RGBA")
    except FileNotFoundError:
        print("Base image not found")
        return

    red_fuji = Image.open(red_fuji_path).convert("RGBA").resize((100, 85))

    # Paste Red Fuji (Replaces ID=1) -> y = 85
    base_img.paste(red_fuji, (462, 85))

    base_img.save(base_path)
    print("Successfully updated Red Fuji (Large) in symbols.png")

if __name__ == "__main__":
    update_red_fuji_large()
