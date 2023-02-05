import dash
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc

import pickle

DEFAULT_LABEL_COLORS = {
    "Skills": "#ffe599",
    "College Name": "#5e72e4",
    "Graduation Year": "#f4f5f7",
    "Designation": "#11cdef",
    "Name": "#2dce89",
    "Degree": "#f5365c",
    "Companies worked at": "#fb6340",
    "Location": "#849cbc",
    "Email Address": "#4a6a48",
    "Years of Experience": "#e0ecfc"
}

# Initialize the application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# text = "Soumya Balan Soumya Balan - BE Computer Science - 3 yr Work Experience at Microsoft Corporation  Thiruvananthapuram, Kerala - Email me on Indeed: indeed.com/r/Soumya- Balan/8c7fbb9917935f20  ➢ To work in a progressive organization where I can enhance my skills and learning to contribute to the success of the organization.  Willing to relocate: Anywhere  WORK EXPERIENCE  Technical Support Engineer  Microsoft iGTSC -  Bengaluru, Karnataka -  July 2013 to October 2015  Position: TECHNICAL SUPPORT ENGINEER  Company: Microsoft Corporation - Microsoft India Global Technical Support Center (Microsoft IGTSC), Bangalore  Years of Experience: 2 Years and 4 Months  Responsibilities  ➢ Represent Microsoft and communicate with corporate customers via telephone, written correspondence, or electronic service regarding technically complex escalated problems identified in Microsoft software products, and manage relationships with those customers.  ➢ Manage not only the technically complex problems, but also politically charged situations requiring the highest level of customer skill.  ➢ Receive technically complex, critical or politically hot customer issues, and maintain ownership of issue until resolved completely.  ➢ Solve highly complex problems, involving broad, in-depth product knowledge or in-depth product specialty.  ➢ Use trace analysis, and other sophisticated tools to analyze problems and develop solutions to meet customer needs.  ➢ Lead triage meetings to share knowledge with other engineers and develop customer solutions efficiently.  ➢ Act as technical lead, mentor, and model for a team of engineers, provide direction to others, review solutions and articles, mentoring existing & aspiring Engineers.  https://www.indeed.com/r/Soumya-Balan/8c7fbb9917935f20?isid=rex-download&ikw=download-top&co=IN https://www.indeed.com/r/Soumya-Balan/8c7fbb9917935f20?isid=rex-download&ikw=download-top&co=IN   ➢ Write technical articles for knowledge base.  ➢ Consult, collaborate and take escalations when necessary.  ➢ Maintain working knowledge of pre-release products and take ownership for improvement in key technical areas.  ➢ Manage customer escalations and recognize when to solicit additional help. Participate in technical discussions and engage with product team if required to resolve issues and represent customer segments.  Exchange Server Knowledge  ➢ Exchange Server 2007 ➢ Exchange Server 2010 ➢ Exchange Server 2013 ➢ O365  EDUCATION  BE in Computer Science and Engineering  Vivekananda Engineering College for Women -  Chennai, Tamil Nadu  2013  BTEC HNC in Aviation  Frankfinn Institute of Airhostess Training -  Calicut, Kerala  2008  State Board +2  2007  SSLC  State  2005  SKILLS  DBMS, O365, Communication Skills, Exchange 2013, Hospitality, Networking, Computer Operating, Programming, Computer Hardware, Java, Exchange 2010, Teaching  ADDITIONAL INFORMATION  Skill Set ➢ Excellent communication and interpersonal skills.    ➢ Proficient in Computer Applications -Microsoft Office Windows (Windows 2007, XP, 8, 8.1 and Windows 10), Linux, Fedora. ➢ Strong analytical and problem solving skills. ➢ Ability in managing a team of professionals and enjoy being in a team.  Project Details  UG PROJECT TITLE: Memory Bounded Anytime Heuristic Search A* Algorithm  ➢ This Project presents a heuristic-search algorithm called Memory-bounded Anytime Window A* (MAWA*), which is complete, anytime, and memory bounded. MAWA* uses the window-bounded anytime-search methodology of AWA* as the basic framework and combines it with the memory- bounded A* -like approach to handle restricted memory situations. Simple and efficient versions of MAWA* targeted for tree search have also been presented. Experimental results of the sliding-tile puzzle problem and the traveling-salesman problem show the significant advantages of the proposed algorithm over existing methods.  Technical and Co-Curricular activities  ➢ Star Performer in Microsoft IGTSC in 2014. ➢ Paper Presentations on Applications of Robotics in INOX 2K12. ➢ Attended a Three-Day workshop on C and C++ Programming and Aliasing. ➢ Attended a One-Day workshop on Java and Hardware Workshop at VECW ➢ Paper presentation 4G Technologies, Cloud Computing, Heuristic Algorithms and Applications, Open Source Software. ➢ Multimedia presentations on Artificial Intellegence, 6th Sense, and Robotics. ➢ Completed training of OCA (9i, 10g) from Oracle University. ➢ Attended SPARK training program in Infosys Mysore. ➢ Attended System Hardware Training program at HCL, Pondicherry."
filename = "ner_resumes.sav"
nlp = pickle.load(open(filename, 'rb'))


def entname(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "2",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem"
    })


def entbox(children, color):
    return html.Mark(children, style={
        "background": color,
        "padding": "0.45em 0.45em",
        "margin": "0 0.25em",
        "line-height": "0.7",
        "border-radius": "0.35em",
    })


def entity(children, name):
    if type(children) is str:
        children = [children]
    children.append(entname(name))
    color = DEFAULT_LABEL_COLORS[name]
    return entbox(children, color)


mytitle = dcc.Markdown(children='# NER Resume Screening')
myinput = dcc.Textarea(
    id='textarea-input',
    value='',
    style={'width': '100%', 'height': 200},
)
mytext = html.Div(children="")

# mytext = dcc.Textarea(id='textarea-output', value='', style={'width': '100%', 'height': 300})

# define de app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([myinput], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mytext], width=10)
    ], justify='center'),
], fluid=True)


@app.callback(
    Output(mytext, component_property='children'),
    Input(myinput, component_property='value')
)
def render(text):
    doc = nlp(text)
    children = []
    last_idx = 0
    for ent in doc.ents:
        children.append(doc.text[last_idx:ent.start_char])
        children.append(
            entity(doc.text[ent.start_char:ent.end_char], ent.label_))
        last_idx = ent.end_char
    children.append(doc.text[last_idx:])
    return children


@app.callback(
    Output(mytext, component_property='style'),
    Input(myinput, component_property='value')
)
def show_div(text):
    if len(text) == 0:
        return {'display': 'none'}
    else:
        return {
            'display': 'block',
            'flex-direction': 'column',
            'overflow-y': 'scroll',
            'overflow-x': 'hidden',
            'scrollbar-width': 'thin',
            'height': '200px',
            'width': '100%',
            'margin-right': 'auto',
            'margin-left': 'auto',
            'border': '10px solid black',
            'border-radius': '10px',
            'padding': '10px 20px',
            'text-align': 'justify'}


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
