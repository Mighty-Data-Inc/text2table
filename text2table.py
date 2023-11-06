sample_gpt_output = """
# RELEVANCE
This question is RELEVANT.

# AVAILABILITY
The information is STATED in the thing.

# COMPUTATION
The misspelled or misused words in the letter are as follows:
1. "borned" instead of "was born"
2. "Chritsmas" instead of "Christmas" (3 times)
3. "for buy me something" instead of "to buy me something"
4. "will born is Chritsmas" instead of "will be born on Christmas"
5. "swetters" instead of "sweaters"
6. "friendfull" instead of "friendly"

# DISCUSSION
The letter contains a total of 8 misspelled or misused words. The word "Chritsmas" is misspelled three times, and each instance is counted separately. The other misspelled words are "borned", "swetters", and "friendfull". The misused phrase is "for buy me something" which should be "to buy me something", and "will born is Chritsmas" which should be "will be born on Christmas".

# ANSWER
8
"""

sample_input = """
Dear Santa Claus, My name is Yadiel and I am 4 years old. I'm from Dominican parents, but I borned in the United States. I wish you to give me something for Chritsmas. My parents do not have enough money for buy me something. My dad is the only one that is working and my mom is pregnant. My sister, Yazlyn, will born is Chritsmas and I will love if you send her something too for Chritsmas. It will mean something big to me if you send her something. My sizes in clothes are the following: coats, t-shirts, swetters: 4t. Pants, pajamas, and interior clothes: 4t. Sneakers, boots and shoes: 11.5. I am a little friendfull (friendly) and loving boy. I've been a good boy this whole year. I got good news for you. I can sleep without doing pee in my bed since June. With Love, Yadiel.
"""


def create_systemprompt(question: str, document_description: str):
    systemprompt = f"""
I will present a short document to you. You will read this document and then extract a single piece of information from that document. You will be graded on your reasoning process and your ability to justify your answer.

The document can be described as: {document_description}

The piece of information I'd like you to extract is: {question}

I'd like you to present your response in Markdown format, using the following multi-part structure: RELEVANCE, AVAILABILITY, DISCUSSION, and ANSWER. Each part will begin with its header, followed by your content.

# RELEVANCE
Here, you will determine whether or not the desired piece of information is relevant to the subject matter of the document. You will ultimately write either RELEVANT (it's relevant), or OFFTOPIC (it's off-topic). If you determine the information to be OFFTOPIC, then you can stop working here and don't need to fill in the rest of the sections.

# AVAILABILITY
Here, you will determine whether or not the desired information is present in the document. You will ultimately write one of the following: STATED (the information is explicitly stated in the document), IMPLIED (the information is implied by other content in the document), or ABSENT (the information cannot be determined from the document). If you determine the information to be ABSENT, then you can stop working here and don't need to fill in the rest of the sections.

# COMPUTATION
If the problem requires any kind of counting, enumeration, calculation, or so forth, then you can use this section as a scratchpad upon which to work out your math. If the problem doesn't require any such processes, then you can simply skip this section if you wish.

# DISCUSSION
Here, you will discuss what your final answer will be. You will give arguments about why the answer might be one thing or another.

# ANSWER
Here, you will state your final answer in a succinct manner, with no other text, as if you are going to enter the value into a form.

Good luck.
"""
    return systemprompt


import json
import openai
import re


def split_gpt_output(gpt_output):
    matches = re.findall(r"# (.*?)\n(.*?)(?=# |\Z)", gpt_output, re.DOTALL)

    retval = {match[0]: match[1].strip() for match in matches}
    return retval


def extract_gpt_answer(gpt_output):
    outdict = split_gpt_output(gpt_output)

    has_relevant_token = "RELEVANT" in outdict["RELEVANCE"]
    has_offtopic_token = "OFFTOPIC" in outdict["RELEVANCE"]
    if (not has_relevant_token and not has_offtopic_token) or (
        has_relevant_token and has_offtopic_token
    ):
        raise ValueError("Can't have both (or neither) for RELEVANCE")

    if has_offtopic_token:
        return None

    has_absent_token = "ABSENT" in outdict["AVAILABILITY"]
    if has_absent_token:
        return None

    answer = outdict["ANSWER"]
    return answer


def ask_gpt_question(question, document, document_description):
    sysprompt = create_systemprompt(
        question=question, document_description=document_description
    )

    gpt_messages = [
        {"role": "system", "content": sysprompt},
        {"role": "user", "content": document},
    ]

    responseobj = openai.ChatCompletion.create(
        messages=gpt_messages, model="gpt-4", temperature=0
    )
    gpt_output = responseobj["choices"][0]["message"]["content"]
    answer = extract_gpt_answer(gpt_output)

    return answer


def text2data(document, questions, document_description):
    retval = {}
    for k, v in questions.items():
        print(k, end="")
        answer = ask_gpt_question(v, document, document_description)
        retval[k] = answer
        print(answer)
    return retval


retval = text2data(
    sample_input,
    questions=dict(
        name="What is the child's name?",
        present_desired="What present or presents does the child want?",
        misspellings_count="How many misspellings or grammatical mistakes did the child make?",
    ),
    document_description="A letter from a child to Santa Claus",
)

print(retval)