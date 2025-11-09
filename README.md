# KindleImagePreviewer

this is a tool to preview how images would look on a kindle, when you set a custom sleep screen with KOReader.
![Example ](/assets/preview.png)

![Example on kindle](/assets/yuyuko_example.webp)

# How to use:
https://youtu.be/uy50kZ9SN4c

1. find your kindle's resolution with the button at the top (scroll down to the table, look for ABCxDEF)
2. enter the resolution in the settings
3. click "select" and select your image
4. your image will be exported to `<CWD>/images/<IMAGE_NAME>_gray.png`

# How to apply the custom screensaver
1. (Skip to step N if you already have a background dir)
2. Open KOReader
3. Navigate to where your books are, then go up one of your kindle (Mine: `/mnt/us/`)
4. Top right -> Plus icon -> New Folder -> Enter name (i did `/mnt/us/bgs/`)
5. Exit KOReader
6. Plug in your kindle
7. Move `<CWD>/images/<IMAGE_NAME>_gray.png` to your backgrounds dir
8. Unplug kindle
9. Open KOReader
10. Open a book
11. Tap the top of the screen
12. Cog Wheel -> Screen -> Sleep screen -> Wallpaper
13. Turn on "Show custom image or cover on sleep screen" (or the random image)
14. Custom images -> Choose image or document cover -> Choose file
15. Long press your file -> Choose
16. Turn off your kindle :)

# Another example (for horizontal stuff)
![Example ](/assets/sunny_preview.png)

![Example on kindle](/assets/sunny_example.webp)
