import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import sin
import pyrr
from PIL import Image
# from objData import objData
from gltfReader import *




gltfSrcfile: str = "assets/model/monkey.gltf"
gltfdata = gltfReader(gltfSrcfile)

# Create vertex and color array

# print( type(vertices) )

# vertices = gltfdata.getAccessorData(0)
# print(gltfdata.getAccessorData(0))
bufViewType, bufViewData, compType2, cnt, accType = gltfdata.getAccessorData(0)
# vertices = np.array(bufViewData, dtype = np.float32)
vertices = np.frombuffer(buffer = bufViewData, dtype = np.float32).copy()
# print( type(vertices) )

# Create new array for holding indices


# print( type(indices) )
# print(indices)
# indices = gltfdata.getAccessorData(1)
# print(gltfdata.getAccessorData(1))
bufViewType, bufViewData, compType2, cnt, accType = gltfdata.getAccessorData(1)
indices = np.frombuffer(buffer = bufViewData, dtype = np.int16).tolist()
indices = np.array(indices)

print(vertices)
print(type(vertices))
print(indices)
print(type(indices))


# vertices = [0.5,  0.5, -0.5,
#  0.5, -0.5, -0.5,
#  0.5,  0.5,  0.5,
#  0.5, -0.5,  0.5,
# -0.5,  0.5, -0.5,
# -0.5, -0.5, -0.5,
# -0.5,  0.5,  0.5,
# -0.5, -0.5,  0.5]
# indices =[5, 3, 1,
# 3, 8, 4,
# 8, 5, 6,
# 2, 8, 6,
# 2, 3, 4,
# 5, 2, 6,
# 5, 7, 3,
# 3, 7, 8,
# 8, 7, 5,
# 2, 4, 8,
# 2, 1, 3,
# 5, 1, 2]

# Below vertices and indices taken from "import_json_gltf.py"
# vertices = [ 
#   0.5, 0.5, -0.5,  0.5, -0.5, -0.5,
#   0.5, 0.5,  0.5,  0.5, -0.5,  0.5,
#  -0.5, 0.5, -0.5, -0.5, -0.5, -0.5,
#  -0.5, 0.5,  0.5, -0.5, -0.5,  0.5
# ]
# indices = [0, 4, 6, 0, 6, 2, 3, 2, 6, 3, 6, 7, 7, 6, 4, 7, 4, 5, 5, 1, 3, 5, 3, 7, 1, 0, 2, 1, 2, 3, 5, 4, 0, 5, 0, 1]

# Below vertices and indices taken from "gltfReader.py"
# vertices =[ 0.5, 0.5, -0.5,  0.5, -0.5, -0.5,
#   0.5, 0.5,  0.5,  0.5, -0.5,  0.5,
#  -0.5, 0.5, -0.5, -0.5, -0.5, -0.5,
#  -0.5, 0.5,  0.5, -0.5, -0.5,  0.5]
# indices = [0,4,6,0,6,2,3,2,6,3,6,7,7,6,4,7,4,5,5,1,3,5,3,7,1,0,2,1,2,3,5,4,0,5,0,1]

tmpvertices = vertices
tmpindices = indices
# Below vertices and indices taken from "gltfReader.py"
# vertices = [-1.0, 0.0, 1.0, 1.0, 0.0, 1.0, -1.0, 0.0, -1.0, 1.0, 0.0, -1.0]
# indices = [0,1,3,0,3,2]

print( np.array_equal(tmpvertices, np.array(vertices)) )
print( np.array_equal(tmpindices, np.array(indices)) )

print( (tmpvertices == vertices).all() )
print( (tmpindices == indices).all() )



global proj_mat




checkerTex = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 0.0, 0.0, 0.0]

## STEP 1
# Prepare vertex and fragment shader code

vertex_src = """
# version 330 core

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in vec2 a_texture;

out vec3 v_color;
out vec2 v_texture;

uniform mat4 model;
uniform mat4 projection;

void main(){
    gl_Position = projection * model * vec4(a_position, 1.0);
    v_color = a_color;
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330 core

in vec3 v_color;
in vec2 v_texture;
out vec4 out_color;

uniform sampler2D s_texture;

void main(){
    //out_color = vec4(v_color, 1.0);
    out_color = texture(s_texture, v_texture);
}
"""


# Initialise glfw module and raise exception if not able to do successfully.
if not glfw.init():
    raise Exception("Can't initialise GLFW.")

# Create the window object where OpenGL interaction will happen.
window  = glfw.create_window(800, 600, "OpenGL Test", None, None)

# If window creation is not successful raise exception.
if not window:
    glfw.terminate()
    raise Exception("Can't create window.")

# Below statement is optional. Its just to set window position on monitor.
glfw.set_window_pos(window, 400, 300)

# Define a function for window resize callback. Inside function set the viewport size to new one.
def window_resize(window, w, h):
    # glfw.set_window_size(window, w, h)
    proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h, 0.1 , 100 )
    glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)
    glViewport(0, 0, w, h)

