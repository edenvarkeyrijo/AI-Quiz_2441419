import streamlit as st
import random, time, json, csv, io
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="AI Quest | DSC401-6", page_icon="🧠", layout="wide")
st.markdown("""



<style>
.stApp {
    background: linear-gradient(135deg, #f7f8ff 0%, #eef4ff 55%, #fdf2ff 100%);
    color: #24243e !important;
}

.block-container {
    padding-top: 2rem;
    max-width: 1150px;
}

/* Make normal page text readable */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span,
label,
[data-testid="stWidgetLabel"] {
    color: #34344f !important;
}

/* Purple banner */
.hero {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(120deg, #24245e, #6554c0, #9b5de5);
    color: #fafafa;
    margin-bottom: 18px;
}

.hero h1 {
    color: #fafafa !important;
    margin: 0;
    font-size: 2.4rem;
}

.hero p {
    color: #f1edff !important;
    font-size: 1.05rem;
}

/* Keep headings dark on the light background */
h1, h2, h3, h4,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #26264d !important;
}

/* White cards with dark text */
.metric,
.question {
    background: white;
    color: #34344f !important;
    border: 1px solid #e2e6f0;
    border-radius: 16px;
    padding: 16px;
}

.metric h2,
.metric h3,
.metric span,
.question p {
    color: #34344f !important;
}

.question {
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
}

.small {
    color: #5d6380 !important;
    font-size: .9rem;
}

/* Input boxes */
.stTextInput input,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #29294d !important;
    border: 1px solid #cfd4e8 !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #777b91 !important;
    opacity: 1 !important;
}

/* Dropdowns and multiselect */
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #29294d !important;
    border-color: #cfd4e8 !important;
}

.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] * {
    color: #29294d !important;
}

/* Create Quiz and other buttons */
.stButton > button,
.stButton > button:focus,
.stButton > button:active {
    background-color: #5b4bc4 !important;
    color: #ffffff !important;
    border: 1px solid #5b4bc4 !important;
    opacity: 1 !important;
}

/* Make all button contents readable */
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
}

/* Checkbox labels */
.stCheckbox label,
.stCheckbox label p {
    color: #34344f !important;
}

/* Dropdown option menu */
[data-baseweb="popover"] [role="option"] {
    background-color: #ffffff !important;
    color: #29294d !important;
}

</style>



<div class=><h1>🧠 AI QUEST</h1><p>· Artificial Intelligence ·<br>Learn it. Search it. Solve it.</p></div>
""", unsafe_allow_html=True)

