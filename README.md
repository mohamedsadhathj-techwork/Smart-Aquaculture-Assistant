# AI-Powered Smart Aquaculture Assistant

## Smart Fish Health Prediction & Water Quality Management System

### Project Overview

The AI-Powered Smart Aquaculture Assistant is an IoT and machine learning based system designed to monitor water conditions and assist in identifying fish health risks in aquaculture environments.

The system uses an ESP32 microcontroller connected with water-quality sensors. Sensor readings are collected and displayed through a Streamlit dashboard. Machine learning is used to analyse aquaculture data and classify fish health conditions.

### Objectives

- Monitor water conditions in real time.
- Collect sensor data using ESP32.
- Analyse important water-quality parameters.
- Predict fish health conditions.
- Provide warnings for abnormal conditions.
- Display sensor information through a monitoring dashboard.

### Hardware Components

- ESP32 DevKit
- DS18B20 Temperature Sensor
- pH Sensor
- TDS Sensor
- Water Level / Presence Sensor
- Breadboard
- Jumper Wires

### Software Technologies

- Python
- Jupyter Notebook
- Arduino IDE
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Machine Learning

A Random Forest Classifier is used for fish health classification.

The machine learning model is trained using:

- Temperature
- Dissolved Oxygen
- pH
- Turbidity

The target variable is:

- Health Status

The model classifies fish health into Stable and At Risk categories.

### Dataset

The project uses an aquaculture dataset containing water-quality and fish-health related information.

Important parameters include:

- Temperature
- Dissolved Oxygen
- pH
- Turbidity
- Fish Weight
- Survival Rate
- Disease Occurrence
- Health Status

### Live Sensor Monitoring

The current ESP32 prototype monitors:

- Temperature
- pH
- TDS
- Water Level / Presence

The sensor readings are sent to the computer through serial communication and displayed in the Streamlit application.

### System Workflow

```text
Sensors
   ↓
ESP32 Microcontroller
   ↓
Sensor Data Collection
   ↓
Data Processing
   ↓
Fish Health Analysis
   ↓
Health Status / Warning
   ↓
Smart Aquaculture Monitoring Dashboard
