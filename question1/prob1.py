import math

class SegmentTreeNode:
    def __init__(self, v=0):
        self.sum = v
    def merge(self, left, right):
        if left is not None and right is not None:
            self.sum = left.sum + right.sum
        elif left is None and right is None:
            self.sum = 0
        elif left is None:
            self.sum = right.sum
        else:
            self.sum = left.sum

class SegmentTree:
    def __init__(self, a):
        n = len(a)
        power = math.ceil(math.log(n, 2))
        total = 2 ** (power + 1)
        self.__tree = [None] * int(total)
        self.__leaf_length = int(total/2)-1
        self.__build(1, 0, self.__leaf_length, a)

    def __build(self, node, l, r, a):
        if l == r:
            self.__tree[node] = SegmentTreeNode()
            try:
                self.__tree[node].sum = a[l]
            except IndexError:
                self.__tree[node].sum = 0
            return
        leftchild = 2 * node
        rightchild = leftchild + 1
        mid = (l + r) // 2
        self.__build(leftchild, l, mid, a)
        self.__build(rightchild, mid + 1, r, a)
        self.__tree[node] = SegmentTreeNode()
        l = self.__tree[leftchild]
        r = self.__tree[rightchild]
        self.__tree[node].merge(l, r)

    def __query(self, node, l, r, i, j):
        if l >= i and r <= j:
            return self.__tree[node]
        elif j < l or i > r:
            return None
        else:
            leftchild = 2 * node
            rightchild = leftchild + 1
            mid = (l + r) // 2
            l = self.__query(leftchild, l, mid, i, j)
            r = self.__query(rightchild, mid + 1, r, i, j)
            if l is not None and r is not None:
                return SegmentTreeNode(l.sum+r.sum)
            elif l is None and r is None:
                return SegmentTreeNode(0)
            elif l is None:
                return SegmentTreeNode(r.sum)
            else:
                return SegmentTreeNode(l.sum)

    def query(self, i, j): 
        return self.__query(1, 0, self.__leaf_length, i, j)

class MaxSegmentTreeNode:
    def __init__(self, v=[]):
        self.max = v
    def merge(self, left, right, k):
        if left is not None and right is not None:
            self.max = sorted(left.max + right.max)[-k:]
        elif left is None and right is None:
            self.max = []
        elif left is None:
            self.max = right.max
        else:
            self.max = left.max

class MaxSegmentTree:
    def __init__(self, a, k):
        n = len(a)
        power = math.ceil(math.log(n, 2))
        total = 2 ** (power + 1)
        self.__tree = [None] * int(total)
        self.__leaf_length = int(total/2)-1
        self.__build(1, 0, self.__leaf_length, a, k)

    def __build(self, node, l, r, a, k):
        if l == r:
            self.__tree[node] = MaxSegmentTreeNode()
            try:
                self.__tree[node].max = [a[l]]
            except IndexError:
                self.__tree[node].max = []
            return
        leftchild = 2 * node
        rightchild = leftchild + 1
        mid = (l + r) // 2
        self.__build(leftchild, l, mid, a, k)
        self.__build(rightchild, mid + 1, r, a, k)
        self.__tree[node] = MaxSegmentTreeNode()
        l = self.__tree[leftchild]
        r = self.__tree[rightchild]
        self.__tree[node].merge(l, r, k)

    def __query(self, node, l, r, i, j, k):
        if l >= i and r <= j:
            return self.__tree[node]
        elif j < l or i > r:
            return None
        else:
            leftchild = 2 * node
            rightchild = leftchild + 1
            mid = (l + r) // 2
            l = self.__query(leftchild, l, mid, i, j, k)
            r = self.__query(rightchild, mid + 1, r, i, j, k)
            if l is not None and r is not None:
                return MaxSegmentTreeNode(sorted(l.max+r.max)[-k:])
            elif l is None and r is None:
                return MaxSegmentTreeNode([])
            elif l is None:
                return MaxSegmentTreeNode(r.max)
            else:
                return MaxSegmentTreeNode(l.max)

    def query(self, i, j, k): 
        return self.__query(1, 0, self.__leaf_length, i, j, k)
        
