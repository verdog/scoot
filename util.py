import math

GOAL_WIDTH = 1900
FIELD_LENGTH = 10280
FIELD_WIDTH = 8240

# Math utils

def sign(x):
    if x <= 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def clamp(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x

class Vector3:
    def __init__(self, data=[0, 0, 0]):
        self.data = data
    def __add__(self, value):
        return Vector3([self.data[0]+value.data[0],self.data[1]+value.data[1],self.data[2]+value.data[2]])
    def __sub__(self, value):
        return Vector3([self.data[0]-value.data[0],self.data[1]-value.data[1],self.data[2]-value.data[2]])
    def __mul__(self, value): # dot product
        return (self.data[0]*value.data[0] + self.data[1]*value.data[1] + self.data[2]*value.data[2])
    def normalize(self):
        if abs(self.data[0]) > abs(self.data[1]) and abs(self.data[0]) > abs(self.data[2]):
            self.data[1] /= abs(self.data[0])
            self.data[2] /= abs(self.data[0])
            self.data[0] = sign(self.data[0])
        elif abs(self.data[1]) > abs(self.data[0]) and abs(self.data[1]) > abs(self.data[2]):
            self.data[0] /= abs(self.data[1])
            self.data[2] /= abs(self.data[1])
            self.data[1] = sign(self.data[1])
        else:
            self.data[0] /= abs(self.data[2])
            self.data[1] /= abs(self.data[2])
            self.data[2] = sign(self.data[2])
        return self
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __str__(self):
        return str(self.data[0]) + ' ' + str(self.data[1]) + ' ' + str(self.data[2])

def rotation_to_matrix(rot):
    CR = math.cos(rot.roll)
    SR = math.sin(rot.roll)
    CP = math.cos(rot.pitch)
    SP = math.sin(rot.pitch)
    CY = math.cos(rot.yaw)
    SY = math.sin(rot.yaw)

    matrix = []
    matrix.append(Vector3([CP*CY, CP*SY, SP]))
    matrix.append(Vector3([CY*SP*SR-CR*SY, SY*SP*SR+CR*CY, -CP * SR]))
    matrix.append(Vector3([-CR*CY*SP-SR*SY, -CR*SY*SP+SR*CY, CP*CR]))
    return matrix

def target_to_local(location_origin, rotation_origin, location_target):
    ol = location_origin # origin location
    tl = location_target # target location
    vec3_origin = Vector3([ol.x, ol.y, ol.z])
    vec3_target = Vector3([tl.x, tl.y, tl.z])

    # gets the world coords of target and returns them local relative to origin
    matrix = rotation_to_matrix(rotation_origin)

    x = (vec3_target - vec3_origin) * matrix[0]
    y = (vec3_target - vec3_origin) * matrix[1]
    z = (vec3_target - vec3_origin) * matrix[2]
    return Vector3([x,y,z])