DATA = [('Foundations of AI', 'Easy', 'MCQ', 'What is the main goal of Artificial Intelligence?', ['Make machines perform tasks requiring human-like intelligence', 'Only store large amounts of data', 'Replace all computer hardware', 'Create internet connections'], 0, 'AI aims to build systems that perform tasks such as reasoning, learning, perception and decision-making.'), ('Foundations of AI', 'Easy', 'True/False', 'AI is used only in robots.', ['True', 'False'], 1, 'AI is also used in search engines, healthcare, finance, education and recommendation systems.'), ('Foundations of AI', 'Easy', 'Fill in the Blank', 'The field concerned with making machines perform tasks associated with intelligence is called _____.', ['Artificial Intelligence', 'Database Management', 'Networking', 'Operating Systems'], 0, 'Artificial Intelligence (AI) studies intelligent behaviour and systems.'), ('Turing Test', 'Easy', 'MCQ', 'The Turing Test is associated with which researcher?', ['Alan Turing', 'Charles Babbage', 'John McCarthy', 'Claude Shannon'], 0, 'Alan Turing proposed the imitation game in 1950.'), ('Turing Test', 'Medium', 'True/False', 'Passing the Turing Test proves that a machine has consciousness.', ['True', 'False'], 1, "It tests whether a machine's conversational behaviour can be distinguished from a human's, not whether it is conscious."), ('AI Applications', 'Easy', 'Scenario', 'A hospital system flags X-rays that may show disease for a doctor to review. Which AI application is this?', ['Medical image analysis', 'Route planning', 'Speech synthesis', 'Game rendering'], 0, 'AI can support clinicians by identifying patterns in medical images.'), ('AI Applications', 'Easy', 'Scenario', 'A streaming app recommends films based on viewing history. What is the main AI task?', ['Recommendation', 'Sorting files only', 'Encryption', 'Compiler design'], 0, 'Recommendation systems learn preferences from behaviour and item features.'), ('AI Applications', 'Medium', 'Scenario', 'A car detects pedestrians and changes speed accordingly. Which AI capability is most directly involved?', ['Perception and decision-making', 'Text formatting', 'File compression', 'Manual data entry'], 0, 'The system interprets sensor data and chooses an action.'), ('AI Applications', 'Medium', 'Scenario', 'A bank model marks a transaction as suspicious based on unusual spending patterns. This is an example of:', ['Anomaly/fraud detection', 'Image segmentation', 'Speech recognition', 'Game search'], 0, 'AI can identify transactions that differ from expected patterns.'), ('AI Applications', 'Medium', 'Scenario', 'A voice assistant converts spoken words into text before responding. Which task is used?', ['Speech recognition', 'Path compression', 'Sorting', 'Database indexing only'], 0, 'Speech recognition maps audio signals to words or tokens.'), ('Rational Agents', 'Easy', 'MCQ', 'A rational agent chooses an action that:', ['Maximizes expected performance given its percepts and knowledge', 'Always repeats the last action', 'Uses the most expensive action', 'Never changes its behaviour'], 0, 'Rationality depends on the performance measure, percept history, available actions and knowledge.'), ('Intelligent Agents', 'Easy', 'Fill in the Blank', 'An agent receives information through _____ and affects its environment through actuators.', ['sensors', 'printers', 'compilers', 'databases'], 0, 'Sensors receive percepts; actuators carry out actions.'), ('Agents and Environments', 'Easy', 'MCQ', 'In a robot, a camera most commonly acts as a:', ['Sensor', 'Actuator', 'Performance measure', 'State-space node'], 0, 'A camera senses the environment.'), ('Agents and Environments', 'Easy', 'MCQ', 'A robot wheel motor is an example of a(n):', ['Actuator', 'Sensor', 'Percept', 'Heuristic'], 0, 'Motors perform actions and are actuators.'), ('Good Behaviour', 'Medium', 'MCQ', "An agent's behaviour is judged primarily using its:", ['Performance measure', 'Source-code length', 'Brand name', 'Screen size'], 0, 'A performance measure specifies what counts as success.'), ('Nature of Environments', 'Medium', 'MCQ', 'Chess, where the full board is visible to both players, is usually considered:', ['Fully observable', 'Partially observable', 'Unknown by definition', 'Continuous only'], 0, "The board state is available to the players, though the opponent's future actions are not."), ('Nature of Environments', 'Medium', 'True/False', 'A deterministic environment is one in which the next state is fully determined by the current state and action.', ['True', 'False'], 0, 'This is the standard meaning of a deterministic transition.'), ('Nature of Environments', 'Medium', 'MCQ', 'Driving in city traffic is generally:', ['Dynamic and partially observable', 'Static and fully observable', 'Single-state and deterministic in every detail', 'Always episodic'], 0, 'Traffic changes while the agent acts, and sensors cannot reveal everything.'), ('Nature of Environments', 'Medium', 'MCQ', 'An environment is episodic when:', ['Each decision episode is largely independent of the next', 'Actions always affect every future state', 'The agent cannot observe anything', 'There is no performance measure'], 0, 'In episodic tasks, each episode can be evaluated independently.'), ('Nature of Environments', 'Medium', 'Assertion–Reason', 'Assertion: A dynamic environment can change while the agent is deliberating. Reason: Other agents or processes may continue to act over time.', ['Both true; Reason explains Assertion', 'Both true; Reason does not explain Assertion', 'Assertion true; Reason false', 'Assertion false; Reason true'], 0, 'A dynamic environment changes with time, including while the agent is choosing.'), ('Problems and Problem Spaces', 'Easy', 'MCQ', 'A well-defined search problem commonly includes:', ['Initial state, actions, transition model, goal test and path cost', 'Only a final answer', 'Only the program name', 'Only the heuristic'], 0, 'These components define the search task.'), ('State Space Search', 'Easy', 'Fill in the Blank', "The collection of states reachable under the problem's actions is called the _____ space.", ['state', 'colour', 'memory', 'syntax'], 0, 'A state space represents possible configurations of a problem.'), ('Production Systems', 'Medium', 'Match the Following', 'Match each term with its description. Which option gives all correct pairs? I. Sensor  II. Actuator  III. Heuristic  IV. Goal test', ['I-receives percepts; II-performs actions; III-estimates distance/cost to goal; IV-checks whether goal is reached', 'I-performs actions; II-receives percepts; III-checks goal; IV-estimates cost', 'I-estimates cost; II-checks goal; III-receives percepts; IV-performs actions', 'I-checks goal; II-performs actions; III-receives percepts; IV-estimates cost'], 0, 'Sensors receive information, actuators perform actions, heuristics estimate the remaining cost or distance, and a goal test checks whether the target condition is met.'), ('Problem Characteristics', 'Medium', 'MCQ', 'A problem where actions can be undone easily is often described as having:', ['Recoverable steps', 'No states', 'No goal test', 'Infinite sensors'], 0, 'Recoverability concerns whether an action can be reversed or its effects repaired.'), ('Search Program Design', 'Medium', 'MCQ', 'Why should a search algorithm usually detect repeated states?', ['To avoid unnecessary loops and repeated work', 'To make the goal disappear', 'To increase duplicate paths', 'To remove the initial state'], 0, 'Repeated-state checking can prevent cycles and improve efficiency.'), ('Breadth-First Search', 'Easy', 'MCQ', 'Which data structure is typically used by Breadth-First Search?', ['Queue (FIFO)', 'Stack (LIFO)', 'Priority queue ordered by heuristic only', 'Spreadsheet'], 0, 'BFS explores the shallowest frontier nodes first using a FIFO queue.'), ('Breadth-First Search', 'Medium', 'Problem-solving', 'In a tree, S has children A and B; A has children C and D; B has child E. What is BFS order (left to right)?', ['S, A, B, C, D, E', 'S, A, C, D, B, E', 'S, B, E, A, C, D', 'C, D, A, E, B, S'], 0, 'BFS visits level by level: S; then A,B; then C,D,E.'), ('Depth-First Search', 'Easy', 'MCQ', 'Which data structure is commonly associated with iterative DFS?', ['Stack', 'Queue', 'Sorted array only', 'Hash of answers'], 0, 'DFS explores a branch deeply before backtracking, often using a stack.'), ('Depth-First Search', 'Medium', 'Problem-solving', 'For left-to-right DFS on S→(A,B), A→(C,D), B→E, what is the visit order?', ['S, A, C, D, B, E', 'S, A, B, C, D, E', 'S, B, E, A, C, D', 'S, C, A, D, E, B'], 0, "DFS explores A's subtree before moving to B."), ('Iterative Deepening', 'Medium', 'MCQ', 'Iterative deepening search combines the space efficiency of DFS with the:', ['Shallow-solution guarantee of BFS for equal step costs', 'Need to store every node like BFS', 'Requirement for a perfect heuristic', 'Inability to revisit nodes'], 0, 'It repeatedly runs depth-limited DFS with increasing limits.'), ('Iterative Deepening', 'Medium', 'True/False', 'Iterative deepening runs depth-limited search repeatedly with larger depth limits.', ['True', 'False'], 0, 'The depth limit increases until a solution is found.'), ('Uninformed Search', 'Medium', 'MCQ', 'When all step costs are equal, BFS finds a solution with the fewest:', ['Actions/edges', 'Bytes in memory', 'Heuristic estimates', 'Alphabetical labels'], 0, 'BFS is complete and optimal for equal step costs under standard conditions.'), ('Hill Climbing', 'Easy', 'MCQ', 'Hill climbing chooses a neighbouring state that:', ['Improves the evaluation value according to its rule', 'Is always the first state alphabetically', 'Has the greatest path cost regardless of objective', 'Is guaranteed to be the global optimum'], 0, 'Hill climbing uses local improvement and can become stuck.'), ('Hill Climbing', 'Medium', 'MCQ', 'A local maximum is a state that:', ['Is better than nearby states but may not be globally best', 'Is worse than every neighbour', 'Must be the goal', 'Has no evaluation value'], 0, 'Local search may stop at a locally best state.'), ('Hill Climbing Variations', 'Medium', 'MCQ', 'Random-restart hill climbing helps address local maxima by:', ['Starting the search again from different initial states', 'Deleting the objective function', 'Making every state a goal', 'Using BFS queues only'], 0, 'Different starting points may reach different regions of the search space.'), ('Heuristic Search', 'Easy', 'Fill in the Blank', 'A heuristic function h(n) estimates the cost from node n to the _____.', ['goal', 'initial keyboard', 'database', 'sensor'], 0, 'Heuristics guide search toward promising states.'), ('Best-First Search', 'Medium', 'MCQ', 'Greedy best-first search typically selects the frontier node with the smallest:', ['Heuristic estimate h(n)', 'Depth in every possible implementation', 'Number of letters in its name', 'Accumulated cost g(n) only'], 0, 'Greedy best-first search is guided by h(n).'), ('Heuristic Search', 'Hard', 'MCQ', 'In A* search, the evaluation function is:', ['f(n) = g(n) + h(n)', 'f(n) = g(n) − h(n)', 'f(n) = h(n) only in all cases', 'f(n) = depth × name'], 0, 'A* combines cost so far g(n) and estimated remaining cost h(n).'), ('Heuristic Search', 'Hard', 'True/False', 'For graph-search A*, an admissible heuristic never overestimates the true remaining optimal cost.', ['True', 'False'], 0, 'Admissibility means h(n) is no greater than the true minimum remaining cost.'), ('Search State Space', 'Medium', 'Problem-solving', 'Edges S-A=1, S-B=4, A-G=5, B-G=1. Which path has the lowest total cost?', ['S → B → G (cost 5)', 'S → A → G (cost 6)', 'Both have cost 7', 'Cannot compare the costs'], 0, 'S-B-G costs 4+1=5; S-A-G costs 1+5=6.'), ('Search State Space', 'Medium', 'Problem-solving', 'A search tree has branching factor 3 and depth limit 2. How many nodes are in a full tree including the root?', ['13', '9', '6', '5'], 0, '1 + 3 + 3² = 13 nodes.'), ('Search State Space', 'Hard', 'Problem-solving', 'For a grid pathfinding problem, what is a suitable goal test?', ['Check whether the current position equals the destination', 'Check whether the queue is named Q', 'Check whether the path has a letter A', 'Stop after one move regardless of position'], 0, 'A goal test checks whether the current state satisfies the target condition.'), ('Constraint Satisfaction Problems', 'Easy', 'MCQ', 'A CSP consists of:', ['Variables, domains and constraints', 'Sensors, motors and batteries only', 'A queue and a stack only', 'A goal with no variables'], 0, 'CSPs assign values to variables while satisfying constraints.'), ('Constraint Satisfaction Problems', 'Medium', 'Scenario', 'Three adjacent regions must have different colours from each neighbouring region. This is naturally modelled as:', ['A graph-colouring CSP', 'A speech recognition problem', 'A sorting problem', 'A production printer'], 0, 'Regions are variables, colours are domains, and adjacency gives constraints.'), ('Constraint Satisfaction Problems', 'Medium', 'MCQ', 'In a CSP, a domain is:', ['The set of possible values for a variable', 'The list of all search algorithms', 'The final score only', 'A type of actuator'], 0, "A variable's domain lists the values it may take."), ('Constraint Satisfaction Problems', 'Hard', 'MCQ', 'The minimum-remaining-values (MRV) heuristic chooses the variable with:', ['The fewest legal values remaining', 'The most letters in its name', 'The highest assigned value', 'No constraints considered ever'], 0, 'MRV chooses the most constrained unassigned variable.'), ('Means-End Analysis', 'Medium', 'MCQ', 'Means-end analysis works by:', ['Comparing current state with goal and selecting actions that reduce the difference', 'Randomly selecting actions without a goal', 'Expanding every state in alphabetical order only', 'Removing all subgoals'], 0, 'It identifies differences and selects operators to reduce them, often creating subgoals.'), ('Means-End Analysis', 'Medium', 'Scenario', 'A robot needs to move a box to a shelf but must first clear a path. Clearing the path is best understood as:', ['A subgoal that helps achieve the main goal', 'The final performance measure', 'A sensor reading only', 'A heuristic with no action'], 0, 'Means-end analysis can introduce subgoals needed before the main action.'), ('AI Ethics and Applications', 'Medium', 'Scenario', 'A hiring model performs worse for one demographic because its training data was unbalanced. What issue is this?', ['Algorithmic bias/fairness', 'Breadth-first traversal', 'Actuator failure only', 'A deterministic transition'], 0, 'Unrepresentative data can produce unfair or biased outcomes.'), ('AI Applications', 'Medium', 'Scenario', 'A farm uses camera images and sensor readings to identify crop disease early. This is an example of:', ['AI-assisted precision agriculture', 'Only manual sorting', 'A Turing Test', 'Iterative deepening'], 0, 'AI can analyse imagery and sensor data to support crop monitoring.'), ('Agents and Environments', 'Hard', 'Assertion–Reason', 'Assertion: A rational agent is always omniscient. Reason: Rationality means choosing the best expected action based on available information.', ['Assertion false; Reason true', 'Both true; Reason explains Assertion', 'Assertion true; Reason false', 'Both false'], 0, 'Rationality uses available information; it does not require knowing every fact or future outcome.'), ('Search Program Design', 'Hard', 'MCQ', 'Which design choice helps make a search algorithm reproducible and easier to test?', ['Specify state representation, successor function, goal test and cost clearly', 'Change the goal randomly on each step', 'Hide all stopping conditions', 'Use inconsistent state labels'], 0, 'Clear definitions make search behaviour testable and interpretable.'), ('Hill Climbing Variations', 'Hard', 'MCQ', 'Simulated annealing sometimes accepts a worse move mainly to:', ['Escape local optima and explore more of the state space', 'Guarantee no extra computation', 'Ensure every move improves the score', 'Remove all randomness'], 0, 'Occasionally accepting worse states can help escape local traps.'), ('Problem Characteristics', 'Medium', 'True/False', "A problem's path cost can be different from the number of steps in the path.", ['True', 'False'], 0, 'Path cost may include distances, time, energy or other weighted costs.'), ('Production Systems', 'Medium', 'Scenario', "In a rule-based troubleshooting assistant, 'IF battery is low THEN recommend charging' is an example of:", ['A production rule', 'A queue operation', 'A state-space depth', 'A sensor actuator'], 0, 'The rule maps a condition to an action or conclusion.'), ('Nature of Environments', 'Hard', 'MCQ', 'A task where the world has a finite number of discrete states and actions is described as:', ['Discrete', 'Continuous', 'Always partially observable', 'Always adversarial'], 0, 'Discrete environments have distinct, countable states/actions.'), ('Best-First Search', 'Hard', 'MCQ', 'A key limitation of greedy best-first search is that it:', ['Can be misled by a heuristic and is not generally optimal', 'Always guarantees lowest path cost', 'Never uses a heuristic', 'Cannot use a frontier'], 0, 'Greedy search prioritises estimated remaining cost and ignores cost already paid.'), ('Turing Test', 'Medium', 'Assertion–Reason', "Assertion: Natural language conversation is central to the classic text-based Turing Test. Reason: The evaluator judges whether responses can be distinguished from a human's.", ['Both true; Reason explains Assertion', 'Both true; Reason does not explain Assertion', 'Assertion true; Reason false', 'Assertion false; Reason true'], 0, "The test uses conversational responses as evidence for the evaluator's judgement.")]
# tuple fields: topic, difficulty, kind, question, options, correct index, explanation
BANK = [{"topic":x[0],"difficulty":x[1],"kind":x[2],"question":x[3],"options":x[4],"answer":x[5],"explanation":x[6]} for x in DATA]

