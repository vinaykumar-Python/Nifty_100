import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_next_3_years(df, value_column):

    data = df[["year", value_column]].dropna().copy()

    if len(data) < 5:
        return None

    data["year"] = (
        data["year"]
        .str.extract(r'(\d{4})')
        .astype(int)
    )

    X = data[["year"]]
    y = data[value_column]

    model = LinearRegression()
    model.fit(X, y)

    future = pd.DataFrame({
        "year": [
            data["year"].max() + 1,
            data["year"].max() + 2,
            data["year"].max() + 3,
        ]
    })

    future[value_column] = model.predict(future)

    return pd.concat([data, future], ignore_index=True)