from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate Graph-Based Features
def create_graph_and_extract_features(num_users):
    G = nx.erdos_renyi_graph(num_users, 0.1)
    features = []
    for node in G.nodes():
        degree = G.degree(node)
        clustering = nx.clustering(G, node)
        betweenness = nx.betweenness_centrality(G).get(node, 0)
        features.append([degree, clustering, betweenness])

    return pd.DataFrame(features, columns=['degree', 'clustering_coefficient', 'betweenness_centrality']), G

# Generate Traditional Features
def generate_synthetic_data(num_users, graph):
    np.random.seed(42)
    followers = [graph.degree[node] for node in graph.nodes()]
    number_of_posts, number_of_requests, account_age_days, labels = [], [], [], []

    for i in range(num_users):
        degree = followers[i]
        account_age = np.random.randint(30, 365)

        if degree > 5:
            label = 0
            posts = np.random.randint(50, 500)
            requests = np.random.randint(10, 100)
        else:
            label = 1
            posts = np.random.randint(50, 200)
            requests = np.random.randint(0, 10)

        if label == 1:
            posts += np.random.randint(100, 300)
        else:
            posts += np.random.randint(50, 150)

        number_of_posts.append(posts)
        number_of_requests.append(requests)
        account_age_days.append(account_age)
        labels.append(label)

    data = {
        'number_of_posts': number_of_posts,
        'number_of_requests': number_of_requests,
        'account_age_days': account_age_days,
        'number_of_followers': followers,
        'label': labels
    }
    
    return pd.DataFrame(data)

# Merge Features
def merge_features(graph_features, traditional_features):
    return pd.concat([traditional_features, graph_features], axis=1)

# Build ANN Model
def build_ann_model(input_shape):
    model = models.Sequential([
        layers.Input(shape=(input_shape,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train Models
def train_classifiers(X_train, y_train):
    svm_model = SVC(probability=True)
    xgb_model = XGBClassifier()
    ann_model = build_ann_model(X_train.shape[1])
    
    ann_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    svm_model.fit(X_train, y_train)
    xgb_model.fit(X_train, y_train)

    return svm_model, ann_model, xgb_model

# Max Voting
def max_voting(svm_model, ann_model, xgb_model, X_test):
    svm_preds = svm_model.predict(X_test)
    ann_preds = (ann_model.predict(X_test) > 0.5).astype(int)
    xgb_preds = xgb_model.predict(X_test)

    all_preds = np.stack([svm_preds, ann_preds.flatten(), xgb_preds], axis=1)
    final_preds = [np.bincount(pred).argmax() for pred in all_preds]
    
    return np.array(final_preds)

# Generate Graph Image
def generate_graph_image(G, predictions, test_nodes):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)

    # Default color for all nodes (gray = unknown)
    node_colors = ['gray'] * len(G.nodes)

    # Assign red (fake) or green (real) only for test nodes
    for idx, node in enumerate(test_nodes):
        if idx < len(predictions):  # Avoid out-of-bounds errors
            node_colors[node] = 'red' if predictions[idx] == 1 else 'green'

    nx.draw(G, pos, with_labels=True, node_size=300, node_color=node_colors, font_size=6, font_weight="bold")

    plt.title("Fake Profile Detection (Red = Fake, Green = Real)")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return graph_base64

# API Endpoint
@app.get("/generate")
def generate_data():
    num_users = 100

    graph_features, G = create_graph_and_extract_features(num_users)
    traditional_features = generate_synthetic_data(num_users, G)
    combined_features = merge_features(graph_features, traditional_features.drop(columns=['label']))
    labels = traditional_features['label']
    
    X_train, X_test, y_train, y_test = train_test_split(combined_features, labels, test_size=0.2, random_state=42)
    test_nodes = list(X_test.index)

    svm_model, ann_model, xgb_model = train_classifiers(X_train, y_train)
    predictions = max_voting(svm_model, ann_model, xgb_model, X_test)

    accuracy = accuracy_score(y_test, predictions)
    graph_base64 = generate_graph_image(G, predictions, test_nodes)

    return {
        "predictions": predictions.tolist(),
        "synthetic_data": traditional_features.iloc[test_nodes].to_dict(orient="records"),
        "accuracy": accuracy,
        "graph": graph_base64
    }