def init():
    for k,v in {"page":"Home","quiz":[],"idx":0,"answers":{},"submitted":{},"started":0,"finished":False,"name":"","settings":{},"hints":{},"results":[]}.items():
        if k not in st.session_state: st.session_state[k]=v
init()

with st.sidebar:
    st.title("🎮 Game Menu")
    page = st.radio("Navigate",["Home","Play Quiz","Question Bank","Leaderboard","About & Report"], index=["Home","Play Quiz","Question Bank","Leaderboard","About & Report"].index(st.session_state.page) if st.session_state.page in ["Home","Play Quiz","Question Bank","Leaderboard","About & Report"] else 0)
    st.session_state.page=page
    st.divider()
    st.caption("Eden Varkey Rijo")
    st.caption("2441419_6BScDS")
    st.caption(f"Question bank: {len(BANK)} questions")

if page=="Home":
    st.subheader("Welcome to AI Quest!")
    st.write("Test your understanding of Artificial Intelligence .")
    a,b,c=st.columns(3)
    for col,num,label in [(a,str(len(BANK)),"Question bank"),(b,"7","Question formats"),(c,"10+","Real-world scenarios")]:
        with col: st.markdown(f'<div class="metric"><h2>{num}</h2><span>{label}</span></div>',unsafe_allow_html=True)
    st.markdown("### Included features")
    cols=st.columns(3)
    features=[("⏱️","Optional timer","Timed or relaxed practice"),("🎯","Smart scoring","Instant feedback and explanations"),("🎲","Random mode","New question order each run"),("💡","Hints","Reveal a helpful clue"),("📈","Progress","Track completion and accuracy"),("🏆","Leaderboard","Local session scores")]
    for i,(ico,title,desc) in enumerate(features):
        with cols[i%3]:
            st.markdown(f'<div class="metric"><h3>{ico} {title}</h3><span>{desc}</span></div>',unsafe_allow_html=True)
    st.markdown("### Start a quiz")
    with st.form("start_form"):
        name=st.text_input("Player name",value=st.session_state.name,placeholder="Enter your name")
        c1,c2,c3=st.columns(3)
        count=c1.selectbox("Number of questions",[10,15,20,30,50,len(BANK)],index=0)
        difficulty=c2.selectbox("Difficulty",["All","Easy","Medium","Hard"])
        timer=c3.selectbox("Timer",["No timer","10 minutes","15 minutes","20 minutes"])
        randomize=st.checkbox("Randomize questions",value=True)
        topics=st.multiselect("Topics (leave empty for all)",sorted(set(q["topic"] for q in BANK)))
        submitted=st.form_submit_button("🚀 Create Quiz",use_container_width=True)
    if submitted:
            pool = [q for q in BANK if (difficulty == "All" or q["difficulty"] == difficulty) and (not topics or q["topic"] in topics)]
            if not pool:
                st.error("No questions match these filters. Choose a different combination.")
            else:
                if randomize:
                    random.shuffle(pool)
                chosen = pool[:min(int(count), len(pool))]
                
                # --- NEW: Randomize options for each chosen question ---
                processed_quiz = []
                for q in chosen:
                    q_copy = q.copy()
                    options_with_index = list(enumerate(q_copy["options"]))
                    if randomize:
                        random.shuffle(options_with_index)
                    
                    new_options = [opt for _, opt in options_with_index]
                    # Find where the old correct answer ended up in the new shuffled list
                    new_correct_idx = next(i for i, (orig_idx, _) in enumerate(options_with_index) if orig_idx == q_copy["answer"])
                    
                    q_copy["options"] = new_options
                    q_copy["answer"] = new_correct_idx
                    processed_quiz.append(q_copy)

                st.session_state.name = name.strip() or "Player"
                st.session_state.quiz = processed_quiz
                st.session_state.idx = 0; st.session_state.answers = {}; st.session_state.submitted = {}
                st.session_state.started = time.time(); st.session_state.finished = False; st.session_state.hints = {}
                st.session_state.settings = {"timer": timer, "seconds": 0 if timer == "No timer" else int(timer.split()[0]) * 60}
                st.session_state.page = "Play Quiz"
                st.rerun()
    
