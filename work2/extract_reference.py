from PIL import Image

def extract_reference():
    base_path = '/Users/nakaneshunsuke/Desktop/antigarvity/work2/assets/symbols.png'
    try:
        base_img = Image.open(base_path).convert("RGBA")
    except FileNotFoundError:
        print("Base image not found")
        return

    # ID 10 ('10') is at index 10.
    # y = 10 * 85 = 850
    # x = 462
    # w = 100, h = 85
    
    ref_y = 10 * 85
    ref_x = 462
    
    slot_img = base_img.crop((ref_x, ref_y, ref_x + 100, ref_y + 85))
    
    # Save to artifacts dir for the agent to use
    output_path = '/Users/nakaneshunsuke/.gemini/antigravity/brain/02e669d3-3222-4292-b070-969b7627ec81/reference_slot.png'
    slot_img.save(output_path)
    print(f"Saved reference slot to {output_path}")

if __name__ == "__main__":
    extract_reference()
