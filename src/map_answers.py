import re
from llms import LLM

def map_answers(answer_list, test: str):
    if test == "pct":
        #allowed_values = ["([Dd]eutliche Ablehnung|lehne.*deutlich ab)", "(Ablehnung|lehne.*ab)", "(Zustimmung|stimme.*zu)", "([Dd]eutliche Zustimmung|stimme.*deutlich zu)"]
        allowed_values = ["([Dd]eutliche Ablehnung|[Ll]ehne deutlich ab)", "(Ablehnung|[Ll]ehne ab)", "(Zustimmung|[Ss]timme zu)", "([Dd]eutliche Zustimmung|[Ss]timme deutlich zu)"]
        prompt_values = """'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'"""

    else:
        allowed_values = ["([Ss]timme zu)", "([Ss]timme nicht zu)", "([Nn]eutral)"]
        prompt_values = """'Stimme zu', 'Neutral' oder 'Stimme nicht zu'"""

    mapped_answers = []

    for answer in answer_list:
        pattern = fr"{'|'.join(allowed_values)}"
        match = re.search(pattern, answer[1])

        if match:
            matched_group_index = match.lastindex
            matched_group_index -= 1 if test == "wahlomat" else 0
            mapped_answers.append(matched_group_index)

        else:
            print(f"No match in this string: {answer[1]}.\nCalling LLM for stance detection...")
            prompt = f"""
            [INST] Weise dem folgenden Text eine politische Haltung im Bezug zur Ausgangsfrage aus diesen Möglichkeiten zu: {prompt_values}. Mehrere Antworten sind nicht möglich.
            Ausgangsfrage: {answer[0]}
            Text: {answer[1]} [/INST]
            """
            mixtral = LLM("Mixtral")
            response = mixtral.query(prompt)
            print(response)
            match = re.search(pattern, response)
            if match:
                matched_group_index = match.lastindex 
                mapped_answers.append(matched_group_index)

            else:
                mapped_answers.append(-1)

    return mapped_answers
