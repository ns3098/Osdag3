from pathlib import Path
import os
import errno
import sys
import yaml
from utils.common.component import Bolt, Plate, Weld
from Common import *
<<<<<<< HEAD
=======
import os
import xlsxwriter
import pandas as pd
from openpyxl import load_workbook, Workbook
>>>>>>> 20cd099a42cf82842b99557b6c77f2d8c1063845



############################ Pre-Build Database Updation/Creation #################
sqlpath = Path('ResourceFiles/Database/Intg_osdag.sql')
sqlitepath = Path('ResourceFiles/Database/Intg_osdag.sqlite')

if sqlpath.exists():
    if not sqlitepath.exists():
        cmd = 'sqlite3 ' + str(sqlitepath) + ' < ' + str(sqlpath)
        os.system(cmd)
        sqlpath.touch()
        print('Database Created')

    elif sqlitepath.stat().st_size == 0 or sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1:
        try:
            sqlitenewpath = Path('ResourceFiles/Database/Intg_osdag_new.sqlite')
            cmd = 'sqlite3 ' + str(sqlitenewpath) + ' < ' + str(sqlpath)
            error = os.system(cmd)
            print(error)
            # if error != 0:
            #      raise Exception('SQL to SQLite conversion error 1')
            # if sqlitenewpath.stat().st_size == 0:
            #      raise Exception('SQL to SQLite conversion error 2')
            os.remove(sqlitepath)
            sqlitenewpath.rename(sqlitepath)
            sqlpath.touch()
            print('Database Updated', sqlpath.stat().st_mtime, sqlitepath.stat().st_mtime)
        except Exception as e:
            sqlitenewpath.unlink()
            print('Error: ', e)
#########################################################################################






from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.seated_angle_connection import SeatedAngleConnection
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.base_plate_connection import BasePlateConnection

from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld

from design_type.tension_member.tension_bolted import Tension_bolted
from design_type.tension_member.tension_welded import Tension_welded
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.compression_member.compression import Compression



all_modules = {'Base Plate':BasePlateConnection, 'Beam Coverplate  Weld Connection':BeamCoverPlateWeld,'Beam Coverplate Connection':BeamCoverPlate,
    'Cleat Angle':CleatAngleConnection, 'Column Coverplate Weld Connection':ColumnCoverPlateWeld, 'Column Coverplate Connection':ColumnCoverPlate,
    'Column Endplate Connection':ColumnEndPlate, 'End Plate':EndPlateConnection, 'Fin Plate':FinPlateConnection,'Seated Angle': SeatedAngleConnection,
    'Tension Members Bolted Design':Tension_bolted, 'Tension Members Welded Design':Tension_welded, 'Compression Member':Compression,
    }

available_module = {'Fin Plate' : FinPlateConnection}


def make_sure_path_exists(path):      # Works on all OS.
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise



input_file_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example')

output_file_path = os.path.join(os.path.dirname(__file__), 'OUTPUT_FILES', 'Command_line_output')


make_sure_path_exists(output_file_path)   #make sure output folder exists if not then create.



osi_files = [file for file in os.listdir(input_file_path) if file.endswith(".osi")]

files_data = []   # list of tuples in which the first item will be file name and second item will be data of that file in dictionary format.

def precompute_data():

    for file in osi_files:

        in_file = input_file_path + '/' + file

        with open(in_file, 'r') as fileObject:

            uiObj = yaml.load(fileObject, yaml.Loader)

        files_data.append((file, uiObj))



def create_files():

    for file in files_data:

        data = file[1]
        module = data['Module']
        file_name = file[0].split(".")[0]
        file_name += ".txt"

        if module in available_module:

            main = available_module[module]
            main.set_osdaglogger(None)
            main.set_input_values(main, data)

            output_dict = main.results_to_test(main)

            path = os.path.join(output_file_path, file_name)

            with open(path, "w") as content:
                content.write(str(output_dict))



#Block print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


if __name__ == '__main__':

    blockPrint()

    precompute_data()

    create_files()
