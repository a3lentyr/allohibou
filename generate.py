import tempfile
import itertools as IT
import os
import random
import math
from math import sqrt

# mass
alpha = 1.0
beta = .002
k = 0.08
#damping
eta = .99
delta_t = .01

    
# force directed graph drawing
def Coulomb_force(xi, xj):
    dx = xj[0] - xi[0]
    dy = xj[1] - xi[1]
    ds2 = dx * dx + dy * dy
    ds = math.sqrt(ds2)
    ds3 = ds2 * ds
    if ds3 == 0.0:
        const = 0
    else:
        const = beta / (ds2 * ds)
    return [-const * dx, -const * dy]


def Hooke_force(xi, xj, dij):
    dx = xj[0] - xi[0]
    dy = xj[1] - xi[1]
    ds = math.sqrt(dx * dx + dy * dy)
    dl = ds - dij
    const = k * dl / ds
    return [const * dx, const * dy]
    
def forcedrawing(x,v,d):
    m=len(x)
    ekint = [0.0, 0.0]
    for i in xrange(m):
        Fx = 0.0
        Fy = 0.0
        for j in xrange(m):
            if j == 1:
                continue
            dij = d[i][j]
            FijH = [0.0,0.0]
            
            FijC = Coulomb_force(x[i], x[j])
            if dij != 0.0:
                FijH = Hooke_force(x[i], x[j], dij)
                
            Fx += FijC[0]+FijH[0]
            Fy += FijC[1]+FijH[1]
        v[i][0] = (v[i][0] + alpha * Fx * delta_t) * eta
        v[i][1] = (v[i][1] + alpha * Fy * delta_t) * eta
        ekint[0] = ekint[0] + alpha * (v[i][0] * v[i][0])
        ekint[1] = ekint[1] + alpha * (v[i][1] * v[i][1])
        
    for i in xrange(m):
        x[i][0] += v[i][0] * delta_t
        x[i][1] += v[i][1] * delta_t
    return x,v

    
def get_ordered_list(points, x_list, i):
   x=x_list[i][0]
   y=x_list[i][0]
   points.sort(key = lambda p: sqrt((x_list[p][0] - x)**2 + (x_list[p][1] - y)**2))
   return points

def create_multiple_link(nrows,x,i,d,segment,num_max=3):
    next_list = range(nrows)
    random.shuffle(next_list)
    next_list = get_ordered_list(next_list,x,i)
    
    links_count=sum(d[i])/0.3

    # finding links that can be allocated
    d,segment = create_single_link(d,segment,x,next_list,i,num_max)
                
    return d,segment
    
    
def create_single_link(d,segment,x,next_list,i,num_max=3):
    found_list=[]
    links_count=sum(d[i])/0.3
    if(links_count>=num_max):
        return d,segment
    
    # finding links that can be allocated
    for j in next_list:
        links_next=sum(d[j])/0.3
        if(i != j and links_next<num_max and d[i][j]<=0):
            inter=False
            for seg2 in segment:
                inter = inter or intersect(x[i],x[j],seg2[0],seg2[1])
                
            if not inter:
                found_list.append(j)
                
    # selecting closest link
    found_sorted=get_ordered_list(found_list, x, i)
   
    if len(found_sorted)>0:
        j=found_sorted[0]
        
        col=[0,0,0]
        for colindex in range(3):
            col[colindex]=sum([1 for c in d[i] if c==(0.3+colindex*0.01)]) +sum([1 for c in d[j] if c==(0.3+colindex*0.01)])
            
        indices = [colenum for colenum, colindex in enumerate(col) if colindex == min(col)]  
        random.shuffle(indices)
        color = indices[0]*0.01
        

        d[i][j]=.3+color # passing color info within d
        d[j][i]=d[i][j]
        segment.append([x[i] ,x[j]])
        next_list = get_ordered_list(next_list,x,j)
        d,segment=create_single_link(d,segment,x,next_list,j,num_max)
                
    return d,segment
    
   
# link creation and adjustment
def create_random_links(x,m):
    d = []
    nrows = m
    ncols = m
    for i in xrange(nrows):
        dr = []
        for j in xrange( ncols):
            dr.append(.0)
        d.append(dr)
    
    segment=[]
    
    # first we create a cycle
    cycle_list = range(nrows)
    random.shuffle(cycle_list)
    
    for i in cycle_list:
        d,segment = create_multiple_link(nrows,x,i,d,segment,2)
    cycle_list=list(reversed(cycle_list))
    
    # Then we complete the links            
    for i in cycle_list:
        d,segment = create_multiple_link(nrows,x,i,d,segment,4)
        
     
    return d
    
def onSegment(p, q, r):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])): 
       return True
  
    return False
  
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]) 
  
    if (val == 0):
        return 0
    
    if (val > 0):
        return 1
    return 2

  
