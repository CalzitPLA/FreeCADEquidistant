import math
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Polygon
import FreeCAD as App
import Draft, Part
import FreeCADGui


## Abstand a der Equidistante
#Variablen & Listen iniizieren
coord =[]
vertex_coordinates = []
p1=[]
equi_obj =[]
equi_list_sorted=[]
equi_list_sorted2=[]
vecs=[]

def run(selection_obj):
    pts=[]
    for obj in FreeCADGui.Selection.getSelection():
         for e in obj.Shape.Edges:
            ws=e.Curve
            pts += ws.discretize(4)
            #equi_list_sorted2.append((pts[0],ws[1],ws[2]))
    Draft.makeWire(pts, closed = True)
    for obj in pts:
      vecs.append(obj)
    vecs.append(vecs[0]) # to close the wire
    wire = Part.makePolygon(vecs)
    Part.show(wire)
    #Draft.make_sketch(wire, autoconstraints=True)
    return wire

#Equidistantenpunkte berechnen
def Equidistante(unique_list_inp,path):
  p1 =[]
  p_equi = []
  unique_list_tripple=[]
  e_real = np.array([ 0,0,0])
  count=-1
  i = len(unique_list_inp)
  for obj in unique_list_inp:
   count=+1
   unique_list_tripple.append((obj[0],obj[1],0))
  xy1 = np.asarray(unique_list_tripple[0])
  xy2 = np.asarray(unique_list_tripple[1])
  xy3 = np.asarray(unique_list_tripple[2])
  equi_list = []
  equid = 3 ## mm
#### Berechnen über Parallelogram
  
           #################
          #               #
         #               #
        #               #
       #################
        
  v21 = xy1 - xy2
  v23 = xy3 - xy2
  e_vec = v21 + v23
  dot_v = np.dot(v23,v21)
  betrag_v23 = np.sqrt(v23[0]*v23[0] + v23[1]*v23[1]+v23[2]*v23[2])
  betrag_v21 = np.sqrt(v21[0]*v21[0] + v21[1]*v21[1]+v21[2]*v21[2])
  cos_alpha_213 = dot_v / (np.absolute(betrag_v23) * np.absolute(betrag_v21))
  alpha_213 = np.arccos(round(cos_alpha_213, 6))/math.pi*180
  beta_213  = 180 - alpha_213
  ## error handling
  multiplic = 1
  if beta_213 == 0:
    v21 = np.asarray([v21[1], (-1) * v21[0] , 0. ])
    v23 = np.asarray([(-1) * v23[1],  v23[0] , 0. ])
    a_para = v21[1] * equid 
    a_para_check = v21[1] * equid * 0.1
    b_para = v21[0] * equid 
    b_para_check = v21[0] * equid * 0.1
    multiplic = (-1)
  else:
   a_para = equid / np.sin(beta_213/180 * (math.pi/2))
   a_para_check = 0.1 / np.sin(beta_213/180 * (math.pi/2))
  if alpha_213 == 0:
    multiplic = (-1)
    v21 = np.asarray([v21[1], (-1) * v21[0] , 0. ])
    v23 = np.asarray([(-1) *v23[1],  v23[0] , 0. ])
    a_para = v21[1] * equid
    a_para_check = v21[1] * equid * 0.1
    b_para = v21[0] * equid 
    b_para_check = v21[0] * equid * 0.1
  else:
   b_para = equid / np.sin(alpha_213/math.pi/2)
   b_para_check = 0.1 / np.sin(alpha_213/180 * (math.pi/2))
  a_vers= v21 / np.linalg.norm(v21) * np.absolute(a_para)
  a_vers_check= v21 / np.linalg.norm(v21) * np.absolute(a_para_check)
  b_vers= v23 / np.linalg.norm(v23) * np.absolute(a_para)
  b_vers_check= v23 / np.linalg.norm(v23) * np.absolute(a_para_check)
  p_equi_check = xy2 + a_vers_check + b_vers_check
  if insidecheck2([[p_equi_check[0],p_equi_check[1]]], path) == False:
    a_vers= -1 * a_vers
    b_vers= -1 * b_vers
    p_equi = xy2 + a_vers + b_vers
  ab_vers = a_vers + b_vers
  ab_vers/= np.linalg.norm(ab_vers)
  p_equi = xy2 + ab_vers * equid
  return p_equi, equid

