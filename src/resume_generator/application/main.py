from dotenv import load_dotenv

import resume_generator.application.port_selector as settings
from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.prompt_generator import PromptGenerator


def main():
    load_dotenv()

    user_processor = settings.get_user_processor()
    user = user_processor.read_user()

    offer = """
About the job

Dołącz do zespołu R&D rozwijającego nowoczesne rozwiązania AI

Poszukujemy ML & GenAI Solutions Scientist, który dołączy do zespołu R&D rozwijającego innowacyjne rozwiązania oparte na uczeniu maszynowym oraz Generative AI dla międzynarodowych produktów Comarch. Jeśli lubisz analizować złożone problemy biznesowe, projektować modele ML i rozwijać rozwiązania wykorzystujące duże modele językowe (LLM), ta rola jest właśnie dla Ciebie.

Profil stanowiska

    minimum 2 lata komercyjnego doświadczenia w obszarze Data Science lub Machine Learning
    praktyczne doświadczenie w projektowaniu, trenowaniu, optymalizacji oraz ewaluacji modeli uczenia maszynowego
    bardzo dobrą znajomość Pythona, eksploracyjnej analizy danych (EDA) oraz inżynierii cech (Feature Engineering)
    doświadczenie w pracy z narzędziami do analizy danych, relacyjnymi bazami danych oraz technologiami przetwarzania rozproszonego (np. Apache Spark)
    doświadczenie z monitorowaniem modeli i metryk oraz znajomość narzędzi takich jak Grafana lub Prometheus
    znajomość języka angielskiego na poziomie minimum B2

Mile widziane

    praktyczna znajomość architektur RAG (Retrieval-Augmented Generation)
    znajomość metodyk Agile oraz AI Development Lifecycle (AIDLC)
    doświadczenie w projektach związanych z systemami lojalnościowymi

Twoje zadania

    analiza wymagań biznesowych oraz projektowanie modeli uczenia maszynowego odpowiadających na potrzeby produktu
    rozwój, optymalizacja i ewaluacja modeli ML oraz wsparcie zespołu w projektowaniu nowych rozwiązań analitycznych
    przygotowywanie dokumentacji technicznej i badawczej dla tworzonych modeli oraz rozwiązań AI
    udział w projektowaniu rozwiązań wykorzystujących Generative AI, architektury RAG oraz systemów agentowych opartych o LLM (Agentic AI
    współpraca przy projektowaniu rozwiązań przetwarzania danych oraz aplikacji działających w środowiskach chmurowych
    współpraca z zespołem R&D przy migracji i rozwoju nowej architektury systemowej oraz wdrażaniu innowacyjnych rozwiązań AI

Dla Ciebie

    Prywatna opieka medyczna w Allianz - dostęp do specjalistów i badań diagnostycznych dla Ciebie i Twoich najbliższych
    System kafeteryjny - możesz wybrać pełne dofinansowanie do karty Multisport czy przeznaczyć środki na kulturę, wypoczynek lub sport i zakupy
    Możliwość pracy w modelu hybrydowym po okresie wdrożenia (2 dni pracy zdalnej, 3 dni pracy z biura)
    Możliwość korzystania z zaawansowanych narzędzi AI i Google Workspace
    Współpraca z różnymi zespołami kompetencyjnymi, która pozwoli Ci na poznanie nowych technologii i poszerzenie wiedzy w obszarze IT
    Profesjonalny rozwój zawodowy, realny wpływ na podejmowane decyzje biznesowe

    """
    prompt_generator = PromptGenerator(offer, user)
    agent = AgentInvoker(prompt_generator)
    print(agent.get_user_education_summary())


if __name__ == "__main__":
    main()
