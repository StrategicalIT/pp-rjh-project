url = "http://api.wunderground.com/api/yourkey/conditions/q/AU/melbourne.json"
        response = requests.get(url)
        parsed = json.loads(response.content)
        weather = parsed["current_observation"]["weather"]
        temp = parsed["current_observation"]["temp_c"]
        hum = parsed["current_observation"]["relative_humidity"]