from gltfReader import *

gltfSrcfile: str = "assets/model/cone.gltf"
gltfdata = gltfReader(gltfSrcfile)


test = gltfdata.getBufferData(0)
test = gltfdata.getBufferViewData(1)
test = gltfdata.getMeshData(0, 0, "POSITION")

pass