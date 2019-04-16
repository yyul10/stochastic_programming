import itertools
import random

from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation,
                                    PySP_StochasticRHSAnnotation)
# Define the probability table for the stochastic parameters
i=0
d1_rhs_table=\
[3.9323, 2.6324, -3.1408, -0.3789, 3.7175, -0.7154, -0.0245, 2.5941, -0.0305, -0.3112,
 -2.01, 2.7088, -0.4833, -1.6373, -3.0267, 1.3714, -1.3194, 10.6709, -1.9522, 1.2065,
 0.2786, -0.3919, -2.7767, -0.2428, -1.8458, -0.4796, 0.1375, -0.6534, -0.9684, -1.7311,
 -2.2169, 0.9958, -2.405, 2.6091, -1.6641, 1.167, 4.8966, 2.3375, -1.0663, -0.6731,
 -1.8048, 2.8722, -0.9826, 3.1187, -1.295, -2.0326, 0.1602, -0.8889, -0.3146, -0.3717,
 -2.4787, -0.0625, -2.6977, 1.2482, -1.7434, -1.1329, 3.3738, -1.6965, -0.2341, 3.3963,
 2.048, 0.0905, 1.1836, 0.4437, -2.9092, -1.0815, -2.6525, -3.1664, 2.3964, -0.5076,
 1.2734, -1.7652, -0.9546, -1.2779, -1.7421, -1.0183, -0.4392, 1.0994, -0.0678, 1.4886,
 -1.1482, -0.0366, 0.1029, -1.4013, 2.4265, -0.8231, 0.0363, 4.9604, 4.2461, 1.3526,
 -2.0547, -2.0218, -1.4739, -1.495, -1.509, -0.5191, -0.0872, 1.9653, -1.6092, 1.1035]

num_scenarios = len(d1_rhs_table)
scenario_data = dict(('Scenario'+str(i), (d1val))
                      for i, (d1val) in
                     enumerate(d1_rhs_table, 1))

model = ConcreteModel()

model.constraint_stage = PySP_ConstraintStageAnnotation()
model.stoch_rhs = PySP_StochasticRHSAnnotation()

# use mutable parameters so that the right-hand-side can be updated for each scenario
model.d1_rhs = Param(mutable=True, initialize=0.0)

# first-stage variables
model.x1 = Var(bounds=(0.7,296.4))
model.x2 = Var(bounds=(1.3,49.4))

# second-stage variables
model.y1 = Var(within=NonNegativeReals)
model.y2 = Var(within=NonNegativeReals)


# stage-cost expressions
model.FirstStageCost = \
    Expression(initialize=(0.1*model.x1+0.5*model.x2))
model.SecondStageCost = \
    Expression(initialize=(-3*model.y1-5*model.y2))

model.s1 = Constraint(expr= model.x1 - 0.5*model.x2 >= 0)
model.constraint_stage.declare(model.s1, 1)

model.s2 = Constraint(expr= model.x1 + model.x2 <= 200)
model.constraint_stage.declare(model.s2, 1)

model.s4 = Constraint(expr= model.y1 <= 4)
model.constraint_stage.declare(model.s4, 2)

model.s5 = Constraint(expr= 2*model.y2 <=12)
model.constraint_stage.declare(model.s5, 2)

model.s6 = Constraint(expr= 3*model.y1 + 2*model.y2 <= 18)
model.constraint_stage.declare(model.s6, 2)

# one constraint with stochastic right-hand-sides
model.d1 = Constraint(expr = 3.7498295146225757 + 0.05370186*model.x1\
                      + 0.22231025*model.x2 - model.y1 - model.y2 >=model.d1_rhs)
model.constraint_stage.declare(model.d1, 2)
model.stoch_rhs.declare(model.d1)


model.obj = Objective(expr=model.FirstStageCost + model.SecondStageCost)

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

    # Second Stage
    st_model.StageCost[second_stage] = 'SecondStageCost'
    st_model.StageVariables[second_stage].add('y1')
    st_model.StageVariables[second_stage].add('y2')

    return st_model

def pysp_instance_creation_callback(scenario_name, node_names):

    #
    # Clone a new instance and update the stochastic
    # parameters from the sampled scenario
    #
    instance = model.clone()

    d1_rhs_val = scenario_data[scenario_name]
    instance.d1_rhs.value = d1_rhs_val

    return instance