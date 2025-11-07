"""Preset colour gradients for simplex noise visualization."""

# Advice on adding your own presets:
# 1. Copy one of the existing presets below.
# 2. Change the name and RGB values as desired.
# 3. Add the following line at the end of the file to include your preset:
#    preset_colours.update(preset_yourpresetname)
# 4. Save the file and run the main program. Your preset should now show up.


preset_colours = {}

preset_traffic = {"TRAFFIC LIGHTS":
                  [[255, 0, 0],
                  [255, 255, 0],
                  [0, 255, 0]]}

preset_rainbow = {"VIBRANT RAINBOW":
                  [[255, 0, 0],
                  [255, 255, 0],
                  [0, 255, 0],
                  [0, 255, 255],
                  [0, 0, 255],
                  [255, 0, 255]]}

preset_greyscale = {"GLOOMY GREYSCALE":
                    [[0, 0, 0],
                    [255, 255, 255]]}

preset_icy = {"ICE-COLD BLUES":
              [[0, 128, 255],
               [135, 0, 255],
              [255, 255, 255]]}

preset_hot = {"RED-HOT FIRE":
              [[255, 0, 0],
               [255, 170, 0],
               [255, 255, 0],
              [255, 255, 255]]}

# Add your own presets here!

# preset_template = {"PRESET NAME":
#                      [[R, G, B],
#                      [R, G, B],
#                      [R, G, B]]}

preset_colours.update(preset_traffic)
preset_colours.update(preset_rainbow)
preset_colours.update(preset_greyscale)
preset_colours.update(preset_icy)
preset_colours.update(preset_hot)