def get_start_index(time_stamp_list, l, r, time_stamp):
    
    if l==r or time_stamp<time_stamp_list[l]:
        return l
    if time_stamp>time_stamp_list[r]:
        return -1
    mid = (l+r)//2
    if time_stamp == time_stamp_list[mid]:
        if mid >= 1 and time_stamp_list[mid-1]==time_stamp:
            return get_start_index(time_stamp_list, l, mid-1, time_stamp)
        else:
            return mid
    elif time_stamp < time_stamp_list[mid]:
        if (mid >=1 and time_stamp>time_stamp_list[mid-1]):
            return mid
        else:
            return get_start_index(time_stamp_list, l, mid-1, time_stamp)
    else:
        return get_start_index(time_stamp_list, mid+1, r, time_stamp)

def get_stop_index(time_stamp_list, l , r, time_stamp):
    if l==r or time_stamp>time_stamp_list[r]:
        return r
    if time_stamp < time_stamp_list[l]:
        return -1
    mid = (l+r)//2
    if time_stamp == time_stamp_list[mid]:
        if mid < r and time_stamp_list[mid+1]==time_stamp:
            return get_stop_index(time_stamp_list, mid+1, r, time_stamp)
        else:
            return mid
    elif time_stamp > time_stamp_list[mid]:
        if mid < r and time_stamp < time_stamp_list[mid+1]:
            return mid
        else:
            return get_stop_index(time_stamp_list, mid+1, r, time_stamp)
    else:
        return get_stop_index(time_stamp_list, l, mid-1, time_stamp)








line1 = input().strip(' ').split(' ')
num_of_input = int(line1[1])

SiFj = {}
SiFj_timestamp = {}
SiFj_linenum = {}
SiFj_sum = {}
SiFj_sum_segtree = {}
SiFjk_max_segtree = {}

SiFjFk = {}
SiFjFk_timestamp = {}
SiFjFk_sum = {}
SiFjFk_sum_segtree = {}


for line_iterator in range(num_of_input):
    input_line = input().strip(' ').split(' ')
    num_of_items = len(input_line)
    time_stamp = int(input_line[0])
    symbol = input_line[1]
    iter = 2
    while iter<num_of_items:
        field = input_line[iter]
        field_value = int(input_line[iter+1])
        try:
            SiFj[symbol+field].append(field_value)
            SiFj_timestamp[symbol+field].append(time_stamp)
            SiFj_linenum[symbol+field].append(line_iterator)
            SiFj_sum[symbol+field].append(SiFj_sum[symbol+field][-1]+field_value)
        except:
            SiFj[symbol+field] = [field_value]
            SiFj_timestamp[symbol+field] = [time_stamp]
            SiFj_linenum[symbol+field]=[line_iterator]
            SiFj_sum[symbol+field] = [field_value]
        iter = iter+2
print('tickfile completed')
try:
    input_line = input().strip(' ').split(' ')
    input_flag = True
except:
    input_flag = False
while(input_flag):
    
    num_of_items = len(input_line)
    query_type = input_line[0]
    if query_type == 'sum':
        start_time = int(input_line[1])
        stop_time = int(input_line[2])
        symbol = input_line[3].strip('\r')
        field = input_line[4].strip('\r')
        if (symbol+field) in SiFj:
            list_oi = SiFj[symbol+field]
            timestamp_oi = SiFj_timestamp[symbol+field]
            if (symbol+field) in SiFj_sum_segtree:
                print(SiFj_sum_segtree[symbol+field].query(get_start_index(timestamp_oi, 0, len(timestamp_oi)-1, start_time), get_stop_index(timestamp_oi, 0, len(timestamp_oi)-1, stop_time)).sum)
            else:
                SiFj_sum_segtree[symbol+field] = SegmentTree(SiFj[symbol+field])
                print(SiFj_sum_segtree[symbol+field].query(get_start_index(timestamp_oi, 0, len(timestamp_oi)-1, start_time), get_stop_index(timestamp_oi, 0, len(timestamp_oi)-1, stop_time)).sum)
        else:
            print(0)

    if query_type == 'product':
        start_time = int(input_line[1])
        stop_time = int(input_line[2])
        symbol = input_line[3].strip('\r')
        field1 = input_line[4].strip('\r')
        field2 = input_line[5].strip('\r')
        key = symbol+min(field1, field2)+max(field1,field2)
        #print(key)
        if key in SiFjFk_sum_segtree:
            #print(key)
            print(SiFjFk_sum_segtree[key].query(get_start_index(SiFjFk_timestamp[key],0,len(SiFjFk_timestamp[key])-1, 
                    start_time), get_stop_index(SiFjFk_timestamp[key], 0, len(SiFjFk_timestamp[key])-1, stop_time)).sum)
        else:
            if (symbol+field1) in SiFj and (symbol+field2) in SiFj:
                list_oi1 = SiFj[symbol+field1]
                timestamp_oi1 = SiFj_timestamp[symbol+field1]
                linenum_oi1 = SiFj_linenum[symbol+field1]
                list_oi2 = SiFj[symbol+field2]
                timestamp_oi2 = SiFj_timestamp[symbol+field2]
                linenum_oi2 = SiFj_linenum[symbol+field2]
                #print(timestamp_oi1)
                #print(timestamp_oi2)
                SiFjFk[key] = []
                SiFjFk_timestamp[key] = []
                field1_values = []
                field2_values = []
                field1_timestamp = []
                field2_timestamp = []
