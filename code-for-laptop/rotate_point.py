
# rotate point


import math as m

class Point:  
    x=0
    y=0
    
    def __init__(self, x,y):
        self.x=x
        self.y=y


def rotate_point(cx, cy, angle, p):
  s = m.sin(angle);
  c = m.cos(angle);

  #translate point back to origin:
  p.x -= cx;
  p.y -= cy;

  #rotate point
  xnew = p.x * c - p.y * s;
  ynew = p.x * s + p.y * c;

  #translate point back:
  p.x = xnew + cx;
  p.y = ynew + cy;
  return p;


def rotate_point2(cx, cy, angle, p):
    
    return Point(m.cos(angle) * (p.x - cx) - m.sin(angle) * (p.y - cy) + cx,\
                  m.sin(angle) * (p.x - cx) + m.cos(angle) * (p.y - cy) + cy)


# 2D clockwise theta degrees rotation of point (x, y) around point (a, b) 

theta = 90

pt = Point(10,0)

a=0
b=0

print(pt.x,pt.y)

angle = theta * m.pi/180.0   # want radians

rot_p = rotate_point2(a, b, angle, pt)

print(rot_p.x, rot_p.y)



