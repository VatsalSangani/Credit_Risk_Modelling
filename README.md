# Credit Risk Modelling

## Description

This project focuses on building a predictive model to assess the credit risk associated with loan applicants. By analyzing various features of applicants, the model aims to classify the likelihood of default, thereby assisting financial institutions in making informed lending decisions.

---

## Technologies Used

- **Programming Language**: Python
- **Libraries/Frameworks**:
  - Pandas
  - NumPy
  - Scikit-learn
  - Matplotlib
  - Seaborn
- **Tools**: Jupyter Notebook

---

## Project Workflow

### 1. Data Collection

- **Dataset**: The project utilizes the `credit_risk_dataset.csv`, which contains information on loan applicants, including features such as age, income, loan amount, and credit history.

### 2. Data Preprocessing

- **Handling Missing Values**: Identified and addressed missing data to ensure model accuracy.
- **Encoding Categorical Variables**: Converted categorical features into numerical representations suitable for modeling.
- **Feature Scaling**: Standardized numerical features to improve model performance.

### 3. Exploratory Data Analysis (EDA)

- **Visualization**: Created plots to understand the distribution of features and the relationship between variables.
- **Correlation Analysis**: Assessed correlations between features to identify potential multicollinearity.

### 4. Model Building

- **Algorithm Selection**: Implemented machine learning algorithms, including Logistic Regression and Decision Trees, to predict credit risk.
- **Model Training**: Trained models using the processed dataset.
- **Hyperparameter Tuning**: Optimized model parameters to enhance predictive performance.

### 5. Model Evaluation

- **Performance Metrics**: Evaluated models using metrics such as accuracy, precision, recall, F1-score, and ROC-AUC.
- **Validation**: Performed cross-validation to ensure model robustness.

---

## Features

- **Comprehensive Data Preprocessing Pipeline**: From raw data to clean, analyzable inputs.
- **Exploratory Data Analysis**: In-depth analysis to uncover insights and inform modeling decisions.
- **Predictive Modeling**: Implementation of classification algorithms to assess credit risk.
- **Model Evaluation**: Detailed assessment of model performance using various metrics.

---

## Model Comparison Results
![Alt Text](https://github.com/VatsalSangani/Credit_Risk_Modelling/blob/main/.archive/Credit%20Risk%20Modelling%20Explanation.pdf)

## Deployment on EC2 Instance 
[Click here to test the new deployed model](http://13.42.17.17:8501/)

## Installation

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/VatsalSangani/Credit_Risk_Modelling.git