def intersect(p1, q1, p2, q2):
    if (p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2):
        return False
        
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1)
  
    if (o1 != o2 and o3 != o4): 
        #print("intersect")
        return True 
  
    if (o1 == 0 and onSegment(p1, p2, q1)):
        return True 
  
    if (o2 == 0 and onSegment(p1, q2, q1)):
        return True 
  
    if (o3 == 0 and onSegment(p2, p1, q2)):
        return True 
  
    if (o4 == 0 and onSegment(p2, q1, q2)):
        return True 
  
    return False; 

    
    
def get_places_coordinates(m):
    x = []
    v = []
    
    # we generate a grid 4*4
    grid=[]

    for i in range(4):
        for j in range(4):
            grid.append([i/4.0,j/4.0])
                
    # count the number of links
    count_links=0
    count_single=0
    while count_links <20.9 or count_single>0:
    
        random.shuffle(grid)
                
        x = []
        v = []
            
        for i in xrange(m):
            xi = grid[i]
            x.append(xi)
            v.append([0.0, 0.0])
        
        best_d = create_random_links(x,m)
        count_links=sum([sum(d) for d in best_d])/0.6
        count_single=sum([1 for d in best_d if sum(d)/0.3<=1])
    
    # finish with a simple Forced based drawing
    
    for i in range(0,700):
        x,v=forcedrawing(x,v,best_d)
    
    
    return x,best_d
    
        
# return a unique file name
def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence 
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


def main():
    header = 'header.txt'
    header_file = open(header,'r')
    header_text = header_file.read()
    
    footer = 'footer.txt'
    footer_file = open(footer,'r')
    footer_text = footer_file.read()

    # forming list of places
    form_list=["triangle","carre","rond","losange"]
    color_list=["violet","orange","green"]
    
    places_list=[]
    for form in form_list:
        for color in color_list:
            places_list.append(form+"-"+color)
    
    data_dict={}
    
    for name in places_list:
        name_file = open(name+".svg",'r')
        name_text = name_file.read()
        data_dict[name]=name_text
        name_file.close()
        
    # forming list of marchandise    
    form_list_m=["triangle","triangle","triangle","carre","rond","losange","losange"]
    m_list=[]
    for form in form_list_m:
        for color in color_list:
            m_list.append(form+"-"+color+"-m")
    random.shuffle(form_list_m)
            
    data_dictm={}
    
    for name in m_list:
        name_file = open(name+".svg",'r')
        name_text = name_file.read()
        data_dictm[name]=name_text
        name_file.close()
    
    # placing places
    places_coord,d = get_places_coordinates(len(places_list))
    
    
    # -- rescale such that everything is in 30:270 and 30:230
    minx=min([x[0] for x in places_coord])
    maxx=max([x[0] for x in places_coord])
    miny=min([y[1] for y in places_coord])
    maxy=max([y[1] for y in places_coord])
    
    trans_places=[]
    for pair_coord in places_coord:
        x= int((pair_coord[0]-minx)*(270-30)/(maxx-minx)+30) #random.randint(30,270)
        y= int((pair_coord[1]-miny)*(250-30)/(maxy-miny)+30) #random.randint(30,230)
        trans_places.append([x,y])
        
    content_text=""
    m_index=0
    # adding path
    shortened_list=[]
    color_list=["red","blue","black"]
    for i,place_list in enumerate(d):
        for j,target in enumerate(place_list):
            if target>0 and j>i:
                # path between 4 and 4 are only drawn as half
                x1=trans_places[i][0]
                y1=trans_places[i][1]
                x2=trans_places[j][0]
                y2=trans_places[j][1]
                color=color_list[int((target-0.3)*100)]
                unique_color = (len([1 for c in d[i] if c==target]) <=1) # do not remove unique color
                unique_color = (unique_color or len([1 for c in d[j] if c==target])<=1)
                
                if sum(place_list)/0.3>3 and sum(d[j])/0.3>3 and i not in shortened_list and j not in shortened_list and not unique_color:
                    x2=(x1+x2)/2
                    y2=(y1+y2)/2
                    shortened_list.append(i)
                    shortened_list.append(j)
                content_text+= '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" stroke="'+color+'" />' 
                
                xm=(trans_places[i][0]+trans_places[j][0])/2
                ym=(trans_places[i][1]+trans_places[j][1])/2
                
                content_text+='<g transform="translate('+str(xm)+','+str(ym)+')">' 
                content_text+=data_dictm[m_list[m_index]]+'</g>' # m content
                m_index+=1                

    # Adding places
    
    for i,name in enumerate(places_list):
        x= trans_places[i][0]
        y= trans_places[i][1]
        content_text+='<g transform="translate('+str(x)+','+str(y)+')">' # placing it
        content_text+=data_dict[name]+'</g>' # content
        
    # Creating file
    new_path = uniquify('file.svg')
    new_file = open(new_path,'w')
    title = header_text+content_text+footer_text
    new_file.write(title)

    new_file.close()
    footer_file.close()
    header_file.close()
  
if __name__== "__main__":
  main()
