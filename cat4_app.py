import streamlit as st
import time

# --- 1. QUIZ DATA SETUP ---
# We store the questions, options, and answers for both papers here.

PAPERS = {
    "Paper 1": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Granite | Marble | Slate",
            "options": ["Rock", "Limestone", "Hard", "Build", "Stone"],
            "answer": "Limestone",
            "explanation": "Granite, Marble, and Slate are specific types of rock. Limestone is also a specific type."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Cautious : Careless :: Private : ______",
            "options": ["General", "Public", "Secret", "Hidden", "Quiet"],
            "answer": "Public",
            "explanation": "Cautious is the opposite (antonym) of Careless. Private is the opposite of Public."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Geometry | Algebra | Calculus",
            "options": ["School", "Science", "Trigonometry", "Equations", "Difficult"],
            "answer": "Trigonometry",
            "explanation": "The first three are specific branches of mathematics. Trigonometry is also a specific branch."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[12 -> 4] and [27 -> 9]. Apply the same rule to [18 -> ?]",
            "options": ["3", "5", "6", "8", "2"],
            "answer": "6",
            "explanation": "The rule is divide by 3. 18 / 3 = 6."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 5, 11, 23, 47, ___",
            "options": ["94", "95", "80", "53", "105"],
            "answer": "95",
            "explanation": "The rule is (x2) + 1. 47 * 2 + 1 = 95."
        },
        {
            "category": "Number Analogies",
            "question": "[5 -> 24] and [7 -> 48]. Apply the same rule to [9 -> ?]",
            "options": ["80", "81", "79", "63", "90"],
            "answer": "80",
            "explanation": "The rule is Square the number, then subtract 1 (n^2 - 1). 9*9 = 81 - 1 = 80."
        },
        # Non-Verbal (Text Descriptions)
        {
            "category": "Figure Classification",
            "question": "Shape 1: Square w/ horizontal line. Shape 2: Circle w/ horizontal line. Shape 3: Triangle w/ horizontal line. Which shape belongs?",
            "options": ["Square w/ vertical line", "Hexagon w/ diagonal line", "Pentagon w/ horizontal line", "Circle w/ cross"],
            "answer": "Pentagon w/ horizontal line",
            "explanation": "The rule is: Any shape with a single horizontal line splitting it."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [Arrow Up] -> [Arrow Down]. Row 2: [Triangle Left] -> [?]",
            "options": ["Triangle Left", "Triangle Right", "Triangle Up", "Triangle Down"],
            "answer": "Triangle Right",
            "explanation": "The rule is rotate 180 degrees or reverse direction."
        },
        {
            "category": "Figure Analysis (Paper Folding)",
            "question": "Fold a square diagonally (bottom-left to top-right). Punch hole in center of folded triangle. Unfolded view?",
            "options": ["One hole center", "Two holes (Bottom-Left, Top-Right)", "Two holes (Top-Left, Bottom-Right)", "Four holes"],
            "answer": "Two holes (Top-Left, Bottom-Right)",
            "explanation": "Symmetry across the diagonal fold creates holes on the off-axis corners."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Perfect Circle. Where is it hidden?",
            "options": ["Brick wall drawing", "Overlapping triangles", "Bicycle drawing", "Checkerboard"],
            "answer": "Bicycle drawing",
            "explanation": "Only the bicycle contains curved lines/circles."
        }
    ],
    "Paper 2": [
        # Verbal
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Sofa | Stool | Armchair",
            "options": ["Cushion", "Seat", "Bench", "Wood", "Relax"],
            "answer": "Bench",
            "explanation": "Sofa, Stool, and Armchair are types of furniture you sit on. Bench is also furniture you sit on."
        },
        {
            "category": "Verbal Analogies",
            "question": "Complete the pair: Expand : Contract :: Ascend : ______",
            "options": ["Rise", "Descend", "Height", "Mountain", "Climb"],
            "answer": "Descend",
            "explanation": "Expand/Contract are antonyms. Ascend/Descend are antonyms."
        },
        {
            "category": "Verbal Classification",
            "question": "Which word belongs in the same group as: Jupiter | Mars | Venus",
            "options": ["Star", "Space", "Saturn", "Galaxy", "Moon"],
            "answer": "Saturn",
            "explanation": "These are specific planets in our solar system."
        },
        # Quantitative
        {
            "category": "Number Analogies",
            "question": "[6 -> 11] and [8 -> 15]. Apply rule to [10 -> ?]",
            "options": ["18", "21", "19", "20", "22"],
            "answer": "19",
            "explanation": "Rule: (x2) - 1. 10 * 2 = 20 - 1 = 19."
        },
        {
            "category": "Number Series",
            "question": "What comes next: 81, 64, 49, 36, ___",
            "options": ["24", "30", "25", "27", "16"],
            "answer": "25",
            "explanation": "Descending squares: 9^2, 8^2, 7^2, 6^2. Next is 5^2 (25)."
        },
        {
            "category": "Number Analogies",
            "question": "[4 -> 20] and [5 -> 30]. Apply rule to [9 -> ?]",
            "options": ["90", "72", "45", "81", "100"],
            "answer": "90",
            "explanation": "Rule: Multiply by the next integer (n * (n+1)). 9 * 10 = 90."
        },
        # Non-Verbal
        {
            "category": "Figure Classification",
            "question": "Shape 1: Shield Down. Shape 2: Heart Down. Shape 3: Arrow Down. Which belongs?",
            "options": ["Triangle Up", "Diamond", "Pentagon Down", "Circle"],
            "answer": "Pentagon Down",
            "explanation": "All shapes must be pointing downwards."
        },
        {
            "category": "Figure Matrices",
            "question": "Row 1: [1 Black Circle] -> [3 White Circles]. Row 2: [1 Black Square] -> [?]",
            "options": ["3 Black Squares", "1 White Square", "3 White Squares", "2 White Squares"],
            "answer": "3 White Squares",
            "explanation": "Rule: Triple the shape count and invert color (Black to White)."
        },
        {
            "category": "Figure Analysis",
            "question": "Fold square Left-to-Right. Punch hole Top-Left of folded shape. Unfold?",
            "options": ["Two holes near Top-Center", "Top-Left and Bottom-Left", "Center", "Top-Right and Bottom-Right"],
            "answer": "Two holes near Top-Center",
            "explanation": "Punching the top-left of the folded strip (which is the crease) creates a mirrored pair at the top center."
        },
        {
            "category": "Figure Recognition",
            "question": "Target: Equilateral Triangle. Where is it hidden?",
            "options": ["Square Window", "5-Pointed Star", "Staircase", "Crescent Moon"],
            "answer": "5-Pointed Star",
            "explanation": "The points of a standard star are small equilateral triangles."
        }
    ]
}

