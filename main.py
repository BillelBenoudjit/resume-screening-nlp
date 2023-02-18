import dash
import pickle
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc, html, Output, Input, State

from pdf_reader import parse_contents

# Default values for styling
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
server = app.server

# Get the ner model
filename = "ner_resumes.sav"
nlp = pickle.load(open(filename, 'rb'))
# Soumya Balan Soumya Balan - BE Computer Science - 3 yr Work Experience at Microsoft Corporation  Thiruvananthapuram, Kerala - Email me on Indeed: indeed.com/r/Soumya- Balan/8c7fbb9917935f20  ➢ To work in a progressive organization where I can enhance my skills and learning to contribute to the success of the organization.  Willing to relocate: Anywhere  WORK EXPERIENCE  Technical Support Engineer  Microsoft iGTSC -  Bengaluru, Karnataka -  July 2013 to October 2015  Position: TECHNICAL SUPPORT ENGINEER  Company: Microsoft Corporation - Microsoft India Global Technical Support Center (Microsoft IGTSC), Bangalore  Years of Experience: 2 Years and 4 Months  Responsibilities  ➢ Represent Microsoft and communicate with corporate customers via telephone, written correspondence, or electronic service regarding technically complex escalated problems identified in Microsoft software products, and manage relationships with those customers.  ➢ Manage not only the technically complex problems, but also politically charged situations requiring the highest level of customer skill.  ➢ Receive technically complex, critical or politically hot customer issues, and maintain ownership of issue until resolved completely.  ➢ Solve highly complex problems, involving broad, in-depth product knowledge or in-depth product specialty.  ➢ Use trace analysis, and other sophisticated tools to analyze problems and develop solutions to meet customer needs.  ➢ Lead triage meetings to share knowledge with other engineers and develop customer solutions efficiently.  ➢ Act as technical lead, mentor, and model for a team of engineers, provide direction to others, review solutions and articles, mentoring existing & aspiring Engineers.  https://www.indeed.com/r/Soumya-Balan/8c7fbb9917935f20?isid=rex-download&ikw=download-top&co=IN https://www.indeed.com/r/Soumya-Balan/8c7fbb9917935f20?isid=rex-download&ikw=download-top&co=IN   ➢ Write technical articles for knowledge base.  ➢ Consult, collaborate and take escalations when necessary.  ➢ Maintain working knowledge of pre-release products and take ownership for improvement in key technical areas.  ➢ Manage customer escalations and recognize when to solicit additional help. Participate in technical discussions and engage with product team if required to resolve issues and represent customer segments.  Exchange Server Knowledge  ➢ Exchange Server 2007 ➢ Exchange Server 2010 ➢ Exchange Server 2013 ➢ O365  EDUCATION  BE in Computer Science and Engineering  Vivekananda Engineering College for Women -  Chennai, Tamil Nadu  2013  BTEC HNC in Aviation  Frankfinn Institute of Airhostess Training -  Calicut, Kerala  2008  State Board +2  2007  SSLC  State  2005  SKILLS  DBMS, O365, Communication Skills, Exchange 2013, Hospitality, Networking, Computer Operating, Programming, Computer Hardware, Java, Exchange 2010, Teaching  ADDITIONAL INFORMATION  Skill Set ➢ Excellent communication and interpersonal skills.    ➢ Proficient in Computer Applications -Microsoft Office Windows (Windows 2007, XP, 8, 8.1 and Windows 10), Linux, Fedora. ➢ Strong analytical and problem solving skills. ➢ Ability in managing a team of professionals and enjoy being in a team.  Project Details  UG PROJECT TITLE: Memory Bounded Anytime Heuristic Search A* Algorithm  ➢ This Project presents a heuristic-search algorithm called Memory-bounded Anytime Window A* (MAWA*), which is complete, anytime, and memory bounded. MAWA* uses the window-bounded anytime-search methodology of AWA* as the basic framework and combines it with the memory- bounded A* -like approach to handle restricted memory situations. Simple and efficient versions of MAWA* targeted for tree search have also been presented. Experimental results of the sliding-tile puzzle problem and the traveling-salesman problem show the significant advantages of the proposed algorithm over existing methods.  Technical and Co-Curricular activities  ➢ Star Performer in Microsoft IGTSC in 2014. ➢ Paper Presentations on Applications of Robotics in INOX 2K12. ➢ Attended a Three-Day workshop on C and C++ Programming and Aliasing. ➢ Attended a One-Day workshop on Java and Hardware Workshop at VECW ➢ Paper presentation 4G Technologies, Cloud Computing, Heuristic Algorithms and Applications, Open Source Software. ➢ Multimedia presentations on Artificial Intellegence, 6th Sense, and Robotics. ➢ Completed training of OCA (9i, 10g) from Oracle University. ➢ Attended SPARK training program in Infosys Mysore. ➢ Attended System Hardware Training program at HCL, Pondicherry.

