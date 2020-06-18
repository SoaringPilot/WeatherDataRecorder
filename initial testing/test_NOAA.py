from noaa_sdk import noaa
n = noaa.NOAA()
res = n.get_forecasts('28409', 'US', True)
for i in res:
    print(i)