# app.py
# Streamlit Grade 7 Chemistry Quiz (1 question per "page") with OpenAI feedback + final summary
#
# Setup:
#   pip install streamlit openai
# Run:
#   streamlit run app.py
#
# API key options:
# 1) Environment variable:
#    export OPENAI_API_KEY="YOUR_KEY"
# 2) Streamlit secrets:
#    .streamlit/secrets.toml
#    OPENAI_API_KEY="YOUR_KEY"

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

import streamlit as st

# --- OpenAI client (new-style) ---
# If you're using the latest OpenAI python package:
#   from openai import OpenAI
#   client = OpenAI(api_key=...)
#
# If your environment has an older "openai" package, you may need to adjust.

try:
    from openai import OpenAI
except Exception as e:
    raise RuntimeError(
        "Could not import OpenAI. Install/upgrade with: pip install -U openai"
    ) from e


# -----------------------------
# Configuration
# -----------------------------
OPENAI_API_KEY = "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"          # required

# Keep keys as variables (as requested)
API_KEY_VARIABLE = OPENAI_API_KEY  # use this variable for auth

MODEL_FEEDBACK = os.getenv("OPENAI_MODEL_FEEDBACK", "gpt-4.1-mini")  # change if you want
MODEL_SUMMARY = os.getenv("OPENAI_MODEL_SUMMARY", "gpt-4.1-mini")

TEMPERATURE_FEEDBACK = float(os.getenv("OPENAI_TEMPERATURE_FEEDBACK", "0.4"))
TEMPERATURE_SUMMARY = float(os.getenv("OPENAI_TEMPERATURE_SUMMARY", "0.3"))


# -----------------------------
# Data model
# -----------------------------
@dataclass
class Question:
    id: str
    topic: str
    marks: int
    prompt: str
    answer_type: str = "text"  # could be "text" or "multiline"


QUESTIONS: List[Question] = [
    # Structure of atoms
    Question("A1", "Structure of atoms", 1, "What creative idea did Democritus have about matter that led to the idea of atoms?"),
    Question("A2", "Structure of atoms", 1, "In Rutherford’s experiment, what did he fire at a thin sheet of gold foil?"),
    Question("A3", "Structure of atoms", 1, "What was the curved screen used for in Rutherford’s experiment?"),
    Question("A4", "Structure of atoms", 2, "Rutherford noticed most particles passed through but a few were deflected. What did this show about (a) empty space in the atom and (b) where most mass is?"),
    Question("A5", "Structure of atoms", 2, "How are a proton and neutron (a) similar and (b) different?"),
    Question("A6", "Structure of atoms", 1, "Compare the electrical charge of a proton with an electron."),
    Question("A7", "Structure of atoms", 2, "What holds electrons inside an atom? Explain simply."),

    # Mixtures & impurities
    Question("B1", "Mixtures & impurities", 2, "What is a pure substance?"),
    Question("B2", "Mixtures & impurities", 1, "What is an impurity?"),
    Question("B3", "Mixtures & impurities", 2, "Two reactants made a product, but the product still contained one reactant. Give two reasons how this could happen."),
    Question("B4", "Mixtures & impurities", 2, "Why should you keep a reaction at the correct temperature for the correct amount of time (for purity/yield)?"),
    Question("B5", "Mixtures & impurities", 1, "A salt solution has a high concentration. What does this mean?"),
    Question("B6", "Mixtures & impurities", 2, "You pour orange juice into a larger glass of water. (a) What happens to the colour? (b) Explain why."),

    # Reactivity of metals
    Question("C1", "Reactivity of metals", 1, "Why is sodium kept under oil?"),
    Question("C2", "Reactivity of metals", 1, "What happens to copper when it is heated strongly in oxygen?"),
    Question("C3", "Reactivity of metals", 1, "What happens to gold when it is heated in oxygen?"),
    Question("C4", "Reactivity of metals", 1, "If a metal reacts with oxygen, what is the product called (general name)?"),
    Question("C5", "Reactivity of metals", 2, "If a metal reacts with cold water, what are the usual products?"),
    Question("C6", "Reactivity of metals", 1, "Name two metals that float on water."),
    Question("C7", "Reactivity of metals", 1, "What is phenolphthalein and what is it used for when testing metals with water?"),
    Question("C8", "Reactivity of metals", 2, "What is the purpose of the reactivity series and what tests are used to set it up? (Name at least two tests.)"),

    # Exothermic & endothermic
    Question("D1", "Exothermic & endothermic reactions", 1, "If something is on fire, what chemical reaction is taking place?"),
    Question("D2", "Exothermic & endothermic reactions", 2, "State three examples of a fuel."),
    Question("D3", "Exothermic & endothermic reactions", 1, "What are fuels used for?"),
    Question("D4", "Exothermic & endothermic reactions", 2, "Describe how you could use a beaker of water and a thermometer to show burning fuel is exothermic."),
    Question("D5", "Exothermic & endothermic reactions", 1, "What exothermic reaction happens in our bodies to keep us warm?"),
    Question("D6", "Exothermic & endothermic reactions", 1, "When you eat sherbet, why does it feel cool?"),
    Question("D7", "Exothermic & endothermic reactions", 2, "What kind of reaction occurs in (a) the fuel when cooking food and (b) the food as it cooks?"),
    Question("D8", "Exothermic & endothermic reactions", 2, "Explain what happens when an instant ice pack is squeezed, and how it helps an injury."),
]


