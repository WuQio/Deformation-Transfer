# -*- coding:utf-8 -*-
import numpy as np
import time as tm

start = tm.clock()


def get_v4(v1, v2, v3):
    '''
    传入3个点list类型，输出v4，list类型
    '''
    a = []
    b = []
    v4 = []  # 各列表之间不能用逗号，要用分号
    for i in range(3):
        a.append(v2[i] - v1[i])
        b.append(v3[i] - v1[i])
    multiple = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    mo = np.sqrt(multiple[0] ** 2 + multiple[1] ** 2 + multiple[2] ** 2)
    for i in range(3):
        multiple[i] /= mo
    for i in range(3):
        v4.append(v1[i] + multiple[i])
    return v4


def get_point_list(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    point_list = []
    v = []
    s = ""
    for line in lines:  # 读出s0文件中的每个点坐标，组装成 point_list_s0
        for char in line:
            if char != ' ':
                s += char
            else:
                num = float(s)
                v.append(num)
                s = ""
        num = float(s)
        v.append(num)
        s = ''
        point_list.append(v)
        v = []
    return point_list


point_list_s0 = get_point_list('s0_v.obj')
point_list_s1 = get_point_list('s1_v.obj')
point_list_t0 = get_point_list('t0_v.obj')

s = ""

face = open("face.obj")
face_lines = face.readlines()
face.close()
w_x = np.array([])
w_y = w_x
w_z = w_x
for line in face_lines:
    number = []
    for char in line:
        if (char == ' ') | (char == '\n'):
            number.append(int(s))
            s = ""
        else:
            s += char
    v1, _v1, t0_v1 = point_list_s0[number[0] - 1], point_list_s1[number[0] - 1], point_list_t0[number[0] - 1]
    v1_array, _v1_array, t0_v1_array = np.array(v1), np.array(_v1), np.array(t0_v1)
    v2, _v2, t0_v2 = point_list_s0[number[1] - 1], point_list_s1[number[1] - 1], point_list_t0[number[1] - 1]
    v2_array, _v2_array, t0_v2_array = np.array(v2), np.array(_v2), np.array(t0_v2)
    v3, _v3, t0_v3 = point_list_s0[number[2] - 1], point_list_s1[number[2] - 1], point_list_t0[number[2] - 1]
    v3_array, _v3_array, t0_v3_array = np.array(v3), np.array(_v3), np.array(t0_v3)
    v4, _v4, t0_v4 = get_v4(v1, v2, v3), get_v4(_v1, _v2, _v3), get_v4(t0_v1, t0_v2, t0_v3)
    v4_array, _v4_array, t0_v4_array = np.array(v4), np.array(_v4), np.array(t0_v4)

    V = np.matrix([v2_array - v1_array, v3_array - v1_array, v4_array - v1_array]).T
    _V = np.matrix([_v2_array - _v1_array, _v3_array - _v1_array, _v4_array - _v1_array]).T
    t0_V = np.matrix([t0_v2_array - t0_v1_array, t0_v3_array - t0_v1_array, t0_v4_array - t0_v1_array]).T
    S = _V * V.I  # 得到S，matrix类型
    # w.append(((S*t0_V).T).getA1())
    tmp = (S * t0_V).T
    w_x = np.append(w_x, tmp[:, 0])  # w此时是array类型
    w_y = np.append(w_y, tmp[:, 1])
    w_z = np.append(w_z, tmp[:, 2])

del point_list_s0, point_list_s1, point_list_t0, face_lines

VNUM = 1069  # 点的个数
FNUM = 1947  # 面的个数
col_num = VNUM + FNUM  # get_A模块，得到稀疏矩阵
row_num = 3 * FNUM
A = np.array([[0] * col_num] * row_num)  # A此时是array类型
n = VNUM  # 点数
face = open("face.obj")
face_lines = face.readlines()
face.close()
f = 1  # 第f个面，对读入的三角面计数
for line in face_lines:
    s = ""
    number = []  # 每个三角形三个点的序号
    for char in line:
        if (char == ' ') | ('\n' == char):
            number.append(int(s))
            s = ""
        else:
            s += char
    for count in range(3):
        A[3 * (f - 1) + count][number[0] - 1] = -1
        if count < 2:
            A[3 * (f - 1) + count][number[count + 1] - 1] = 1
        else:
            A[3 * (f - 1) + count][n + f - 1] = 1
    f += 1

A_I = np.matrix(A).I  # 将A转换成matrix类型
w_x = np.matrix(w_x).T  # 将w_x转换成matrix类型
w_y = np.matrix(w_y).T  #
w_z = np.matrix(w_z).T  #
xx = A_I * w_x
yy = A_I * w_y
zz = A_I * w_z
x_arr = np.array(xx)
y_arr = np.array(yy)
z_arr = np.array(zz)
fp = open("obj.obj", "w")
for r in range(VNUM):
    fp.write('v ')
    s = str(x_arr[r])
    fp.write(s[1:len(s) - 1])
    fp.write(' ')
    s = str(y_arr[r])
    fp.write(s[1:len(s) - 1])
    fp.write(' ')
    s = str(z_arr[r])
    fp.write(s[1:len(s) - 1])
    fp.write('\n')
for line in face_lines:
    fp.write('f ')
    fp.write(str(line))

fp.close()
end = tm.clock()
print "Cost %s seconds" % (end - start)
