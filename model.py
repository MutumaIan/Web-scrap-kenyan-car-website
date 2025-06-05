import pandas as pd
import numpy as np
import optuna
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def load_dataset(filepaths):
    """Load and concatenate CSV files into a single DataFrame."""
    dfs = [pd.read_csv(fp) for fp in filepaths]
    df = pd.concat(dfs).reset_index(drop=True)
    return df


def train_model(df, target_column="Price"):
    """Train a price prediction model using XGBoost and Optuna."""
    X = df.drop(columns=[target_column])
    # Convert price strings like "KSh 1,200,000" to float
    y = df[target_column].astype(str).str.replace("[^0-9]", "", regex=True).astype(float)

    def objective(trial):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        params = {
            'eta': trial.suggest_float('eta', 0.005, 0.01),
            'n_estimators': trial.suggest_int('n_estimators', 400, 2000),
            'max_depth': trial.suggest_int('max_depth', 7, 9),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 1.0),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.5, 1.5),
            'min_child_weight': trial.suggest_float('min_child_weight', 1, 3),
            'learning_rate': trial.suggest_float('learning_rate', 0.005, 0.1),
            'nthread': -1,
            'early_stopping_rounds': 5,
        }
        model = XGBRegressor(**params)
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=0)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        return rmse

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=10)
    print("Best parameters:", study.best_params)
    print("Best RMSE:", study.best_value)
    return study.best_params


if __name__ == "__main__":
    # Example usage
    df = load_dataset(["car_listings.csv"])
    train_model(df)
