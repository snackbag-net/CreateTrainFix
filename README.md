# CreateTrainFix

A temporary solution to fixing the Create Mod train crashes

## Installation

Python version: 3.12\
Clone the repository to wherever you want. Then execute `pip install -r requirements.txt` to install all requirements.

## How to use

Put the `create_tracks.dat` into the `input` folder. You can find the file in your server
under `world/data/create_tracks.dat`\
Run the `main.py` file\
You will be prompted to run a command. Enter `dimtrain minecraft:the_nether` and you will get a list of all trains in
the
nether, and you should also see that some trains are missing a graph.

**Example:**

```
Train {"text":"Unnamed Train"}, index 54 is missing a graph.
Train {"text":"Split off from: Unnamed Train"}, index 89 is missing a graph.
Train {"text":"Meme freight "}, index 100 is missing a graph.
Train {"text":"Lava Train [NatiM6]"}, index 105 is missing a graph.
```

Now you can go into the NBT file using VSCode (or any other preferred editor) with the NBT Explorer plugin and delete
those trains.

## Planned Features
- [ ] Command to reload NBT file
- [ ] Automatic train deletion