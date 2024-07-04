# Writing Feature Extractor

## Overview

Writing Feature Extractor is a tool designed to analyze creative writing samples and extract various literary features using advanced language models. It provides insights into aspects such as emotional intensity, mood, pacing, and level of suspense, offering writers and literary analysts a tool for understanding and improving their work.

## Features

- **Multi-Model Support**: Utilizes various language models including GPT, Claude, and Gemini for feature extraction.
- **Customizable Features**: Supports both predefined and custom literary features.
- **Flexible Analysis**: Capable of analyzing text at both paragraph and section levels.
- **Data Visualization**: Generates graphs to visualize extracted features across the text.
- **Text Statistics**: Provides additional metrics like readability scores, word count, and dialogue percentage.

## Installation

1. Ensure you have Python 3.10 or higher installed.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/writing-feature-extractor.git
   cd writing-feature-extractor
   ```
3. Install the required dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

1. Copy the `.env.example` file to `.env` and fill in your API keys for the language models you intend to use.
2. Customize the `feature_config.yaml` file to define the features you want to extract.

## Usage

### Basic Usage

To analyze a text file:

```
python main.py path/to/your/text_file.txt
```

### Advanced Options

- Analyze by section instead of paragraph:
  ```
  python main.py path/to/your/text_file.txt --mode section
  ```

- Save results to a custom CSV file:
  ```
  python main.py path/to/your/text_file.txt --save --csv-file custom_results.csv
  ```

- Generate a graph from saved results:
  ```
  python main.py --graph --csv-file results.csv --bar-feature Pacing --color-feature Mood
  ```

## Adding Custom Features

1. Define your new feature in `feature_config.yaml`.
2. If needed, create a new feature class in `writing_features.py`.
3. Update `WritingFeatureFactory` in `writing_feature_factory.py` to include your new feature.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- This project uses various open-source libraries and language models. See `pyproject.toml` for a full list of dependencies.
- Special thanks to the developers of LangChain, which powers much of the language model interaction in this project.