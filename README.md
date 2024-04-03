# MTG Image Merger

This Python script takes in a list of MTG (Magic: The Gathering) card names along with counts of cards, sets, and collector numbers, and merges all the card images into one using Scryfall.

## Usage

1. Place your deck list inside a file named `cards.txt`.
2. Run the Python script.
3. The script will output an image in the same directory, containing merged images of all the cards in your deck.

## Instructions

### 1. Installing Dependencies

Before running the script, ensure you have Python installed on your system. You'll also need to install the necessary Python libraries. You can install them using pip:

```bash
pip install -r requirements.txt
```

### 2. Creating Your Deck List

Create a file named cards.txt and add your deck list in the following format:

```
Count Card Name (Set) CollectorNumber
Count Card Name (Set) CollectorNumber
...
```

Anything on the same line after the collector number will be ignored.

For example:

```
1 The Wise Mothman (PIP) 4
1 Agent Frank Horrigan (PIP) 89
1 Alpha Deathclaw (PIP) 91
1 Altar of the Brood (KTK) 216
...
```

### 3. Running the Script

Run the Python script:

```
python mtg_image_merger.py
```

### 4. Output

The script will generate an image file named merged_image.png in the same directory, containing merged images of all the cards in your deck.

Inside the script, you can change the variable at the top if you don't want multiple of the same image if there is more than one copy in the list.