# SPecify and set callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# Make this window the current context to handle OpenGL
# OpenGL commands need context to draw on screen.
###
### Call any OpenGL command only after successful creation of context
###
glfw.make_context_current(window)


# print("GL_VENDOR : " + str(glGetString(GL_VENDOR)))
# print("GL_RENDERER : " + str(glGetString(GL_RENDERER)))
# print("GL_VERSION : " + str(glGetString(GL_VERSION)))
# print("GL_SHADING_LANGUAGE_VERSION : " + str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
# print("GL_EXTENSIONS : " + str(glGetString(GL_EXTENSIONS)).replace(" ","\n") )


# Set screen clear color
glClearColor(0.5, 0.4, 0.6, 1)
glEnable(GL_DEPTH_TEST)


# convert python arrays to numpy arrays as OpenGL expects in this format
# vertices = np.array(vertices, dtype = np.float32)
# indices = np.array(indices, dtype = np.uint32)
checkerTex = np.array(checkerTex, dtype=np.uint8)

## STEP 2
# Compile both vertex and fragment shaders and create program
vs = compileShader(vertex_src,GL_VERTEX_SHADER)
fs = compileShader(fragment_src, GL_FRAGMENT_SHADER)
shader = compileProgram(vs, fs)
# shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER), validate = True)
glDeleteShader(vs)
glDeleteShader(fs)

# Specify to use the shader program for rendering.
glUseProgram(shader)


print(vertices)
print(type(vertices))
print(indices)
print(type(indices))
print(type(np.array(vertices)))
print(type(np.array(indices)))

## STEP 3
# Generate buffer objects name. In this case we generated 2 named buffer objects.
# one for vertices and another for color
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
# glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
if type(vertices) == np.ndarray:
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
else:
    glBufferData(GL_ARRAY_BUFFER, np.array(vertices).nbytes, np.array(vertices), GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
# glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
# glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
glEnableVertexAttribArray(0)
# glEnableVertexAttribArray(1)
# glEnableVertexAttribArray(2)

EDO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EDO)
if type(vertices) == np.ndarray:
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
else:
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array(indices).nbytes, np.array(indices), GL_STATIC_DRAW)


w,h = glfw.get_window_size(window)
print(w,h)
proj_mat = pyrr.matrix44.create_perspective_projection_matrix(45, w/h , 0.1 , 1000 )
trans_mat = pyrr.matrix44.create_from_translation(pyrr.vector3.create(0,0,-3))

model_loc = glGetUniformLocation(shader, "model")
projectoin_loc = glGetUniformLocation(shader, "projection")

glUniformMatrix4fv(projectoin_loc, 1, GL_FALSE, proj_mat)


tex = glGenTextures(2)
glBindTexture(GL_TEXTURE_2D, tex[0])
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

print( "GL_ACTIVE_TEXTURE", glGetInteger(GL_ACTIVE_TEXTURE) )
print( "GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS", glGetInteger(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS) )

text_ref = Image.open("assets/texture/orange.png")
text_data = text_ref.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_ref.width, text_ref.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, checkerTex)
glGenerateMipmap(GL_TEXTURE_2D)

# glActiveTexture(GL_TEXTURE0)
# tex_loc = glGetAttribLocation(shader, "a_texture")
# glEnableVertexAttribArray(tex_loc)
# glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 12, 0)


glBindTexture(GL_TEXTURE_2D, tex[1])
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

print( "GL_ACTIVE_TEXTURE", glGetInteger(GL_ACTIVE_TEXTURE) )
print( "GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS", glGetInteger(GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS) )

text_ref = Image.open("assets/texture/apple.jpg")
text_data = text_ref.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_ref.width, text_ref.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, checkerTex)
glGenerateMipmap(GL_TEXTURE_2D)

def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"OpenGL error: {err}")

# Start main eventloop for window
while not glfw.window_should_close(window):

    # Fetch all event
    glfw.poll_events()

    # Quit logic
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        # glDeleteTextures(2, tex)
        glDeleteTextures(len(tex), tex)
        glDeleteProgram(shader)
        print("VBO ", VBO, "EDO", EDO)
        # glBindBuffer(GL_ARRAY_BUFFER, 0)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # glDeleteBuffers(1, EDO)
        # glDeleteBuffers(1, VBO)
        glfw.terminate()
        exit(0)

    # Indication to refresh screen color. It'll use the color mentioned in glClearColor()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_x , rot_y)
    model = pyrr.matrix44.multiply(rotation , trans_mat)
    
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # Instruction to start drawing with data provided data in step 3
    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    check_gl_error()

    if glfw.get_key(window, glfw.KEY_LEFT):
        glRotate(0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex[0])
    if glfw.get_key(window, glfw.KEY_RIGHT):
        glRotate(-0.1, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, tex[1])
    
    # Swap buffers
    glfw.swap_buffers(window)



# Destroy the window
glfw.terminate()
    