# Define the application components
appTitle = dcc.Markdown(children='# 📑 NER Resume Screening App')
inputPart = dcc.Markdown(children="##### Please insert your resume in the text input or upload it for screening.")
resumeUploader = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File (.pdf)')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )
resumeInput = dbc.Textarea(
    id='resume-input',
    value='',
    style={'width': '100%'},
    rows="6"
)
outputPart = dcc.Markdown(children="##### Here comes the screening of the resume.")
resumeRecognition = html.Div(children="")
matchPart = dcc.Markdown(children="##### Skills matching.")
skillsInputLabel = dbc.Label("Add the wanted skills below.")
skillsInput = dbc.Input(id='skills-input', placeholder="Skills goes here...", type="text", value="")
skillsInputFormText = dbc.FormText("The skills should be separated by a commas ','.")
skillsButton = dbc.Button("Match Skills", id='skills-button', color="primary", className="me-1", n_clicks=0)
skillsMatching = dcc.Markdown(children="", style={'margin-top': '5px'})

# Define de app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([appTitle], width=6)
    ], justify='center'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Row([
               dbc.Col([inputPart], width=12)
            ], justify='center', style={'text-align': 'justify'}),
            dbc.Row([
               dbc.Col([resumeUploader], width=12)
            ], justify='right')
        ], width=3),
        dbc.Col([resumeInput], width=7)
    ], justify='center'),
    dbc.Row([
        dbc.Col([outputPart], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([resumeRecognition], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([matchPart], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            skillsInputLabel,
            skillsInput,
            skillsInputFormText,
            skillsButton
        ], width=10)
    ], justify='center'),
    dbc.Row([
        dbc.Col([skillsMatching], width=10)
    ], justify='center')
], fluid=True)


# Resume matching callback
@app.callback(
    Output('resume-input', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children[0]


# Named entity recognition callback
@app.callback(
    Output(resumeRecognition, component_property='children'),
    Input(resumeInput, component_property='value')
)
def render(text):
    if text is not None:
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


def entity_name(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "2",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem"
    })


def entity_box(children, color):
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
    children.append(entity_name(name))
    color = DEFAULT_LABEL_COLORS[name]
    return entity_box(children, color)


# Display callback
@app.callback(
    Output(outputPart, component_property='style'),
    Output(matchPart, component_property='style'),
    Output(skillsInputLabel, component_property='style'),
    Output(skillsInput, component_property='style'),
    Output(skillsInputFormText, component_property='style'),
    Output(skillsButton, component_property='style'),
    Output(resumeRecognition, component_property='style'),
    Input(resumeInput, component_property='value')
)
def show_text(text):
    if text is None:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
            {'display': 'none'}, {'display': 'none'}, \
            {'display': 'none'}, {'display': 'none'}
    else:
        return {'display': 'block', 'margin-top': '5px'}, \
            {'display': 'block'}, \
            {'display': 'block'}, \
            {'display': 'block'}, \
            {'display': 'block', 'margin-top': '5px'}, \
            {'display': 'block', 'margin-top': '5px'}, \
            {'display': 'block',
             'flex-direction': 'column',
             'overflow-y': 'scroll',
             'overflow-x': 'hidden',
             'scrollbar-width': 'thin',
             'height': '150px',
             'width': '100%',
             'margin-right': 'auto',
             'margin-left': 'auto',
             'border': '5px solid rgb(194, 219, 254)',
             'border-radius': '10px',
             'padding': '10px 20px',
             'text-align': 'justify',
             'line-height': '2.5',
             'direction': 'ltr'}


# Skills matching callback
@app.callback(
    Output(skillsMatching, component_property='children'),
    Input('skills-button', 'n_clicks'),
    State('resume-input', component_property='value'),
    State('skills-input', component_property='value')
)
def get_matching_score(n_clicks, text, skills):
    if len(skills) > 0:
        req_skills = skills.lower().split(",")
        resume_skills = unique_skills(get_skills(text))
        resume_skills = [skill.lower() for skill in resume_skills]
        score = 0
        for x in req_skills:
            if x in resume_skills[0]:
                score += 1
        req_skills_len = len(req_skills)
        match = round(score / req_skills_len * 100, 1)
        return f"##### The current Resume is {match}% matched to your requirements."


def get_skills(text):
    doc = nlp(text)
    skills_set = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "Skills":
            subset.append(ent.text)
    skills_set.append(subset)
    return subset


def unique_skills(x):
    return list(set(x))


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
