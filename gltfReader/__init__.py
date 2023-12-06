import json
from dataclasses import dataclass
from typing import List
from base64 import b64decode
import numpy as np


@dataclass
class MeshPrimitive:
    attributes: object
    indices: int
    material: int
    mode: int
    targets: List[object]

@dataclass
class Mesh:
    primitives: List[MeshPrimitive]
    weights: List[float]
    name: str


class gltfReader:

    data: any = None

    def getComponentTypeStr(cp: int):
        if cp == 5120:
            return ("BYTE", "Int8Array", 8)
        elif cp == 5121:
            return ("UNSIGNED_BYTE", "Uint8Array", 8)
        elif cp == 5122:
            return ("SHORT", "Int16Array", 16)
        elif cp == 5123:
            return ("UNSIGNED_SHORT", "Uint16Array", 16)
        elif cp == 5125:
            return ("UNSIGNED_INT", "Uint32Array", 32)
        elif cp == 5126:
            return ("FLOAT", "Float32Array", 32)


    def __init__(self, filename: str):
        # Specify the path to your JSON file
        json_file_path = filename

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            self.data = json.load(file)

    # Populate asset details
    # asset = data["asset"]

    # currentScene = data["scene"]
    # scene = data["scenes"]

    def getBufferData(self, index: int) -> bytearray:
        """ This method returns buffer data for given index. """
        # TODO: Image logic needs to be implemented. At the moment this function return embded bytes array.

        tmpData: any
        if self.data["buffers"][index]["uri"][:4] == "data":
            tmpData = b64decode( str.split( self.data["buffers"][index]["uri"], "," )[1] )
            if len(tmpData) != self.data["buffers"][index]["byteLength"]:
                raise("Error: byteLength value not matching with extracted data")

        return tmpData

    # print( getBufferData(0) )

    def getBufferViewData(self, index: int) -> (str, bytearray):
        """ 
        This method returns a tuple for bufferView target and bufferView data for given index. 
        This takes byteOffset and byteLength into consideration.
        """
        bv = self.data["bufferViews"][index]
        bufData = gltfReader.getBufferData( self, bv["buffer"] )
        target = "ARRAY_BUFFER" if bv["target"] == 34962 else "ELEMENT_ARRAY_BUFFER"
        bufViewData = bufData[ bv["byteOffset"] : bv["byteLength"] + bv["byteOffset"] ]

        return target, bufViewData

    # print( getBufferViewData(2) )

    def getAccessorbyIndex(self, index: int):
        acc = self.data["accessors"][index]
        compType1, _componentType, compTypeSize = gltfReader.getComponentTypeStr( self.data["accessors"][index]["componentType"] )
        _type = self.data["accessors"][index]["type"]
        _count = self.data["accessors"][index]["count"]
        if "min" in acc:
            _min = acc["min"] 
        else:
            _min = None

        if "max" in acc:
            _max = acc["max"] 
        else:
            _max = None

        _target, _bufViewData = gltfReader.getBufferViewData(self, acc["bufferView"])

        return _target, _bufViewData, _componentType, _count, _type, _min, _max


    def getAccessorData(self, index: int):

        _target, _bufViewData, _componentType, _count, _type, _, _ = self.getAccessorbyIndex(index)
        # acc = self.data["accessors"][index]
        # _type = self.data["accessors"][index]["type"]
        # _count = self.data["accessors"][index]["count"]
        # compType1, _componentType, compTypeSize = gltfReader.getComponentTypeStr( self.data["accessors"][index]["componentType"] )
        # bufViewType, bufViewData = gltfReader.getBufferViewData(self, acc["bufferView"])

        return _target, _bufViewData, _componentType, _count, _type

    def getAccessorMinMax(self, index: int):
        _, _, _, _, _, _min, _max = self.getAccessorbyIndex(index)
        return _min, _max


    

    def getMeshData(self, index: int, primitive: int, attrib: str):
        attribList = ["POSITION","NORMAL","TEXCOORD_0","TANGENT"]
        # _meshes: List[Mesh] = []

        # _tmpMesh = Mesh()
        # _tmpMesh.name

        # _meshes.append(self.data["meshes"])

        if attrib in attribList:
            _position = self.data["meshes"][index]["primitives"][primitive]["attributes"]["POSITION"]
        _indices = self.data["meshes"][index]["primitives"][primitive]["indices"]
        # _mode = self.data["meshes"][index]["primitives"][primitive]["mode"]
            # _target1, _bufViewData1, _componentType1, _count1, _type1, _, _ = self.getAccessorbyIndex(_position)
            # _target2, _bufViewData2, _componentType2, _count2, _type2, _, _ = self.getAccessorbyIndex(_indices)
            
        return _position, _indices

    # print( getAccessorData(2) )
    # print( getAccessorData(3) )

