#-----------Connecting to the external systems & stylesheets--------------------------
import sys

import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import date
from plotly.io._renderers import show
from plotly.graph_objs.surface.contours import y

import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

username = 'JesseLinden'
api_key =  'uAVeMPCoDHLsTPUKzdbl'
chart_studio.tools.set_credentials_file(username='JesseLinden', api_key='uAVeMPCoDHLsTPUKzdbl')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#------------------Organising the Data in Pandas---------------------------

df = pd.read_csv("draaiboek.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
df = df.fillna(0)

loonkosten = df.loc[ 
    (df['Categorie'] == '4000 - Bruto loon') |
    (df['Categorie'] == '40004 - Overwerk') |
    (df['Categorie'] == '40016 - Subsidie personeelskosten') |
    (df['Categorie'] == '4002 - Loonkosten voorschot') |
    (df['Categorie'] == '4004 - Overwerk') |
    (df['Categorie'] == '4008 - Kosten vakantiegeld')  
]
# print(pers_kosten[:10])

sociallasten = df.loc[ 
    (df['Categorie'] == '4040 - Sociale lasten')
]

pensioen = df.loc[ 
    (df['Categorie'] == '40151 - Pensioenpremies') |
    (df['Categorie'] == '4042 - Pensioenpremies') 
]

overig = df.loc[ 
    (df['Categorie'] == '4021 - Kosten nettovergoedingen') |
    (df['Categorie'] == '4028 - Overige personeelskosten') |
    (df['Categorie'] == '4031 - Vergoeding reiskosten voorzover boven € 0,19 per kilometer') |
    (df['Categorie'] == '40313 - Reiskostenverg.belast') |
    (df['Categorie'] == '4038 - Vergoeding reiskosten (tot € 0,19) per kilometer') |
    (df['Categorie'] == '40381 - Reiskostenverg. Onbelast') |
    (df['Categorie'] == '40480 - Overige werkkosten - transitievergoeding vanuit forfait WKR') |
    (df['Categorie'] == '4200 - Werken derden') |
    (df['Categorie'] == '4201 - Werken derden verlegd') |
    (df['Categorie'] == '4340 - Studie en opleiding') |
    (df['Categorie'] == '4345 - Coaching') |
    (df['Categorie'] == '4346 - Training') |
    (df['Categorie'] == '4350 - Verzekeringen personeel') |
    (df['Categorie'] == '4370 - Kantinekosten Houten') |
    (df['Categorie'] == '4481 - Eigen bijdrage leaseauto') |
    (df['Categorie'] == '4700 - Managementfee') |
    (df['Categorie'] == '4710 - Accountantskosten') 
]

auto = df.loc[  
    (df['Categorie'] == '4400 - Brandstoffen TE') |
    (df['Categorie'] == '4410 - Onderhoud auto') |
    (df['Categorie'] == '44120 - Autokosten Binnen EU') |
    (df['Categorie'] == '4420 - Parkeerkosten') |
    (df['Categorie'] == '4440 - Leasekosten') |
    (df['Categorie'] == '4460 - Huur auto\'s') |
    (df['Categorie'] == '4470 - Boetes en bekeuringen') |
    (df['Categorie'] == '4490 - Overige autokosten')
]

verkoop = df.loc[  
    (df['Categorie'] == '45013 - Verkoopprovisie') |
    (df['Categorie'] == '4510 - Sponsoring en giften') |
    (df['Categorie'] == '4515 - Relatiegeschenken') |
    (df['Categorie'] == '4520 - Representatiekosten') |
    (df['Categorie'] == '4525 - Zakelijke diners/overwerk eten') |
    (df['Categorie'] == '4590 - Verkoopkosten') |
    (df['Categorie'] == '4716 - Incassokosten') |
    (df['Categorie'] == '4718 - Marketing')
]

kantoor = df.loc[  
    (df['Categorie'] == '4310 - Porti') |
    (df['Categorie'] == '4600 - Kantoorbenodigdheden') |
    (df['Categorie'] == '4601 - Kantoorinventaris') |
    (df['Categorie'] == '4607 - Computerkosten/ICT') |
    (df['Categorie'] == '4610 - Vakliteratuur') |
    (df['Categorie'] == '4625 - Drukwerk') |
    (df['Categorie'] == '4630 - Vaste telefonie') |
    (df['Categorie'] == '4631 - Mobiele telefonie') |
    (df['Categorie'] == '4635 - Internet, reclame') |
    (df['Categorie'] == '4640 - BIM software & licenties') |
    (df['Categorie'] == '4641 - Kennisbank licenties & software') |
    (df['Categorie'] == '4650 - Contributies & abonnementen') |
    (df['Categorie'] == '4685 - Certificering/kwaliteitsmanagement') |
    (df['Categorie'] == '4689 - Kantoorkosten Diensten Binnen EU') |
    (df['Categorie'] == '4690 - Overige kantoorkosten') 
]

algemeen = df.loc[  
    (df['Categorie'] == '4299 - Betalingsverschillen inkoop/verkoop') |
    (df['Categorie'] == '4301 - VST Fire Solutions BV') |
    (df['Categorie'] == '4311 - Assurantiepremie') |
    (df['Categorie'] == '4320 - Vergoeding woon-werk') |
    (df['Categorie'] == '4325 - Werkkosten') |
    (df['Categorie'] == '43507 - Betalingsverschillen inkoop') |
    (df['Categorie'] == '43508 - Betalingsverschillen verkoop') |
    (df['Categorie'] == '4358 - Overige administratieve lasten') |
    (df['Categorie'] == '4715 - Advieskosten') |
    (df['Categorie'] == '4725 - Juridische kosten') |
    (df['Categorie'] == '4740 - Verzekeringen, algemeen') |
    (df['Categorie'] == '4811 - Boete belastingdienst') |
    (df['Categorie'] == '4820 - Bankkosten') |
    (df['Categorie'] == '4970 - Afschrijving hard/software') |
    (df['Categorie'] == '5550 - Algemene kosten')
]

huisvesting = df.loc[ 
    (df['Categorie'] == '4100 - Huur Houten') |
    (df['Categorie'] == '4120 - Schoonmaakkosten') |
    (df['Categorie'] == '4130 - Afval (container)') |
    (df['Categorie'] == '4190 - Overige huisvestingskosten') 
]

pers_kosten_drop = df[ 
    (df['Categorie'] == '4000 - Bruto loon') |
    (df['Categorie'] == '40004 - Overwerk') |
    (df['Categorie'] == '40016 - Subsidie personeelskosten') |
    (df['Categorie'] == '4002 - Loonkosten voorschot') |
    (df['Categorie'] == '4004 - Overwerk') |
    (df['Categorie'] == '4008 - Kosten vakantiegeld')  |

    (df['Categorie'] == '4040 - Sociale lasten') |

    (df['Categorie'] == '40151 - Pensioenpremies') |
    (df['Categorie'] == '4042 - Pensioenpremies') |
    
    (df['Categorie'] == '4021 - Kosten nettovergoedingen') |
    (df['Categorie'] == '4028 - Overige personeelskosten') |
    (df['Categorie'] == '4031 - Vergoeding reiskosten voorzover boven € 0,19 per kilometer') |
    (df['Categorie'] == '40313 - Reiskostenverg.belast') |
    (df['Categorie'] == '4038 - Vergoeding reiskosten (tot € 0,19) per kilometer') |
    (df['Categorie'] == '40381 - Reiskostenverg. Onbelast') |
    (df['Categorie'] == '40480 - Overige werkkosten - transitievergoeding vanuit forfait WKR') |
    (df['Categorie'] == '4200 - Werken derden') |
    (df['Categorie'] == '4201 - Werken derden verlegd') |
    (df['Categorie'] == '4340 - Studie en opleiding') |
    (df['Categorie'] == '4345 - Coaching') |
    (df['Categorie'] == '4346 - Training') |
    (df['Categorie'] == '4350 - Verzekeringen personeel') |
    (df['Categorie'] == '4370 - Kantinekosten Houten') |
    (df['Categorie'] == '4481 - Eigen bijdrage leaseauto') |
    (df['Categorie'] == '4700 - Managementfee') |
    (df['Categorie'] == '4710 - Accountantskosten') |

    (df['Categorie'] == '4400 - Brandstoffen TE') |
    (df['Categorie'] == '4410 - Onderhoud auto') |
    (df['Categorie'] == '44120 - Autokosten Binnen EU') |
    (df['Categorie'] == '4420 - Parkeerkosten') |
    (df['Categorie'] == '4440 - Leasekosten') |
    (df['Categorie'] == '4460 - Huur auto\'s') |
    (df['Categorie'] == '4470 - Boetes en bekeuringen') |
    (df['Categorie'] == '4490 - Overige autokosten') |

    (df['Categorie'] == '45013 - Verkoopprovisie') |
    (df['Categorie'] == '4510 - Sponsoring en giften') |
    (df['Categorie'] == '4515 - Relatiegeschenken') |
    (df['Categorie'] == '4520 - Representatiekosten') |
    (df['Categorie'] == '4525 - Zakelijke diners/overwerk eten') |
    (df['Categorie'] == '4590 - Verkoopkosten') |
    (df['Categorie'] == '4716 - Incassokosten') |
    (df['Categorie'] == '4718 - Marketing') |

    (df['Categorie'] == '4310 - Porti') |
    (df['Categorie'] == '4600 - Kantoorbenodigdheden') |
    (df['Categorie'] == '4601 - Kantoorinventaris') |
    (df['Categorie'] == '4607 - Computerkosten/ICT') |
    (df['Categorie'] == '4610 - Vakliteratuur') |
    (df['Categorie'] == '4625 - Drukwerk') |
    (df['Categorie'] == '4630 - Vaste telefonie') |
    (df['Categorie'] == '4631 - Mobiele telefonie') |
    (df['Categorie'] == '4635 - Internet, reclame') |
    (df['Categorie'] == '4640 - BIM software & licenties') |
    (df['Categorie'] == '4641 - Kennisbank licenties & software') |
    (df['Categorie'] == '4650 - Contributies & abonnementen') |
    (df['Categorie'] == '4685 - Certificering/kwaliteitsmanagement') |
    (df['Categorie'] == '4689 - Kantoorkosten Diensten Binnen EU') |
    (df['Categorie'] == '4690 - Overige kantoorkosten') |

    (df['Categorie'] == '4299 - Betalingsverschillen inkoop/verkoop') |
    (df['Categorie'] == '4301 - VST Fire Solutions BV') |
    (df['Categorie'] == '4311 - Assurantiepremie') |
    (df['Categorie'] == '4320 - Vergoeding woon-werk') |
    (df['Categorie'] == '4325 - Werkkosten') |
    (df['Categorie'] == '43507 - Betalingsverschillen inkoop') |
    (df['Categorie'] == '43508 - Betalingsverschillen verkoop') |
    (df['Categorie'] == '4358 - Overige administratieve lasten') |
    (df['Categorie'] == '4715 - Advieskosten') |
    (df['Categorie'] == '4725 - Juridische kosten') |
    (df['Categorie'] == '4740 - Verzekeringen, algemeen') |
    (df['Categorie'] == '4811 - Boete belastingdienst') |
    (df['Categorie'] == '4820 - Bankkosten') |
    (df['Categorie'] == '4970 - Afschrijving hard/software') |
    (df['Categorie'] == '5550 - Algemene kosten') |

    (df['Categorie'] == '4100 - Huur Houten') |
    (df['Categorie'] == '4120 - Schoonmaakkosten') |
    (df['Categorie'] == '4130 - Afval (container)') |
    (df['Categorie'] == '4190 - Overige huisvestingskosten') 
].index
df.drop(pers_kosten_drop, inplace=True)
# print(df)

#Append
som_loonkosten = pd.DataFrame(loonkosten.sum()).T
som_loonkosten['Categorie'] = 'Loonkosten'
som_sociallasten = pd.DataFrame(sociallasten.sum()).T
som_sociallasten['Categorie'] = 'Sociale lasten'
som_pensioen = pd.DataFrame(pensioen.sum()).T
som_pensioen['Categorie'] = 'Pensioenen'
som_overig = pd.DataFrame(overig.sum()).T
som_overig['Categorie'] = 'Overige personeelskosten'
som_verkoop = pd.DataFrame(verkoop.sum()).T
som_verkoop['Categorie'] = 'Verkoop kosten'
som_auto = pd.DataFrame(auto.sum()).T
som_auto['Categorie'] = 'Auto kosten'
som_kantoor = pd.DataFrame(kantoor.sum()).T
som_kantoor['Categorie'] = 'Kantoor kosten'
som_algemeen = pd.DataFrame(algemeen.sum()).T
som_algemeen['Categorie'] = 'Algemene kosten'
som_huisvesting = pd.DataFrame(huisvesting.sum()).T
som_huisvesting['Categorie'] = 'Huisvestigingskosten'
# print(som_loonkosten)

df = df.append(som_loonkosten, ignore_index=True)
df = df.append(som_sociallasten, ignore_index=True)
df = df.append(som_pensioen, ignore_index=True)
df = df.append(som_overig, ignore_index=True)
df = df.append(som_auto, ignore_index=True)
df = df.append(som_verkoop, ignore_index=True)
df = df.append(som_kantoor, ignore_index=True)
df = df.append(som_algemeen, ignore_index=True)
df = df.loc[df['heel2020'] > 1000] 


df1 = pd.read_csv("draaiboek.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
df1 = df1.fillna(0)
df1 = df1.loc[df1['heel2020'] > 10000]

# df2 = df

df3 = df1['heel2020'].sum()
# new_row ={'Categorie':'Overige Kosten', 'heel2020':df3}
# print(new_row)
df2= df
df2 = df2.fillna(0)


# df3 = df2.iloc['Totaal','heel2020']
# print (df3)

dg = pd.read_csv("winstboek.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
dg = dg.fillna(0)
# dg = dg.set_index(dg['Categorie'])
dg = dg.loc[(dg['Categorie']=='Omzet') | (dg['Categorie']=='Resultaat')]
dgg = dg.T
new_header = dgg.iloc[0]
dgg = dgg[1:]
dgg.columns = new_header

# dgg = dgg.set_index('maand')
maanden = ['Januari','Februari','Maart','April','Mei','Juni','Juli','Augustus','September','Oktober','November','December','Jaar']
dgg.insert(loc=0, column='Maand', value=maanden)
heel_2020 = dgg.loc[dgg['Maand'] == 'Jaar'].index
dgg.drop(heel_2020, inplace=True)
dgg['Omzet'] = abs(dgg['Omzet'])
dgg['Kosten'] = dgg['Omzet'] - dgg['Resultaat']
dgg['Totale omzet']=dgg['Omzet'].cumsum(axis = 0) 
dgg['Totale kosten']=dgg['Kosten'].cumsum(axis = 0) 
dgg['Totale winst']=dgg['Resultaat'].cumsum(axis = 0)
# print(dgg)

# dg['Kosten'] = dg['Omzet'] - dg['Resultaat']
# print(dg)



dh = pd.read_csv("simpeldraai.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
dh.columns = dh.columns.astype(str)
dh['Totale omzet']=dh['Omzet'].cumsum(axis = 0) 
dh['Totale kosten']=dh['Kosten'].cumsum(axis = 0) 
dh['Totale winst']=dh['Resultaat'].cumsum(axis = 0) 


dh1 = pd.read_csv("simpeldraai20211.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
dh1 = dh1.fillna(0)
dh1.columns = dh1.columns.astype(str)


dh1['Totale omzet']=dh1['Omzet'].cumsum(axis = 0)
dh1['Totale kosten']=dh1['Kosten'].cumsum(axis = 0)
dh1['Totale winst']=dh1['Resultaat'].cumsum(axis = 0)

# doelstelling = 3000000.0
# reeks = np.arange(1, 10, 11)
# print(reeks)
dh1['Omzet doelstelling'] = [250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000,3000000]

# print(dh1[:14])


di = pd.read_csv("FinBalanceSheet2021.csv", error_bad_lines=False, lineterminator='\n', encoding='latin-1')
di = di.fillna(0)
# dg = dg.set_index(dg['Categorie'])
di = di.loc[(di['Categorie']=='8000 - Omzet BI') | (di['Categorie']=='Resultaat')]
dii = di.T
new_header = dii.iloc[0]
dii = dii[1:]
dii.columns = new_header

# dgg = dgg.set_index('maand')
maanden = ['Januari','Februari','Maart','April','Mei','Juni','Juli','Augustus','September','Oktober','November','December','Jaar']
dii.insert(loc=0, column='Maand', value=maanden)
heel_2021 = dii.loc[dii['Maand'] == 'Jaar'].index
dii.drop(heel_2021, inplace=True)
dii['Omzet'] = abs(dii['8000 - Omzet BI'])
dii['Kosten'] = dii['Omzet'] - dii['Resultaat']
dii['Totale omzet']=dii['Omzet'].cumsum(axis = 0) 
dii['Totale kosten']=dii['Kosten'].cumsum(axis = 0) 
dii['Totale winst']=dii['Resultaat'].cumsum(axis = 0)
# print(dii)




#----------------Non-interactive plotly graphs-----------------------

fig = px.pie(df2,
    values='heel2020',
    names='Categorie',
    labels='Categorie',
    title='Kostenanalyse',
    hover_name="Categorie",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    # text='Alles boven de €8000',
    # height=750,
)

fig.update_layout(
        hoverlabel=dict(
        bgcolor="white",
        font_size=10,
        font_family="Rockwell"),
        showlegend=True,
        legend_title="Categoriën van kosten",
        font=dict(
        size=14,
        color='rgb(50,50,50)'),
    )
    
fig1 = px.pie(df1,
    values='heel2020',
    names='Categorie',
    labels='Categorie',
    title='Kostenanalyse draaiboek',
    # text='test',
    hover_name="Categorie",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    # height=600,
)

fig1.update_layout(
        hoverlabel=dict(
        bgcolor="white",
        font_size=10,
        font_family="Rockwell"),
        showlegend=True,
        legend_title="Categoriën van kosten",
        font=dict(
        size=14,
        color='rgb(50,50,50)'),
    )

fig2 = px.line(dgg,
        x = 'Maand',
        y = ['Totale omzet','Totale kosten','Totale winst'],
        color_discrete_sequence=px.colors.qualitative.D3,
        )

fig2.update_layout(
    title='Omzet, kosten en resultaat 2020',
    xaxis_title="Tijd in maanden",
    yaxis_title="Omzet, kosten en winst in €",
    # legend_title="Legend Title",
    font=dict(
        size=14,
        color='rgb(50,50,50)',
    )
)

fig3 = px.line(dh1,
        x = 'Categorie',
        y = ['Totale omzet','Totale kosten','Totale winst','Omzet doelstelling'],
        color_discrete_sequence=px.colors.qualitative.G10,
        )

fig3.update_layout(
    title='Omzet, kosten en resultaat 2021 Met prognose doelstelling',
    xaxis_title="Tijd in maanden",
    yaxis_title="Omzet, kosten en winst in €",
    # legend_title="Legend Title",
    font=dict(
        size=14,
        color='rgb(50,50,50)',
    )
)

# Adding labels
annotations = []

# Source
annotations.append(dict(xref='paper', yref='paper', x=0.05, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text='Kosten boven €10.000',
                              font=dict(family='Arial',
                                        size=16,
                                        color='rgb(50,50,50)'),
                              showarrow=False))

fig1.update_layout(annotations=annotations)


#----------------HTML layout-----------------------

app.layout = html.Div([

    html.Div([
     html.Div([   
         html.H1(['Financieel Dashboard'], 
                  style={'align-text':'center'},),
         html.Br(),
         html.Div([
            dcc.Graph(figure=fig)     
         ],
        style={"border":"1px black solid",
                    "margin":"4px",
                    "padding":"4px"},
        className="six columns"),

        html.Div([
            dcc.Graph(figure=fig2)
            ],
            style={"border":"1px black solid",
                   "margin":"6px",
                    "padding":"6px"
            },
        className="six columns"),

        html.Div([
        
        ],
        
        className="four columns"),
        html.Br(),
        
     ]),

    #  html.Div([html.H1('l')]),
    #  html.Br(),
    #  html.Div([html.H1('l')]),
    #  html.Br(),
    #  html.Div([html.H1('l')]),
    #  html.Br(),
    #  html.Div([html.H1('l')]),
    #  html.Br(),

     html.Div([   
        html.Div([
            dcc.Graph(figure=fig1)  
        ],
        style={"border":"2px black solid",
                "margin":"4px",
                "padding":"4px"},
        className="six columns"),

        html.Div([
            dcc.Graph(figure=fig3)
        ],
        style={"border":"2px black solid",
                "margin":"4px",
                "padding":"4px"},
        className="six columns"),

        html.Div([
            # dcc.Graph(figure=fig3)
            ],
            className="four columns"),
     ])   
    ])        
])  


#---------Dash Callback with graph-------------------------

# @app.callback(
#     Output('graph', 'figure'),
#     [Input('persoon','value')]
# )

# def build_graph(name):
    
#     return

if __name__ == '__main__':
    app.run_server(debug=True, port=8040)

