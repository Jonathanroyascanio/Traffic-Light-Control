import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

if __name__ == '__main__':
    # Define file paths
    csv_file_v1 = "./independent_eval_cyclic.csv"
    csv_file_v2 = "./FinalJudgment_TunedV2.csv"

    # Read the CSV files
    df_v1 = pd.read_csv(csv_file_v1)
    df_v2 = pd.read_csv(csv_file_v2)

    # List of columns to plot
    columns_to_plot = ['system_total_stopped', 'system_total_waiting_time', 'system_mean_waiting_time', 'system_mean_speed', 
                    't_stopped', 't_accumulated_waiting_time', 't_average_speed', 'agents_total_stopped', 
                    'agents_total_accumulated_waiting_time']

    # Create plots
    for column in columns_to_plot:
        fig = go.Figure()

        # Add traces for each CSV file
        if column = 
        fig.add_trace(go.Scatter(x=df_v1['step'], y=df_v1[column], mode='lines', name=f'Cyclic agent {column}'))
        fig.add_trace(go.Scatter(x=df_v2['step'], y=df_v2[column], mode='lines', name=f'TunedV2 {column}'))

        # Set title and labels
        fig.update_layout(
            title=f'{column} vs Steps',
            xaxis_title='Steps',
            yaxis_title=column,
            template='plotly_white'
        )

        # Show the plot
        fig.show()

