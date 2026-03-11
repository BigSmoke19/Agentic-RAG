import wikipediaapi
import os

wiki = wikipediaapi.Wikipedia(
    user_agent="FootballRAG/1.0 (mohammadsafieddine789@gmail.com)",
    language="en"
)

# List of football topics you want
topics = [
    # Champions League Finals
    "2010 UEFA Champions League Final",
    "2011 UEFA Champions League Final",
    "2012 UEFA Champions League Final",
    "2013 UEFA Champions League Final",
    "2014 UEFA Champions League Final",
    "2015 UEFA Champions League Final",
    "2016 UEFA Champions League Final",
    "2017 UEFA Champions League Final",
    "2018 UEFA Champions League Final",
    "2019 UEFA Champions League Final",
    "2020 UEFA Champions League Final",
    "2021 UEFA Champions League Final",
    "2022 UEFA Champions League Final",
    "2023 UEFA Champions League Final",
    "2024 UEFA Champions League Final",
    "2025 UEFA Champions League Final",

    # Ballon d'Or
    "Ballon d'Or 2010",
    "Ballon d'Or 2011",
    "Ballon d'Or 2012",
    "Ballon d'Or 2013",
    "Ballon d'Or 2014",
    "Ballon d'Or 2015",
    "Ballon d'Or 2016",
    "Ballon d'Or 2017",
    "Ballon d'Or 2018",
    "Ballon d'Or 2019",
    "Ballon d'Or 2021",
    "Ballon d'Or 2022",
    "Ballon d'Or 2023",
    "Ballon d'Or 2024",
    "Ballon d'Or 2025",

    # World Cups
    "2010 FIFA World Cup",
    "2014 FIFA World Cup",
    "2018 FIFA World Cup",
    "2022 FIFA World Cup",

    # GOATs
    "Lionel Messi",
    "Cristiano Ronaldo",

    # World Cup & UCL Winners
    "Andrés Iniesta",
    "Xavi Hernández",
    "Sergio Ramos",
    "Luka Modrić",
    "Karim Benzema",
    "Robert Lewandowski",
    "Neymar",
    "Kylian Mbappé",

    # Premier League Stars
    "Mohamed Salah",
    "Sadio Mané",
    "Kevin De Bruyne",
    "Virgil van Dijk",

    # World Cup Heroes
    "Thomas Müller",
    "Manuel Neuer",
    "Antoine Griezmann",
    "Paulo Dybala",

    # Recent Stars
    "Erling Haaland",
    "Vinicius Junior",
]

os.makedirs("football_data", exist_ok=True)

for topic in topics:
    page = wiki.page(topic)
    if page.exists():
        filename = topic.replace(" ", "_").replace("/", "-") + ".txt"
        with open(f"football_data/{filename}", "w", encoding="utf-8") as f:
            f.write(page.text)
        print(f"✅ Saved: {filename}")
    else:
        print(f"❌ Not found: {topic}")


### Then Your RAG Will Answer Questions Like:

###You: who won the champions league final in 2013?
###Agent: Bayern Munich won the 2013 UEFA Champions League Final...

###You: who won ballon d'or in 2016?
###Agent: Cristiano Ronaldo won the 2016 Ballon d'Or...

###You: how many goals did Messi score in 2022 world cup?
###Agent: Lionel Messi scored 7 goals in the 2022 FIFA World Cup...
