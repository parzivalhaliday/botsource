# predict_gender.py

import requests
import os
import json

def predict_gender(summoner_info, champion_data):
    try:
        api_key = os.getenv('RIOT_API_KEY')
        region = 'europe'

        # Oyuncu bilgilerini ayır
        if "#" not in summoner_info:
            return "Lütfen doğru bir Riot ID ve etiket girin."

        summoner_name, tag_line = summoner_info.split("#", 1)

        response = requests.get(f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}')
        response.raise_for_status()
        summoner_data = response.json()

        summoner_puuid = summoner_data['puuid']
        # Top N mastery bilgilerini al
        mastery_url = f"https://tr1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_puuid}?api_key={api_key}"
        response_mastery = requests.get(mastery_url)

        if response_mastery.status_code == 200:
            mastery_data = response_mastery.json()

            total_mastery_points = sum(mastery["championPoints"]
                                       for mastery in mastery_data)

            # Kadın ve erkek şampiyonları ve çarpanları burada
            female_champions = {
            "Yuumi": 10,
            "Seraphine": 5,
            "Zyra": 6,
            "Vex": 4,
            "Sona": 10,
            "Syndra": 6,
            "Senna": 2,
            "Renata Glasc": 4,
            "Orianna": 2,
            "Neeko": 7,
            "Soraka": 10,
            "Nilah": 1.2,
            "Nami": 17,
            "Lux": 8,
            "Lulu": 2.5,
            "Morgana": 8,
            "Miss Fortune": 6,
            "Leona": 3,
            "Kai'Sa": 4,
            "Evelynn": 3,
            "Caitlyn": 5,
            "Ashe": 5,
            "Annie": 2,
            "Akali": 4,
            "Ahri": 7,
            "Janna": 7,
            "Karma": 7
            }

            male_champions = {
          "Aatrox": 10,
          "Akshan": 5,
          "Alistar": 10,
          "Azir": 10,
          "Braum": 3,
          "Corki": 10,
          "Darius": 9,
          "Draven": 11,
          "Dr. Mundo": 10,
          "Fiddlesticks": 10,
          "Fiora": 6,
          "Fizz": 7,
          "Gangplank": 7,
          "Garen": 8,
          "Gnar": 5.5,
          "Gragas": 8,
          "Graves": 10,
          "Hecarim": 10,
          "Heimerdinger": 3,
          "Illaoi": 2,
          "Jarvan IV": 8,
          "Jax": 13,
          "Jhin": 4.4,
          "Kalista": 8.5,
          "Kassadin": 10,
          "Karthus": 7,
          "Kayn": 4,
          "Kha'Zix": 6,
          "Kindred": 3,
          "Kled": 10,
          "Kog'Maw": 10,
          "Lee Sin": 6,
          "Lucian": 4,
          "Malphite": 8.7,
          "Malzahar": 6,
          "Maokai": 4,
          "Master Yi": 4,
          "Mordekaiser": 8,
          "Wukong": 7,
          "Nasus": 9,
          "Nautilus": 8,
          "Nocturne": 10,
          "Olaf": 9.9,  
          "Pantheon": 8,
          "Ornn": 10,
          "Pyke": 5,
          "Rammus": 6,
          "Rek'Sai": 10,
          "Rengar": 15,
          "Rumble": 3,
          "Ryze": 10,
          "Shaco": 10,
          "Skarner": 25,
          "Sion": 8,
          "Singed": 15,
          "Swain": 4,
          "Talon": 10,
          "Trundle": 8,
          "Tryndamere": 10,
          "Urgot": 15,
          "Viego": 3,
          "Viktor": 10,
          "Vladimir": 7,
          "Volibear": 10,
          "Warwick": 10,
          "Zed": 7,
          "Zac": 10,
          "Yorick": 15,
          "Yasuo": 7
        }


            female_points = sum(
                mastery["championPoints"] * female_champions.get(
                    champion_data.get(str(mastery["championId"]), "Bilinmiyor"), 1)
                for mastery in mastery_data
                if champion_data.get(str(mastery["championId"])) in female_champions)
            male_points = sum(
                mastery["championPoints"] *
                male_champions.get(champion_data.get(str(mastery["championId"]), "Bilinmiyor"), 1)
                for mastery in mastery_data
                if champion_data.get(str(mastery["championId"])) in male_champions)

            female_ratio = female_points / total_mastery_points
            male_ratio = male_points / total_mastery_points

            gender_emoji = "👧" if female_ratio > male_ratio else "👦"

            result = f"{summoner_name.replace('+', ' ')} adlı oyuncunun cinsiyeti: {'Kadın' if female_ratio > male_ratio else 'Erkek'} {gender_emoji}\n"
            result += f"Kadın olma ihtimali: {female_ratio:.2%}\n"
            result += f"Erkek olma ihtimali: {male_ratio:.2%}\n"

            return result
        else:
            return "Champion mastery data could not be fetched."
    except requests.RequestException as e:
        return f"An error occurred during API request: {e}"
