\ENCODING=ISO-8859-1
\Problem name: network_d

Minimize
 obj: s1 + s2 + s3
Subject To
 c_u_budget_:          x1 + x2 + 4 x3 <= 10
 c_e_d1_:              f11 + f12 + s1  = 2.05
 c_e_d2_:              f21 + f22 + s2  = 2.05
 c_e_d3_:              f31 + f32 + s3  = 1.5
 c_u_c1_:              - 0.7 x1 + f11 + f22 + f32 <= 0
 c_u_c2_:              - 0.7 x2 + f12 + f21 + f32 <= 0
 c_u_c3_:              - x3 + f12 + f22 + f31 <= 0
 c_e_ONE_VAR_CONSTANT: ONE_VAR_CONSTANT  = 1
End
