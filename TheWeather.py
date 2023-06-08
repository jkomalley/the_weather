import requests
# import json


class TheWeather():
    def __init__(self, latitude: float = 0.0, longitude: float = 0.0):
        """Initialize TheWeather module
        :param latitude:
        :param longitude:
        """
        self.latitude = latitude
        self.longitude = longitude

    def get_grid_endpoints_from_coordinates(self):
        points_url = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
        try:
            response = requests.get(points_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            ret = response.json()
        except requests.exceptions.JSONDecodeError as err:
            raise SystemExit(err)

        return ret

    def get_current_detailed_forcast(self) -> str | None:
        """Retrieve the current forecast from the NWS
        :return: str
        """
        detailed_forecast = None
        grid_endpoints_metadata = self.get_grid_endpoints_from_coordinates()

        try:
            forecast_url = grid_endpoints_metadata["properties"]["forecast"]
        except KeyError as err:
            raise SystemExit(err)

        try:
            response = requests.get(forecast_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError as err:
            raise SystemExit(err)

        detailed_forecast = response_json["properties"]["periods"][0]["detailedForecast"]

        return detailed_forecast

    def print_current_weather(self) -> None:
        print(f"The weather for {self.latitude},{self.longitude}:")
        cur_weather = self.get_current_detailed_forcast()
        if cur_weather is not None:
            print(cur_weather)
        else:
            print("Unable to retrieve weather info at this time.")


if __name__ == "__main__":
    tw = TheWeather(39.207069, -76.727173)
    tw.print_current_weather()