#Wire aus Punktdatensatz erstellen
def equi_list_sorted2f(equi_list_sorted_c):
 equi_list_sorted2=[]
 for obj in equi_list_sorted_c:
  equi_list_sorted2.append((obj[0], obj[1], 0))
 vecs = ([FreeCAD.Vector(t) for t in equi_list_sorted2]) # convert tuples to vectors
 vecs.append(vecs[0]) # to close the wire
 wire = Part.makePolygon(vecs)
 Part.show(wire )
 return wire

def insidecheck2 ( points,path):
  a=0
  in_points = path.contains_points(points)
  if in_points.any() == False: #any()
    answer = False #path.contains_points(points)
    a=1
  return in_points

#Positioniere eingegebenes Objekt
def position(baseobj,New_Point,Rot_Vec,Rot_Angle):
 baseobj.Placement = App.Placement(New_Point,App.Rotation(Rot_Vec,Rot_Angle))
#Boundingbox berechnen
def calculate_bounding_box(path):
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for point in path:
        x = point[0]
        y = point[1]
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    return (min_x, max_x, min_y, max_y)

# Objekt der Form "Polygon >> Line >> Startpoint, Endpoint" zerlegen und sortieren
# Es ensteht eine Liste der Eckpunkte in aufsteigender Reihenfolge
def unique_coordinates (polygon3):
 for obj in polygon3:
  coord.append((obj.StartPoint.x, obj.StartPoint.y))
 return coord

##### Hauptscripte ######   
Gui.activeDocument().activeView().viewTop()
doc = App.ActiveDocument

start_point = FreeCADGui.Selection.getSelection()[0] 
selection_object2 = FreeCADGui.Selection.getSelection()[1]
base=[]
pts=run(selection_object2)
shape2 = selection_object2.Shape
bbox2 = shape2.BoundBox
center2 = bbox2.Center
translation2 = FreeCAD.Vector(-center2.x, -center2.y, -bbox2.ZMin)
selection_object2.Placement.Base = selection_object2.Placement.Base.add(translation2)
sketch = Draft.make_sketch(selection_object2, autoconstraints=True)
sk = Draft.make_sketch(selection_object2, autoconstraints=False)
################### geändert
Gui.Selection.addSelection('Intersection_tester','Wire')
selection_object3 = FreeCADGui.Selection.getSelection()[0]
sk2 = Draft.make_sketch(selection_object3, autoconstraints=False)
################### geändert

polygon = doc.Sketch001.Geometry
polygon2 = polygon
polygon3 = doc.Sketch002.Geometry #####geändert
unique_list = unique_coordinates(polygon3) 
point_count = len(unique_list)  #######
polygon = np.asmatrix(unique_list)
points = np.random.rand(100, 2)
path = Path(polygon)
path2 = Path(polygon)
i=0
while i < point_count-2:
 equi_obj.append(Equidistante((unique_list[i],unique_list[i+1],unique_list[i+2]),path)[0].tolist()) ########
 i = i+1
equid = Equidistante((unique_list[i-1],unique_list[i],unique_list[i+1]),path)[1]
wire = equi_list_sorted2f(equi_obj)
point_list=[]
doc = App.ActiveDocument 
p2 = App.Vector(1000, 500, 0)
Gui.Selection.clearSelection()
Gui.Selection.addSelection('Intersection_tester','Shape001')
base = FreeCADGui.Selection.getSelection()[0]
bbox = base.Shape.BoundBox
i=0
steps = 180
while i < (steps +1 ):
 x_a = (np.cos(i/(steps/2)*math.pi)*bbox.DiagonalLength*2)
 y_a = (np.sin(i/(steps/2)*math.pi)*bbox.DiagonalLength*2)
 #m_l= (x_a-start_point.Placement.Base.x)/(y_a-start_point.Placement.Base.y)
 p2 = App.Vector(x_a,y_a, 0)
 tool = Draft.make_line(start_point.Placement.Base, p2)
 FreeCAD.ActiveDocument.recompute()
 dist, points, geom = base.Shape.distToShape(tool.Shape)
###############
 lp= len(points) - 1
 point_holder_max=points[0][0]
 point_holder_min=points[0][0]
 if lp > 0:
  x_max=0
  x_min=1
  for line in points:
   x = (line[0].y -start_point.Placement.Base.y)/(y_a-start_point.Placement.Base.y)
   if x > x_max:# and x <= 1:
     x_max = x
     point_holder_max = line[0]
   if x < x_min:# and x >= 0:
     x_min = x
     point_holder_min = line[0]  
 if equid < 0:
  point_list.append(point_holder_max)############ geändert
 else:
  point_list.append(point_holder_min)
###################
 i += 1
spline1 = Draft.make_bspline(point_list, closed=False)
doc.recompute()
App.ActiveDocument.recompute()
