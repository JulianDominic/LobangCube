import pickle
import sqlite3
import pandas as pd
import numpy as np
import altair as alt

df = pd.read_csv('../data/mock_users.csv')
conn = sqlite3.connect('../data/user_data.db')
df.to_sql('people', conn, if_exists='replace', index=False)

conn.close()

loaded_qol_model = pickle.load(open("./models/qol_model.pickle", 'rb'))
loaded_retirement_model = pickle.load(open("./models/retirement_model.pickle", 'rb'))
loaded_disaster_model = pickle.load(open("./models/disaster_model.pickle", 'rb'))
loaded_scaler = pickle.load(open("./models/scaler.pickle",'rb'))


def getInfo(age,housing,income,cpf,exp,saving):
    scaled = loaded_scaler.transform([[age,housing,income,cpf,exp,saving]])
    print(scaled)
    qol = loaded_qol_model.predict(scaled)
    dis = loaded_disaster_model.predict(scaled)
    ret = loaded_retirement_model.predict(scaled)
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
    scaled = loaded_scaler.transform([[age,housing,income,cpf,exp,saving]])

    initial = loaded_qol_model.predict(scaled)
    
    qol_list = []
    for i in range(len(scaled[0])):
        temp = scaled
        temp[0][i] += 0.05
        qol_list.append(loaded_qol_model.predict(temp)-initial)
    
    qol_list = [float(arr[0]) for arr in qol_list]
    
    ans = [x for _, x in sorted(zip(qol_list, params))]
    return ans

def disaster_suggestion(age,housing,income,cpf,exp,saving):
    params = ["age","housing","income","cpf","expenses","savings"]
    scaled = loaded_scaler.transform([[age,housing,income,cpf,exp,saving]])
    initial = loaded_disaster_model.predict(scaled)
    print(initial)
    
    disaster_list = []
    for i in range(len(scaled[0])):
        temp = scaled
        temp[0][i] += 0.05
        disaster_list.append(loaded_disaster_model.predict(temp)-initial)

    disaster_list = [float(arr[0]) for arr in disaster_list]
    ans = [x for _, x in sorted(zip(disaster_list, params))]
    return ans

def retirement_suggestion(age,housing,income,cpf,exp,saving):
    params = ["age","housing","income","cpf","expenses","savings"]
    scaled = loaded_scaler.transform([[age,housing,income,cpf,exp,saving]])
    initial = loaded_retirement_model.predict(scaled)
    
    retirement_list = []
    for i in range(len(scaled[0])):
        temp = scaled
        temp[0][i] += 0.05
        retirement_list.append(loaded_retirement_model.predict(temp)-initial)
    retirement_list = [float(arr[0]) for arr in retirement_list]
    ans = [x for _, x in sorted(zip(retirement_list, params))]
    return ans


def chart(age,housing,income,cpf,exp,saving,ageslider):
    
    agelist = [i for i in range(ageslider-age)]
    qol_scorelist = []
    dis_scorelist = []
    ret_scorelist = []
    for i in range(ageslider-age):
        scaled = loaded_scaler.transform([[age,housing,income,cpf,exp,saving]])
        ret_scorelist.append(loaded_retirement_model.predict(scaled)[0])
        qol_scorelist.append(loaded_qol_model.predict(scaled)[0])
        dis_scorelist.append(loaded_disaster_model.predict(scaled)[0])
        age+=1
        cpf+=0.2*income
        saving+=income*0.8-exp

    df = pd.DataFrame(data = {'age': agelist,'QOL score':qol_scorelist,'Disaster score':dis_scorelist, 'Retirement score': ret_scorelist})
    return df
    
