import json
from dataclasses import dataclass
from typing import List
from base64 import b64decode
import numpy as np

class gltfIns:

    data: any = None

    @dataclass
    class Asset:
        copyright: str
        generator: str
        version: str
        minVersion: str
        # extensions: extension
        # extras: extras

    @dataclass
    class Scene:
        nodes: List[int]
        name: str
        # extensions: extension
        # extras: extras


    @dataclass
    class Buffer:
        index: int
        uri: str
        data: bytearray
        byteLength: int

        # def setData(self, uriS: str):
        #     if uriS[:4] == "data":
        #         data = b64decode(str.split(uriS, ",")[1])
        #         if len(data) != self.byteLength:
        #             raise("bytes size not matching")

    @dataclass
    class BufferView:
        index: int
        bufferIndex: int
        data: bytearray
        byteLength: int
        byteOffset: int
        target: str

    # def whatTarget(self):
    #     print(self.target)

    @dataclass
    class Accessor:
        index: int
        bufferView: int
        componentType: int
        componentTypeStr: str
        componentTypeBytes: int
        count: int
        type: str
        data: any

        def getdata(self):
            if self.componentTypeStr[1] == "Int8Array":
                return np.frombuffer( self.data, np.int8)
            if self.componentTypeStr[1] == "Uint8Array":
                return np.frombuffer( self.data, np.uint8)
            if self.componentTypeStr[1] == "Int16Array":
                return np.frombuffer( self.data, np.uint16)
            if self.componentTypeStr[1] == "Uint16Array":
                return np.frombuffer( self.data, np.uint16)
            if self.componentTypeStr[1] == "Uint32Array":
                return np.frombuffer( self.data, np.uint32)
            if self.componentTypeStr[1] == "Float32Array":
                return np.frombuffer( self.data, np.float32)


    @dataclass
    class Mesh:
        index: int
        name: str
        ARRAY_BUFFER: bytearray
        ELEMENT_ARRAY_BUFFER: bytearray


    asset: Asset
    scene: Scene
    buffers: List[Buffer] = []
    bufferViews: List[BufferView] = []
    accessors: List[Accessor] = []
    meshes: List[Mesh] = []



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

    def getBufferData(self, index: int):
        # for i, b in enumerate(data["buffers"]):
        bufferData = self.data["buffers"][index]["byteLength"]
        byteLength = self.data["buffers"][index]["byteLength"]

        tmpData: any
        if self.data["buffers"][index]["uri"][:4] == "data":
            tmpData = b64decode( str.split( self.data["buffers"][index]["uri"], "," )[1] )
            if len(tmpData) != self.data["buffers"][index]["byteLength"]:
                raise("bytes size not matching")

        return tmpData

    # print( getBufferData(0) )

    def getBufferViewData(self, index: int):
        bv = self.data["bufferViews"][index]
        bufData = gltfIns.getBufferData( self, bv["buffer"] )
        target = "ARRAY_BUFFER" if bv["target"] == 34962 else "ELEMENT_ARRAY_BUFFER"
        tmpBD = bufData[ bv["byteOffset"] : bv["byteLength"] + bv["byteOffset"] ]

        return target, tmpBD

    # print( getBufferViewData(2) )

    def getAccessorData(self, index: int):
        acc = self.data["accessors"][index]
        accType = self.data["accessors"][index]["type"]    
        compType1, compType2, compTypeSize = gltfIns.getComponentTypeStr( self.data["accessors"][index]["componentType"] )
        bufViewType, bufViewData = gltfIns.getBufferViewData(self, acc["bufferView"])

        return bufViewType, bufViewData, compType2, accType

    # print( getAccessorData(2) )
    # print( getAccessorData(3) )


    # def getMeshPosition(s: str, n: str, m: str):

    #     scn_i: int
    #     # scn_name: str
    #     node_l: List[int]
    #     node_i: int
    #     # node_name: str
    #     mesh_i: int
    #     # mesh_name: str

    #     for i,scn_l in enumerate(data["scenes"]):
    #         print(scn_l)
    #         if scn_l["name"] == s:
    #             node_l = scn_l["nodes"]
        
    #     for i, no in enumerate(node_l):
    #         print(node_l)
    #         for j, mi in enumerate(node_l):
    #             if data["nodes"][j]["name"] == n:
    #                 mesh_i = data["nodes"][j]["mesh"]
            
    #                 print(data["meshes"][mesh_i])
            
    # def getMeshPositionData(mesh_i):
    #     prim = None
    #     prim_pos_acc = data["meshes"][mesh_i]["primitives"][0]["attributes"]["POSITION"]
    #     prim_pos_ind_acc = data["meshes"][mesh_i]["primitives"][0]["indices"]
    #     # componentTypeStr = getComponentTypeStr(acc["componentType"]),
    #     # componentTypeBytes = getComponentTypeStr(acc["componentType"])[2],


    # getMeshPositionData(0)



    # getMeshPosition("Scene","Cube","")
    # pass


    # for i, b in enumerate(data["buffers"]):

    #     tmpData: any
    #     if b["uri"][:4] == "data":
    #         tmpData = b64decode(str.split(b["uri"], ",")[1])
    #         if len(tmpData) != b["byteLength"]:
    #             raise("bytes size not matching")

    #     tmpBuffer = Buffer(
    #     index = i,
    #     uri = b["uri"],
    #     data = tmpData,
    #     byteLength = b["byteLength"]
    #     )
    #     buffers.append(tmpBuffer)



    # # print(buffers[0].byteLength)

    # for i, bv in enumerate(data["bufferViews"]):
    #     tmpBV = BufferView(
    #         index = i,
    #         bufferIndex = bv["buffer"] ,
    #         byteLength = bv["byteLength"],
    #         byteOffset = bv["byteOffset"],
    #         target = "ARRAY_BUFFER" if bv["target"] == 34962 else "ELEMENT_ARRAY_BUFFER",
    #         data = buffers[bv["buffer"]].data[bv["byteOffset"] : bv["byteLength"] + bv["byteOffset"]]
    #     )
    #     bufferViews.append(tmpBV)



    # for i, acc in enumerate(data["accessors"]):
    #     tmpAcc = Accessor(
    #         index = i,
    #         bufferView = acc["bufferView"],
    #         componentType = acc["componentType"],
    #         componentTypeStr = getComponentTypeStr(acc["componentType"]),
    #         componentTypeBytes = getComponentTypeStr(acc["componentType"])[2],
    #         count = acc["count"],
    #         type = acc["type"],
    #         data = bufferViews[acc["bufferView"]].data,
    #     )
    #     accessors.append(tmpAcc)
 

    # for a in accessors:
    #     print(a.getdata())


