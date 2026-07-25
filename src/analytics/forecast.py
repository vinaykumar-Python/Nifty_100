import pandas as pd
from sklearn.linear_model import LinearRegression

import pandas as pd

def forecast_next_3_years(df, metric):

    print(df[["year", metric]].head(20))
    print(df["year"].unique())

    return None
    # Convert safely
    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    # Remove invalid years
    df = df.dropna(subset=["year"])

    if len(df) < 3:
        return None

    # Convert after removing NaNs
    df["year"] = df["year"].astype("int64")

    df = df.sort_values("year")

    X = df[["year"]]

    y = df[metric]

    model = LinearRegression()

    model.fit(X, y)

    last_year = int(df["year"].max())

    future = pd.DataFrame({
        "year": [
            last_year + 1,
            last_year + 2,
            last_year + 3
        ]
    })

    future[metric] = model.predict(future)

    history = df[["year", metric]]

    result = pd.concat(
        [history, future],
        ignore_index=True
    )

    return result