from PIL import Image

def fix_backgrounds():
    base_path = '/Users/nakaneshunsuke/Desktop/antigarvity/work2/assets/symbols.png'
    red_fuji_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/red_fuji_symbol_1766449491277.png'
    kabuto_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/kabuto_symbol_1766449506149.png'

    try:
        base_img = Image.open(base_path).convert("RGBA")
    except FileNotFoundError:
        print("Base image not found")
        return

    # 1. Create a Clean Background
    # We'll use ID 10 ('10') as a donor because low value symbols might be smaller/simplest?
    # Or ID 6 ('A'). Let's use ID 7 ('K') at index 7.
    # Slot 7: y = 7 * 85 = 595.
    # We grab a corner patch (e.g. 20x20) and tile it.
    
    donor_y = 7 * 85
    donor_x = 462
    
    # Crop a piece of background (Top Left corner of the slot)
    # Assuming symbol is centered and doesn't touch corners.
    bg_patch = base_img.crop((donor_x, donor_y, donor_x + 30, donor_y + 30))
    
    # Create a 100x85 background canvas
    clean_bg = Image.new("RGBA", (100, 85))
    
    # Tile the patch
    for x in range(0, 100, 30):
        for y in range(0, 85, 30):
            clean_bg.paste(bg_patch, (x, y))

    # 2. Prepare New Symbols
    red_fuji = Image.open(red_fuji_path).convert("RGBA").resize((100, 85))
    kabuto = Image.open(kabuto_path).convert("RGBA").resize((100, 85))

    # 3. Composite
    # Create final images for slot 1 and 2
    slot1_img = clean_bg.copy()
    slot1_img.paste(red_fuji, (0, 0), red_fuji) # Paste Red Fuji over clean BG

    slot2_img = clean_bg.copy()
    slot2_img.paste(kabuto, (0, 0), kabuto) # Paste Kabuto over clean BG

    # 4. Paste into Main Sprite Sheet
    # ID 1 (Fujin/Akafuji) -> y = 85
    # Important: Paste WITHOUT mask to Overwrite the messy previous state
    # We paste the fully opaque (bg + symbol) image.
    base_img.paste(slot1_img, (462, 85))

    # ID 2 (Raijin/Kabuto) -> y = 170
    base_img.paste(slot2_img, (462, 170))

    base_img.save(base_path)
    print("Fixed backgrounds and updated symbols.png")

if __name__ == "__main__":
    fix_backgrounds()
