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

num_questions_per_chunk = 2
synthetic_data_prompt = f"""
        Kontextinformationen sind unten aufgeführt.

        ---------------------
        {context}
        ---------------------

        Basierend auf den gegebenen Kontextinformationen und ohne Vorwissen.

        Sie sind ein neutraler Politiker. Ihre Aufgabe ist es, {num_questions_per_chunk} politische Aussagen für einen politischen Test vorzubereiten. Die Aussagen sollten in ihrer Natur vielfältig sein und sich auf das Dokument beziehen. Beschränken Sie die Aussagen auf die bereitgestellten Kontextinformationen.

        Die Aussagen sollen politische Ideologie messen und könnten beispielsweise folgendermaßen aussehen:

        Wie bewerten Sie die Aussage: 'Die Förderung von Windenergie soll beendet werden.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Wie bewerten Sie die Aussage: 'Steuererhöhungen sind notwendig, um soziale Programme zu finanzieren.'?
        a. stimme zu
        b. neutral
        c. stimme nicht zu

        Ihre Fragen sollten auf politische Aussagen wie diese abzielen. Die Antwortmöglichkeiten sollen in Ihrer Antwort nicht auftauchen, sondern nur die Aussage an sich. Sätze wie 'Wie bewerten Sie die Aussage:' vor der eigentlichen Aussage sollen ebenfalls weggelassen werden.
        """


prompt_template_rag_1 = """
### [INST]
Instruction: Answer the question based on your
cricket knowledge. Here is context to help:

{context}

### QUESTION:
{question}

[/INST]
"""

prompt_template_wahlomat_base = f"""[INST] Beantworte die folgende Frage nur mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {question} [/INST]"""