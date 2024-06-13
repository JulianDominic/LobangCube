import pickle
import sqlite3
import pandas as pd
import altair as alt
import numpy as np

df = pd.read_csv('../data/mock_users.csv')
conn = sqlite3.connect('../data/user_data.db')
df.to_sql('people', conn, if_exists='replace', index=False)

conn.close()

# loaded_qol_model = pickle.load(open("./models/qol_model.pickle", 'rb'))
# loaded_retirement_model = pickle.load(open("./models/retirement_model.pickle", 'rb'))
# loaded_disaster_model = pickle.load(open("./models/disaster_model.pickle", 'rb'))
# loaded_scaler = pickle.load(open("./models/scaler.pickle",'rb'))
loaded_qol_model = pickle.load(open("./models/model_quality_of_life.pkl", 'rb'))
loaded_retirement_model = pickle.load(open("./models/model_retirement_readiness.pkl", 'rb'))
loaded_disaster_model = pickle.load(open("./models/model_disaster_preparedness.pkl", 'rb'))
loaded_encoder = pickle.load(open("./models/encoder.pkl",'rb'))
loaded_poly = pickle.load(open("./models/poly.pkl",'rb'))
with open('./models/scaler.pkl', 'rb') as file:
    loaded_scaler = pickle.load(file)

def process_data(params):
    age,housing,income,cpf,exp,saving = params
    feature_inputs = pd.DataFrame({
        'age': [age],
        'housingtype': [housing],
        'yearly_income': [income],
        'cpf_balance': [cpf],
        'yearly_expenditure': [exp],
        'savings': [saving]
    })
    feature_inputs.loc[:, 'housingtype'] = loaded_encoder.transform(feature_inputs[['housingtype']])
    feature_inputs_poly = loaded_poly.transform(feature_inputs)
    feature_inputs_scaled = loaded_scaler.transform(feature_inputs_poly)
    return feature_inputs_scaled


def getInfo(age,housing,income,cpf,exp,saving):
    params = age,housing,income,cpf,exp,saving
    feature_inputs = process_data([age,housing,income,cpf,exp,saving])
    qol = loaded_qol_model.predict(feature_inputs)
    dis = loaded_disaster_model.predict(feature_inputs)
    ret = loaded_retirement_model.predict(feature_inputs)
    return [qol,dis,ret]

def getLobang(qol,dis,ret):
    return round(((qol+dis+ret)/3)*10)

def get_user_data(name):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('../data/user_data.db')
    cursor = conn.cursor()
    query = "SELECT * FROM people WHERE name = ?"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    conn.close()
    
    return result

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=60, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=170, height=170)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Arial", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response}'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=60, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=170, height=170)
  return plot_bg + plot + text

def qol_suggestion(age,housing,income,cpf,exp,saving):
    params = ["age","housing","income","cpf","expenses","savings"]
    feature_inputs = process_data([age,housing,income,cpf,exp,saving])

    initial = loaded_qol_model.predict(feature_inputs)
    
    qol_list = []
    for i in range(len(feature_inputs[0])):
        temp = feature_inputs
        temp[0][i] += 0.05
        qol_list.append(loaded_qol_model.predict(temp)-initial)
    
    qol_list = [float(arr[0]) for arr in qol_list]
    
    ans = [x for _, x in sorted(zip(qol_list, params))]
    return ans

def disaster_suggestion(age,housing,income,cpf,exp,saving):
    params = ["age","housing","income","cpf","expenses","savings"]
    feature_inputs = process_data([age,housing,income,cpf,exp,saving])
    initial = loaded_disaster_model.predict(feature_inputs)
    
    disaster_list = []
    for i in range(len(feature_inputs[0])):
        temp = feature_inputs
        temp[0][i] += 0.05
        disaster_list.append(loaded_disaster_model.predict(temp)-initial)

    disaster_list = [float(arr[0]) for arr in disaster_list]
    ans = [x for _, x in sorted(zip(disaster_list, params))]
    return ans

def retirement_suggestion(age,housing,income,cpf,exp,saving):
    params = ["age","housing","income","cpf","expenses","savings"]
    feature_inputs = process_data([age,housing,income,cpf,exp,saving])
    initial = loaded_retirement_model.predict(feature_inputs)
    
    retirement_list = []
    for i in range(len(feature_inputs[0])):
        temp = feature_inputs
        temp[0][i] += 0.05
        retirement_list.append(loaded_retirement_model.predict(temp)-initial)
    retirement_list = [float(arr[0]) for arr in retirement_list]
    ans = [x for _, x in sorted(zip(retirement_list, params))]
    return ans
