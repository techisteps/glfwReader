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

        # TODO add error handling for file reading
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



    def getMeshPrimitiveData(self, index: int, primitive: int, attrib: str):

        _prim = self.data["meshes"][index]["primitives"][primitive]
        _indices = self.getAccessorData(_prim["indices"])
        _vAttr = None

        # print(self.getAccessorData(_prim["indices"]))

        for k, v in enumerate(_prim["attributes"]):
            print(k , v)
            if v == attrib:
                _vAttr = self.getAccessorData(_prim["attributes"][v])

        if _vAttr != None:
            return _vAttr, _indices
        else:
            return None
        

    def bytes2nparray(self, d: any):
        # tmpdata = np.frombuffer( d[1] ).copy()
        _dtype = d[2]
        # if _dtype == "Int8Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.int8 ).copy(), dtype=np.int8)
        # elif _dtype == "Uint8Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.uint8 ).copy(), dtype=np.uint8)
        # elif _dtype == "Int16Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.int16 ).copy(), dtype=np.int16)
        # elif _dtype == "Uint16Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.uint16 ).copy(), dtype=np.uint16)
        # elif _dtype == "Uint32Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.uint32 ).copy(), dtype=np.uint32)
        # elif _dtype == "Float32Array":
        #     retData = np.array( np.frombuffer( d[1], dtype=np.float32 ).copy(), dtype=np.float32)

        if _dtype == "Int8Array":
            retData = np.frombuffer( d[1], dtype=np.int8 ).copy()
        elif _dtype == "Uint8Array":
            retData = np.frombuffer( d[1], dtype=np.uint8 ).copy()
        elif _dtype == "Int16Array":
            retData = np.frombuffer( d[1], dtype=np.int16 ).copy()
        elif _dtype == "Uint16Array":
            retData = np.frombuffer( d[1], dtype=np.uint16 ).copy()
        elif _dtype == "Uint32Array":
            retData = np.frombuffer( d[1], dtype=np.uint32 ).copy()
        elif _dtype == "Float32Array":
            retData = np.frombuffer( d[1], dtype=np.float32 ).copy()

        return retData

    def getMeshIndices(self, mesh_index: int, primitive_index: int):
        _i = self.data["meshes"][mesh_index]["primitives"][primitive_index]["indices"]
        _target, _bufViewData, _componentType, _count, _type, _, _ = self.getAccessorbyIndex(_i)

        indices = np.frombuffer(buffer = _bufViewData, dtype = np.uint16).tolist()
        indices = np.array(indices)

        return indices


    def getMeshPosition(self, mesh_index: int, primitive_index: int):
        _i = self.data["meshes"][mesh_index]["primitives"][primitive_index]["attributes"]["POSITION"]
        _target, _bufViewData, _componentType, _count, _type, _, _ = self.getAccessorbyIndex(_i)

        vertices = np.frombuffer(buffer = _bufViewData, dtype = np.float32).copy()

        return vertices



    def getMeshData(self, mesh_index: int, primitive_index: int):
        _prim = self.data["meshes"][mesh_index]["primitives"][primitive_index]
        _indices = self.getAccessorData(_prim["indices"])
        _indices = self.bytes2nparray(_indices)

        # _indices = np.frombuffer(buffer = self.getAccessorData(_prim["indices"]), dtype = np.int16).tolist()
        # _indices = np.array(_indices)

        _attr = _prim["attributes"]
        vPos = None
        vNor = None
        vTan = None
        vTex = None

        if "POSITION" in _attr.keys():
            vPos = self.getAccessorData(_attr["POSITION"])
        if "NORMAL" in _attr.keys():
            vNor = self.getAccessorData(_attr["NORMAL"])
        if "TANGENT" in _attr.keys():
            vTan = self.getAccessorData(_attr["TANGENT"])
        if "TEXCOORD_0" in _attr.keys():
            vTex = self.getAccessorData(_attr["TEXCOORD_0"])

        _pos = self.bytes2nparray(vPos) if vPos != None else None
        _nor = self.bytes2nparray(vNor) if vNor != None else None
        _tan = self.bytes2nparray(vTan) if vTan != None else None
        _tex0 = self.bytes2nparray(vTex) if vTex != None else None

        return _indices, _pos, _nor, _tan, _tex0



if __name__ == "__main__":

    gltfSrcfile: str = "assets/model/box.gltf"
    gltfdata = gltfReader(gltfSrcfile)

    vertex = gltfdata.getMeshPrimitiveData(0, 0, "POSITION")
    vertex = gltfdata.getMeshData(0, 0)
    pass












    

    # def getMeshData(self, index: int, primitive: int, attrib: str):
    # # def getMeshData(self, index: int, primitive: int):
    #     attribList = ["POSITION","NORMAL","TEXCOORD_0","TANGENT"]
    #     # _meshes: List[Mesh] = []
    #     vPos = None
    #     vNor = None
    #     vTan = None
    #     vTex = None
    #     # _tmpMesh = Mesh()
    #     # _tmpMesh.name

    #     # _meshes.append(self.data["meshes"])

    #     # if attrib in attribList:
    #     #     _position = self.data["meshes"][index]["primitives"][primitive]["attributes"]["POSITION"]
    #     # _indices = self.data["meshes"][index]["primitives"][primitive]["indices"]
    #     # # _mode = self.data["meshes"][index]["primitives"][primitive]["mode"]
    #     #     # _target1, _bufViewData1, _componentType1, _count1, _type1, _, _ = self.getAccessorbyIndex(_position)
    #     #     # _target2, _bufViewData2, _componentType2, _count2, _type2, _, _ = self.getAccessorbyIndex(_indices)

    #     tmpVert = []

    #     for k, v in enumerate(self.data["meshes"][index]["primitives"][primitive]["attributes"]):
    #         print(k , v)
    #         if v == "POSITION":
    #             vPos = self.data["meshes"][index]["primitives"][primitive]["attributes"][v]
    #         elif v == "NORMAL":
    #             vNor = self.data["meshes"][index]["primitives"][primitive]["attributes"][v]
    #         elif v == "TANGENT":
    #             vTan = self.data["meshes"][index]["primitives"][primitive]["attributes"][v]
    #         elif v == "TEXCOORD_0":
    #             vTex = self.data["meshes"][index]["primitives"][primitive]["attributes"][v]
    #         # tmpVert.append(self.data["meshes"][index]["primitives"][primitive]["attributes"][v])
        
    #     tmpVert

    #     print(tmpVert)
    #     for i in tmpVert:
    #         print(self.getAccessorData(i))
    #     print(self.getAccessorData(self.data["meshes"][index]["primitives"][primitive]["indices"]))
    #     #     _position = self.data["meshes"][index]["primitives"][primitive]["attributes"]["POSITION"]
    #     # _mode = self.data["meshes"][index]["primitives"][primitive]["mode"]
    #         # _target1, _bufViewData1, _componentType1, _count1, _type1, _, _ = self.getAccessorbyIndex(_position)
    #         # _target2, _bufViewData2, _componentType2, _count2, _type2, _, _ = self.getAccessorbyIndex(_indices)

    #     _indices = self.data["meshes"][index]["primitives"][primitive]["indices"]

    #     # return _position, _indices
    #     return _indices

    # # print( getAccessorData(2) )
    # # print( getAccessorData(3) )


