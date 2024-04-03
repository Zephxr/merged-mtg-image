import requests
import json
import os
from PIL import Image
import io
import math

REPEAT_CARDS_WITH_MULTIPLE_COPIES = True
COMPRESS_IMAGES = True
COMPRESSION_QUALITY = 75

def get_card_image(card_name, set_code=None, card_num=None):
    # Get the image of the card from scryfall, if set_code and card_num are provided, get the specific card and do not use fuzzy search or the card name
    url = "https://api.scryfall.com/cards/named"
    if set_code and card_num:
        url = f"https://api.scryfall.com/cards/{set_code.lower()}/{card_num.replace(' ', '')}"
    else:
        url += f"?fuzzy={card_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error getting card image for {card_name}")
        print(f"Link: {url}")
        print(f"Response: {response.text}")
        return None
    card_data = json.loads(response.text)
    if "image_uris" in card_data:
        image_url = card_data["image_uris"]["normal"]
    elif "card_faces" in card_data:
        front_image_url = card_data["card_faces"][0]["image_uris"]["normal"]
        back_image_url = card_data["card_faces"][1]["image_uris"]["normal"]
        front_image_response = requests.get(front_image_url)
        back_image_response = requests.get(back_image_url)
        if front_image_response.status_code != 200 or back_image_response.status_code != 200:
            print(f"Error getting card image for {card_name}")
            return None
        front_image = Image.open(io.BytesIO(front_image_response.content))
        back_image = Image.open(io.BytesIO(back_image_response.content))
        return front_image, back_image
    else:
        print(f"Error getting card image for {card_name}")
        # Write the response to a file to see what the error is
        with open("error_response.json", "w") as f:
            f.write(response.text)
            print(f"Error response written to error_response.json")
        return None
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        print(f"Error getting card image for {card_name}")
        return None
    image = Image.open(io.BytesIO(image_response.content))
    return image

def merge_images(initImages):
    images = []
    for image in initImages:
        if isinstance(image, tuple):
            images.append(image[0])
            images.append(image[1])
        else:
            images.append(image)
    num_images = len(images)
    grid_size = math.ceil(math.sqrt(num_images))
    num_rows = math.ceil(num_images / grid_size)
    widths, heights = zip(*((i.size if not isinstance(i, tuple) else i[0].size) for i in images))
    max_width = max(widths)
    max_height = max(heights)
    total_width = max_width * grid_size
    total_height = max_height * num_rows
    new_image = Image.new('RGB', (total_width, total_height))
    for i, image in enumerate(images):
        x_offset = (i % grid_size) * max_width
        y_offset = (i // grid_size) * max_height
        if isinstance(image, tuple):
            new_image.paste(image[0], (x_offset, y_offset))
            new_image.paste(image[1], (x_offset + image[0].size[0], y_offset))
        else:
            new_image.paste(image, (x_offset, y_offset))
    return new_image

def save_image(image):
    # Save the image to the current directory
    directory = os.getcwd()
    image.save(directory + '/merged_image.png')
    print(f"Image saved to {directory}/merged_image.png")

def parse_cards_string(cards_string):
    # Each card is in the format "count card_name (set_code) card_num optional_extra"
    # Each card is separated by a comma
    cards = []
    card_list = cards_string.split("\n")
    for card in card_list:
        # If the card is empty, skip it
        if not card.strip():
            continue
        cardparts = card.strip().split(" ")
        count = 1
        card_name = " ".join(cardparts)
        if cardparts[0].isdigit():
            count = int(cardparts[0])
            card_name = " ".join(cardparts[1:])
        set_code = None
        card_num = None
        if "(" in card_name and ")" in card_name:
            set_code = card_name[card_name.find("(") + 1:card_name.find(")")]
            # Grab everything after the set code RP
            after = card_name[card_name.find(")") + 2:]
            split = after.split(" ")
            if split:
                card_num = split[0]
            card_name = card_name[:card_name.find("(")].strip()
        if REPEAT_CARDS_WITH_MULTIPLE_COPIES:
            for _ in range(count):
                cards.append((card_name, set_code, card_num))
        else:
            cards.append((card_name, set_code, card_num))
    return cards

cards = []
# Read cards.txt to get the list of cards
cardsString = ""
with open("cards.txt", "r") as f:
    cardsString = f.read()

print("Working...")
if cardsString:
    cards = parse_cards_string(cardsString)
images = []
for card in cards:
    images.append(get_card_image(*card))
merged_image = merge_images(images)
save_image(merged_image)

if COMPRESS_IMAGES:
    print("Compressing image...")
    merged_image.save("merged_image_compressed.jpg", quality=COMPRESSION_QUALITY)
    print("Compressed image saved to merged_image_compressed.jpg")