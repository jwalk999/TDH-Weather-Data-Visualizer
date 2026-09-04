


# search for weather stations using coordinates, print them to outputs.txt

with open(".venv/outputs.txt", "a") as f:

    import meteostat as ms

    STATION = ms.stations.meta("72301")

    print(STATION, file=f)