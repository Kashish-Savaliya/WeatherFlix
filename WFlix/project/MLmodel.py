import pandas as pd
import pickle

weather = pd.read_csv("/WFlix/project/IndianWeatherRepository_2.csv",
                      index_col="location_name")

null_pct = weather.isnull().sum() / weather.shape[0]

valid_columns = weather.columns[null_pct < 0.05]
weather = weather[valid_columns].copy()

weather["humidity"].plot()

weather.last_updated = pd.to_datetime(weather.last_updated, dayfirst=True, format='mixed')

target_columns = ['temperature_celsius', 'humidity', 'wind_mph', 'feels_like_celsius', 'visibility_km']

# for column in target_columns:
#     weather[f"target_{column}"] = weather[column].shift(-1)
#
# weather = weather.ffill()

from sklearn.linear_model import Ridge

rr = Ridge(alpha=0.1)
pickle.dump(rr, open('MLmodel.pkl', 'wb'))
predictors = weather.columns[~weather.columns.isin(
    ["target", "region", "country", "timezone", "condition_text", "wind_direction", "moon_phase", "sunrise", "sunset",
     "moonrise", "moonset"])]


def pct_diff(old, new):
    return (new - old) / old


def compute_rolling(weather, horizon, col):
    label = f"rolling_{horizon}_{col}"
    weather[label] = weather[col].rolling(horizon).mean()
    weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
    return weather


def backtest(weather, model, predictors, start, step):
    for column in target_columns:
        weather[f"target_{column}"] = weather[column].shift(-1)
    weather = weather.ffill()

    all_predictions = []
    for i in range(start, weather.shape[0], step):
        train = weather.iloc[:i, :]
        test = weather.iloc[i:(i + step), :]
        target_variables = ['target_humidity','target_temperature_celsius' , 'target_wind_mph',
                            'target_feels_like_celsius', 'target_visibility_km']
        for target_var in target_variables:
            model.fit(train[predictors], train[target_var])
            preds = model.predict(test[predictors])
            preds = pd.Series(preds, index=test.index)
            combined = pd.concat([test[target_var], preds], axis=1)
            combined.columns = [f"actual_{target_var}", f"prediction_{target_var}"]
            combined[f"diff_{target_var}"] = (
                        combined[f"prediction_{target_var}"] - combined[f"actual_{target_var}"]).abs()
            all_predictions.append(combined)

    #     rolling_horizons = [3, 14]
    #     for horizon in rolling_horizons:
    #         for col in ["temperature_celsius", "precip_mm", "humidity", "feels_like_celsius"]:
    #             weather = compute_rolling(weather, horizon, col)
    #
    # weather = weather.iloc[14:, :]
    weather = weather.ffill()
    # weather.last_updated = pd.to_datetime(weather.last_updated)
    # weather = weather.drop_duplicates(subset="last_updated")

    return pd.concat(all_predictions)

# print(weather)
# import pandas as pd
# weather.last_updated = pd.to_numeric(weather.last_updated)
# predictions = backtest(weather,rr,predictors,3650,90)
# predictions = predictions.ffill().bfill()
# print(predictions)