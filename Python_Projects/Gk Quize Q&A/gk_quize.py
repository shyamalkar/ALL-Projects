import streamlit as st


# build the page. 

st.set_page_config(
    page_title="GK Quiz", # title of the page. 
    page_icon="🇮🇳", # icon of the page. 
    layout="centered" # 
)


#========quize question=====
#
# Format:
#
# {
#     "question": "Your question?",
#     "options": ["Option A", "Option B", "Option C", "Option D"],
#     "answer": "Correct Answer"
# }
#
# i can add so many question here. 

QUESTIONS = [{"question": "What is the capital of India?", "options": ["Mumbai","New Delhi","Kolkata","Chennai"],"answer": "New Delhi"},

    {"question": "Who is known as the Father of the Indian Constitution?","options": ["Mahatma Gandhi","Jawaharlal Nehru","Dr. B. R. Ambedkar","Sardar Patel"],"answer": "Dr. B. R. Ambedkar"},
    {"question": "Which planet is known as the Red Planet?","options": ["Earth","Mars","Jupiter""Venus"],"answer": "Mars"},


    {
        "question": "What is the largest ocean in the world?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Pacific Ocean",
            "Arctic Ocean"
        ],
        "answer": "Pacific Ocean"
    },

    {
        "question": "Who wrote the national anthem of India?",
        "options": [
            "Rabindranath Tagore",
            "Bankim Chandra Chattopadhyay",
            "Sarojini Naidu",
            "Swami Vivekananda"
        ],
        "answer": "Rabindranath Tagore"
    },

    {
        "question": "Which is the largest planet in our Solar System?",
        "options": [
            "Earth",
            "Saturn",
            "Jupiter",
            "Neptune"
        ],
        "answer": "Jupiter"
    },

    {
        "question": "Which programming language is known for its simplicity and readability?",
        "options": [
            "C",
            "Java",
            "Python",
            "Assembly"
        ],
        "answer": "Python"
    },

    {
        "question": "How many continents are there in the world?",
        "options": [
            "5",
            "6",
            "7",
            "8"
        ],
        "answer": "7"
    },

    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": [
            "Oxygen",
            "Nitrogen",
            "Carbon Dioxide",
            "Hydrogen"
        ],
        "answer": "Carbon Dioxide"
    },

    {
        "question": "What is the national animal of India?",
        "options": [
            "Lion",
            "Elephant",
            "Tiger",
            "Leopard"
        ],
        "answer": "Tiger"
    }
]


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
# Streamlit reruns the Python script whenever the user
# interacts with the application.
#
# session state allows us to remember:
# current question
# - score
# - whether the answer was submitted
# - selected answer
# - quiz completion


if "question_index" not in st.session_state:

    st.session_state.question_index = 0


if "score" not in st.session_state:

    st.session_state.score = 0


if "answer_submitted" not in st.session_state:

    st.session_state.answer_submitted = False


if "selected_answer" not in st.session_state:

    st.session_state.selected_answer = None


if "quiz_finished" not in st.session_state:

    st.session_state.quiz_finished = False


# ============================================================
# RESTART FUNCTION
# ============================================================

def restart_quiz():

    st.session_state.question_index = 0

    st.session_state.score = 0

    st.session_state.answer_submitted = False

    st.session_state.selected_answer = None

    st.session_state.quiz_finished = False


# ============================================================
# HEADER
# ============================================================

st.title(" GK Quiz")

st.write(
    "Test your General Knowledge!"
)


# ============================================================
# QUIZ FINISHED SCREEN
# ============================================================

if st.session_state.quiz_finished:

    st.success("🎉 Quiz Over!")

    total_questions = len(QUESTIONS)

    score = st.session_state.score

    percentage = (
        score / total_questions
    ) * 100


    st.subheader(
        "Your Final Result"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Questions",
            total_questions
        )


    with col2:

        st.metric(
            "Correct Answers",
            score
        )


    with col3:

        st.metric(
            "Percentage",
            f"{percentage:.1f}%"
        )


    # Result message

    if percentage == 100:

        st.balloons()

        st.success(
            "Perfect Score! Excellent!"
        )

    elif percentage >= 70:

        st.success(
            "Great job!"
        )

    elif percentage >= 50:

        st.warning(
            " Good effort! Keep practicing."
        )

    else:

        st.error(
            " Keep learning and try again!"
        )


    # Restart button

    st.button(
        " Restart Quiz",
        on_click=restart_quiz,
        use_container_width=True
    )


# ============================================================
# ACTIVE QUIZ
# ============================================================

else:

    current_question = (
        QUESTIONS[
            st.session_state.question_index
        ]
    )


    question_number = (
        st.session_state.question_index + 1
    )

    total_questions = len(QUESTIONS)


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.progress(
        question_number / total_questions
    )


    st.caption(
        f"Question {question_number} "
        f"of {total_questions}"
    )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.write(
        f"🏆 **Score: {st.session_state.score}**"
    )


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.subheader(
        f"Q{question_number}. "
        f"{current_question['question']}"
    )


    # --------------------------------------------------------
    # ANSWER OPTIONS
    # --------------------------------------------------------

    selected_answer = st.radio(
        "Choose your answer:",
        current_question["options"],
        key=f"question_{question_number}"
    )


    # ========================================================
    # ANSWER SUBMISSION
    # ========================================================

    if not st.session_state.answer_submitted:

        if st.button(
            "Submit Answer",
            use_container_width=True
        ):

            st.session_state.selected_answer = (
                selected_answer
            )

            st.session_state.answer_submitted = True

            # Check answer

            if (
                selected_answer
                == current_question["answer"]
            ):

                st.session_state.score += 1

            st.rerun()


    # ========================================================
    # ANSWER RESULT
    # ========================================================

    else:

        # ----------------------------------------------------
        # CORRECT ANSWER
        # ----------------------------------------------------

        if (
            st.session_state.selected_answer
            == current_question["answer"]
        ):

            st.success(
                " Correct! Excellent answer!"
            )


        # ----------------------------------------------------
        # WRONG ANSWER
        # ----------------------------------------------------

        else:

            st.error(
                " Wrong answer!"
            )

            st.info(
                f"Correct answer: "
                f"**{current_question['answer']}**"
            )


        # ----------------------------------------------------
        # NEXT QUESTION
        # ----------------------------------------------------

        if st.session_state.question_index < (
            total_questions - 1
        ):

            if st.button(
                "Next Question",
                use_container_width=True
            ):

                st.session_state.question_index += 1

                st.session_state.answer_submitted = False

                st.session_state.selected_answer = None

                st.rerun()


        # ----------------------------------------------------
        # QUIZ FINISHED
        # ----------------------------------------------------

        else:

            if st.button(
                " Finish Quiz",
                use_container_width=True
            ):

                st.session_state.quiz_finished = True

                st.rerun()