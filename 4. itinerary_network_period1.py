# DLP with 2 classes
import numpy as np
import pandas as pd
import itertools
from pyomo.environ import *
from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation, StochasticConstraintBoundsAnnotation, 
                                    StochasticConstraintBodyAnnotation)

model = ConcreteModel()

v = {1:280,2:300,3:190,4:220,5:140}
c = [[0,1,1,0,0,1],
     [1,0,1,1,0,0],
     [0,1,1,0,0,1],
     [1,0,1,1,0,0],
     [0,0,1,0,1,0]]
capa = {1:100,2:100,3:300,4:100,5:100,6:100}
d_mean = {1:50,2:30,3:200,4:100,5:160}

# Possible Demands 
d1_rhs_table = [25,50,75]
d2_rhs_table = [15,30,45]
d3_rhs_table = [100,200,300]
d4_rhs_table = [50,100,150]
d5_rhs_table = [80,160,240]

model.constraint_stage = PySP_ConstraintStageAnnotation()
model.stoch_rhs = StochasticConstraintBoundsAnnotation()
num_scenarios = len(d3_rhs_table) * len(d4_rhs_table) * len(d5_rhs_table)
scenario_data = dict(('Scenario'+str(i), (d3val, d4val, d5val))
                     for i, (d3val, d4val, d5val) in
                     enumerate (itertools.product(d3_rhs_table, d4_rhs_table, d5_rhs_table),1))

# Declare Variables
# model.x1 = Var(within=NonNegativeIntegers)
# model.x2 = Var(within=NonNegativeIntegers)
model.x3 = Var(within=NonNegativeIntegers)
model.x4 = Var(within=NonNegativeIntegers)
model.x5 = Var(within=NonNegativeIntegers)

# model.t1 = Var(within=NonNegativeIntegers)
# model.t2 = Var(within=NonNegativeIntegers)
model.t3 = Var(within=NonNegativeIntegers)
model.t4 = Var(within=NonNegativeIntegers)
model.t5 = Var(within=NonNegativeIntegers)

# model.d1_rhs = Param(mutable=True, initialize=0.0)
# model.d2_rhs = Param(mutable=True, initialize=0.0)
model.d3_rhs = Param(mutable=True, initialize=0.0)
model.d4_rhs = Param(mutable=True, initialize=0.0)
model.d5_rhs = Param(mutable=True, initialize=0.0)

# Objective 
# model.obj = Objective(expr= model.x['x1']*v[1]+model.x['x2']*v[2]+model.x['x3']*v[3]
#                       +model.x['x4']*v[4]+model.x['x5']*v[5],sense=maximize)
model.FirstStageCost = Expression(initialize=0)
model.SecondStageCost = Expression(initialize=model.t3*v[3]+model.t4*v[4]+model.t5*v[5])

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
# model.d11 = Constraint(expr=model.t1 <= model.d1_rhs)
# model.constraint_stage.declare(model.d11,2)
# model.stoch_rhs.declare(model.d11)

# model.d12 = Constraint(expr=model.t1 - model.x1 <= 0)
# model.constraint_stage.declare(model.d12,2)

# model.d21 = Constraint(expr=model.t2 <= model.d2_rhs)
# model.constraint_stage.declare(model.d21,2)
# model.stoch_rhs.declare(model.d21)

# model.d22 = Constraint(expr=model.t2 - model.x2 <= 0)
# model.constraint_stage.declare(model.d22,2)

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
#     st_model.StageVariables[first_stage].add('x1')
#     st_model.StageVariables[first_stage].add('x2')
    st_model.StageVariables[first_stage].add('x3')
    st_model.StageVariables[first_stage].add('x4')
    st_model.StageVariables[first_stage].add('x5')
    # Second Stage
    st_model.StageCost[second_stage] = 'SecondStageCost'
#     st_model.StageVariables[second_stage].add('t1')
#     st_model.StageVariables[second_stage].add('t2')
    st_model.StageVariables[second_stage].add('t3')
    st_model.StageVariables[second_stage].add('t4')
    st_model.StageVariables[second_stage].add('t5')
    return st_model

def pysp_instance_creation_callback(scenario_name, node_names):

    instance = model.clone()

    d3_rhs_val, d4_rhs_val, d5_rhs_val  = scenario_data[scenario_name]
#     instance.d1_rhs.value = d1_rhs_val
#     instance.d2_rhs.value = d2_rhs_val
    instance.d3_rhs.value = d3_rhs_val
    instance.d4_rhs.value = d4_rhs_val
    instance.d5_rhs.value = d5_rhs_val

    return instance