#                if field1==field2:
#                    for counter in range(len(timestamp_oi1)):
#                        SiFjFk[key].append(list_oi1[counter]**2)
#                        SiFjFk_timestamp[key].append(timestamp_oi1[counter])
#                else:
                common_linenums = sorted(list(set(linenum_oi1).intersection(set(linenum_oi2))))
                cli = 0
                f1i = 0
                f2i = 0
                while cli<len(common_linenums):
                    if linenum_oi1[f1i]==common_linenums[cli]:
                        field1_values.append(list_oi1[f1i])
                        field1_timestamp.append(timestamp_oi1[f1i])
                        cli = cli+1
                    f1i = f1i+1
                cli = 0
                while cli<len(common_linenums):
                    if linenum_oi2[f2i]==common_linenums[cli]:
                        field2_values.append(list_oi2[f2i])
                        field2_timestamp.append(timestamp_oi2[f2i])
                        cli = cli+1
                    f2i = f2i+1
                for counter in range(len(common_linenums)):
                    SiFjFk[key].append(field1_values[counter]*field2_values[counter])
                    SiFjFk_timestamp[key].append(field1_timestamp[counter])
                         
                    #print(common_timestamps)
#                    for cl in common_linenums:
#
#                        field1_values = [list_oi1[i] for i, x in enumerate(linenum_oi1) if x == ts]
#                        field2_values = [list_oi2[i] for i, x in enumerate(linenum_oi2) if x == ts]
#                        for value1 in field1_values:
#                            for value2 in field2_values:
#                                SiFjFk[key].append(value1*value2)
#                                SiFjFk_timestamp[key].append(ts)
                if len(SiFjFk[key])==0:
                    print(0)
                else:
                    SiFjFk_sum_segtree[key] = SegmentTree(SiFjFk[key])
                    #print(key)
                    #print(SiFjFk_timestamp[key])
                    #print(get_start_index(SiFjFk_timestamp[key],0,len(SiFjFk_timestamp[key])-1,start_time))
                    #print(get_stop_index(SiFjFk_timestamp[key], 0, len(SiFjFk_timestamp[key])-1, stop_time))
                    print(SiFjFk_sum_segtree[key].query(get_start_index(SiFjFk_timestamp[key],0,len(SiFjFk_timestamp[key])-1, 
                        start_time), get_stop_index(SiFjFk_timestamp[key], 0, len(SiFjFk_timestamp[key])-1, stop_time)).sum)
            else:
                print(0)
                
    if query_type == 'max':
        start_time = int(input_line[1])
        stop_time = int(input_line[2])
        symbol = input_line[3].strip('\r')
        field = input_line[4].strip('\r')
        k = int(input_line[5])
        if (symbol+field) in SiFj:
            list_oi = SiFj[symbol+field]
            timestamp_oi = SiFj_timestamp[symbol+field]
            key = symbol+field+str(k)
            if key in SiFjk_max_segtree:
                output_list = SiFjk_max_segtree[key].query(get_start_index(timestamp_oi, 0, len(timestamp_oi)-1, start_time), get_stop_index(timestamp_oi, 0, len(timestamp_oi)-1, stop_time),k).max
                output_list = [str(x) for x in output_list]
                print(' '.join(output_list[::-1]))
            else:
                SiFjk_max_segtree[key] = MaxSegmentTree(SiFj[symbol+field],k)
                
                output_list = SiFjk_max_segtree[key].query(get_start_index(timestamp_oi, 0, len(timestamp_oi)-1, start_time), get_stop_index(timestamp_oi, 0, len(timestamp_oi)-1, stop_time),k).max
                output_list = [str(x) for x in output_list]
                print(' '.join(output_list[::-1]))
        else:
            print()


    try:
        input_line = input().strip(' ').split(' ')
    except:
        input_flag = False