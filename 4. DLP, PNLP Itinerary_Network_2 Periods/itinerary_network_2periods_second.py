import numpy as np
import pandas as pd
import itertools
from pyomo.environ import *
import pyomo.environ as pyo
from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation, StochasticConstraintBoundsAnnotation, 
                                    StochasticConstraintBodyAnnotation)

model = ConcreteModel()

# --------k is the replication number-------
k = 24
# ----------k is [0,1, ..., 24]-------------

v = {1:280,2:300,3:190,4:220,5:140}
v_bid1 = [[339, 317, 209, 176, 0], [271, 365, 0, 284, 0], [215, 256, 207, 255, 167], [322, 302, 0, 210, 0], [308, 229, 214, 180, 168],
          [295, 328, 0, 227, 0], [283, 284, 200, 236, 0], [315, 376, 0, 205, 146], [317, 279, 198, 277, 166], [233, 350, 205, 233, 162], 
          [357, 345, 0, 180, 140], [303, 383, 0, 209, 0], [334, 316, 242, 233, 178], [328, 272, 223, 215, 0], [335, 319, 0, 224, 168], 
          [295, 225, 228, 229, 0], [238, 229, 202, 220, 0], [285, 266, 211, 263, 162], [349, 290, 224, 235, 153], [197, 215, 0, 186, 0], 
          [311, 244, 0, 250, 0], [303, 298, 0, 225, 0], [335, 319, 0, 224, 168], [259, 377, 0, 178, 0], [273, 353, 0, 205, 0]]
v_bid2 = [[339, 317, 209, 176, 133], [271, 365, 139, 284, 101], [215, 256, 207, 255, 167], [322, 302, 187, 210, 120], [308, 229, 214, 180, 168],
          [295, 328, 149, 227, 106], [283, 284, 200, 236, 99], [315, 376, 187, 205, 146], [317, 279, 198, 277, 166], [233, 350, 205, 233, 162],
          [357, 345, 133, 180, 140], [303, 383, 144, 209, 138], [334, 316, 242, 233, 178], [328, 272, 223, 215, 121], [335, 319, 166, 224, 168], 
          [295, 225, 228, 229, 120], [238, 229, 202, 220, 106], [285, 266, 211, 263, 162], [349, 290, 224, 235, 153], [197, 215, 155, 186, 101], 
          [311, 244, 173, 250, 122], [303, 298, 145, 225, 126], [335, 319, 166, 224, 168], [259, 377, 169, 178, 121], [273, 353, 139, 205, 107]]
c = [[0,1,1,0,0,1],
     [1,0,1,1,0,0],
     [0,1,1,0,0,1],
     [1,0,1,1,0,0],
     [0,0,1,0,1,0]]
capa = {1:100,2:100,3:300,4:100,5:100,6:100}


d_mean = [50,30,200,100,160]
d_new1 = [[0, 0, 102, 26, 0], [0, 0, 0, 26, 0], [0, 0, 102, 26, 58], [0, 0, 0, 26, 0], [0, 0, 102, 26, 58],
          [0, 0, 0, 26, 0], [0, 0, 102, 26, 0], [0, 0, 0, 26, 58], [0, 0, 102, 26, 58], [0, 0, 102, 26, 58],
          [0, 0, 0, 26, 58], [0, 0, 0, 26, 0], [0, 0, 102, 26, 58], [0, 0, 102, 26, 0], [0, 0, 0, 26, 58],
          [0, 0, 102, 26, 0], [0, 0, 102, 26, 0], [0, 0, 102, 26, 58], [0, 0, 102, 26, 58], [0, 0, 0, 26, 0],
          [0, 0, 0, 26, 0], [0, 0, 0, 26, 0], [0, 0, 0, 26, 58], [0, 0, 0, 26, 0], [0, 0, 0, 26, 0]]
