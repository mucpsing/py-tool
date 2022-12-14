# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# test2.py
# Created on: 2022-09-21 10:59:16.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: test2 <河道> <WORK_DB_PATH> <v03_10__af> <v03_10__be> <OUT_NAME> <平滑容差> <平滑算法> 
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code
import arceditor


# Import arcpy module
import arcpy

# Check out any necessary licenses
arcpy.CheckOutExtension("3D")

# Load required toolboxes
arcpy.ImportToolbox("C:/Users/Administrator/Documents/ArcGIS/CPS_test.tbx")

# Script arguments
河道 = arcpy.GetParameterAsText(0)
if 河道 == '#' or not 河道:
    河道 = "河道" # provide a default value if unspecified

WORK_DB_PATH = arcpy.GetParameterAsText(1)
if WORK_DB_PATH == '#' or not WORK_DB_PATH:
    WORK_DB_PATH = "C:\\Users\\Administrator\\Documents\\ArcGIS\\来宾至桂平2000吨级航道工程防洪评价.gdb" # provide a default value if unspecified

v03_10__af = arcpy.GetParameterAsText(2)
if v03_10__af == '#' or not v03_10__af:
    v03_10__af = "raw\\03_10%_af" # provide a default value if unspecified

v03_10__be = arcpy.GetParameterAsText(3)
if v03_10__be == '#' or not v03_10__be:
    v03_10__be = "raw\\03_10%_be" # provide a default value if unspecified

OUT_NAME = arcpy.GetParameterAsText(4)

平滑容差 = arcpy.GetParameterAsText(5)
if 平滑容差 == '#' or not 平滑容差:
    平滑容差 = "30 Meters" # provide a default value if unspecified

平滑算法 = arcpy.GetParameterAsText(6)
if 平滑算法 == '#' or not 平滑算法:
    平滑算法 = "PAEK" # provide a default value if unspecified

# Local variables:
v_OUT_NAME__sg_kir = WORK_DB_PATH
v_OUT_NAME__smooth = v_OUT_NAME__sg_kir

# Process: 02流速-插值后转栅格
arcpy.gp.toolbox = "C:/Users/Administrator/Documents/ArcGIS/CPS_test.tbx";
# Warning: the toolbox C:/Users/Administrator/Documents/ArcGIS/CPS_test.tbx DOES NOT have an alias. 
# Please assign this toolbox an alias to avoid tool name collisions
# And replace arcpy.gp.02插值后转栅格(...) with arcpy.02插值后转栅格_ALIAS(...)
arcpy.gp.02插值后转栅格(WORK_DB_PATH, OUT_NAME, v_OUT_NAME__sg_kir, v03_10__af, v03_10__be, "speed", "speed")

# Process: 03流速-输出等值线
arcpy.gp.toolbox = "C:/Users/Administrator/Documents/ArcGIS/CPS_test.tbx";
# Warning: the toolbox C:/Users/Administrator/Documents/ArcGIS/CPS_test.tbx DOES NOT have an alias. 
# Please assign this toolbox an alias to avoid tool name collisions
# And replace arcpy.gp.02删栏转等值线(...) with arcpy.02删栏转等值线_ALIAS(...)
arcpy.gp.02删栏转等值线(WORK_DB_PATH, v_OUT_NAME__sg_kir, OUT_NAME, 平滑算法, 平滑容差, "true", 河道, v_OUT_NAME__smooth)

