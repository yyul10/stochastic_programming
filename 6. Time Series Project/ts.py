#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________
#
# ad: Annotated with location of stochastic rhs entries
#       for use with pysp2smps conversion tool.

import itertools
import random

from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation,
                                    PySP_StochasticRHSAnnotation)

#
# Define the probability table for the stochastic parameters
#
demand=[0,92.84228,103.6135,82.04553]
y_start=95.68

d1_rhs_table=\
[-0.554210069444451,
 -0.780251736111111,
 -1.36775173611112,
 -0.0611892361111046,
 0.593498263888904,
 -0.247126736111099,
 1.47849826388888,
 -0.861605902777796,
 -0.165043402777798,
 3.37870659722221,
 -2.22462673611111,
 -0.202647569444423,
 -1.51337673611111,
 1.36974826388888,
 -1.17733506944445,
 1.16381076388888,
 2.55558159722221,
 -1.89712673611113,
 0.236831597222221,
 3.03672743055557,
 -0.293793402777766,
 0.491206597222231,
 2.89703993055556,
 0.16276909722221,
 -2.72671006944445,
 -2.45316840277778,
 1.36641493055555,
 -1.78702256944445,
 -0.818585069444453,
 -0.535460069444426,
 0.0855815972222445,
 -1.69285590277775,
 -4.18962673611111,
 -4.40546006944443,
 -0.489626736111106,
 -0.54764756944445,
 4.29537326388889,
 1.3647482638889,
 0.679748263888897,
 0.185477430555565,
 -2.82941840277778,
 2.18078993055555,
 -2.29983506944447,
 -0.981189236111121,
 4.14953993055556,
 0.0366232638888846,
 -0.681710069444435,
 0.0886024305555537]


num_scenarios = len(d1_rhs_table)
scenario_data = dict(('Scenario'+str(i), (d1val))
                      for i, (d1val) in
                     enumerate(d1_rhs_table, 1))

#
# Define the reference model
#

model = ConcreteModel()

# these annotations are required for using this
# model with the SMPS conversion tool
model.constraint_stage = PySP_ConstraintStageAnnotation()
model.stoch_rhs = PySP_StochasticRHSAnnotation()

# use mutable parameters so that the constraint
# right-hand-sides can be updated for each scenario
model.d1_rhs = Param(mutable=True, initialize=0.0)

# first-stage variables
model.delta1 = Var(bounds=(0,300))
model.delta2 = Var(bounds=(0,300))
model.delta3 = Var(bounds=(0,300))
model.delta4 = Var(bounds=(0,300))
#model.delta5 = Var(bounds=(0,300))

# second-stage variables

model.y1 = Var(within=NonNegativeReals)
model.z1 = Var(within=NonNegativeReals)
model.x1 = Var(within=NonNegativeReals)

model.y2 = Var(within=NonNegativeReals)
model.z2 = Var(within=NonNegativeReals)
model.x2 = Var(within=NonNegativeReals)

model.y3 = Var(within=NonNegativeReals)
model.z3 = Var(within=NonNegativeReals)
model.x3 = Var(within=NonNegativeReals)

model.y4 = Var(within=NonNegativeReals)
model.z4 = Var(within=NonNegativeReals)
model.x4 = Var(within=NonNegativeReals)

model.y5 = Var(within=NonNegativeReals)
model.z5 = Var(within=NonNegativeReals)
model.x5 = Var(within=NonNegativeReals)

totalCost = model.x1+model.x2+model.x3+model.x4+model.x5+3*(model.z1+model.z2+model.z3+model.z4+model.z5)


# stage-cost expressions
model.FirstStageCost = \
    Expression(initialize=0)
model.SecondStageCost = \
    Expression(initialize=(totalCost))

#
# this model has two first-stage constraints
#

# model.s1 = Constraint(expr= model.x1 - 0.5*model.x2 >= 0)
# model.constraint_stage.declare(model.s1, 1)

# model.s2 = Constraint(expr= model.x1 + model.x2 <= 200)
# model.constraint_stage.declare(model.s2, 1)

#
# this model has four second-stage constraints
#



model.s11 = Constraint(expr= model.y1 == y_start)
model.constraint_stage.declare(model.s11, 2)

model.s12 = Constraint(expr= model.x1 >= model.y1-demand[1]-model.d1_rhs)
model.constraint_stage.declare(model.s12, 2)
model.stoch_rhs.declare(model.s12)

