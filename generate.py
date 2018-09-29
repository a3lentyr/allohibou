import tempfile
import itertools as IT
import os
import random
import math

# mass
alpha = 1.0
beta = .001
k = 0.1
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
            Fij = 0.0
            if dij == 0.0:
                Fij = Coulomb_force(x[i], x[j])
            else:
                Fij = Hooke_force(x[i], x[j], dij)
            Fx += Fij[0]
            Fy += Fij[1]
        v[i][0] = (v[i][0] + alpha * Fx * delta_t) * eta
        v[i][1] = (v[i][1] + alpha * Fy * delta_t) * eta
        ekint[0] = ekint[0] + alpha * (v[i][0] * v[i][0])
        ekint[1] = ekint[1] + alpha * (v[i][1] * v[i][1])
        
    for i in xrange(m):
        x[i][0] += v[i][0] * delta_t
        x[i][1] += v[i][1] * delta_t
    return x,v

def create_random_links(m):
    d = []
    nrows = m
    ncols = m
    for i in xrange(nrows):
        dr = []
        for j in xrange( ncols):
            dr.append(.0)
        d.append(dr)
    
    for i in xrange(nrows):
        # count how many link already created
        links=sum(d[i])/0.3
        if links<3 and i<nrows-1:
            # create only links with latter nodes
            next_list = range(i+1,nrows)
            random.shuffle(next_list)
            links_count=links
            for j in next_list:
                links_next=sum(d[j])/0.3
                if(links_count<3 and links_next<3):
                    d[i][j]=.3
                    d[j][i]=.3
                    links_count+=1
        
     
    return d
    
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    
def score_link(x,d):
    count=0
    # make the list of segments
    segment=[]
    for i,pos in enumerate(x):
        for j,target in enumerate(d[i]):
            if target>0 and j>i:
                segment.append([pos,x[j]])
                
    for i,seg1 in enumerate(segment):
        for j,seg2 in enumerate(segment):
            if j>i and intersect(seg1[0],seg1[1],seg2[0],seg2[1]):
                count+=1
    
    return count
    
def find_best_links(x):
    m=len(x)
    best_d =[]
    best_score=1000
    
    for test in range(0,200):
        d = create_random_links(m)
        s = score_link(x,d)
        if best_score> s:
            best_d = d
            best_score = s

            
    return best_d,best_score
    
def get_places_coordinates(d):
    m=len(d)
    x = []
    v = []
    best_score=1000
    best_d = d
    for i in xrange(m):
        xi = [random.random(), random.random()]
        x.append(xi)
        v.append([0.0, 0.0])

    for i in range(0,200):
        x,v=forcedrawing(x,v,best_d)
        d_test,score = find_best_links(x)
        if score<best_score:
            best_d=d_test
            best_score=score
        print(best_score)
        
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
    
    # placing places
    d = create_random_links(len(places_list))
    places_coord,d = get_places_coordinates(d)
    
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
    # adding path
    for i,place_list in enumerate(d):
        for j,target in enumerate(place_list):
            if target>0:
                content_text+= '<line x1="'+str(trans_places[i][0])+'" y1="'+str(trans_places[i][1])+'" x2="'+str(trans_places[j][0])+'" y2="'+str(trans_places[j][1])+'" stroke="black" />'

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
