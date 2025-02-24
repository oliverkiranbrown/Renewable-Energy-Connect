from faker import Faker
import pandas as pd
import numpy as np

# define required categories
user_category = ['Community Energy Group', 'Asset Owner', 'Homeowner','Service Provider (Company)','Service Provider (Individual)', 'Product / System Installers']
professional_category = ['Legal','Planning Applications','System Design','Civil Engineering','Electrical Engineering','Groundworks','Fundraising','Finance']
project_stages = ['Project definition','Feasibility study','Heads of Terms','Legal & Finance','Build','Commision, Monitor and Maintain']

# make a list of colours for the different profesions
colour_choices = ['Bisque',
                  'Brown',
                  'BlueViolet',
                  'CadetBlue',
                  'GoldenRod',
                  'IndianRed',
                  'LightCoral',
                  'LightSkyBlue']
prof_colours = pd.DataFrame(professional_category,columns=['primary_professional_category'])
prof_colours['node_colour'] = colour_choices


# create fake companies
fake = Faker()

orgs = []
num_orgs = 100
for i in range(0,num_orgs):
    orgs.append(fake.company())

def gen_prob_vec(input_labels,val):
    return_list = np.append(input_labels,'NA')
    prob_vec = np.full(len(input_labels),val)
    prob_vec = np.append(prob_vec,1-sum(prob_vec))
    return (return_list, prob_vec)

# make a probability vector to assign secondary professional categories to fake data
val_1 = 0.03
val_2 = 0.01
secondary_prof_cat, secondary_prof_vec = gen_prob_vec(professional_category,val_1)
secondary_proj_cat, secondary_proj_vec = gen_prob_vec(project_stages,val_2)

# try force the stating node positions
x_ords = [10,400,600,350,200,100]
y_ords = [10,10,250,400,500,600]

# create the fake df
df = pd.DataFrame(data = orgs, columns=['name'])
df['primary_professional_category'] = np.random.choice(professional_category, size = len(df))
df['secondary_professional_category'] = np.random.choice(secondary_prof_cat,size = len(df), p = secondary_prof_vec)
df['primary_project_stage'] = np.random.choice(project_stages, size = len(df))
df['secondary_project_stage'] = np.random.choice(secondary_proj_cat, size = len(df), p = secondary_proj_vec)
df['node_size'] = 5
df = pd.merge(df,prof_colours,on='primary_professional_category',how='left')

# create a dataframe for the project stages
df_stages = pd.DataFrame(data = project_stages, columns=['stages'])
df_stages['node_colour'] = 'DarkSalmon'
df_stages['node_size'] = 70
df_stages['x'] = x_ords
df_stages['y'] = x_ords

# create the node dict of dicts
project_stages_nodes = []
for idx, row in df_stages.iterrows():
    project_stages_nodes.append((row['stages'], {"color": row.node_colour,
                                                 "size": row.node_size,
                                                 "x": row.x,
                                                 "y": row.y}
                                ))

# create the actor node dicts of dicts
actor_nodes = []
for idx, row in df.iterrows():
    actor_nodes.append((row['name'], {"Primary Professional Category":row.primary_professional_category,
                                               "secondary_professional_category":row.secondary_professional_category,
                                               "primary_project_stage": row.primary_project_stage,
                                               "secondary_project_stage": row.secondary_project_stage,
                                               "color": row.node_colour,
                                               "size": row.node_size}
                                               ))