d_new2 = [[0, 0, 0, 0, 0], [0, 0, 102, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
          [0, 0, 102, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
          [0, 0, 102, 0, 0], [0, 0, 102, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 102, 0, 0], 
          [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 102, 0, 0], 
          [0, 0, 102, 0, 0], [0, 0, 102, 0, 0], [0, 0, 102, 0, 0], [0, 0, 102, 0, 0], [0, 0, 102, 0, 0]]

# Possible Demands 
# d1_rhs_table = [49,50,51]
# d2_rhs_table = [29,30,31]
# d3_rhs_table = [99,100,101]
# d4_rhs_table = [79,80,81]
# d5_rhs_table = [149,150,151]
d1_rhs_table = [ceil((d_mean[0]-d_new2[k][0])*0.9),floor((d_mean[0]-d_new2[k][0])*1.1)+1]
d2_rhs_table = [ceil((d_mean[1]-d_new2[k][1])*0.9),floor((d_mean[1]-d_new2[k][1])*1.1)+1]
d3_rhs_table = [ceil((d_mean[2]-d_new2[k][2])*0.9),floor((d_mean[2]-d_new2[k][2])*1.1)+1]
d4_rhs_table = [ceil((d_mean[3]-d_new2[k][3])*0.9),floor((d_mean[3]-d_new2[k][3])*1.1)+1]
d5_rhs_table = [ceil((d_mean[4]-d_new2[k][4])*0.9),floor((d_mean[4]-d_new2[k][4])*1.1)+1]

model.constraint_stage = PySP_ConstraintStageAnnotation()
model.stoch_rhs = StochasticConstraintBoundsAnnotation()
num_scenarios = len(d1_rhs_table) * len(d2_rhs_table) * len(d3_rhs_table) * len(d4_rhs_table) * len(d5_rhs_table)
scenario_data = dict(('Scenario'+str(i), (d1val, d2val, d3val, d4val, d5val))
                     for i, (d1val, d2val, d3val, d4val, d5val) in
                     enumerate (itertools.product(d1_rhs_table, d2_rhs_table, d3_rhs_table, d4_rhs_table, d5_rhs_table),1))

# Declare Variables
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT_EXPORT)

model.x1 = Var(within=NonNegativeIntegers)
model.x2 = Var(within=NonNegativeIntegers)
model.x3 = Var(within=NonNegativeIntegers)
model.x4 = Var(within=NonNegativeIntegers)
model.x5 = Var(within=NonNegativeIntegers)

model.t1 = Var(within=NonNegativeIntegers)
model.t2 = Var(within=NonNegativeIntegers)
model.t3 = Var(within=NonNegativeIntegers)
model.t4 = Var(within=NonNegativeIntegers)
model.t5 = Var(within=NonNegativeIntegers)

model.d1_rhs = Param(mutable=True, initialize=0.0)
model.d2_rhs = Param(mutable=True, initialize=0.0)
model.d3_rhs = Param(mutable=True, initialize=0.0)
model.d4_rhs = Param(mutable=True, initialize=0.0)
model.d5_rhs = Param(mutable=True, initialize=0.0)

# Objective 
model.FirstStageCost = Expression(initialize=0)
model.SecondStageCost = Expression(initialize=model.t1*v_bid2[k][0]+model.t2*v_bid2[k][1]+model.t3*v_bid2[k][2]
                      +model.t4*v_bid2[k][3]+model.t5*v_bid2[k][4])

# Capacity Constraints
c1 =np.transpose(c)[0]
model.c1 = Constraint(expr= model.x1*c1[0]+model.x2*c1[1]+model.x3*c1[2]
                      +model.x4*c1[3]+model.x5*c1[4] <= capa[1])
model.constraint_stage.declare(model.c1,1)
c2 =np.transpose(c)[1]
model.c2 = Constraint(expr= model.x1*c2[0]+model.x2*c2[1]+model.x3*c2[2]
                      +model.x4*c2[3]+model.x5*c2[4] <= capa[2])
model.constraint_stage.declare(model.c2,1)
c3 =np.transpose(c)[2]
model.c3 = Constraint(expr= model.x1*c3[0]+model.x2*c3[1]+model.x3*c3[2]
                      +model.x4*c3[3]+model.x5*c3[4] <= capa[3])
model.constraint_stage.declare(model.c3,1)
c4 =np.transpose(c)[3]
model.c4 = Constraint(expr= model.x1*c4[0]+model.x2*c4[1]+model.x3*c4[2]
                      +model.x4*c4[3]+model.x5*c4[4] <= capa[4])
model.constraint_stage.declare(model.c4,1)
c5 =np.transpose(c)[4]
model.c5 = Constraint(expr= model.x1*c5[0]+model.x2*c5[1]+model.x3*c5[2]
                      +model.x4*c5[3]+model.x5*c5[4] <= capa[5])
model.constraint_stage.declare(model.c5,1)
c6 =np.transpose(c)[5]
model.c6 = Constraint(expr= model.x1*c6[0]+model.x2*c6[1]+model.x3*c6[2]
                      +model.x4*c6[3]+model.x5*c6[4] <= capa[6])
model.constraint_stage.declare(model.c6,1)

# Second Stage Min{X,D} Constraint (when D is stochastic)
model.d11 = Constraint(expr=model.t1 <= model.d1_rhs)
model.constraint_stage.declare(model.d11,2)
model.stoch_rhs.declare(model.d11)

model.d12 = Constraint(expr=model.t1 - model.x1 <= 0)
model.constraint_stage.declare(model.d12,2)

model.d21 = Constraint(expr=model.t2 <= model.d2_rhs)
model.constraint_stage.declare(model.d21,2)
model.stoch_rhs.declare(model.d21)

model.d22 = Constraint(expr=model.t2 - model.x2 <= 0)
model.constraint_stage.declare(model.d22,2)

model.d31 = Constraint(expr=model.t3 <= model.d3_rhs)
model.constraint_stage.declare(model.d31,2)
model.stoch_rhs.declare(model.d31)

model.d32 = Constraint(expr=model.t3 - model.x3 <= 0)
model.constraint_stage.declare(model.d32,2)

model.d41 = Constraint(expr=model.t4 <= model.d4_rhs)
model.constraint_stage.declare(model.d41,2)
model.stoch_rhs.declare(model.d41)

model.d42 = Constraint(expr=model.t4 - model.x4 <= 0)
model.constraint_stage.declare(model.d42,2)

model.d51 = Constraint(expr=model.t5 <= model.d5_rhs)
model.constraint_stage.declare(model.d51,2)
model.stoch_rhs.declare(model.d51)

model.d52 = Constraint(expr=model.t5 - model.x5 <= 0)
model.constraint_stage.declare(model.d52,2)

# Final Objective
model.obj = Objective(expr=(model.FirstStageCost+model.SecondStageCost)*(-1))

def pysp_scenario_tree_model_callback():
    from pyomo.pysp.scenariotree.tree_structure_model import \
        CreateConcreteTwoStageScenarioTreeModel

    st_model = CreateConcreteTwoStageScenarioTreeModel(num_scenarios)

    first_stage = st_model.Stages.first()
    second_stage = st_model.Stages.last()

    # First Stage
    st_model.StageCost[first_stage] = 'FirstStageCost'  
    st_model.StageVariables[first_stage].add('x1')
    st_model.StageVariables[first_stage].add('x2')
    st_model.StageVariables[first_stage].add('x3')
    st_model.StageVariables[first_stage].add('x4')
    st_model.StageVariables[first_stage].add('x5')
    # Second Stage
    st_model.StageCost[second_stage] = 'SecondStageCost'
    st_model.StageVariables[second_stage].add('t1')
    st_model.StageVariables[second_stage].add('t2')
    st_model.StageVariables[second_stage].add('t3')
    st_model.StageVariables[second_stage].add('t4')
    st_model.StageVariables[second_stage].add('t5')
    return st_model

def pysp_instance_creation_callback(scenario_name, node_names):

    instance = model.clone()

    d1_rhs_val, d2_rhs_val, d3_rhs_val, d4_rhs_val, d5_rhs_val  = scenario_data[scenario_name]
    instance.d1_rhs.value = d1_rhs_val
    instance.d2_rhs.value = d2_rhs_val
    instance.d3_rhs.value = d3_rhs_val
    instance.d4_rhs.value = d4_rhs_val
    instance.d5_rhs.value = d5_rhs_val

    return instance