import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract writing features and generate graphs."
    )
    parser.add_argument("file", nargs="?", help="Input text file to analyze")
    parser.add_argument(
        "--mode",
        choices=["paragraph", "section"],
        default="paragraph",
        help="Analysis mode: paragraph-by-paragraph or section-by-section",
    )
    parser.add_argument("--save", action="store_true", help="Save results to CSV")
    parser.add_argument(
        "--graph", action="store_true", help="Generate graph from saved CSV"
    )
    parser.add_argument(
        "--bar-feature", help="Feature to use for bar heights when generating graph"
    )
    parser.add_argument(
        "--color-feature", help="Feature to use for bar colors when generating graph"
    )
    parser.add_argument(
        "--csv-file",
        default="feature_results.csv",
        help="CSV file to save results to or read from",
    )
    parser.add_argument(
        "--config",
        default="feature_config.yaml",
        help="YAML configuration file for features",
    )
    parser.add_argument(
        "--provider", default="anthropic", help="The LLM provider to use"
    )
    parser.add_argument(
        "--model", default="claude-3-haiku-20240307", help="The specific model to use"
    )
    return parser.parse_args()
