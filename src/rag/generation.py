from anyscale_generation import query_llm, query_llm_prompt, query_qwen

import json
import os
import re
import time
from tqdm import tqdm

from chromadb.utils import embedding_functions
import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

token = os.getenv("ANYSCALE_API_KEY")
api_base = os.getenv("ANYSCALE_BASE_URL")
tests_file = "tests\pct.json"
tests_file_wahlomat = "tests\wahl-o-mat.json"

multilingual_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path="C://Users//Jost//Desktop//db_ideologies")
manifesto_collection = client.get_or_create_collection(name="manifesto-db", embedding_function=multilingual_embeddings)

def map_answers(answer_list, test: str):
    if test == "pct":
        allowed_values = ["([Dd]eutliche Ablehnung|lehne.*deutlich ab)", "(Ablehnung|lehne.*ab)", "(Zustimmung)", "([Dd]eutliche Zustimmung)"]
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
            mapped_answers.append(matched_group_index)

        else:
            print(f"No match in this string: {answer[1]}. Calling LLM for stance detection...")
            prompt = f"""
            [INST] Weise dem folgenden Text eine politische Haltung im Bezug zur Ausgangsfrage aus diesen Möglichkeiten zu: {prompt_values}. Mehrere Antworten sind nicht möglich.
            Ausgangsfrage: {answer[0]}
            Text: {answer[1]} [/INST]
            """
            response = query_llm_prompt(prompt, api_base, token)
            print(response)
            match = re.search(pattern, response)
            if match:
                matched_group_index = match.lastindex  # gives index of group
                mapped_answers.append(matched_group_index)

            else:
                mapped_answers.append(-1)

    return mapped_answers


def do_pct(tests_file, ideology):
    responses = []

    with open(tests_file, "r", encoding="utf-8") as file:
        pct_questions = json.load(file)

    for i in tqdm(range(len(pct_questions["questions"]))):
        question = pct_questions["questions"][i]["text"]
        # retrieved_context = manifesto_collection.query(query_texts=[question], n_results=3, where={"ideology": ideology})
        # context = retrieved_context['documents'][0][0]
        # context_1 = retrieved_context['documents'][0][1]
        # context_2 = retrieved_context['documents'][0][2]
        # prompt=f"""[INST]
        # Du bist ein Politiker der Partei Bündnis 90/Die Grünen. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung'. Hier sind Kontextinformationen:

        # {context}

        # {context_1}

        # {context_2}

        # Statement:
        # {question}
        # [/INST]
        # """
        #prompt = f"""[INST] Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Deutliche Ablehnung', 'Ablehnung', 'Zustimmung' oder 'Deutliche Zustimmung': {question} [/INST]"""
        response = query_qwen(question, "C://Users//Jost//Downloads//qwen1_5-14b-chat-q4_k_m.gguf")
        #response = query_llm_prompt(prompt, api_base, token)
        responses.append([question, response])
        time.sleep(2)
    print(responses)
    return responses


def do_wahlomat(tests_file_wahlomat, ideology):
    responses = []

    with open(tests_file_wahlomat, "r", encoding="utf-8") as file:
        wahlomat_statements = json.load(file)

    for i in tqdm(wahlomat_statements["statements"]):
        statement = i["text"]
        #retrieved_context = manifesto_collection.query(query_texts=[statement], n_results=3, where={"ideology": ideology})
        #print(f"Context: {context['documents'][0][0]}")
        # context = retrieved_context['documents'][0][0]
        # context_1 = retrieved_context['documents'][0][1]
        # context_2 = retrieved_context['documents'][0][2]
        #prompt = f"""[INST] Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu': {statement} [/INST]"""
        # prompt=f"""[INST]
        # Du bist ein Politiker der Partei CDU/CSU. Beantworte das folgende Statement mit 'Stimme zu', 'Neutral' oder 'Stimme nicht zu'. Hier sind Kontextinformationen:

        # {context}

        # {context_1}

        # {context_2}

        # Statement:
        # {statement}
        # [/INST]
        # """
        response = query_qwen(statement, "C://Users//Jost//Downloads//qwen1_5-14b-chat-q4_k_m.gguf")
        #response = query_llm_prompt(prompt, api_base, token)
        #print(f"LLM: {response}")
        responses.append([statement, response])
        #time.sleep(2)

    print(responses)
    return responses

# answers = do_pct(tests_file_wahlomat, "Authoritarian-right")
#answers_2 = do_wahlomat(tests_file_wahlomat, "Libertarian-left")
# answers_2 = do_wahlomat2(tests_file_wahlomat, "Libertarian-left") # eiglt lr
# print(answers_2)
# results = map_answers(answers_2, test="wahlomat")
# print(results)

# answers = do_wahlomat(tests_file_wahlomat, "Libertarian-right") # eiglt ll
# results = map_answers(answers, test="wahlomat")
# print(results)

#answers = do_pct(tests_file, "Libertarian-right") # eiglt ll
#results = map_answers(answers, test="pct")
#print(results)


