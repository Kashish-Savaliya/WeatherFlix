import pandas as pd
# weather = pd.read_csv("C:\\Users\\abc\\Desktop\\WeatherFlix\\myenv\\WFlix\\project\\IndianWeatherRepository_2.csv", index_col="location_name")
# weather.target=weather.shift(-1)["temperature_celsius"]
def backtest(weather,model,predictors,start,step):
  all_predictions = []
  for i in range(start,weather.shape[0],step):
    train = weather.iloc[:i,:]
    test = weather.iloc[i:(i+step),:]

    model.fit(train[predictors],train["target"])

    preds = model.predict(test[predictors])

    preds = pd.Series(preds,index=test.index)
    combined = pd.concat([test["target"],preds],axis=1)
    combined.columns = ["actual","prediction"]
    combined["diff"] = (combined["prediction"]-combined["actual"]).abs()
    all_predictions.append(combined).ffill().bfill()
    def pct_diff(old, new):
        return (new - old) / old

    def compute_rolling(weather, horizon, col):
        label = f"rolling_{horizon}_{col}"

        # weather[label]= weather[col].rolling(horizon).mean()
        weather[label] = weather[col].rolling(horizon).mean()
        weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
        return weather
    # print(weather)
    rolling_horizons = [3, 14]
    for horizon in rolling_horizons:
        for col in ["temperature_celsius", "precip_mm", "humidity", "feels_like_celsius"]:
            weather = compute_rolling(weather, horizon, col)
    weather = weather.iloc[14:, :]
    weather = weather.ffill()
    weather.last_updated = pd.to_datetime(weather.last_updated)
    weather.last_updated.duplicated().sum()
    weather = weather.drop_duplicates(subset="last_updated")

  return pd.concat(all_predictions)



