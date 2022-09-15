# Import modules
import arcpy

# Set local variables
input_param = arcpy.GetParameterAsText(0)
try:
    # check if indata is in StatePlane, has no PRJ, or one other than StatePlane
    if input_param.lower() == "true":
        # Set the Is Unknown parameter to FALSE, and the Is StatePlane parameter to TRUE
        arcpy.SetParameterAsText(1, "true")
        arcpy.SetParameterAsText(2, "false")
        arcpy.AddMessage("true")
    elif input_param.lower() == "false":
        # Set the Is Unknown parameter to TRUE, and the Is StatePlane parameter to FALSE
        arcpy.SetParameterAsText(1, "false")
        arcpy.SetParameterAsText(2, "true")
        arcpy.AddMessage("false")
    else:
        # Set the Is Unknown parameter to FALSE, and the Is StatePlane parameter to FALSE
        arcpy.SetParameterAsText(1, "false")
        arcpy.SetParameterAsText(2, "false")
        arcpy.AddMessage("check param fail")

except Exception as e:
    # arcpy.AddMessage("check param error: " + input_param)
    arcpy.AddMessage("check param error: " + e[0])
