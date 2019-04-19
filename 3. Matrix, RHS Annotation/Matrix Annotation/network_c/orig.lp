\ENCODING=ISO-8859-1
\Problem name: network

Minimize
 obj: x4 + x5 + x6
Subject To
 c_u_x14_:             x1 + x2 + 4 x3 <= 10
 c_e_x15_:             x4 + x7 + x8  = 2
 c_e_x16_:             x10 + x5 + x9  = 2
 c_e_x17_:             x11 + x12 + x6  = 1.5
 c_u_x18_:             - 5.960319592 x1 + x10 + x12 + x7 <= 0.7
 c_u_x19_:             - 5.960319592 x2 + x12 + x8 + x9 <= 0.7
 c_u_x20_:             - x3 + x10 + x11 + x8 <= 0
 c_e_ONE_VAR_CONSTANT: ONE_VAR_CONSTANT  = 1
Bounds
 0 <= x1 <= 217
 0 <= x2 <= 217
 0 <= x3 <= 217
End
