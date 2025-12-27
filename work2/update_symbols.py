from PIL import Image

def update_symbols():
    # Load base symbols image
    base_path = '/Users/nakaneshunsuke/Desktop/antigarvity/work2/assets/symbols.png'
    try:
        base_img = Image.open(base_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: {base_path} not found.")
        return

    # Load new symbols
    # Artifact paths (I'll need to copy them to a temp loc or read direct if possible, 
    # but I must use absolute paths. The artifacts are in /Users/nakaneshunsuke/.gemini/antigravity/brain/...)
    # I will assume the agent system knows the path or I need to find them.
    # The previous tool output gave:
    # Red Fuji: /Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/red_fuji_symbol_1766449491277.png
    # Kabuto: /Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/kabuto_symbol_1766449506149.png
    
    red_fuji_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/red_fuji_symbol_1766449491277.png'
    kabuto_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/kabuto_symbol_1766449506149.png'

    red_fuji = Image.open(red_fuji_path).convert("RGBA")
    kabuto = Image.open(kabuto_path).convert("RGBA")

    # Target Size: 100x85 (Based on draw code: 100 width, 85 height destination, but source is also read as 100x85?)
    # Code: ctx.drawImage(img, 462, sym.id * 85, 100, 85, ...)
    # This means the SPRITE SHEET has them at x=462, y=id*85, w=100, h=85.
    
    target_size = (100, 85)
    red_fuji = red_fuji.resize(target_size)
    kabuto = kabuto.resize(target_size)

    # Paste Red Fuji (Replaces FUJIN, ID=1) -> y = 1 * 85 = 85
    # x = 462
    base_img.paste(red_fuji, (462, 85), red_fuji)

    # Paste Kabuto (Replaces RAIJIN, ID=2) -> y = 2 * 85 = 170
    # x = 462
    base_img.paste(kabuto, (462, 170), kabuto)

    # Save
    base_img.save(base_path)
    print("Successfully updated symbols.png")

if __name__ == "__main__":
    update_symbols()
