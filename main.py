from dotenv import load_dotenv

from writing_feature_extractor.cli import parse_arguments
from writing_feature_extractor.core.available_models import AvailableModels
from writing_feature_extractor.core.feature_config import load_feature_config
from writing_feature_extractor.core.feature_extraction import extract_features
from writing_feature_extractor.core.model_factory import ModelFactory
from writing_feature_extractor.features.writing_feature_factory import (
    WritingFeatureFactory,
)
from writing_feature_extractor.utils.generate_graph_from_csv import (
    generate_graph_from_csv,
)
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.utils.text_processing import (
    load_text,
    split_into_sections,
)

logger = get_logger(__name__)


def main():
    args = parse_arguments()

    if args.graph:
        return handle_graph_generation(args)
    elif args.file:
        handle_feature_extraction(args)
    else:
        logger.error(
            "Please provide an input file or use --graph with a saved CSV file"
        )


def handle_feature_extraction(args):
    text = load_text(args.file)
    features = load_feature_config(args.config)

    feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
        features
    )

    llm = ModelFactory.get_llm_model(AvailableModels.GPT_3_5, DynamicFeatureModel)
    logger.debug(f"Obtained LLM model: {llm}")

    sections = split_into_sections(text)
    result = extract_features(sections, args.mode, feature_collectors, llm)

    if result:
        feature_collectors, text_units = result
        if args.save:
            save_results_to_csv(feature_collectors, text_units, args.csv_file)


def handle_graph_generation(args):
    if not (args.bar_feature and args.color_feature):
        logger.error(
            "Please specify --bar-feature and --color-feature when using --graph"
        )
        return
    generate_graph_from_csv(args.csv_file, args.bar_feature, args.color_feature)


if __name__ == "__main__":
    load_dotenv()
    main()