model.s13 = Constraint(expr= model.z1 >= demand[1]+model.d1_rhs - model.y1)
model.constraint_stage.declare(model.s13, 2)
model.stoch_rhs.declare(model.s13)
############################################################################

model.s21 = Constraint(expr= model.y2 == model.x1+ model.delta1)
model.constraint_stage.declare(model.s21, 2)

model.s22 = Constraint(expr= model.x2 >= model.y2-demand[2]-model.d1_rhs)
model.constraint_stage.declare(model.s22, 2)
model.stoch_rhs.declare(model.s22)

model.s23 = Constraint(expr= model.z2 >= demand[2]+model.d1_rhs - model.y2)
model.constraint_stage.declare(model.s23, 2)
model.stoch_rhs.declare(model.s23)
############################################################################
model.s31 = Constraint(expr= model.y3 == model.x2+ model.delta2)
model.constraint_stage.declare(model.s31, 2)

model.s32 = Constraint(expr= model.x3 >= model.y3-demand[3]-model.d1_rhs)
model.constraint_stage.declare(model.s32, 2)
model.stoch_rhs.declare(model.s32)

model.s33 = Constraint(expr= model.z3 >= demand[3]+model.d1_rhs - model.y3)
model.constraint_stage.declare(model.s33, 2)
model.stoch_rhs.declare(model.s33)
#############################################################################
model.s41 = Constraint(expr= model.y4 == model.x3+ model.delta3)
model.constraint_stage.declare(model.s41, 2)

model.s42 = Constraint(expr= model.x4 >= model.y4-demand[4]-model.d1_rhs)
model.constraint_stage.declare(model.s42, 2)
model.stoch_rhs.declare(model.s42)

model.s43 = Constraint(expr= model.z4 >= demand[4]+model.d1_rhs - model.y4)
model.constraint_stage.declare(model.s43, 2)
model.stoch_rhs.declare(model.s43)
###########################################################################
model.s51 = Constraint(expr= model.y5 == model.x4+ model.delta4)
model.constraint_stage.declare(model.s51, 2)

model.s52 = Constraint(expr= model.x5 >= model.y5-demand[5]-model.d1_rhs)
model.constraint_stage.declare(model.s52, 2)
model.stoch_rhs.declare(model.s52)

model.s53 = Constraint(expr= model.z5 >= demand[5]+model.d1_rhs - model.y5)
model.constraint_stage.declare(model.s53, 2)
model.stoch_rhs.declare(model.s53)
#
# these one constraints have stochastic right-hand-sides
#
# model.d1 = Constraint(expr = 3.1470 + 0.046*model.x1 + 0.184*model.x2 - model.y1 - model.y2 >=model.d1_rhs)
# model.constraint_stage.declare(model.d1, 2)
# model.stoch_rhs.declare(model.d1)

# always define the objective as the sum of the stage costs
model.obj = Objective(expr=model.FirstStageCost + model.SecondStageCost)

def pysp_scenario_tree_model_callback():
    from pyomo.pysp.scenariotree.tree_structure_model import \
        CreateConcreteTwoStageScenarioTreeModel

    st_model = CreateConcreteTwoStageScenarioTreeModel(num_scenarios)

    first_stage = st_model.Stages.first()
    second_stage = st_model.Stages.last()

    # First Stage
    st_model.StageCost[first_stage] = 'FirstStageCost'
    st_model.StageVariables[first_stage].add('delta1')
    st_model.StageVariables[first_stage].add('delta2')
    st_model.StageVariables[first_stage].add('delta3')
    st_model.StageVariables[first_stage].add('delta4')
    #st_model.StageVariables[first_stage].add('delta5')

    # Second Stage
    st_model.StageCost[second_stage] = 'SecondStageCost'
    st_model.StageVariables[second_stage].add('y1')
    st_model.StageVariables[second_stage].add('y2')
    st_model.StageVariables[second_stage].add('y3')
    st_model.StageVariables[second_stage].add('y4')
    st_model.StageVariables[second_stage].add('y5')

    st_model.StageVariables[second_stage].add('z1')
    st_model.StageVariables[second_stage].add('z2')
    st_model.StageVariables[second_stage].add('z3')
    st_model.StageVariables[second_stage].add('z4')
    st_model.StageVariables[second_stage].add('z5')

    st_model.StageVariables[second_stage].add('x1')
    st_model.StageVariables[second_stage].add('x2')
    st_model.StageVariables[second_stage].add('x3')
    st_model.StageVariables[second_stage].add('x4')
    st_model.StageVariables[second_stage].add('x5')
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
