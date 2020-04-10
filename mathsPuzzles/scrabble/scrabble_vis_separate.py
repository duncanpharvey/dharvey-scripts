import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows = 1, cols = 2, subplot_titles = ("all letter combinations", "real words"))

x = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
y_total = [1999, 6405, 18790, 25646, 48307, 69814, 86696, 110555, 132063, 147805, 157415, 177560, 180235, 185615, 192527, 188541, 182312, 176179, 165556, 147003, 135984, 120567, 102279, 89488, 76671, 62179, 50855, 41806, 31654, 24152, 18877, 13495, 9661, 7329, 4976, 3213, 2254, 1431, 749, 484, 314, 138, 80, 50, 15]
y_real = [1735, 3714, 6149, 11256, 14722, 15817, 15953, 14406, 10881, 9018, 7065, 4810, 3567, 2391, 1431, 873, 553, 254, 174, 108, 54, 34, 17, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

trace1 = go.Bar(name = "all", x= x, y = y_total)

trace2 = go.Bar(name = "real", x = x, y = y_real)

fig.add_trace(trace1, row = 1, col = 1)
fig.add_trace(trace2, row = 1, col = 2)

fig.update_xaxes(range = [5, 49], title_text = "point total")
fig.update_yaxes(range = [0, 200000], title_text = "count")
fig.update_layout(showlegend = False)

fig.show()
