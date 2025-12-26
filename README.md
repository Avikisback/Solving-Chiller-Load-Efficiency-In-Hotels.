# Hotel Chiller Load Efficiency Predictor

This project is a Python-based application designed to predict the load of a hotel chiller system using Machine Learning. It utilizes a Random Forest Regressor to analyze environmental and operational data and provides recommendations for chiller operations to optimize efficiency.

## Features

-   **Data Integration**: Merges operational data (Power, Efficiency, Load) with environmental data (Temperature, Humidity).
-   **Machine Learning Model**: Trains a Random Forest Regressor to predict Chiller Load (`CH Load`).
-   **GUI Interface**: A user-friendly Tkinter interface allows users to input current conditions and get real-time predictions.
-   **Operational Recommendations**: Suggests chiller operating modes (e.g., "Turn on all chillers", "Run at low capacity") based on the predicted load.

## Prerequisites

-   Python 3.x
-   Required Python libraries (see `requirements.txt`)

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd hotel_chiller
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

**Important Note on Data Sources:**
The script currently references local Excel files for training the model:
-   `E:\python\hackathon\PLANT TON_EFFICIENCY\main.xlsx`
-   `E:\python\hackathon\TEMPERATURE\NEW.xlsx`

Before running the application, you must:
1.  Ensure you have the corresponding data files.
2.  Update the file paths in `Chiller Load Efficiency.py` (lines 14-15) to point to the correct location of these files on your machine.

## Usage

Run the main script to launch the application:

```bash
python "Chiller Load Efficiency.py"
```

### Using the GUI
1.  The application will launch a window titled "The Current Days Chiller Load".
2.  Enter the required parameters:
    -   Temperature [°C]
    -   Relative Humidity [%]
    -   Wet Bulb Temperature [°C]
    -   Total Power Consumption (kW_Tot)
    -   Power Efficiency (kW per Refrigeration Ton)
    -   Percentage of Chiller Load (Precent_CH)
    -   Refrigeration Tons (RT)
3.  Click the button (if available in the UI flow) to generate the prediction and operational advice.

## Project Structure

-   `Chiller Load Efficiency.py`: Main application script containing the ML model training and GUI code.
-   `requirements.txt`: List of Python dependencies.
-   `README.md`: Project documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