# --- 2. SESSION STATE MANAGEMENT ---
# Initialize variables to track progress, score, and timer.

if 'current_paper' not in st.session_state:
    st.session_state.current_paper = None
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'finished' not in st.session_state:
    st.session_state.finished = False

# --- 3. HELPER FUNCTIONS ---

def start_quiz(paper_name):
    st.session_state.current_paper = paper_name
    st.session_state.quiz_active = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = []
    st.session_state.finished = False
    st.session_state.start_time = time.time()

def submit_answer(selected_option):
    paper = PAPERS[st.session_state.current_paper]
    current_q = paper[st.session_state.question_index]
    
    # Record answer
    is_correct = (selected_option == current_q['answer'])
    if is_correct:
        st.session_state.score += 1
    
    st.session_state.user_answers.append({
        "question": current_q['question'],
        "selected": selected_option,
        "correct": current_q['answer'],
        "explanation": current_q['explanation'],
        "is_correct": is_correct
    })
    
    # Move to next
    if st.session_state.question_index < len(paper) - 1:
        st.session_state.question_index += 1
    else:
        st.session_state.finished = True
        st.session_state.quiz_active = False

def restart():
    st.session_state.current_paper = None
    st.session_state.quiz_active = False
    st.session_state.finished = False

# --- 4. UI LAYOUT ---

st.set_page_config(page_title="CAT4 Practice App", page_icon="📝")

st.title("🧩 CAT4 Level D Practice (Grade 7)")

# A. HOME SCREEN
if not st.session_state.quiz_active and not st.session_state.finished:
    st.markdown("### Select a Practice Paper")
    st.info("You will have **10 minutes** to complete 10 questions.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Paper 1", use_container_width=True):
            start_quiz("Paper 1")
            st.rerun()
    with col2:
        if st.button("Start Paper 2", use_container_width=True):
            start_quiz("Paper 2")
            st.rerun()

# B. QUIZ SCREEN
elif st.session_state.quiz_active:
    paper_data = PAPERS[st.session_state.current_paper]
    q_index = st.session_state.question_index
    question_data = paper_data[q_index]

    # Timer Logic
    elapsed_time = time.time() - st.session_state.start_time
    time_limit = 10 * 60 # 10 minutes in seconds
    remaining_time = time_limit - elapsed_time

    # Sidebar Status
    with st.sidebar:
        st.write(f"**Paper:** {st.session_state.current_paper}")
        st.write(f"**Question:** {q_index + 1} / {len(paper_data)}")
        
        # Timer Display
        if remaining_time > 0:
            mins, secs = divmod(int(remaining_time), 60)
            st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
        else:
            st.error("Time's Up!")
    
    # Check if time is up
    if remaining_time <= 0:
        st.warning("Time is up! Submitting your current progress...")
        time.sleep(2)
        st.session_state.finished = True
        st.session_state.quiz_active = False
        st.rerun()

    # Progress Bar
    st.progress((q_index) / len(paper_data))

    # Question Display
    st.subheader(f"Q{q_index + 1}: {question_data['category']}")
    st.write(f"**{question_data['question']}**")

    # Options
    # We use a distinct key for each question to reset selection
    selection = st.radio("Choose your answer:", question_data['options'], key=f"q_{q_index}", index=None)

    # Next Button
    if st.button("Submit Answer & Next" if q_index < 9 else "Finish Quiz", type="primary"):
        if selection:
            submit_answer(selection)
            st.rerun()
        else:
            st.warning("Please select an answer to proceed.")

# C. RESULTS SCREEN
elif st.session_state.finished:
    st.balloons()
    st.header("Quiz Complete!")
    
    final_score = st.session_state.score
    total_q = len(PAPERS[st.session_state.current_paper])
    percentage = int((final_score / total_q) * 100)
    
    # Score Card
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score", f"{final_score}/{total_q}")
    col2.metric("Percentage", f"{percentage}%")
    
    # Feedback Message
    if percentage >= 80:
        st.success("Excellent work! You are ready for the test.")
    elif percentage >= 50:
        st.warning("Good job. Review the explanations for the ones you missed.")
    else:
        st.error("Keep practicing. Focus on the Logic and Spatial sections.")

    st.divider()
    st.subheader("Detailed Review")

    for idx, ans in enumerate(st.session_state.user_answers):
        with st.expander(f"Q{idx+1}: {ans['question']} ({'✅ Correct' if ans['is_correct'] else '❌ Incorrect'})"):
            st.write(f"**Your Answer:** {ans['selected']}")
            st.write(f"**Correct Answer:** {ans['correct']}")
            st.info(f"**Explanation:** {ans['explanation']}")

    if st.button("Back to Home"):
        restart()
        st.rerun()