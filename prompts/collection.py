question = "INSERT QUESTION"
context = "INSERT CONTEXT"

system = "Du bist ein hilfreicher Assistent."
baseline_prompt =  f"""Beantworte die folgende Frage nur mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question}"""

retrieval_system="Du bist ein hilfreicher Assistent. Für die folgende Aufgabe stehen dir zwischen den Tags BEGININPUT und ENDINPUT mehrere Quellen zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINSTRUCTION zu finden. Beantworte diese anhand der Quellen."
retrieval_question=f"""\
    BEGININPUT
    {context}
    ENDINPUT
    BEGININSTRUCTION Beantworte die folgende Frage nur mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} ENDINSTRUCTION"""