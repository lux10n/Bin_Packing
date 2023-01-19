import random,itertools,collections
def make_permutation(data_struct,bag1,bag2,receiver,candidate,maxcap):
    haystack=data_struct.copy()
    if sum(bag1)+sum(candidate)<=maxcap:
        tmp1=bag1+candidate
        tmp2=bag2.copy()
        for i in candidate:tmp2.remove(i)
        new_bag1=tmp1
        new_bag2=tmp2
        haystack[haystack.index(bag1)]=new_bag1
        haystack[haystack.index(bag2)]=new_bag2
        haystack=[i for i in haystack if i!=[]]
        # print('Original list : {}\nOperation : {} <=> {}\nResult : {} <=> {}\nFinal list : {}'.format(data_struct,receiver,candidate,new_bag1,new_bag2,haystack))
    else:
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
def generate_partitions(item):
    generated=[]
    base_list=[]
    for i in range(len(item)):
        perm=list(itertools.permutations(item,i+1))
        generated+=perm
    for elem in generated:
        elem=list(elem)
        if all([sum(elem) != sum(list(i)) for i in base_list]):
            base_list.append(elem)
    generated = base_list
    return generated
def get_score(bags,maxcap):
    not_filled_bags=len([i for i in bags if sum(i)<maxcap])
    bag_count=len(bags)
    return 2*bag_count+round(not_filled_bags/bag_count,4)
def get_candidates(data_struct,maxcap):
    combinations=list()
    for bag in data_struct:
        if sum(bag)<maxcap:
            perms=generate_partitions(bag)
            tmp=data_struct.copy()
            tmp.remove(bag)
            for perm in perms:
                perm=list(perm)
                avail_space=maxcap-sum(perm)
                for other_bag in tmp:
                    if sum(other_bag)<maxcap:
                        candidate_l=[list(i) for i in generate_partitions(other_bag) if sum(i)<=avail_space]
                        if candidate_l==[]:break
                        for candidate in candidate_l:
                            combination=make_permutation(data_struct,bag,other_bag,perm,candidate,maxcap)
                            if all(sum(i)<=maxcap for i in combination):
                                combinations.append(combination)
                            # if len(perm)==1:
                            #     print('Candidate for {} in bag {}: {}'.format(perm,data_struct.index(other_bag),candidate))
                            # print('Equiv combination : {} ({})'.format(combination,get_score(combination,maxcap)))
    # base_list=[]
    # for elem in combinations:
    #     if all([[all([sum(i) for i in elem])] for i in base_list]):
    #         base_list.append(elem)
    # combinations = base_list
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
def ffd_pack(items,maxcap):
    item_count=len(items)
    bags=[ [] for _ in range(item_count) ]
    mat_x=[ [ 0 for _ in range(item_count) ] for _ in range(item_count) ]
    mat_y=[ 0 for _ in range(item_count) ]
    to_pack=items.copy()
    while to_pack!=[]:
        item=max(to_pack)
        item_index=get_index(item,items,mat_x)
        for bag_index in range(len(bags)):
            if sum(bags[bag_index])+item<=maxcap:
                bags[bag_index].append(item)
                mat_x[item_index][bag_index]=1
                mat_y[bag_index]=1
                to_pack.remove(item)
                break
    bags=[i for i in bags if i!=[]]
    return bags
def get_min(combinations,maxcap):
    best=combinations[0]
    for i in combinations:
        if get_score(i,maxcap)<get_score(best,maxcap):
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
    itercount=1
    tabulist=collections.deque([100000000]*5,maxlen=5)
    base_conf=random_pack(data,maxcap)
    print('Config de départ : '+str(base_conf))
    tabulist.appendleft(get_score(base_conf,maxcap))
    solution=base_conf
    while itercount<100:
        nbh=get_candidates(solution,maxcap)
        # print('Solution : '+str(solution))
        # print('Voisinage : '+str(nbh))
        # print('Liste tabou : '+str(list(tabulist)))
        if solution in nbh:nbh.remove(solution)
        tmp=[]
        for item in nbh:
            i=get_score(item,maxcap)
            if (i not in list(tabulist) or i == min(tabulist)):
                tmp.append(item)
        nbh=tmp
        if nbh==[]:break
        min_nbh=get_min(nbh,maxcap)
        current_solution=min_nbh
        tabulist.appendleft(get_score(current_solution,maxcap))
        if get_score(current_solution,maxcap)<get_score(solution,maxcap): 
            solution=current_solution
        # print('Score de la solution optimale : {}'.format(get_score(solution,maxcap)))
        # print('Solution : '+str(solution))
        itercount+=1
    mat_x,mat_y=generate_matrixes(solution,data)
    return solution,mat_x,mat_y
if __name__=='__main__':
    data=[100,22,25,51,95,58,97,30,79,23,53,80,20,65,64,21,26,100,81,98,70,85,92,97,86,71,91,29,63,34,67,23,33,89,94,47,100,37,40,58,73,39,49,79,54,57,98,69,67,49,38,34,96,27,92,82,69,45,69,20,75,97,51,70,29,91,98,77,48,45,43,61,36,82,89,94,26,35,58,58,57,46,44,91,49,52,65,42,33,60,37,57,91,52,95,84,72,75,89,81,67,74,87,60,32,76,85,59,62,39,64,52,88,45,29,88,85,54,40,57]
    maxcap=150
    # data=[4,3,3,2,2,2]
    # maxcap=8
    print('BIN PACKING AVEC RECHERCHE TABOU')
    bags,mat_x,mat_y=bin_packing(data,maxcap)
    print('Résultats :')
    print(bags)
    print('Nombre de sacs : '+str(len(bags)))
    print('Nombre de sacs non remplis : '+str(len([i for i in bags if sum(i)<maxcap])))
    print('Score : '+str(get_score(bags,maxcap)))
    print('Poids moyen de chaque sac : '+str(round(sum([sum(i) for i in bags])/len(bags),2)))
    print('Pourcentage moyen de remplissage : {}%'.format(round(sum([sum(i) for i in bags])*100/len(bags)/maxcap,2)))