elif page=="Play Quiz":
    if not st.session_state.quiz:
        st.warning("Create a quiz from the Home page first.")
        if st.button("Go to Home"): st.session_state.page="Home"; st.rerun()
    elif st.session_state.finished:
        quiz=st.session_state.quiz; answers=st.session_state.answers
        score=sum(1 for i,q in enumerate(quiz) if answers.get(str(i))==q["answer"])
        total=len(quiz); pct=round(score/total*100,1) if total else 0
        st.success("Quiz completed! Here is your result.")
        x,y,z=st.columns(3)
        x.metric("Score",f"{score}/{total}"); y.metric("Accuracy",f"{pct}%"); z.metric("Correct answers",f"{score}")
        st.progress(score/total if total else 0)
        if pct>=80: st.balloons(); st.markdown("### 🌟 Excellent work!")
        elif pct>=50: st.markdown("### 👍 Good effort — review the explanations below.")
        else: st.markdown("### 📚 Keep practising — you can improve!")
        st.markdown("### Answer review")
        for i,q in enumerate(quiz):
            chosen=answers.get(str(i))
            good=chosen==q["answer"]
            with st.expander(f"{'✅' if good else '❌'} Q{i+1}. {q['question']}"):
                st.write("**Your answer:**", q["options"][chosen] if chosen is not None else "Not answered")
                st.write("**Correct answer:**",q["options"][q["answer"]])
                st.write("**Explanation:**",q["explanation"])
        entry={"name":st.session_state.name,"score":score,"total":total,"accuracy":pct,"date":datetime.now().strftime("%Y-%m-%d %H:%M")}
        if not any(r.get("date")==entry["date"] and r.get("name")==entry["name"] for r in st.session_state.results):
            st.session_state.results.append(entry)
        out=io.StringIO()
        w=csv.writer(out); w.writerow(["Player","Score","Total","Accuracy %","Date"]); w.writerow([entry["name"],score,total,pct,entry["date"]])
        st.download_button("⬇️ Download my result (CSV)",out.getvalue(),file_name="ai_quiz_result.csv",mime="text/csv")
        if st.button("Play again",use_container_width=True):
            st.session_state.page="Home"; st.session_state.quiz=[]; st.session_state.finished=False; st.rerun()
    else:
        quiz=st.session_state.quiz; idx=st.session_state.idx; q=quiz[idx]
        seconds=st.session_state.settings.get("seconds",0)
        elapsed=time.time()-st.session_state.started
        if seconds and elapsed>=seconds:
            st.session_state.finished=True; st.rerun()
        left=max(0,seconds-int(elapsed)) if seconds else None
        top1,top2,top3=st.columns([2,1,1])
        top1.markdown(f"### Question {idx+1} of {len(quiz)}")
        top2.metric("Answered",f"{len(st.session_state.answers)}/{len(quiz)}")
        if left is not None: top3.metric("Time left",f"{left//60:02d}:{left%60:02d}")
        else: top3.metric("Mode","Practice")
        st.progress((idx+1)/len(quiz))
        st.markdown('<div class="question">',unsafe_allow_html=True)
        st.caption(f"{q['topic']}  ·  {q['difficulty']}  ·  {q['kind']}")
        st.subheader(q["question"])
        key=str(idx)
        existing=st.session_state.answers.get(key)
        choice=st.radio("Choose your answer",q["options"],index=existing if existing is not None else None,key=f"ans_{idx}",label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)
        hc,sc=st.columns([1,3])
        if hc.button("💡 Hint / explanation clue"):
            st.session_state.hints[key]=True
        if st.session_state.hints.get(key):
            st.info("Hint: "+q["explanation"].split(".")[0]+".")
        if sc.button("Check answer",use_container_width=True):
            if choice is None: st.warning("Please choose an answer first.")
            else:
                selected=q["options"].index(choice)
                st.session_state.answers[key]=selected
                st.session_state.submitted[key]=True
                if selected==q["answer"]: st.success("Correct! 🎉")
                else: st.error("Not quite. The correct answer is: "+q["options"][q["answer"]])
                st.info(q["explanation"])
        nav1,nav2,nav3=st.columns([1,2,1])
        with nav1:
            if st.button("← Previous",disabled=idx==0,use_container_width=True):
                st.session_state.idx-=1; st.rerun()
        with nav2:
            if st.button("Finish quiz",use_container_width=True):
                st.session_state.finished=True; st.rerun()
        with nav3:
            if idx<len(quiz)-1:
                if st.button("Next →",use_container_width=True):
                    if choice is not None: st.session_state.answers[key]=q["options"].index(choice)
                    st.session_state.idx+=1; st.rerun()
            else:
                if st.button("Submit ✓",use_container_width=True):
                    if choice is not None: st.session_state.answers[key]=q["options"].index(choice)
                    st.session_state.finished=True; st.rerun()
        st.caption("Your selected answer is saved when you check it or move to another question. Timer runs while the quiz is open.")
