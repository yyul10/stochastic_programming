import itertools
from pyomo.environ import *
from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation, StochasticConstraintBoundsAnnotation, StochasticConstraintBodyAnnotation)

theta1_table = [1,1,1,1,1,1,1,0,0,0]
theta2_table = [1,1,1,1,1,1,1,0,0,0]
d1_rhs_table = [0,1,2,3,5]
d2_rhs_table = [0,1,2,3,5]
d3_rhs_table = [0,1,2,3]

model = ConcreteModel()



#-------C--------
# model.constraint_stage = PySP_ConstraintStageAnnotation()
# model.stoch_matrix = StochasticConstraintBodyAnnotation()
# num_scenarios = len(theta1_table)*len(theta2_table)
# scenario_data = dict(('Scenario'+str(i), (theta1val, theta2val))
#                      for i, (theta1val, theta2val) in
#                      enumerate (itertools.product(theta1_table, theta2_table),1))
#----------------
#-------D--------
model.constraint_stage = PySP_ConstraintStageAnnotation()
model.stoch_rhs = StochasticConstraintBoundsAnnotation()
model.stoch_matrix = StochasticConstraintBodyAnnotation()
num_scenarios = len(theta1_table)*len(theta2_table)*len(d1_rhs_table) * len(d2_rhs_table) * len(d3_rhs_table)
scenario_data = dict(('Scenario'+str(i), (theta1val, theta2val, d1_rhs_val, d2_rhs_val, d3_rhs_val))
                     for i, (theta1val, theta2val, d1_rhs_val, d2_rhs_val, d3_rhs_val) in
                     enumerate (itertools.product(theta1_table, theta2_table, d1_rhs_table, d2_rhs_table, d3_rhs_table),1))
#----------------
model.d1_rhs = Param(mutable=True, initialize=0.0)
model.d2_rhs = Param(mutable=True, initialize=0.0)
model.d3_rhs = Param(mutable=True, initialize=0.0)

model.x1 = Var(within=NonNegativeReals)
model.x2 = Var(within=NonNegativeReals)
model.x3 = Var(within=NonNegativeReals)
model.f11 = Var(within=NonNegativeReals)
model.f12 = Var(within=NonNegativeReals)
model.f21 = Var(within=NonNegativeReals)
model.f22 = Var(within=NonNegativeReals)
model.f31 = Var(within=NonNegativeReals)
model.f32 = Var(within=NonNegativeReals)
model.s1 = Var(within=NonNegativeReals)
model.s2 = Var(within=NonNegativeReals)
model.s3 = Var(within=NonNegativeReals)
model.theta1 = Param(mutable=True, initialize=0)
model.theta2 = Param(mutable=True, initialize=0)

model.FirstStageCost = Expression(initialize=0)
model.SecondStageCost = Expression(initialize=model.s1+model.s2+model.s3)

model.budget = Constraint(expr=model.x1+model.x2+4*model.x3 <= 10)
model.constraint_stage.declare(model.budget,1)


#-------D--------
# model.d1 = Constraint(expr=model.f11+model.f12+model.s1 == 2.05)
# model.constraint_stage.declare(model.d1,2)

# model.d2 = Constraint(expr=model.f21+model.f22+model.s2 == 2.05)
# model.constraint_stage.declare(model.d2,2)

# model.d3 = Constraint(expr=model.f31+model.f32+model.s3 == 1.5)
# model.constraint_stage.declare(model.d3,2)
#----------------
#-------E--------
model.d1 = Constraint(expr=model.f11+model.f12+model.s1 == model.d1_rhs)
model.constraint_stage.declare(model.d1,2)
model.stoch_rhs.declare(model.d1)

model.d2 = Constraint(expr=model.f21+model.f22+model.s2 == model.d2_rhs)
model.constraint_stage.declare(model.d2,2)
model.stoch_rhs.declare(model.d2)

model.d3 = Constraint(expr=model.f31+model.f32+model.s3 == model.d3_rhs)
model.constraint_stage.declare(model.d3,2)
model.stoch_rhs.declare(model.d3)
#----------------
model.c1 = Constraint(expr=model.f11+model.f22+model.f32-model.theta1*model.x1 <= 0)
model.constraint_stage.declare(model.c1,2)
model.stoch_matrix.declare(model.c1, variables=[model.x1])

model.c2 = Constraint(expr=model.f12+model.f21+model.f32-model.theta2*model.x2 <= 0)
model.constraint_stage.declare(model.c2,2)
model.stoch_matrix.declare(model.c2, variables=[model.x2])                                                

model.c3 = Constraint(expr=model.f12+model.f22+model.f31-model.x3 <= 0)
model.constraint_stage.declare(model.c3,2)

model.obj = Objective(expr=model.FirstStageCost+model.SecondStageCost)

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
    
    # Second Stage
    st_model.StageCost[second_stage] = 'SecondStageCost'
    st_model.StageVariables[second_stage].add('f11')
    st_model.StageVariables[second_stage].add('f12')
    st_model.StageVariables[second_stage].add('f21')
    st_model.StageVariables[second_stage].add('f22')
    st_model.StageVariables[second_stage].add('f31')
    st_model.StageVariables[second_stage].add('f32')
    st_model.StageVariables[second_stage].add('s1')
    st_model.StageVariables[second_stage].add('s2')
    st_model.StageVariables[second_stage].add('s3')
    return st_model

def pysp_instance_creation_callback(scenario_name, node_names):

    #
    # Clone a new instance and update the stochastic
    # parameters from the sampled scenario
    #

    instance = model.clone()

    theta1_val, theta2_val, d1_rhs_val, d2_rhs_val, d3_rhs_val = scenario_data[scenario_name]
    instance.theta1.value = theta1_val
    instance.theta2.value = theta2_val
 #-------D--------
    instance.d1_rhs.value = d1_rhs_val
    instance.d2_rhs.value = d2_rhs_val
    instance.d3_rhs.value = d3_rhs_val
 #----------------
    return instance