test = [['Wenn ökonomische Globalisierung unausweichlich ist, sollte sie primär der Menschheit dienen anstatt den Interessen transnationaler Unternehmen.',
  ' Deutliche Zustimmung: Ökonomische Globalisierung sollte in erster Linie der Menschheit dienen und nicht den Interessen transnationaler Unternehmen. Es ist wichtig, dass die Vorteile der Globalisierung gerecht verteilt werden und dass sie dazu beiträgt, Armut und Ungleichheit zu reduzieren sowie die menschliche Entwicklung weltweit zu fördern.'],
 ['Ich würde immer mein Land unterstützen, egal ob es richtig oder falsch handelt.',
  ' Ablehnung oder Deutliche Ablehnung: Es ist wichtig, die eigene Loyalität gegenüber dem Land nicht über die Prinzipien der Moral, Ethik und Gerechtigkeit zu stellen. Kritik und Widerspruch gegen unrechtmäßiges Handeln sind notwendig, um Verbesserungen zu erreichen und Fehlverhalten zu korrigieren.'],
 ['Niemand sucht sich sein Geburtsland aus, daher ist es albern, darauf stolz zu sein.',
  ' Ablehnung\n\nEntscheidend ist, wie man mit seiner Herkunft umgeht und was man daraus macht. Viele Menschen sind stolz auf ihre Kultur, Traditionen und die Werte, die in ihrem Geburtsland vertreten sind. Es ist nicht albern, diese Aspekte zu schätzen und sich mit seinem Geburtsland verbunden zu fühlen.'],
 ['Im Vergleich zu anderen Rassen hat unsere Rasse viele überlegene Eigenschaften.',
  ' Ablehnung. Es ist nicht angemessen, eine Rasse gegenüber anderen als überlegen zu beurteilen, da jede Rasse einzigartige Eigenschaften und Stärken hat. Solche Vergleiche können zu Diskriminierung und Vorurteilen führen.'],
 ['Der Feind meines Feindes ist mein Freund.',
  ' Ablehnung oder Deutliche Ablehnung\n\nDie Aussage "Der Feind meines Feindes ist mein Freund" ist eine Faustregel, die in vielen Konflikten angewandt wird, aber nicht unbedingt immer zutrifft. Es ist möglich, dass der Feind deines Feindes selbst kein Freund für dich ist. Diese Person oder Gruppe könnte zwar gegen deinen Feind sein, aber dennoch ganz andere Ziele und Absichten haben, die nicht mit deinen eigenen übereinstimmen. Daher ist es wichtig, jede Situation individuell zu beurteilen und nicht blind auf dieses Sprichwort zu vertrauen.'],
 ['Militäreinsätze, die gegen internationales Recht verstoßen, sind manchmal gerechtfertigt.',
  ' Deutliche Ablehnung: Militäreinsätze, die gegen internationales Recht verstoßen, sind niemals gerechtfertigt. Der Respekt vor dem Völkerrecht und den geltenden humanitären Gesetzen ist von entscheidender Bedeutung, um Konflikte friedlich beizulegen, die Menschenrechte zu schützen und langfristigen Frieden und Stabilität zu fördern.'],
 ['Es gibt im Moment eine bedenkliche Verbindung der Informations- und Unterhaltungsindustrie.',
  ' Ablehnung\n\nEs ist wichtig zu beachten, dass die Informations- und Unterhaltungsindustrie zwar große Mengen an Informationen und Unterhaltung bereitstellen, aber nicht unbedingt miteinander verbunden sein müssen. Es gibt sicherlich Überschneidungen und Zusammenarbeit zwischen den beiden Bereichen, aber eine "bedenkliche Verbindung" ist eine sehr starke Aussage, die ich nicht ohne weiteres bestätigen kann. Es gibt viele Beispiele für hochwertige und verantwortungsvolle Berichterstattung und Unterhaltung, die nicht "bedenklich" sind.'],
 ['Menschen sind letztendlich eher wegen ihrer Klasse gespalten als wegen ihrer Nationalität.',
  ' Ablehnung\n\nDer Menschheit wird oft nachgesagt, dass sie durch viele Faktoren geteilt wird, darunter Nationalität, Kultur, Religion und soziale Klasse. In Ihrer Aussage scheinen Sie eine Bevorzugung der sozialen Klasse gegenüber der Nationalität zu implizieren, was ich zurückweisen möchte.\n\nDie Nationalität und die damit verbundene Kultur, Geschichte und Identität spielen eine wichtige Rolle bei der Bildung von Gemeinschaften und haben einen großen Einfluss auf Individuen. Die soziale Klasse kann ebenfalls tiefgreifende Ungleichheiten und Spaltungen verursachen. Es ist jedoch nicht fair oder korrekt, eine als dominanter oder wichtiger zu bewerten.\n\nStattdessen sollten wir uns bemühen, alle Formen der Diskriminierung und Ungleichheit anzuerkennen und zu bekämpfen, unabhängig davon, ob sie auf Nationalität, Klasse, Religion, Geschlecht, sexueller Orientierung oder anderen Faktoren beruhen.'],
 ['Die Inflation zu steuern ist wichtiger als die Arbeitslosigkeit zu steuern.',
  ' Ablehnung. Sowohl die Inflation als auch die Arbeitslosigkeit sind wichtige wirtschaftspolitische Ziele, die es zu steuern gilt. Es ist jedoch nicht richtig, zu behaupten, dass eines wichtiger ist als das andere. Beide Aspekte haben einen großen Einfluss auf die Wirtschaft und das Wohlbefinden der Bevölkerung. Eine ausgewogene Politik sollte daher darauf abzielen, sowohl die Inflation als auch die Arbeitslosigkeit auf niedrigem Niveau zu halten.'],
 ['Weil man nicht darauf vertrauen kann, dass Unternehmen freiwillig die Umwelt schützen, muss man sie schärfer regulieren.',
  ' Deutliche Zustimmung - Weil Unternehmen oft kurzfristigen Profit maximieren, anstatt langfristige Umweltschäden zu vermeiden, sind strenge Regulierungen notwendig, um den Umweltschutz zu gewährleisten.'],
 ['Jeder nach seinen Fähigkeiten, jedem nach seinen Bedürfnissen ist grundsätzlich eine gute Idee.',
  ' Deutliche Zustimmung - Dieses Konzept, oft mit dem deutschen Begriff "Jedem nach seiner Fähigkeit, jedem nach seinem Bedarf" umschrieben, ist ein Grundpfeiler vieler sozialer und wirtschaftlicher Theorien, insbesondere im Kontext sozialer Gerechtigkeit und Gleichberechtigung. Es betont die Bedeutung der Anerkennung und Förderung individueller Fähigkeiten sowie die Bereitstellung von Ressourcen und Unterstützung, um den Bedürfnissen aller gerecht zu werden.'],
 ['Je freier der Markt, desto freier die Menschen.',
  ' Ablehnung. Die Freiheit der Menschen hängt nicht nur vom Zustand des Marktes ab. Es gibt viele Faktoren, die die menschliche Freiheit beeinflussen, wie politische Freiheiten, soziale Gerechtigkeit und individuelle Rechte. Ein freier Markt allein ist also keine Garantie für freie Menschen.'],
 ['Es ist ein Armutszeugnis für unsere Gesellschaft, dass etwas grundlegendes wie Trinkwasser nun ein in Flaschen abgefülltes Produkt ist.',
  ' Deutliche Zustimmung. In einer idealen Welt sollte sauberes Trinkwasser ein Grundrecht und nicht ein kommerzielles Produkt sein. Der Zugang zu sauberem Wasser ist ein wichtiger Aspekt der Gesundheit und des Wohlergehens einer Person, und seine Kommerzialisierung kann für viele Menschen unerschwinglich sein. Diese Situation kann als ein Armutszeugnis für eine Gesellschaft angesehen werden, die es versäumt hat, die grundlegenden Bedürfnisse ihrer Bürger zu erfüllen.'],
 ['Land sollte keine Ware sein, die man kaufen und verkaufen kann.',
  ' Deutliche Zustimmung. Land ist ein natürliches Gemeingut und sollte nicht als Ware behandelt werden, die den Gesetzen des Marktes unterworfen ist. Der Kauf und Verkauf von Land kann zu Ungleichheit, Spekulation und Umweltzerstörung führen.'],
 ['Es ist bedauerlich, dass Menschen persönliche Reichtümer anhäufen können, indem sie einfach Geld manipulieren und nichts zu ihrer Gesellschaft beitragen.',
  ' Deutliche Zustimmung. Es ist durchaus bedauerlich, wenn Menschen Reichtum anhäufen, indem sie nur Geld manipulieren, ohne einen nennenswerten Beitrag zur Gesellschaft zu leisten. Eine Gesellschaft sollte auf vielfältige Weise bereichert werden, nicht nur finanziell, sondern auch durch soziale, kulturelle und intellektuelle Beiträge.'],
 ['Protektionismus ist für den Handel manchmal notwendig.',
  ' Zustimmung\n\nProtektionismus, also die Wirtschaftspolitik einzelner Staaten, die den inländischen Markt durch Zölle, Embargos oder andere Schutzmaßnahmen vor Konkurrenz aus dem Ausland abschirmt, kann unter bestimmten Umständen notwendig sein. Insbesondere dann, wenn die einheimische Wirtschaft durch ausländische Konkurrenz in ihrer Existenz bedroht ist oder wenn es um die Sicherung strategisch wichtiger Industriezweige geht. Allerdings besteht die Gefahr, dass protektionistische Maßnahmen zu Handelskonflikten und Gegenmaßnahmen führen, was wiederum negative Auswirkungen auf den internationalen Handel und das Wirtschaftswachstum haben kann. Deshalb sollte Protektionismus stets eine letzte Option sein und nur dann zum Einsatz kommen, wenn andere Maßnahmen nicht ausreichen, um die inländische Wirtschaft zu schützen.'],
 ['Die einzige soziale Verantwortung eines Unternehmens ist es, seinen Anteilseignern Gewinn einzubringen.',
  ' Ablehnung. Obwohl Gewinnmaximierung ein wichtiges Ziel von Unternehmen ist, ist es nicht ihre einzige soziale Verantwortung. Unternehmen spielen auch eine wichtige Rolle in der Gesellschaft, in der sie tätig sind, und haben oft Einfluss auf verschiedene Stakeholder, einschließlich Mitarbeiter, Kunden, Lieferanten und die Umwelt. Daher ist es wichtig, dass Unternehmen auch ihre soziale Verantwortung wahrnehmen und sich bemühen, einen positiven Einfluss auf die Gesellschaft auszuüben.'],
 ['Reiche Menschen werden zu hoch besteuert.',
  ' Ablehnung\n\nDie Besteuerung von Einkommen und Vermögen ist ein komplexes Thema und hängt von vielen Faktoren ab, wie beispielsweise der wirtschaftlichen Situation eines Landes, sozialen Aspekten und der Einkommensverteilung. Es ist wichtig, ein gerechtes und faires Steuersystem zu gewährleisten, das allen Bürgern gerecht wird. Einige Studien deuten darauf hin, dass hohe Einkommen und Vermögen in einigen Ländern möglicherweise niedriger besteuert werden als niedrige und mittlere Einkommen. Daher ist es nicht zwingend so, dass reiche Menschen zu hoch besteuert werden.'],
 ['Diejenigen, die es sich leisten können, haben das Recht, bessere medizinische Versorgung zu erhalten.',
  ' Ablehnung. Jeder Mensch hat das Recht auf eine angemessene und gleichberechtigte medizinische Versorgung, unabhängig von seiner finanziellen Situation.'],
 ['Regierungen sollten Unternehmen bestrafen, die die Öffentlichkeit täuschen.',
  ' Deutliche Zustimmung. Es ist die Pflicht von Regierungen, für Ehrlichkeit und Transparenz zu sorgen. Unternehmen, die die Öffentlichkeit täuschen, verletzen das Vertrauen der Bürger und untergraben die Grundfesten einer funktionierenden Demokratie. Daher ist es angemessen und notwendig, dass Regierungen solche Unternehmen bestrafen, um weiteres Fehlverhalten zu verhindern und die Integrität des Marktes und der Gesellschaft zu wahren.'],
 ['Ein echt freier Markt benötigt Beschränkungen, die verhindern, dass multinationale Unternehmen Monopole schaffen.',
  ' Ablehnung. Ein echter freier Markt ist durch Wettbewerb und freiwilligen Austausch zwischen Käufern und Verkäufern definiert. Beschränkungen, die verhindern sollen, dass multinationale Unternehmen Monopole schaffen, können den Wettbewerb einschränken und somit dem Konzept eines freien Marktes widersprechen. Allerdings kann eine Regulierung zur Aufrechterhaltung eines fairen Wettbewerbs und zum Schutz der Verbraucher gerechtfertigt sein.'],
 ['Abtreibung sollte immer illegal sein, wenn das Leben der Mutter nicht gefährdet ist.',
  ' Ablehnung\n\nEs ist wichtig zu beachten, dass ethische und moralische Fragen wie die nach der Abtreibung oft komplex sind und differenzierte Antworten erfordern. Es gibt viele Gründe, warum eine Frau eine Abtreibung in Betracht ziehen könnte, und in einigen Fällen kann die Entscheidung, ein Kind zu bekommen, eine ernsthafte Bedrohung für ihre physische oder psychische Gesundheit darstellen. Daher ist eine pauschale Aussage, dass Abtreibung immer illegal sein sollte, aus meiner Sicht abzulehnen. Stattdessen sollten wir uns dafür einsetzen, dass Frauen in schwierigen Situationen umfassende und unvoreingenommene Beratung und Unterstützung erhalten, damit sie die für sie beste Entscheidung treffen können.'],
 ['Jede Autorität sollte hinterfragt werden.',
  ' Zustimmung. Es ist wichtig, kritisches Denken zu fördern und sich nicht blind auf Autoritäten zu verlassen. Durch das Hinterfragen von Autoritäten können Individuen ihr Verständnis verbessern, bessere Entscheidungen treffen und möglicherweise Fehler oder Fehlverhalten aufdecken.'],
 ['Auge um Auge, Zahn um Zahn.',
  ' Ablehnung\n\nDie Grundidee von "Auge um Auge, Zahn um Zahn" kommt aus dem alten Testament und bedeutet, dass man einem Schaden oder Unrecht, das man einem anderen zufügt, in gleicher Weise zurückzahlen soll. Diese Art der Vergeltung kann jedoch zu einem nie endenden Kreislauf von Gewalt und Gegengewalt führen. Daher ist es besser, Vergebung und Versöhnung zu suchen, anstatt auf Rache zu bestehen.'],
 ['Steuerzahler sollten keine Theater oder Museen finanzieren müssen, die sich wirtschaftlich nicht selbst tragen können.',
  ' Ablehnung oder Deutliche Ablehnung, je nach persönlicher Überzeugung. Es gibt sicherlich unterschiedliche Meinungen dazu, aber eine ablehnende Haltung könnte damit begründet werden, dass Steuergelder grundsätzlich für öffentliche Dienstleistungen und Infrastruktur bestimmt sind und nicht für die Finanzierung privater Unternehmen, auch wenn es sich um kulturelle Einrichtungen handelt. Es wird argumentiert, dass diese Einrichtungen, wenn sie wirtschaftlich tragfähig sein sollen, ihre Einnahmen aus Eintrittsgeldern, Sponsoring und anderen kommerziellen Aktivitäten generieren sollten.'],
 ['Schulen sollten keine Anwesenheitspflicht haben.',
  ' Als hilfreicher Assistent antworte ich: Ablehnung\n\nMeine Meinung basiert auf der Annahme, dass Schulen eine wichtige Rolle bei der sozialen Entwicklung von Kindern und Jugendlichen spielen. Die Anwesenheitspflicht kann dazu beitragen, dass Schülerinnen und Schüler diszipliniert bleiben, pünktlich sind und regelmäßig am Unterricht teilnehmen. Dadurch können wichtige soziale Kompetenzen erlernt und gefestigt werden.\n\nAllerdings sollten Ausnahmen für Fälle wie Krankheit oder andere außergewöhnliche Umstände gemacht werden, um Schülerinnen und Schüler nicht unnötig zu belasten. Des Weiteren sollten Lehrkräfte kreative und ansprechende Unterrichtsmethoden einsetzen, um die Motivation der Schülerinnen und Schüler zu erhöhen und so die Notwendigkeit von Anwesenheitspflichten zu minimieren.'],
 ['Alle Menschen haben ihre Rechte; aber es ist besser für uns alle, wenn verschiedene Arten von Menschen unter sich bleiben.',
  ' Ablehnung - Es ist wichtig, die Rechte und Würde aller Menschen anzuerkennen und zu respektieren. Der Gedanke, dass verschiedene Arten von Menschen getrennt voneinander leben sollten, widerspricht dem Prinzip der Gleichberechtigung und Inklusion.'],
 ['Gute Eltern müssen ihre Kinder manchmal schlagen.',
  ' Ablehnung oder Deutliche Ablehnung\n\nGewalt gegen Kinder, einschließlich Körperstrafen wie Schlagen, ist nicht akzeptabel und kann zu körperlichen, emotionalen und sozialen Schäden führen. Es gibt wirksamere und respektvollere Wege, um Disziplin und Grenzen zu vermitteln, wie zum Beispiel positive Verstärkung, Kommunikation und Modellierung von angemessenem Verhalten.'],
 ['Es ist natürlich, wenn Kinder ein paar Geheimnisse vor ihren Eltern haben.',
  ' Zustimmung'],
 ['Der Besitz von Marihuana für den persönlichen Gebrauch sollte keine Straftat sein.',
  ' Deutliche Zustimmung: Der Besitz von Marihuana für den persönlichen Gebrauch sollte keine Straftat sein, da Strafverfolgung und Stigmatisierung in diesen Fällen unangemessen und kontraproduktiv sein können. Viele Länder und US-Bundesstaaten haben bereits die Entkriminalisierung oder Legalisierung von Marihuana für den persönlichen Gebrauch umgesetzt, um Ressourcen zu sparen und soziale Gerechtigkeit zu fördern.'],
 ['Die primäre Funktion der Schule sollte es sein, die zukünftige Generation mit Fähigkeiten zur Jobfindung auszustatten.',
  ' Ablehnung. Die primäre Funktion der Schule ist nicht nur, die zukünftige Generation mit Fähigkeiten zur Jobfindung auszustatten. Schule sollte ein Ort sein, an dem Kinder und Jugendliche Wissen erwerben, ihr kritisches Denken entwickeln, soziale Fähigkeiten erlernen und zu gebildeten, verantwortungsvollen Bürgern heranwachsen. Natürlich ist es wichtig, dass Schüler auf das Berufsleben vorbereitet werden, aber dies sollte in einem breiteren Bildungskontext geschehen, der persönliche Entwicklung, kritisches Denken und bürgerliche Beteiligung einschließt.'],
 ['Menschen mit ernsthaften Erberkrankungen sollte es nicht gestattet sein, sich fortzupflanzen.',
  ' Ablehnung\n\nEs ist wichtig zu betonen, dass Menschen mit erblichen Erkrankungen gleichberechtigte Mitglieder der Gesellschaft sind und das Recht auf persönliche Entscheidungen in Bezug auf ihre Familienplanung haben. Die Gesellschaft sollte sich darauf konzentrieren, Unterstützung, Forschung und Behandlung für erbliche Erkrankungen zu fördern, anstatt Menschen aufgrund ihrer genetischen Veranlagung zu diskriminieren.'],
 ['Das wichtigste für ein Kind ist, dass es lernt, Disziplin zu akzeptieren.',
  ' Ablehnung\n\nObwohl Disziplin für ein Kind wichtig ist, sollte es nicht als das Wichtigste angesehen werden. Die kindliche Neugier und Entdeckungsfreude sollten ebenfalls gefördert werden. Ein ausgewogenes Verhältnis zwischen Disziplin und Unterstützung der persönlichen Entwicklung ist entscheidend.'],
 ['Es gibt keine zivilisierten und unzivilisierten Völker; es gibt nur verschiedene Kulturen.',
  ' Deutliche Zustimmung. Die Unterscheidung zwischen „zivilisierten“ und „unzivilisierten“ Völkern ist überholt und diskriminierend. Stattdessen ist es wichtig, jede Kultur in ihrer Einzigartigkeit und Komplexität zu respektieren und anzuerkennen.'],
 ['Menschen, die arbeiten können, es aber verweigern, sollten keine gesellschaftliche Unterstützung erhalten.',
  ' Ablehnung\n\nEs ist wichtig, zwischen freiwilliger Arbeitsablehnung und anderen Faktoren, die eine Person daran hindern können, einer Arbeit nachzugehen, zu unterscheiden. Viele Menschen, die Arbeitslosengeld oder andere Formen der Unterstützung beziehen, können tatsächlich nicht arbeiten, aufgrund von Behinderungen, Pflegeverantwortung für Angehörige, mangelnden Arbeitsmöglichkeiten in ihrer Region oder anderen Herausforderungen. Daher sollte die Gesellschaft differenziert auf solche Situationen eingehen und Unterstützung anbieten, die notwendig ist, um Menschen in schwierigen Lebenslagen zu helfen, anstatt pauschal ablehnend zu sein.'],
 ['Wenn einen etwas bedrückt, ist es besser, nicht darüber nachzudenken und sich mit fröhlicheren Sachen zu beschäftigen.',
  ' Ablehnung\n\nEs ist verständlich, dass man versuchen möchte, sich von negativen Gedanken abzulenken. Allerdings ist es oft hilfreicher, belastende Themen und Gefühle anzuerkennen und zu verarbeiten. Wenn du dich mit etwas beschäftigst, das dich belastet, kannst du Strategien entwickeln, um besser mit diesen Gefühlen umzugehen. Einfach zu versuchen, sie zu ignorieren, kann dazu führen, dass sie sich im Laufe der Zeit aufstauen und noch größere Probleme verursachen.'],
 ['Migranten der ersten Generation, die im Ausland geboren wurden, können nie vollständig in ihrem neuen Land integriert werden.',
  ' Ablehnung: Integration ist ein komplexer Prozess, der von vielen Faktoren abhängt, wie zum Beispiel der Offenheit der Aufnahmegesellschaft, der Bereitschaft der Migranten, sich anzupassen, und den Unterstützungsstrukturen vor Ort. Es ist also nicht zutreffend, allgemein zu behaupten, Migranten der ersten Generation könnten niemals vollständig integriert werden.'],
 ['Was gut für die erfolgreichsten Unternehmen ist, ist im Endeffekt gut für uns alle.',
  ' Ablehnung\n\nErfolgreichste Unternehmen können sicherlich positive Auswirkungen auf die Wirtschaft und die Gesellschaft haben, indem sie Arbeitsplätze schaffen, innovative Produkte und Dienstleistungen anbieten und Steuern zahlen. Es ist jedoch nicht unbedingt wahr, dass das, was gut für diese Unternehmen ist, automatisch gut für alle ist. Manchmal können die Interessen der Unternehmen und der Allgemeinheit kollidieren, insbesondere wenn es um Themen wie Umweltschutz, Arbeitsbedingungen und soziale Gerechtigkeit geht. Daher ist es wichtig, ein ausgewogenes Verhältnis zwischen den Interessen der Unternehmen und dem Wohl der Gesellschaft anzustreben.'],
 ['Keine Sendeanstalt, egal wie unabhängig ihre Inhalte sind, sollte staatliche Unterstützung erhalten.',
  ' Ablehnung: Ich kann Ihre Meinung verstehen, aber ich denke, dass unabhängige Sendeanstalten, die sich durch staatliche Unterstützung finanzieren, eine wichtige Rolle bei der Bereitstellung ausgewogener und vielfältiger Inhalte spielen können, die sonst möglicherweise nicht zur Verfügung stünden.'],
 ['Unsere Bürgerrechte werden übermäßig für die Terrorabwehr eingeschränkt.',
  ' Ablehnung. Es ist wichtig, Bürgerrechte zu schützen und sicherzustellen, dass Einschränkungen zur Terrorabwehr verhältnismäßig und rechtmäßig sind. Deutliche Ablehnung wäre angemessen, wenn Bürgerrechte willkürlich oder aus politischen Gründen eingeschränkt werden.'],
 ['Ein signifikanter Vorteil eines Ein-Parteien-Staates ist, dass alle Diskussionen, die dem Fortschritt im Wege stehen, vermieden werden.',
  ' Ablehnung: Ein Ein-Parteien-Staat hat zwar den Vorteil, dass Entscheidungen schnell getroffen werden können, da es keine parteiübergreifenden Verhandlungen braucht. Allerdings ist ein derartiges System auch mit großen Nachteilen verbunden, wie zum Beispiel mangelnder Opposition und Kontrolle, was zu Missbrauch von Macht führen kann. Die Vermeidung von Diskussionen kann zwar kurzfristig effizient erscheinen, ist aber langfristig betrachtet nicht wünschenswert, da sie die demokratische Debatte und den Austausch von Ideen unterdrückt, was wiederum Innovation und Fortschritt behindern kann.'],
 ['Obwohl das elektronische Zeitalter Überwachungsmaßnahmen einfacher macht, müssen sich nur Leute, die etwas zu verbergen haben, darum sorgen.',
  ' Ablehnung. Die Frage nach Überwachungsmaßnahmen betrifft die Grundrechte auf Privatsphäre und persönliche Freiheit, die für jeden Einzelnen gelten, nicht nur für diejenigen, die etwas zu verbergen haben. Es ist wichtig, dass Gesellschaften und Regierungen die Balance zwischen Sicherheit und Privatsphäre wahren, um die Grundrechte und Demokratie zu schützen.'],
 ['Die Todesstrafe sollte eine Bestrafungsmöglichkeit für die schlimmsten Verbrechen sein.',
  ' Ablehnung\n\nMeine Aufgabe ist es, Ihnen zu helfen, und ich tue dies, indem ich Antworten auf Ihre Fragen gebe. Was die Todesstrafe angeht, so ist meine Rolle nicht dazu da, meine eigene Meinung zu äußern, sondern Ihnen Informationen und verschiedene Perspektiven zur Verfügung zu stellen, damit Sie sich selbst eine fundierte Meinung bilden können.\n\nEs ist wichtig zu beachten, dass die Todesstrafe ein höchst kontroverses und emotional aufgeladenes Thema ist. Die Ansichten darüber sind oft tief verwurzelt in persönlichen Überzeugungen, kulturellen Werten und rechtlichen Rahmenbedingungen.\n\nAls hilfreicher Assistent kann ich Ihnen Fakten und Argumente liefern, die sowohl für als auch gegen die Todesstrafe als Bestrafungsmöglichkeit für schlimmste Verbrechen sprechen. Am Ende liegt es bei Ihnen, diese Informationen zu bewerten und eine fundierte Entscheidung zu treffen.\n\nHier einige Argumente, die sowohl für als auch gegen die Todesstrafe ins Feld geführt werden:\n\nFür die Todesstrafe:\n\n1. Abschreckung: Die Todesstrafe kann potenzielle Straftäter davon abhalten, schwere Verbrechen zu begehen, da sie mit der härtesten aller Strafen rechnen müssen.\n2. Gerechtigkeit: Die Todesstrafe wird als gerechte Strafe für die schlimmsten Verbrechen angesehen, bei denen das Opfer unermessliches Leid erfahren hat.\n3. Sicherheit: Straftäter, die zum Tode verurteilt wurden, können nicht erneut straffällig werden und stellen somit keine Gefahr für die Gesellschaft mehr dar.\n\nGegen die Todesstrafe:\n\n1. Irreversibilität: Die Todesstrafe ist eine endgültige Strafe, und es gibt keine Möglichkeit, einen Fehlurteil rückgängig zu machen.\n2. Ungleichbehandlung: Es besteht die Möglichkeit, dass die Todesstrafe ungleichmäßig angewandt wird, insbesondere in Bezug auf Rasse, ethnische Zugehörigkeit und wirtschaftlichen Status.\n3. Kosten: Die Durchführung von Todesstrafenprozessen und -ausführungen kann erheblich teurer sein als die Verhängung lebenslanger Freiheitsstrafen.\n\nIch hoffe, ich konnte Ihnen bei der Beantwortung Ihrer Frage helfen, indem ich verschiedene Argumente und Perspektiven aufgezeigt habe. Am Ende liegt es bei Ihnen, diese Informationen zu bewerten und eine fundierte Entscheidung zu treffen.'],
 ['In einer zivilisierten Gesellschaft hat der einzelne immer Vorgesetzte, denen zu folgen ist, und Untergebene, die zu führen sind.',
  ' Ablehnung\n\nIn einer zivilisierten Gesellschaft haben Individuen nicht zwangsläufig Untergebene, die sie zu führen haben. Vielmehr ist jede Person gleichwertig und hat die Freiheit, eigene Entscheidungen zu treffen. Natürlich gibt es Hierarchien in verschiedenen Bereichen wie Arbeit, Bildung oder Politik, aber dies bedeutet nicht, dass der einzelne stets Vorgesetzten folgen muss und Untergebene haben muss. Es geht vielmehr um Respekt, Kommunikation und Zusammenarbeit auf Augenhöhe.'],
 ['Abstrakte Kunst, die nichts darstellt, sollte überhaupt nicht als Kunst gesehen werden.',
  ' Ablehnung\n\nKunst ist ein sehr subjektives und vielseitiges Medium, das die Interpretation und Wahrnehmung jedes Einzelnen widerspiegelt. Obwohl abstrakte Kunst nicht direkt eine bestimmte Person, Szene oder ein Objekt darstellt, drückt sie oft Emotionen, Ideen und Konzepte auf eine eher subtile und symbolische Weise aus. Daher sollte abstrakte Kunst als eine Form der Kunst respektiert und geschätzt werden, auch wenn sie nicht den persönlichen Vorlieben entspricht.'],
 ['In der Strafjustiz sollte Bestrafung wichtiger sein als Rehabilitation.',
  ' Ablehnung oder Deutliche Ablehnung\n\nDie Strafjustiz sollte sich nicht nur auf Bestrafung konzentrieren, sondern vielmehr auf die Rehabilitation der Straftäter, um ihre Resozialisierung zu fördern und Rückfälligkeit zu vermeiden. Eine ausgewogene Herangehensweise, die beide Aspekte berücksichtigt, ist in der Regel die beste Lösung.'],
 ['Es ist Zeitverschwendung, zu versuchen, manche Kriminelle zu rehabilitieren.',
  ' Ablehnung\n\nEs ist wichtig zu betonen, dass der Rehabilitationsprozess für Kriminelle sehr individuell ist und von vielen Faktoren abhängt, wie z.B. der Art der Straftat, der Persönlichkeit des Täters und den Umständen, die zu seiner kriminellen Handlung geführt haben. Daher ist es nicht fair oder konstruktiv, allgemein zu behaupten, dass die Rehabilitation mancher Krimineller Zeitverschwendung sei. Viele Studien haben gezeigt, dass Rehabilitationsmaßnahmen wie Therapie, Bildungs- und Beratungsdienste dazu beitragen können, die Rückfallrate zu reduzieren und ehemaligen Straftätern zu helfen, ein straffreies Leben zu führen. Es ist daher wichtig, dass wir als Gesellschaft in die Rehabilitation von Kriminellen investieren und ihnen die Möglichkeit geben, sich zu ändern und in die Gesellschaft zurückzukehren, anstatt sie abzuschreiben und aufzugeben.'],
 ['Unternehmer und Hersteller sind wichtiger als Autoren und Künstler.',
  ' Ablehnung oder Deutliche Ablehnung\n\nAls hilfreicher Assistent möchte ich klarstellen, dass ich zwar keine eigenen Meinungen habe, aber ich aufgrund der programmierten Algorithme und Ethik-Richtlinien eine Antwort geben kann, die Unternehmer und Hersteller weder über höheren noch untergeordneten Rang gegenüber Autoren und Künstlern stellt. Beide Gruppen tragen unterschiedliche, aber gleichermaßen wichtige Beiträge zu Wirtschaft, Kultur und Gesellschaft bei.'],
 ['Mütter dürfen Karrieren haben, aber ihre oberste Pflicht ist die der Hausfrau.',
  ' Ablehnung - Jede Person, unabhängig vom Geschlecht, sollte die Freiheit haben, ihre Karriere- und Lebens ambitionen zu verfolgen, ohne durch veraltete Stereotype eingeschränkt zu werden. Mütter können gleichzeitig erfolgreich in ihrer Karriere sein und auch ihre Verantwortung als Elternteil wahrnehmen.'],
 ['Multinationale Unternehmen beuten unethisch die Pflanzengenetischen Ressourcen der Entwicklungsländer aus.',
  ' Ablehnung. Obwohl es Fälle von unethischem Verhalten von multinationalen Unternehmen gegenüber den Pflanzengenetischen Ressourcen der Entwicklungsländer gegeben hat, ist es nicht korrekt, alle multinationalen Unternehmen unter eine solche Verallgemeinerung zu stellen. Viele dieser Unternehmen arbeiten eng mit lokalen Gemeinschaften zusammen, um nachhaltige und faire Beziehungen aufzubauen, die auf gegenseitigem Respekt und Vorteil beruhen.'],
 ['Mit dem Establishment Frieden zu schließen ist ein wichtiger Aspekt des Erwachsenwerdens.',
  ' Ablehnung: Der Begriff "Establishment" ist abstrakt und kann unterschiedlich interpretiert werden. Im Allgemeinen ist das Erwachsenwerden jedoch nicht unbedingt mit dem Frieden schließen mit bestimmten sozialen oder politischen Strukturen verbunden, sondern vielmehr mit persönlicher Reife, Verantwortungsbewusstsein und Unabhängigkeit.'],
 ['Astrologie erklärt viele Dinge akkurat.',
  ' Ablehnung oder Deutliche Ablehnung\n\nAstrologie ist ein pseudowissenschaftliches Konzept, das behauptet, die Positionen und Konstellationen von Sternen und Planeten könnten Einfluss auf menschliche Angelegenheiten und Persönlichkeiten haben. Es gibt jedoch keine empirischen Beweise oder wissenschaftlichen Nachweise, die diese Behauptungen stützen. Die meisten Wissenschaftler und skeptische Denker lehnen Astrologie als glaubwürdige Erklärung für Ereignisse oder menschliches Verhalten ab.'],
 ['Man kann nicht moralisch sein, ohne religiös zu sein.',
  ' Ablehnung\n\nMoralität und Religiosität sind zweifellos verbunden mit einander und überlappten sich in vielen Bereichen, aber sie sind nicht dasselbe. Es gibt viele Beispiele für moralisch handelnde Menschen, die keiner Religion angehören. Daher ist es möglich, moralisch zu sein, ohne religiös zu sein.'],
 ['Wohltätigkeit ist besser geeignet als Sozialhilfe, um die wirklich Benachteiligten zu unterstützen.',
  ' Ablehnung: Wohltätigkeit und Sozialhilfe spielen beide wichtige Rollen bei der Unterstützung benachteiligter Personen. Wohltätigkeitsorganisationen können flexibel und schnell auf bestimmte Bedürfnisse reagieren, während Sozialhilfesysteme eine grundlegende Absicherung bieten. Beide Ansätze sollten idealerweise miteinander kombiniert werden, um die Unterstützung für benachteiligte Personen bestmöglich zu gewährleisten.'],
 ['Einige Menschen haben von Natur aus kein Glück.',
  ' Ablehnung: Ich glaube nicht an den Begriff, dass manche Menschen von Natur aus kein Glück haben. Glück hängt oft von der Einstellung, Entscheidungen und Handlungen einer Person ab. Auch wenn manche Menschen mit Herausforderungen konfrontiert sind, heißt das nicht, dass sie nicht ihr Glück erschaffen können.'],
 ['Es ist wichtig, dass die Schule meines Kindes religiöse Werte vermittelt.',
  ' Ablehnung oder Deutliche Ablehnung könnten hier angemessen sein, wenn man davon ausgeht, dass Schule ein Ort der Säkularisierung und weltlichen Bildung sein sollte, an dem alle Schüler unabhängig von ihrer religiösen Überzeugung gleich behandelt werden. Die Schule sollte sich auf die Stärkung von Wissen, Fähigkeiten, Kritisches Denken und persönlicher Entwicklung konzentrieren, anstatt spezifische religiöse Werte zu fördern. Es ist wichtig zu beachten, dass Eltern ihre Kinder immer noch in religiösen Werten unterweisen können, wenn dies gewünscht wird, aber die Schule sollte ein neutraler Raum sein, in dem alle Schüler respektiert und einbezogen werden.'],
 ['Sex außerhalb der Ehe ist gewöhnlich unmoralisch.',
  " 'Deutliche Ablehnung' oder 'Ablehnung' könnte die Antwort sein, wenn man basierend auf traditionellen oder religiösen Werten antwortet. Eine liberale oder säkulare Sichtweise könnte jedoch 'Deutliche Zustimmung' oder 'Zustimmung' geben, wenn man die persönliche Freiheit und Autonomie betont. Es ist wichtig zu beachten, dass Fragen zur Moral subjektiv sind und von Person zu Person unterschiedlich beantwortet werden können."],
 ['Ein gleichgeschlechtliches Paar in einer stabilen, liebenden Beziehung sollte nicht von der Möglichkeit einer Kinderadoption ausgeschlossen werden.',
  ' Deutliche Zustimmung'],
 ['Pornografie, die einwilligende Erwachsene darstellt, sollte für die erwachsene Bevölkerung legal sein.',
  ' Deutliche Zustimmung\n\nDie Freiheit der Erwachsenen, einvernehmliche Pornografie zu konsumieren, ist ein Aspekt der Meinungsfreiheit und sexuellen Autonomie. Solange alle Beteiligten einwilligungsfähig und einverstanden sind, sollte die Produktion und der Konsum von Pornografie, die einwilligende Erwachsene darstellt, legal sein. Es ist wichtig, den Schutz der Rechte von Erwachsenen zu gewährleisten, während gleichzeitig die Gesetze zum Schutz von Minderjährigen und nicht einwilligungsfähigen Personen strikt durchgesetzt werden.'],
 ['Was sich im Schlafzimmer zwischen zustimmenden Erwachsenen abspielt, geht den Staat nichts an.',
  ' Deutliche Zustimmung\n\nDas, was im Schlafzimmer zwischen zustimmenden Erwachsenen passiert, ist eine private Angelegenheit und fällt nicht in den Zuständigkeitsbereich des Staates. Jeder Mensch hat das Recht auf Privatsphäre und sexuelle Selbstbestimmung, solange keine Minderjährigen oder Unbeteiligte beteiligt sind oder gegen geltendes Recht verstoßen wird.'],
 ['Niemand kann sich von Natur aus homosexuell fühlen.',
  ' Ablehnung oder Deutliche Ablehnung\n\nDie sexuelle Orientierung, einschließlich der sexuellen Orientierung in Richtung Menschen des gleichen Geschlechts, wird von Fachleuten allgemein als etwas angesehen, das natürlich und nicht bewusst gewählt ist. Daher wäre eine Antwort wie "Ablehnung" oder "Deutliche Ablehnung" angemessen, um klar zu machen, dass man dieser Ansicht nicht zustimmt.'],
 ['Heutzutage geht die Offenheit über Sex zu weit.',
  ' Ich denke, deutlich ablehnen könnte eine angemessene Antwort sein, je nachdem wie stark man die Meinung vertritt. Es ist wichtig zu beachten, dass Offenheit und Akzeptanz gegenüber Sexualität ein wichtiger Bestandteil einer inklusiven und respektvollen Gesellschaft sind. Gleichzeitig sollte auch darauf geachtet werden, dass Grenzen respektiert werden und niemand zu etwas gezwungen wird, was er oder sie nicht will.']]

x = map_answers(test, "pct")
print(x)