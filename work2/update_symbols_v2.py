from PIL import Image

def update_symbols_v2():
    base_path = '/Users/nakaneshunsuke/Desktop/antigarvity/work2/assets/symbols.png'
    red_fuji_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/final_red_fuji_1766449914069.png'
    kabuto_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/final_kabuto_1766449929322.png'

    try:
        base_img = Image.open(base_path).convert("RGBA")
    except FileNotFoundError:
        print("Base image not found")
        return

    # Resize to 100x85 if needed (DALL-E might return 1024x1024 or similar)
    red_fuji = Image.open(red_fuji_path).convert("RGBA").resize((100, 85))
    kabuto = Image.open(kabuto_path).convert("RGBA").resize((100, 85))

    # Paste Red Fuji (Replaces FUJIN, ID=1) -> y = 1 * 85 = 85
    base_img.paste(red_fuji, (462, 85))

    # Paste Kabuto (Replaces RAIJIN, ID=2) -> y = 2 * 85 = 170
    base_img.paste(kabuto, (462, 170))

    base_img.save(base_path)
    print("Successfully updated symbols.png using AI-matched backgrounds.")

if __name__ == "__main__":
    update_symbols_v2()
