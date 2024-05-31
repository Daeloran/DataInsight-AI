
# DataInsight AI
DataInsight AI is an intelligent application designed to extract, analyze, and interpret data from various sources, initially focusing on Excel files, with future expansions to include Planning Analytics cubes and SQL databases. The goal of the application is to provide a versatile toolbox for data manipulation and interpretation, thereby facilitating informed decision-making through the integration of artificial intelligence.

## Key Features

1. **Data Ingestion**
	- **Data Sources**: Currently, the application supports Excel files. Future extensions will include Planning Analytics cubes and  SQL databases.
	- **Data Reading**: Utilizes the Pandas library to read and load data from Excel files.
2. **Data Preprocessing and Cleaning**
	- **Cleaning**: Removes missing values and normalizes data to ensure quality and consistency.
	- **Transformation**: Prepares data for more in-depth analysis.
3. **Data Analysis**
	- **Descriptive Statistics**: Computes basic statistical measures such as mean, median, standard deviation, etc.
	- **Trend Detection**: Identifies trends in the data to predict future behavior.
	- **Anomaly Detection**: Detects anomalies or outliers in datasets.
4. **Data Interpretation with AI**
	- **LLaMA 3 Model via LangChain**: Uses the LLaMA 3 model to provide intelligent and comprehensive interpretations of analysis results.
	- **Report Generation**: Produces detailed summaries and interpretative reports based on the analyses performed.
5. **Data Visualization (Upcoming)**
	- **Charts and Graphs**: Utilizes libraries such as Matplotlib or Plotly to generate graphical visualizations of data (e.g., line charts, bar charts, pie charts).

## Advantages
- **Versatility**: Designed to handle a wide range of data types and analysis scenarios.
- **Extensibility**: Easy to add new data sources and features over time.
- **Artificial Intelligence**: Advanced interpretation and detailed report generation using AI.
- **Usability**: Simple and intuitive interface requiring minimal user interaction in the initial version, with the possibility of user interaction in future versions.

## System Architecture

 1. **Data Ingestion**: Uses Pandas to read Excel files. 
 2. **Preprocessing**: Cleans and transforms data with Pandas. 
 3. **Analysis**: Performs basic data analysis with Pandas. 
 4. **Interpretation**: Integrates LangChain and the LLaMA 3 model for intelligent interpretation. 
 5. **Reports**: Generates detailed analysis summaries. 
 6. **(Optional) Visualization**: Uses Matplotlib or Plotly for graphical data visualizations.