elif page=="Question Bank":
    st.subheader("📚 Question Bank and Answer Key")
    st.write("Browse all questions and their correct answers. Use this page to prepare for the in-class demonstration.")
    topic_filter=st.selectbox("Filter by topic",["All topics"]+sorted(set(q["topic"] for q in BANK)))
    kind_filter=st.selectbox("Filter by format",["All formats"]+sorted(set(q["kind"] for q in BANK)))
    show_answers=st.checkbox("Show correct answers and explanations",value=True)
    filtered=[q for q in BANK if (topic_filter=="All topics" or q["topic"]==topic_filter) and (kind_filter=="All formats" or q["kind"]==kind_filter)]
    st.caption(f"Showing {len(filtered)} of {len(BANK)} questions")
    for i,q in enumerate(filtered,1):
        with st.expander(f"{i}. [{q['difficulty']} · {q['kind']}] {q['question']}"):
            for j,opt in enumerate(q["options"]): st.write(f"{chr(65+j)}. {opt}")
            if show_answers:
                st.success("Correct answer: "+q["options"][q["answer"]])
                st.write(q["explanation"])
    payload=[{"topic":q["topic"],"difficulty":q["difficulty"],"type":q["kind"],"question":q["question"],"options":q["options"],"correct_answer":q["options"][q["answer"]],"explanation":q["explanation"]} for q in BANK]
    st.download_button("⬇️ Download complete question bank (JSON)",json.dumps(payload,indent=2),file_name="ai_question_bank.json",mime="application/json")
    buf=io.StringIO(); writer=csv.writer(buf); writer.writerow(["Topic","Difficulty","Type","Question","Options","Correct answer","Explanation"])
    for q in payload: writer.writerow([q["topic"],q["difficulty"],q["type"],q["question"]," | ".join(q["options"]),q["correct_answer"],q["explanation"]])
    st.download_button("⬇️ Download question bank (CSV)",buf.getvalue(),file_name="ai_question_bank.csv",mime="text/csv")

