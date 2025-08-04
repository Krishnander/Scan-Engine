# AI Malware Detection Engine

This project provides a framework for building an AI-powered malware detection engine. It includes scripts for training a model on the EMBER dataset, making predictions, and a foundation for custom feature extraction.

## Project Goal

The goal is to create a state-of-the-art malware detection model using open-source AI frameworks and tools. This repository provides the code to train and evaluate such a model.

***Note:*** *The EMBER dataset is too large to be included in this repository. You will need to download it separately to run the training scripts.*

## Project Structure

```
.
├── README.md
├── data/
│   └── (This directory will be created by the download script)
├── models/
│   └── (This directory will be created by the training script)
├── scripts/
│   ├── download_data.py      # (Deprecated) Helper to download the dataset
│   ├── simple_download.py    # (Deprecated) A simpler download script
│   ├── train_model.py        # Trains the model on the EMBER dataset
│   └── predict.py            # Makes predictions using the trained model
├── src/
│   └── features/
│       └── static_features.py  # Extracts static features from PE files
└── requirements.txt
```

## Getting Started

### 1. Install Dependencies

First, install the necessary Python libraries. It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
pip install git+https://github.com/elastic/ember.git
```

### 2. Download the Dataset

You need to download the EMBER 2018 dataset. You can do this manually:

1.  **Download the data** from: [https://ember.elastic.co/ember_dataset_2018_2.tar.bz2](https://ember.elastic.co/ember_dataset_2018_2.tar.bz2)
2.  **Create a `data` directory** in the root of this project.
3.  **Extract the contents** of the downloaded `tar.bz2` file into the `data/` directory. You should have a `data/ember2018` directory.

### 3. Train the Model

Once the data is in place, you can train the model by running:

```bash
python scripts/train_model.py
```

This will train a LightGBM model and save it to the `models/` directory as `ember_model.joblib`.

### 4. Make Predictions

To see how to make a prediction, you can run the prediction script:

```bash
python scripts/predict.py
```

This script demonstrates how to load the model and make a prediction on a sample feature vector. You can modify this script to predict on your own files.

## Custom Feature Extraction

The script `src/features/static_features.py` provides a starting point for extracting your own features from PE files. You can extend this script and integrate it into your own data processing pipeline.

This allows you to train models on data other than the EMBER dataset.
