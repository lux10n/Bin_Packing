import random,itertools,math
def boltzmann(temp,old,new):
    try:
        return math.exp((old-new)/temp)
    except OverflowError:
        return float('inf')
def make_permutation(data_struct,bag1,bag2,receiver,candidate):
    haystack=data_struct.copy()
    tmp1=receiver+candidate
    item_to_permute=bag1.copy()
    for i in receiver:item_to_permute.remove(i)
    permuted_receiver=bag2.copy()
    for i in candidate:permuted_receiver.remove(i)
    new_bag1=tmp1
    tmp2=permuted_receiver+item_to_permute
    new_bag2=tmp2
    haystack[haystack.index(bag1)]=new_bag1
    haystack[haystack.index(bag2)]=new_bag2
    haystack=[i for i in haystack if i!=[]]
    return haystack
def get_score(bags):
    return len(bags)
def get_candidates(data_struct,maxcap):
    combinations=list()
    for bag in data_struct:
        if sum(bag)<maxcap:
            perms=[]
            for i in range(len(bag)):
                perms+=list(itertools.permutations(bag,i+1))
            for perm in perms:
                perm=list(perm)
                avail_space=maxcap-sum(perm)
                tmp=data_struct.copy()
                tmp.remove(bag)
                tmp=[i for i in tmp if sum(i)<maxcap]
                for other_bag in tmp:
                    if sum(other_bag)<maxcap:
                        candidate_l=[]
                        for i in range(len(other_bag)):
                            candidate_l+=list(itertools.permutations(other_bag,i+1))
                        for candidate in candidate_l:
                            candidate=list(candidate)
                            if sum(candidate)<=avail_space:
                                combination=make_permutation(data_struct,bag,other_bag,perm,candidate)
                                if all(sum(i)<=maxcap for i in combination):
                                    combinations.append(combination)
    combinations.sort()
    combinations=list(combinations for combinations,_ in itertools.groupby(combinations))
    return combinations
def get_index(item,data,mat_x):
    indexes=[]
    for i in range(len(data)):
        if item==data[i]:
            indexes.append(i)
    for u in indexes:
        if sum(mat_x[u])==0:
            item_index=u
            break
    return item_index
def random_pack(items,maxcap):
    random.shuffle(items)
    item_count=len(items)
    bags=[ [] for _ in range(item_count) ]
    mat_x=[ [ 0 for _ in range(item_count) ] for _ in range(item_count) ]
    mat_y=[ 0 for _ in range(item_count) ]
    to_pack=items.copy()
    while to_pack!=[]:
        item=random.choice(to_pack)
        item_index=get_index(item,items,mat_x)
        while True:
            bag_index=random.randint(0,len(bags)-1)
            if sum(bags[bag_index])+item<=maxcap:
                bags[bag_index].append(item)
                mat_x[item_index][bag_index]=1
                mat_y[bag_index]=1
                to_pack.remove(item)
                break
    bags=[i for i in bags if i!=[]]
    return bags
def get_min(combinations):
    best=combinations[0]
    for i in combinations:
        if get_score(i)<get_score(best):
            best=i
    return best
def bin_packing(data,maxcap):
    def generate_matrixes(bags,data):
        itemcount=len(data)
        bag_count=len(bags)
        mat_x=[ [0 for i in range(bag_count)] for _ in range(itemcount)]
        for bag_index in range(len(bags)):
            for item in bags[bag_index]:
                item_index=get_index(item,data,mat_x)
                mat_x[item_index][bag_index]=1
        mat_y=[1 for i in range(len(bags))]
        return mat_x,mat_y
    temp=len(data)*2+1
    epsilon=1
    base_conf=random_pack(data,maxcap)
    solution=base_conf
    while temp>0:
        nbh=get_candidates(solution,maxcap)
        if nbh==[]:break
        new_sol=random.choice(nbh)
        generated=random.uniform(0,1)
        if boltzmann(temp,get_score(solution),get_score(new_sol))>generated:
            solution=new_sol
        temp-=epsilon
        print('Taille de la solution optimale : {} sacs'.format(len(solution)))
    mat_x,mat_y=generate_matrixes(solution,data)
    return solution,mat_x,mat_y
if __name__=='__main__':
    data=[100,22,25,51,95,58,97,30,79,23,53,80,20,65,64,21,26,100,81,98,70,85,92,97,86,71,91,29,63,34,67,23,33,89,94,47,100,37,40,58,73,39,49,79,54,57,98,69,67,49,38,34,96,27,92,82,69,45,69,20,75,97,51,70,29,91,98,77,48,45,43,61,36,82,89,94,26,35,58,58,57,46,44,91,49,52,65,42,33,60,37,57,91,52,95,84,72,75,89,81,67,74,87,60,32,76,85,59,62,39,64,52,88,45,29,88,85,54,40,57]
    maxcap=150
    # data=[4,3,3,2,2,2]
    # maxcap=8
    print('BIN PACKING AVEC RECUIT SIMULE')
    bags,mat_x,mat_y=bin_packing(data,maxcap)
    print('Résultats :')
    print('Nombre de sacs : '+str(len(bags)))
    print('Poids moyen de chaque sac : '+str(round(sum([sum(i) for i in bags])/len(bags),2)))
    print('Pourcentage moyen de remplissage : {}%'.format(round(sum([sum(i) for i in bags])*100/len(bags)/maxcap,2)))