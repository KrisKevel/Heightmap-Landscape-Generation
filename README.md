# Heightmap Landscape Generation

## Heightmap Generation
Run genereeri.py via "python3 genereeri.py" or enable execution of the file via "chmod +x genereeri.py" and launch it using "./genereeri.py" (Note: requires Python modules tkinter and pypng). In the newly opened GUI, modify desired values before clicking on "Create". The script will then produce a PNG-image that can be imported to UE4 in the next step, this generation may take a few minutes.


## Importing newly created heightmap into Unreal Engine project
Our project uses Unreal Engine version 4.26.0.

In the editor create a new level for the new landscape (File -> New Level). In the new level, select Landscape mode (Modes -> Landscape). On the left side, select Import from File and find the newly created heightmap from the file browser. Once selected, click import. To add our material to the new landscape, drag "AutoGroundMaterial_Inst" from the Materials folder to the selected landscape on the right. To add water (if it is needed), add the WaterSpawner from Blueprint folder to the level at coordinates (0,0,0). 

**Troubleshooting**
* In case material shows up black, proceed to Landscape -> Paint menu and under target layers create the layer info for each layer.
* If shadows look off (eg shadows is shape of a grid) rebuild the lightning (Build Options Menu -> Build Lightning Only).
