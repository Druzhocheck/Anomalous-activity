import pandas as pd
from sklearn.ensemble import IsolationForest
import gpt
from sklearn.preprocessing import OneHotEncoder

def anomaly(dataset):
    anomaly_index = machinelearning(dataset)
    anomaly_msg = dataset["_CMDLINE"].iloc[anomaly_index]
    anomaly_desciption = pd.DataFrame(anomaly_msg.drop_duplicates())
    
    # отработка изоляционного леса
    print(anomaly_desciption["_CMDLINE"])
    
    anomaly_desciption["description"] = [gpt.get_resp(1, cmdline) for cmdline in anomaly_desciption["_CMDLINE"]]
    anomaly_desciption = anomaly_desciption[anomaly_desciption["description"] == "Да."]
    anomaly_desciption["description"] = [gpt.get_resp(2, cmdline) for cmdline in anomaly_desciption["_CMDLINE"]]
    anomaly_desciption["SYSLOG_TIMESTAMP"] = dataset["SYSLOG_TIMESTAMP"]
    anomaly_desciption["_HOSTNAME"] = dataset["_HOSTNAME"]
    return anomaly_desciption

def machinelearning(dataset):
    features = ["_SYSTEMD_OWNER_UID", "_AUDIT_SESSION", "_GID", "_AUDIT_LOGINUID",
                "_SOURCE_REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", "SYSLOG_FACILITY",
                "_UID", "_PID", "__REALTIME_TIMESTAMP", "PRIORITY"]
    print("Длина датасета: ", len(dataset))
    dataset[features] = dataset[features].astype(float)
    dataset = dataset.dropna(subset=features)
    df = dataset[features]
    model=IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.1),max_features=1.0)
    model.fit(df)
    df['scores']=model.decision_function(df[features])
    df['anomaly']=model.predict(df[features])
    anomaly=df.loc[df['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    return anomaly_index

