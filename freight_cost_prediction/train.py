import joblib 
from pathlib import Path

from data_preprocessing import load_vendor_invoice_data , prepare_features,split_data
from model_evaluation import(
   train_linear_regression,
   train_decisiontree_regression,
   train_randomforest_regression,
   evaluate_model
)

def main() : 
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "inventory.db"
    model_dir = Path("models")
    model_dir.mkdir(exist_ok = True)

    df = load_vendor_invoice_data(db_path)

    X,y = prepare_features(df)
    X_train,X_test,y_train,y_test = split_data(X,y)

    lr_model = train_linear_regression(X_train,y_train)
    dt_model = train_decisiontree_regression(X_train,y_train)
    rf_model = train_randomforest_regression(X_train,y_train)

    results = []
    results.append(evaluate_model(lr_model,X_test,y_test,"Linear regression"))
    results.append(evaluate_model(dt_model,X_test,y_test,"Decision tree regression"))
    results.append(evaluate_model(rf_model,X_test,y_test,"Randomforest regression"))

    best_model_info = min(results,key = lambda x: x["mae"])
    best_model_name = best_model_info["model_name"]

    best_model = {
        "Linear regression" : lr_model,
        "Decision tree regression" : dt_model,
        "Randomforest regression" : rf_model
    } [best_model_name]

    model_path = "models/prediction_freight_model.pkl"
    joblib.dump(best_model,model_path)

    print(f"\n Best model saved : {best_model_name}")
    print(f"Model path: {model_path}")

if __name__ == "__main__":
    main()
