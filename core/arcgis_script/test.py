# Import modules
import arcpy

# Set local variables
input_param = arcpy.GetParameterAsText(0)
try:
    # check if indata is in StatePlane, has no PRJ, or one other than StatePlane
    arcpy.AddMessage("input_param ====> " + input_param.lower())

except Exception as e:
    # arcpy.AddMessage("check param error: " + input_param)
    arcpy.AddMessage("fail: " + e[0])
