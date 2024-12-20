import csv
import re

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_metrics_text(text):
    # Initialize data structures to store metrics
    feature1_metrics = {}  # {checkpoint: {mode: rmse}}
    feature2_metrics = {}
    feature3_metrics = {}
    
    # Split the text into sections by checkpoint
    sections = text.strip().split('-----------------------\n')
    
    for section in sections:
        if not section.strip():
            continue
            
        # Extract checkpoint name and mode
        checkpoint_match = re.search(r'Checkpoint: (.+)\.pth', section)
        mode_match = re.search(r'Mode: (\dm)', section)
        
        if checkpoint_match and mode_match:
            checkpoint = checkpoint_match.group(1)
            mode = mode_match.group(1)
            
            # Extract RMSE values for each feature
            feature1_match = re.search(r'Metrics for Feature 1.*?RMSE: ([\d.]+)', section, re.DOTALL)
            feature2_match = re.search(r'Metrics for Feature 2.*?RMSE: ([\d.]+)', section, re.DOTALL)
            feature3_match = re.search(r'Metrics for Feature 3.*?RMSE: ([\d.]+)', section, re.DOTALL)
            
            if feature1_match:
                if checkpoint not in feature1_metrics:
                    feature1_metrics[checkpoint] = {}
                feature1_metrics[checkpoint][mode] = float(feature1_match.group(1))
                
            if feature2_match:
                if checkpoint not in feature2_metrics:
                    feature2_metrics[checkpoint] = {}
                feature2_metrics[checkpoint][mode] = float(feature2_match.group(1))
                
            if feature3_match:
                if checkpoint not in feature3_metrics:
                    feature3_metrics[checkpoint] = {}
                feature3_metrics[checkpoint][mode] = float(feature3_match.group(1))
    
    return feature1_metrics, feature2_metrics, feature3_metrics

def write_csv(metrics, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Checkpoint', '1m', '4m', '6m'])
        
        # Write data rows
        for checkpoint in metrics:
            row = [
                checkpoint,
                metrics[checkpoint].get('1m', ''),
                metrics[checkpoint].get('4m', ''),
                metrics[checkpoint].get('6m', '')
            ]
            writer.writerow(row)

def main(input_file_path):
    try:
        # Read the input file
        input_text = read_input_file(input_file_path)
        
        # Parse the metrics
        feature1_metrics, feature2_metrics, feature3_metrics = parse_metrics_text(input_text)
        
        # Write to CSV files
        write_csv(feature1_metrics, 'quang/time_series_prediction/ablation_experiments/feature1_rmse.csv')
        write_csv(feature2_metrics, 'quang/time_series_prediction/ablation_experiments/feature2_rmse.csv')
        write_csv(feature3_metrics, 'quang/time_series_prediction/ablation_experiments/feature3_rmse.csv')
        
        print("CSV files have been generated successfully!")
        print("- feature1_rmse.csv")
        print("- feature2_rmse.csv")
        print("- feature3_rmse.csv")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    file_path = "quang/time_series_prediction/ablation_experiments/embeddings/results.txt"  # Replace with your actual file path
    main(file_path)