# Meural Canvas
Programming using the meural api, raspberry pi and shortcuts for IOS.

`show_preview.py`
When connected to home network:
Say "meural preview"
You'll be asked which painter you want to see
Based on your input a search is done in `meural_favorites.csv` and an artwork is shown of which the authors name is closest to the name you gave (based on levenshtein distance)
The artwork is then shown for 30 seconds and output of the script is the chosen authors name

`update_favorites.py` will update the `meural_favorites.csv` file. Should be run every once in a while if new artworks have been uploaded to the meural canvas.