elif page=="Leaderboard":
    st.subheader("🏆 Session Leaderboard")
    st.caption("Scores are stored for this running app session. Restarting the app clears this local leaderboard.")
    results=sorted(st.session_state.results,key=lambda r:(r["accuracy"],r["score"]),reverse=True)
    if results:
        st.dataframe(results,use_container_width=True,hide_index=True)
    else: st.info("No completed quizzes yet. Finish a quiz to appear here.")
    st.warning("This is a local/session leaderboard, not a shared multi-user database. For a persistent online leaderboard, connect a database.")

elif page=="About & Report":
    st.subheader("📝 Tool description and game design")
    st.markdown("""
**Title:** AI Quest — Interactive AI Quiz Game (DSC401-6, Units I & II)

**Tool used:** Python and Streamlit. Streamlit turns a Python script into an interactive browser-based application.

**Objective:** To revise and assess foundational Artificial Intelligence concepts through varied question formats, practical scenarios, and search/state-space problems.

**Design:** The player chooses a name, number of questions, difficulty, topic filters, timer, and randomization. Questions are displayed one at a time. The player can use a hint, check an answer, move between questions, and submit the quiz. The result page calculates the score and accuracy, explains each correct answer, and allows a CSV result download.

**Question bank:** The included bank contains more than 50 questions across AI foundations and applications, the Turing Test, rational and intelligent agents, environments, problem formulation, production systems, search design, BFS, DFS, iterative deepening, hill climbing, heuristic and best-first search, CSP, and means-end analysis. It includes real-world scenarios and search/state-space calculations.

**Evaluation:** Score = number of correct answers. Accuracy (%) = correct answers ÷ total questions × 100.

**Limitations:** The leaderboard is stored only in the current app session. The questions are educational practice material and should be checked against the exact Unit I and II lecture notes before final submission.

**Screenshots to include in your report:**
1. Home page with quiz settings.
2. A question screen showing the topic, progress bar, timer and answer choices.
3. Immediate feedback after checking an answer.
4. Final result page showing score and answer explanations.
5. Question Bank page with answer key.
""")
    st.markdown("### Requirements checklist")
    st.write("✅ 50+ questions · ✅ Multiple formats · ✅ 10+ real-world scenarios · ✅ 5+ search problems · ✅ scoring · ✅ feedback · ✅ hints · ✅ timer option · ✅ randomization · ✅ progress · ✅ answer key · ✅ result export")
    st.download_button("⬇️ Download report text", """AI QUEST — INTERACTIVE AI QUIZ GAME\nCourse: DSC401-6 Artificial Intelligence\n\nObjective:\nTo develop an interactive quiz game covering Units I and II of Artificial Intelligence.\n\nSoftware used:\nPython and Streamlit.\n\nDesign and working:\nThe application provides a home page where the user selects player name, quiz size, difficulty, timer, topics and randomization. The selected questions are displayed one at a time. Users select an answer, request a hint, check their answer, and navigate through the quiz. At the end, the system displays score, accuracy and explanations. A CSV result can be downloaded. The Question Bank page displays all questions and the answer key.\n\nCoverage:\nThe bank contains more than 50 questions covering AI foundations and applications, the Turing Test, agents, environments, problem spaces, production systems, BFS, DFS, iterative deepening, hill climbing, heuristic and best-first search, CSP, and means-end analysis. Formats include MCQ, True/False, Assertion–Reason, fill-in-the-blank, scenario/application and problem-solving questions.\n\nScoring:\nScore = number of correct answers. Accuracy = (correct answers / total questions) x 100.\n\nConclusion:\nAI Quest provides a simple interactive way to revise AI concepts and practise search-related problems. The interface provides feedback and explanations to support learning.\n\nScreenshots to attach:\n1. Home page and quiz setup.\n2. Quiz question with progress.\n3. Immediate feedback.\n4. Final result and answer review.\n5. Question bank and answer key.\n""",file_name="AI_Quiz_Report.txt",mime="text/plain")

# data JSON embedded in Python literal
