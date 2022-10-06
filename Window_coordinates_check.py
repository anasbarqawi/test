# coding: utf-8


from pathlib import Path
import json
import csv
import ezdxf

import pandas as pd
import json


def read_csv_file(csv_file):
    '''
    reads the current data structure coming from dynamo
    creates a dictionary from it
    returns the dictionary
    :param csv_file:
    :return:
    '''
    data_d={}
    header_a=[]
    with open(csv_file, mode='r') as inp:
        reader = csv.reader(inp)
        for line in reader:
            line_data=[]
            for element in line:
                try:
                    line_data.append(float(element))
                except:
                    line_data.append(element)

            if len(header_a)>0:
                polygon_a=[[line_data[3],line_data[4],line_data[5]],
                           [line_data[6],line_data[7],line_data[8]],
                           [line_data[9], line_data[10], line_data[11]],
                           [line_data[12], line_data[13], line_data[14]],
                           [line_data[3], line_data[4], line_data[5]]
                           ]
                data_d[line_data[0]]={}
                data_d[line_data[0]]["Polygon"]=polygon_a
                for data_point in range(len(header_a)):
                    header_name=header_a[data_point]
                    data_d[line_data[0]][header_name]=line_data[data_point]
            else:
                header_a=line_data


    print (data_d)

    return data_d


def create_3dPolyLine_from_data(data_d,msp3d):
    '''
    Converts the Polygons into DXF entities on the modelspace

    :param data_d:
    :param msp3d:
    :return:
    '''

    for element in data_d.keys():
        print (data_d[element]["Polygon"])

        msp3d.add_polyline3d(data_d[element]["Polygon"],dxfattribs={"layer":"Target_surface"})
    return msp3d




csv_file_name="Phoenix_TS.csv"
data_d=read_csv_file(csv_file_name)


walls3d = ezdxf.new()
msp3d = walls3d.modelspace()
msp3d=create_3dPolyLine_from_data(data_d,msp3d)

walls3d.saveas("Target_Surfaces.dxf")
print("Anas")