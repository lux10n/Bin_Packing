import random,math
from collections import deque as fifoqueue
def neighborhood(val, ar):
    ind=ar.index(val)
    arlen=len(ar)
    inf,sup=ind-arlen//4,ind+arlen//4
    if inf<0 or sup>len(ar)-1:
        sup=sup-len(ar)
        nbh=ar[inf::]+ar[0:sup+1]
    else:
        nbh=ar[inf:sup+1]
    nbh.remove(val)
    return nbh
def get_max(ar):
    return max(ar)
def get_min(ar):
    return min(ar)
def put_in_bag(item,bags,maxcap):
    bag_index=0
    for i in range(len(bags)):
        if sum(bags[i])+item<=maxcap:
            bags[i].append(item)
            bag_index=i
            break
    return bag_index
def boltzmann(temp,old,new):
    try:
        return math.exp((old-new)/temp)
    except OverflowError:
        return float('inf')

def simple_descent(ar,opt_type='min'):
    visited_items=set()
    solution=random.choice(ar)
    s_sol=solution
    visited_items.add(solution)
    nbh=neighborhood(solution,ar)
    if nbh==[]:return solution
    if opt_type=='min':
        min_nbh=min(solution,get_min(nbh))
        for i in nbh:visited_items.add(i)
        while True:
            solution=min_nbh
            visited_items.add(min_nbh)
            nbh=neighborhood(solution,ar)
            if nbh==[]:break
            min_nbh=min(solution,get_min(nbh))
            for i in nbh:visited_items.add(i)
            if min_nbh==solution or len(visited_items)==len(set(ar)):
                break
        solution=min(solution,min_nbh)
    else:
        max_nbh=max(solution,get_max(nbh))
        for i in nbh:visited_items.add(i)
        while True:
            solution=max_nbh
            visited_items.add(max_nbh)
            nbh=neighborhood(solution,ar)
            if nbh==[]:break
            max_nbh=max(solution,get_max(nbh))
            for i in nbh:visited_items.add(i)
            if max_nbh==solution or len(visited_items)==len(set(ar)):
                break
        solution=max(solution,max_nbh)
    return solution
def tabu_search(data,opt_type='min'):
    itercount=1
    tabulist=fifoqueue([0]*4,maxlen=5)
    current_sol=random.choice(data)
    tabulist.appendleft(current_sol)
    best_sol=current_sol
    if opt_type=='min':
        while itercount<=5:
            nbh=neighborhood(current_sol,data)
            tmp=[]
            for i in nbh:
                if (i not in list(tabulist) or i == min(tabulist)):
                    tmp.append(i)
            nbh=tmp
            if nbh==[]:break
            min_nbh=get_min(nbh)
            current_sol=min_nbh
            tabulist.appendleft(current_sol)
            if current_sol<best_sol: 
                best_sol=current_sol
            itercount+=1
    else:
        while itercount<=5:
            nbh=neighborhood(current_sol,data)
            tmp=[]
            for i in nbh:
                if (i not in list(tabulist) or i == max(tabulist)):
                    tmp.append(i)
            nbh=tmp
            if nbh==[]:break
            max_nbh=get_max(nbh)
            current_sol=max_nbh
            tabulist.appendleft(current_sol)
            if current_sol>best_sol: 
                best_sol=current_sol
            itercount+=1
    return best_sol
def simulated_annealing(data,opt_type='min'):
    temp=len(data)*5+1
    epsilon=0.1
    best_sol=random.choice(data)
    if opt_type=='min':
        while temp>=0:
            nbh=neighborhood(best_sol,data)
            if nbh==[]:break
            new_sol=random.choice(nbh)
            generated=random.uniform(0,1)
            if boltzmann(temp,best_sol,new_sol)>generated:
                best_sol=new_sol
            temp-=epsilon
    else:
        while temp>=0:
            nbh=neighborhood(best_sol,data)
            if nbh==[]:break
            new_sol=random.choice(nbh)
            generated=random.uniform(0,1)
            if boltzmann(temp,best_sol,new_sol)<generated:
                best_sol=new_sol
            temp-=epsilon
    return best_sol
def bin_packing(items,search_max,maxcap):
    nbmax=len(items)
    bags=[[] for i in range (nbmax)]
    items_to_pack=items.copy()
    mat_x=[[0 for i in range(nbmax)] for i in range(nbmax)]
    mat_y=[0 for i in range(nbmax)]
    while items_to_pack!=[]:
        item_to_pack=search_max(items_to_pack,'max')
        item_index=items.index(item_to_pack)
        bag_index=put_in_bag(item_to_pack,bags,maxcap)
        mat_x[item_index][bag_index]=1
        mat_y[bag_index]=1
        items_to_pack.remove(item_to_pack)
    bags=[i for i in bags if i!=[]]
    return bags,mat_x,mat_y