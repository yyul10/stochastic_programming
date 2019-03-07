import itertools
from pyomo.core import *
from pyomo.environ import *
from pyomo.pysp.annotations import (
    PySP_ConstraintStageAnnotation, StochasticConstraintBodyAnnotation, PySP_StochasticRHSAnnotation)

theta1_table = [25, 50, 75]
theta2_table = [15, 30, 45]
theta3_table = [100, 200, 300]
theta4_table = [50, 100, 150]
theta5_table = [80, 160, 240]

num_scenarios = len(theta1_table) * len(theta2_table) * len(theta3_table) * len(theta4_table) * len(theta5_table)
scenario_data = dict(('Scenario' + str(i), (theta1val, theta2val, theta3val, theta4val, theta5val))
                     for i, (theta1val, theta2val, theta3val, theta4val, theta5val) in
                     enumerate(itertools.product(theta1_table, theta2_table, theta3_table, theta4_table, theta5_table), 1))

model = ConcreteModel()
model.constraint_stage = PySP_ConstraintStageAnnotation()
#model.stoch_matrix = StochasticConstraintBodyAnnotation()
model.stoch_rhs = PySP_StochasticRHSAnnotation()

model.theta1 = Param(mutable=True, initialize=0.0)
model.theta2 = Param(mutable=True, initialize=0.0)
model.theta3 = Param(mutable=True, initialize=0.0)
model.theta4 = Param(mutable=True, initialize=0.0)
model.theta5 = Param(mutable=True, initialize=0.0)

model.x1 = Var(domain=NonNegativeReals)
model.x2 = Var(domain=NonNegativeReals)
model.x3 = Var(domain=NonNegativeReals)
model.x4 = Var(domain=NonNegativeReals)
model.x5 = Var(domain=NonNegativeReals)

model.t1 = Var(domain=NonNegativeReals)
model.t2 = Var(domain=NonNegativeReals)
model.t3 = Var(domain=NonNegativeReals)
model.t4 = Var(domain=NonNegativeReals)
model.t5 = Var(domain=NonNegativeReals)

model.FirstStageCost = Expression(initialize=0)
model.SecondStageCost = Expression(initialize=(280 * model.t1 +300 * model.t2 + 190 * model.t3 + 220 * model.t4 + 140 * model.t5))

model.w1 = Constraint(expr=model.x2 + model.x4 <= 100)
model.w2 = Constraint(expr=model.x1 + model.x3 <= 100)
model.w3 = Constraint(expr=model.x1 + model.x2 +model.x3 + model.x4 + model.x5 <= 300)
model.w4 = Constraint(expr=model.x2 + model.x4 <= 100)
model.w5 = Constraint(expr=model.x5 <= 100)
model.w6 = Constraint(expr=model.x1 + model.x3 <= 100)

model.w7 = Constraint(expr=model.t1 <= model.x1)
model.w8 = Constraint(expr=model.t1 <= model.theta1)
model.w9 = Constraint(expr=model.t2 <= model.x2)
model.w10 = Constraint(expr=model.t2 <= model.theta2)
model.w11 = Constraint(expr=model.t3 <= model.x3)
model.w12 = Constraint(expr=model.t3 <= model.theta3)
model.w13 = Constraint(expr=model.t4 <= model.x4)
model.w14 = Constraint(expr=model.t4 <= model.theta4)
model.w15 = Constraint(expr=model.t5 <= model.x5)
model.w16 = Constraint(expr=model.t5 <= model.theta5)

model.constraint_stage.declare(model.w1, 1)
model.constraint_stage.declare(model.w2, 1)
model.constraint_stage.declare(model.w3, 1)
model.constraint_stage.declare(model.w4, 1)
model.constraint_stage.declare(model.w5, 1)
model.constraint_stage.declare(model.w6, 1)
model.constraint_stage.declare(model.w7, 2)
model.constraint_stage.declare(model.w8, 2)
model.constraint_stage.declare(model.w9, 2)
model.constraint_stage.declare(model.w10, 2)
model.constraint_stage.declare(model.w11, 2)
model.constraint_stage.declare(model.w12, 2)
model.constraint_stage.declare(model.w13, 2)
model.constraint_stage.declare(model.w14, 2)
model.constraint_stage.declare(model.w15, 2)
model.constraint_stage.declare(model.w16, 2)

model.stoch_rhs.declare(model.w8)
model.stoch_rhs.declare(model.w10)
model.stoch_rhs.declare(model.w12)
model.stoch_rhs.declare(model.w14)
model.stoch_rhs.declare(model.w16)

model.obj = Objective(expr=-(model.FirstStageCost + model.SecondStageCost))


def pysp_scenario_tree_model_callback():
    from pyomo.pysp.scenariotree.tree_structure_model import CreateConcreteTwoStageScenarioTreeModel

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

    theta1_val, theta2_val, theta3_val, theta4_val, theta5_val = scenario_data[scenario_name]
    instance.theta1.value = theta1_val
    instance.theta2.value = theta2_val
    instance.theta3.value = theta3_val
    instance.theta4.value = theta4_val
    instance.theta5.value = theta5_val

    return instance
