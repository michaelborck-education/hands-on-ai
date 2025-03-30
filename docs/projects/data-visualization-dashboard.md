# Data Visualization Dashboard

**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Learning Focus**: Data analysis, visualization, pandas, matplotlib

## Overview

Create an interactive dashboard that allows users to visualize and explore data relationships through various chart types. Students will learn data manipulation with pandas and visualization with matplotlib.

## Instructions

```python
from ailabkit.chat import get_response
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random
import os
import numpy as np

def data_dashboard():
    """Interactive data visualization dashboard for exploring datasets"""
    
    # Sample dataset (students could replace with their own CSV)
    sample_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Temperature': [12, 14, 16, 19, 22, 25, 27, 26, 23, 19, 15, 13],
        'Rainfall': [50, 45, 35, 30, 25, 15, 10, 12, 20, 35, 40, 48],
        'Visitors': [120, 135, 190, 240, 310, 430, 590, 560, 420, 320, 190, 150]
    }
    
    # Create a DataFrame from the sample data
    df = pd.DataFrame(sample_data)
    
    print("=== Data Visualization Dashboard ===")
    print("This dashboard allows you to explore relationships in data.")
    
    # Create directory for plots if it doesn't exist
    plots_dir = "dashboard_plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    while True:
        print("\nOptions:")
        print("1. View data summary")
        print("2. Line chart")
        print("3. Bar chart")
        print("4. Scatter plot")
        print("5. Get AI insights")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            # Data summary
            print("\n=== Data Summary ===")
            print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print("\nColumns:")
            for column in df.columns:
                print(f"- {column}")
            
            print("\nSummary statistics:")
            print(df.describe())
            
            print("\nFirst few rows:")
            print(df.head())
            
        elif choice == '2':
            # Line chart
            print("\n=== Line Chart ===")
            print("Available columns:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            column_idx = int(input("\nSelect column to plot (1-3): ")) - 1
            column_to_plot = df.columns[column_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.plot(df['Month'], df[column_to_plot], marker='o', linewidth=2)
            plt.title(f'{column_to_plot} by Month')
            plt.xlabel('Month')
            plt.ylabel(column_to_plot)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"line_{column_to_plot.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nLine chart created and saved as {plot_filename}")
            
        elif choice == '3':
            # Bar chart
            print("\n=== Bar Chart ===")
            print("Available columns:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            column_idx = int(input("\nSelect column to plot (1-3): ")) - 1
            column_to_plot = df.columns[column_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.bar(df['Month'], df[column_to_plot], color='skyblue', edgecolor='navy')
            plt.title(f'{column_to_plot} by Month')
            plt.xlabel('Month')
            plt.ylabel(column_to_plot)
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"bar_{column_to_plot.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nBar chart created and saved as {plot_filename}")
            
        elif choice == '4':
            # Scatter plot
            print("\n=== Scatter Plot ===")
            print("Available columns for X-axis:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            x_idx = int(input("\nSelect X-axis column (1-3): ")) - 1
            x_column = df.columns[x_idx + 1]  # +1 to account for skipping 'Month'
            
            print("\nAvailable columns for Y-axis:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                if column != x_column:  # Don't show the X column again
                    print(f"{i}. {column}")
            
            y_idx = int(input("\nSelect Y-axis column (1-3): ")) - 1
            y_column = df.columns[y_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_column], df[y_column], color='purple', alpha=0.7, s=100)
            
            # Add month labels to each point
            for i, month in enumerate(df['Month']):
                plt.annotate(month, (df[x_column][i], df[y_column][i]), 
                             xytext=(5, 5), textcoords='offset points')
            
            plt.title(f'{y_column} vs {x_column}')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Optional: Add trendline
            plt.plot(np.unique(df[x_column]), 
                     np.poly1d(np.polyfit(df[x_column], df[y_column], 1))(np.unique(df[x_column])),
                     color='red', linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"scatter_{x_column.lower()}_{y_column.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nScatter plot created and saved as {plot_filename}")
            
        elif choice == '5':
            # AI insights
            print("\n=== AI Data Insights ===")
            
            try:
                # Prepare data summary for AI
                data_description = f"""
                Dataset with columns: {', '.join(df.columns)}
                Summary statistics:
                {df.describe().to_string()}
                
                First few rows:
                {df.head().to_string()}
                """
                
                insight_prompt = f"""
                Analyze this dataset and provide 3-5 key insights:
                {data_description}
                
                Focus on:
                1. Patterns or trends over months
                2. Correlations between variables
                3. Anomalies or interesting data points
                4. Suggestions for further analysis
                """
                
                print("Generating AI insights...")
                insights = get_response(insight_prompt)
                
                print("\n=== AI Analysis Results ===")
                print(insights)
                
            except Exception as e:
                print(f"Error getting AI insights: {e}")
                print("AI insight generation is not available.")
            
        elif choice == '6':
            print("\nExiting Dashboard. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please select a number between 1 and 6.")

# Run the dashboard
if __name__ == "__main__":
    data_dashboard()
```

## Extension Ideas

- Add more visualization types like pie charts, histograms, or heatmaps
- Implement data filtering options to explore subsets of the data
- Add the ability to load CSV files from disk
- Create a feature to export all visualizations as a report
- Implement interactive plots using libraries like Plotly
- Add clustering or other basic data analysis techniques

---