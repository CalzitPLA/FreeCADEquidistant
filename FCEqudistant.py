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
equi_list_sorted=[]
equi_list_sorted2=[]
vecs=[]


def run(selection_obj):
    pts=[]
    for obj in FreeCADGui.Selection.getSelection():
         for e in obj.Shape.Edges:
            ws=e.Curve
            pts += ws.discretize(10)
            print(pts)
            #equi_list_sorted2.append((pts[0],ws[1],ws[2]))
    Draft.makeWire(pts)
    #print(equi_list_sorted2)
    for obj in pts:
      vecs.append(obj)
      print(obj)
    print(vecs)
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
  equid = 2 ## mm
#### Berechnen über Parallelogram
  
           #################
          #               #
         #               #
        #               #
       #################
        
  v21 = xy1 - xy2
  print(v21)
  print("v21")
  v23 = xy3 - xy2
  print(v23)
  print("v23")
  e_vec = v21 + v23
  dot_v = np.dot(v23,v21)
  print(dot_v)
  betrag_v23 = np.sqrt(v23[0]*v23[0] + v23[1]*v23[1]+v23[2]*v23[2])
  print(betrag_v23)
  betrag_v21 = np.sqrt(v21[0]*v21[0] + v21[1]*v21[1]+v21[2]*v21[2])
  print(betrag_v21)
  cos_alpha_213 = dot_v / (np.absolute(betrag_v23) * np.absolute(betrag_v21))
  print(cos_alpha_213)
  alpha_213 = np.arccos(cos_alpha_213)/math.pi*180
  beta_213  = 180 - alpha_213
  print(beta_213)
  print("beta")
  print(alpha_213)
  print("alpha")
  a_para = equid / np.sin(beta_213/180 * (math.pi/2))
  a_para_check = 0.1 / np.sin(beta_213/180 * (math.pi/2))
  print(a_para)
  print("a_para")
  b_para = equid / np.sin(alpha_213/math.pi/2)
  b_para_check = 0.1 / np.sin(alpha_213/180 * (math.pi/2))
  print(b_para)
  print("b_para")
  a_vers= v21 / np.linalg.norm(v21) * np.absolute(a_para)
  a_vers_check= v21 / np.linalg.norm(v21) * np.absolute(a_para_check)
  print("a")
  print(a_vers)
  b_vers= v23 / np.linalg.norm(v23) * np.absolute(a_para)
  b_vers_check= v23 / np.linalg.norm(v23) * np.absolute(a_para_check)
  print("b")
  print(b_vers)
  print(np.linalg.norm(a_vers))
  p_equi = xy2 + a_vers + b_vers
  p_equi_check = xy2 + a_vers_check + b_vers_check
  print((p_equi[0],p_equi[1]))
  if insidecheck2([[p_equi_check[0],p_equi_check[1]]], path) == False:
    a_vers= -1 * a_vers
    b_vers= -1 * b_vers
    p_equi = xy2 + a_vers + b_vers
  if equid < 0:
    p_equi = xy2 - a_vers - b_vers
  return p_equi

#Wire aus Punktdatensatz erstellen
def equi_list_sorted2f(equi_list_sorted_c):
 equi_list_sorted2=[]
 print(equi_list_sorted_c)
 for obj in equi_list_sorted_c:
  #print(obj)
  equi_list_sorted2.append((obj[0], obj[1], 0))
 vecs = ([FreeCAD.Vector(t) for t in equi_list_sorted2]) # convert tuples to vectors
 vecs.append(vecs[0]) # to close the wire
 wire = Part.makePolygon(vecs)
 Part.show(wire )
 return wire

def insidecheck2 ( points,path):
  a=0
  in_points = path.contains_points(points)
  #print(in_points)
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
 ### get unique coordinates
# Endpointx = []
# Endpointy = []
# Startpointx =[]
# Startpointy = []
# coord_leftover2 = [] 
# coord_leftover = []
# coord = []
# for obj in polygon3:
#  Endpointx = obj.StartPoint.x
#  Endpointy = obj.StartPoint.y
#  count= 0
#  break
# for obj in polygon3:
#  count+=1
#  coord_leftover2.append((obj.StartPoint.x, obj.StartPoint.y, obj.EndPoint.x , obj.EndPoint.y))
#  if count == 100000:
#   break
# count1= 0
# for objo in coord_leftover2:
#  count1+=1
#  if count1 == 100000:
#   break
#  # Schleife um Punkte aneinanderzureihen
#  # Bedingung Startpunkt_neu == Endpunkt_alt
#  # coord_leftover2 dient als Überlauf
#  count2= 0
#  for obj1 in coord_leftover2:
#   count2+=1
#   if count2 == 100000:
#    break
#   #Punkt hinzufügen, wenn nicht vorhanden
#   if obj1[0] == Endpointx and obj1[1] == Endpointy:
#          coord.append((obj1[0], obj1[1]))
#          Endpointx = obj1[2]
#          Endpointy = obj1[3]
#   #Aussortieren ob Punkt gedoppelt oder logisch nicht angehangen werden kann.  
#   else:
#          d = 0
#          for obj2 in coord:
#            if obj1[0]  == obj2[0] and obj1[1]  == obj2[1]:
#             d = 1
#          if d == 0:
#           coord_leftover.append((obj1[0], obj1[0])) 
#  coord_leftover2 = coord_leftover          
#  if len(coord_leftover) == 0:
#    break
 return coord

##### Hauptscripte ######   
Gui.activeDocument().activeView().viewTop()
doc = App.ActiveDocument 
selection_object2 = FreeCADGui.Selection.getSelection()[0]
pts=run(selection_object2)
#sk = Draft.make_sketch(pts, autoconstraints=True)
shape2 = selection_object2.Shape
bbox2 = shape2.BoundBox
center2 = bbox2.Center
translation2 = FreeCAD.Vector(-center2.x, -center2.y, -bbox2.ZMin)
selection_object2.Placement.Base = selection_object2.Placement.Base.add(translation2)
sketch = Draft.make_sketch(selection_object2, autoconstraints=True)
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection('Rectangle_tester','Shape001')
#FreeCADGui.runCommand('Draft_Draft2Sketch',0)
selection_object2 = FreeCADGui.Selection.getSelection()[0]
sk = Draft.make_sketch(selection_object2, autoconstraints=False)
polygon = doc.Sketch001.Geometry
polygon2 = polygon
polygon3 = polygon
unique_list = unique_coordinates(polygon3) 
point_count = len(unique_list)
polygon = np.asmatrix(unique_list)
points = np.random.rand(100, 2)
path = Path(polygon)
path2 = Path(polygon)
equi_obj =[]
i=0
while i < point_count-2:
 print(i) 
 print(unique_list[i+1])
 print("Equi:")
 print(Equidistante((unique_list[i],unique_list[i+1],unique_list[i+2]),path))
 equi_obj.append(Equidistante((unique_list[i],unique_list[i+1],unique_list[i+2]),path).tolist())
 i = i+1
equi_obj.append(Equidistante((unique_list[i],unique_list[i+1],unique_list[0]),path).tolist())
i = i+1
equi_obj.append(Equidistante((unique_list[i],unique_list[0],unique_list[1]),path).tolist())
wire = equi_list_sorted2f(equi_obj)