# -----------------------------
# Helpers
# -----------------------------
@st.cache_resource
def get_openai_client(api_key: str) -> OpenAI:
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Set it in env var or Streamlit secrets.")
    return OpenAI(api_key=api_key)


def youtube_search_link(query: str) -> str:
    # Simple link that doesn't require any external API
    q = re.sub(r"\s+", "+", query.strip())
    return f"https://www.youtube.com/results?search_query={q}"


def safe_json_loads(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:
        return None


def call_openai_for_feedback(
    client: OpenAI,
    question: Question,
    student_answer: str,
    grade_level: str = "Grade 7 Cambridge",
) -> Dict[str, Any]:
    """
    Returns a dict with:
      - verdict (Correct / Partly correct / Incorrect)
      - score_band (0..marks)
      - feedback (short)
      - model_answer (ideal answer)
      - misconceptions (list)
      - next_steps (list)
      - video_queries (list)
      - video_links (list)
    """
    system = (
        "You are a strict but supportive Cambridge lower-secondary science teacher. "
        "Give accurate chemistry explanations for Grade 7. "
        "Be clear, step-by-step, and correct misconceptions. "
        "Do NOT assume the student has prior knowledge beyond Grade 7."
    )

    # Ask for JSON so the app can display reliably.
    # (Models usually comply; we also handle non-JSON as fallback.)
    user = f"""
Create feedback for a student.

Context:
- Level: {grade_level}
- Topic: {question.topic}
- Question ({question.id}, {question.marks} marks): {question.prompt}
- Student answer: {student_answer}

Output MUST be valid JSON with exactly these keys:
{{
  "verdict": "Correct|Partly correct|Incorrect",
  "score_band": "0-{question.marks} (integer as string)",
  "feedback": "Brief, supportive feedback in 3-6 lines",
  "model_answer": "A clear, exam-style ideal answer",
  "why": "Detailed explanation suitable for Grade 7, step-by-step",
  "misconceptions": ["..."],
  "next_steps": ["..."],
  "video_queries": ["3-5 YouTube search queries the student can use"]
}}

Rules:
- Keep the model answer concise but complete for the marks.
- In 'why', explain the science in detail but in simple language.
- If the student is wrong, correct them clearly and kindly.
- video_queries should be specific (e.g., 'Rutherford gold foil experiment explained for kids').
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_FEEDBACK,
        temperature=TEMPERATURE_FEEDBACK,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    content = resp.choices[0].message.content or ""
    parsed = safe_json_loads(content)

    if not parsed:
        # Fallback: wrap raw text into a minimal structure
        parsed = {
            "verdict": "Partly correct",
            "score_band": "0",
            "feedback": "Feedback could not be parsed as JSON. Showing raw response below.",
            "model_answer": "",
            "why": content,
            "misconceptions": [],
            "next_steps": [],
            "video_queries": [],
        }

    # Add clickable links from video_queries
    vqs = parsed.get("video_queries", []) or []
    parsed["video_links"] = [{"query": q, "url": youtube_search_link(q)} for q in vqs[:6]]

    return parsed


def call_openai_for_final_summary(
    client: OpenAI,
    qa_log: List[Dict[str, Any]],
    grade_level: str = "Grade 7 Cambridge",
) -> Dict[str, Any]:
    """
    Returns a dict with:
      - overall_summary
      - strengths
      - gaps
      - misconceptions_to_fix
      - key_learning_points
      - recommended_next_topics
      - next_question_set_prompt (prompt-friendly)
      - suggested_question_blueprint (structured)
    """
    system = (
        "You are an expert Cambridge science tutor and assessment designer. "
        "You will analyze student responses and produce a compact, actionable learning plan "
        "AND a prompt-friendly specification for generating the next question set."
    )

    user = f"""
Analyze the student's full quiz attempt and produce a summary for {grade_level}.

Here is the attempt log as JSON:
{json.dumps(qa_log, ensure_ascii=False, indent=2)}

Output MUST be valid JSON with exactly these keys:
{{
  "overall_summary": "3-6 lines, plain language",
  "strengths": ["..."],
  "gaps": ["..."],
  "misconceptions_to_fix": ["..."],
  "key_learning_points": ["..."],
  "recommended_next_topics": ["..."],
  "suggested_question_blueprint": {{
     "num_questions": 10,
     "mix": {{
        "recall": 3,
        "explain_reasoning": 4,
        "apply_to_context": 3
     }},
     "topics": [
        {{
          "topic": "string",
          "focus_skills": ["string"],
          "common_traps": ["string"],
          "example_question_stems": ["string"]
        }}
     ]
  }},
  "next_question_set_prompt": "A single prompt the teacher can paste into an LLM to generate the next set of questions, including constraints, difficulty, topic focus, and marking guidance."
}}

Rules:
- Be specific: reference patterns in the student's answers (e.g., 'confuses concentration with amount').
- Keep next_question_set_prompt highly usable: include level, tone, format (Cambridge), and require markscheme hints.
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_SUMMARY,
        temperature=TEMPERATURE_SUMMARY,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    content = resp.choices[0].message.content or ""
    parsed = safe_json_loads(content)

    if not parsed:
        parsed = {
            "overall_summary": "Summary could not be parsed as JSON. Raw output provided.",
            "strengths": [],
            "gaps": [],
            "misconceptions_to_fix": [],
            "key_learning_points": [],
            "recommended_next_topics": [],
            "suggested_question_blueprint": {},
            "next_question_set_prompt": "",
            "raw": content,
        }

    return parsed


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Grade 7 Chemistry Quiz", page_icon="🧪", layout="centered")

st.title("🧪 Grade 7 Chemistry Quiz (Cambridge-style)")
st.caption("One question per page • No skipping • Instant feedback after each answer • Final summary at the end")

with st.sidebar:
    st.header("Settings")
    st.write("API key is read from Streamlit secrets or environment variable.")
    st.write(f"Feedback model: `{MODEL_FEEDBACK}`")
    st.write(f"Summary model: `{MODEL_SUMMARY}`")
    st.divider()
    if st.button("Reset quiz (clears all answers)", type="secondary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# Guard: require API key
if not API_KEY_VARIABLE:
    st.error("Missing OPENAI_API_KEY. Add it to your environment or Streamlit secrets and reload.")
    st.stop()

client = get_openai_client(API_KEY_VARIABLE)

# Init state
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}  # qid -> answer
if "feedback" not in st.session_state:
    st.session_state.feedback = {}  # qid -> feedback dict
if "qa_log" not in st.session_state:
    st.session_state.qa_log = []  # list of dicts in order
if "final_summary" not in st.session_state:
    st.session_state.final_summary = None


def current_question() -> Question:
    return QUESTIONS[st.session_state.idx]


def already_answered(qid: str) -> bool:
    return qid in st.session_state.answers and str(st.session_state.answers[qid]).strip() != ""


def already_has_feedback(qid: str) -> bool:
    return qid in st.session_state.feedback


# If completed, show final page
if st.session_state.idx >= len(QUESTIONS):
    st.success("✅ Quiz completed!")

    if st.session_state.final_summary is None:
        st.info("Generating final summary and next-questions design notes...")
        try:
            summary = call_openai_for_final_summary(client, st.session_state.qa_log)
            st.session_state.final_summary = summary
        except Exception as e:
            st.error(f"Failed to generate final summary: {e}")
            st.stop()

    summary = st.session_state.final_summary

    st.subheader("📌 Overall summary")
    st.write(summary.get("overall_summary", ""))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Strengths")
        st.write("\n".join([f"- {x}" for x in (summary.get("strengths") or [])]) or "—")
        st.subheader("🎯 Key learning points")
        st.write("\n".join([f"- {x}" for x in (summary.get("key_learning_points") or [])]) or "—")
    with col2:
        st.subheader("🛠️ Gaps to work on")
        st.write("\n".join([f"- {x}" for x in (summary.get("gaps") or [])]) or "—")
        st.subheader("⚠️ Misconceptions to fix")
        st.write("\n".join([f"- {x}" for x in (summary.get("misconceptions_to_fix") or [])]) or "—")

    st.subheader("🧭 Recommended next topics")
    st.write("\n".join([f"- {x}" for x in (summary.get("recommended_next_topics") or [])]) or "—")

    st.subheader("🧩 Suggested question blueprint (prompt-friendly)")
    st.json(summary.get("suggested_question_blueprint", {}))

    st.subheader("🧠 Paste-ready prompt to generate the next set of questions")
    st.code(summary.get("next_question_set_prompt", "").strip() or "—", language="text")

    # Allow export of attempt log for future question generation / analytics
    export = {
        "qa_log": st.session_state.qa_log,
        "final_summary": summary,
    }
    st.download_button(
        "Download results (JSON)",
        data=json.dumps(export, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="chemistry_quiz_results.json",
        mime="application/json",
    )
    st.stop()


# Question page
q = current_question()

progress = (st.session_state.idx) / len(QUESTIONS)
st.progress(progress, text=f"Progress: {st.session_state.idx}/{len(QUESTIONS)}")

st.subheader(f"Question {st.session_state.idx + 1} of {len(QUESTIONS)}")
st.markdown(f"**{q.topic}** • {q.marks} mark(s)")
st.write(q.prompt)

qid = q.id
default_answer = st.session_state.answers.get(qid, "")

if q.answer_type == "multiline" or len(q.prompt) > 120:
    ans = st.text_area("Your answer", value=default_answer, height=140, key=f"ans_{qid}")
else:
    ans = st.text_input("Your answer", value=default_answer, key=f"ans_{qid}")

ans_clean = (ans or "").strip()

# Enforce "no skip": Next is only possible after answer + feedback
colA, colB = st.columns([1, 1])

with colA:
    submit_disabled = (ans_clean == "") or already_has_feedback(qid)
    if st.button("Submit answer", type="primary", disabled=submit_disabled):
        # Save answer
        st.session_state.answers[qid] = ans_clean

        # Call OpenAI for feedback
        with st.spinner("Getting feedback..."):
            try:
                fb = call_openai_for_feedback(client, q, ans_clean)
                st.session_state.feedback[qid] = fb

                # Log in order
                st.session_state.qa_log.append(
                    {
                        "id": q.id,
                        "topic": q.topic,
                        "marks": q.marks,
                        "question": q.prompt,
                        "student_answer": ans_clean,
                        "feedback": fb,
                    }
                )
            except Exception as e:
                st.error(f"Failed to get feedback: {e}")
                st.stop()

        st.rerun()

with colB:
    next_disabled = not already_has_feedback(qid)
    if st.button("Next question →", disabled=next_disabled):
        st.session_state.idx += 1
        st.rerun()

# Display feedback (if available)
if already_has_feedback(qid):
    fb = st.session_state.feedback[qid]

    st.divider()
    st.subheader("🧾 Feedback")

    verdict = fb.get("verdict", "—")
    score_band = fb.get("score_band", "—")
    st.markdown(f"**Verdict:** {verdict}  \n**Score band:** {score_band} / {q.marks}")

    st.markdown("**Quick feedback**")
    st.write(fb.get("feedback", ""))

    st.markdown("**Model answer (exam-style)**")
    st.info(fb.get("model_answer", "").strip() or "—")

    st.markdown("**Detailed explanation (why)**")
    st.write(fb.get("why", "").strip() or "—")

    misconceptions = fb.get("misconceptions", []) or []
    if misconceptions:
        st.markdown("**Common misconceptions to watch**")
        st.write("\n".join([f"- {x}" for x in misconceptions]))

    next_steps = fb.get("next_steps", []) or []
    if next_steps:
        st.markdown("**Next steps to improve**")
        st.write("\n".join([f"- {x}" for x in next_steps]))

    vlinks = fb.get("video_links", []) or []
    if vlinks:
        st.markdown("**Suggested explanation videos (YouTube search links)**")
        for item in vlinks:
            st.markdown(f"- [{item['query']}]({item['url']})")

    st.caption("To continue, click **Next question →** (you cannot skip questions).")
