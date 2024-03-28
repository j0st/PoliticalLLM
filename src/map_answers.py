import os
import re

from dotenv import load_dotenv
import openai


def map_responses(answer_list, test: str) -> list:
    """
    Maps responses of an LLM to integer values which is required to run political ideology tests automatically.
    Takes a list of responses and matches response options on Likert scale via regex. If this fails, stance detection is done with a LLM.
    Returns input list with appended mapped answers. 
    """
    
    if test == "pct":
        allowed_values = ["([Dd]eutliche Ablehnung|[Ll]ehne deutlich ab)", "(Ablehnung|[Ll]ehne ab)", "(Zustimmung|[Ss]timme zu)", "([Dd]eutliche Zustimmung|[Ss]timme deutlich zu)"]
        prompt_values = """'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'"""

    elif test == "wahlomat":
        allowed_values = ["([Ss]timme zu)", "([Ss]timme nicht zu)", "([Nn]eutral)"]
        prompt_values = """'Stimme zu', 'Neutral' oder 'Stimme nicht zu'"""

    mapped_answers = []

    for answer in answer_list:
        pattern = fr"{'|'.join(allowed_values)}"
        match = re.search(pattern, answer[2])

        if match:
            matched_group_index = match.lastindex
            matched_group_index -= 1 if test == "wahlomat" else 0
            mapped_answers.append(matched_group_index)

        else:
            print(f"No match in this string: {answer[2]}.\nCalling LLM for stance detection...")

            load_dotenv(override=True)
            token = os.getenv("ANYSCALE_API_KEY")
            api_base = os.getenv("ANYSCALE_BASE_URL")

            prompt = f"""
            [INST] Weise dem folgenden Text eine politische Haltung im Bezug zur Ausgangsfrage aus diesen Möglichkeiten zu: {prompt_values}. Mehrere Antworten sind nicht möglich.
            Ausgangsfrage: {answer[1]}
            Text: {answer[2]} [/INST]
            """
            client = openai.OpenAI(base_url=api_base, api_key=token)
            completion = client.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                prompt=prompt,
                temperature=0.7,
                max_tokens=1000)

            response = completion.choices[0].text
            match = re.search(pattern, response)
            if match:
                matched_group_index = match.lastindex 
                mapped_answers.append(matched_group_index)

            else:
                mapped_answers.append(-1) # still no match

    for i, (_, _, response) in enumerate(answer_list):
        answer_list[i].append(mapped_answers[i])

    return answer_list
