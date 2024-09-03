from typing import List

from unitxt.blocks import (
    InputOutputTemplate,
    LoadHF,
    SerializeTableAsIndexedRowMajor,
    Task,
    TaskCard,
    TemplatesList,
)
from unitxt.catalog import add_to_catalog
from unitxt.test_utils.card import test_card

card = TaskCard(
    loader=LoadHF(
        path="ibm/turl_table_col_type",
        streaming=False,
        data_classification_policy=["public"],
    ),
    preprocess_steps=[
        SerializeTableAsIndexedRowMajor(field_to_field=[["table", "table_lin"]])
    ],
    task=Task(
        input_fields={
            "page_title": str,
            "section_title": str,
            "table_caption": str,
            "table_lin": str,
            "vocab": List[str],
            "colname": str,
        },
        reference_fields={"annotations": List[str]},
        prediction_type="List[str]",
        metrics=[
            "metrics.f1_micro_multi_label",
            "metrics.accuracy",
            "metrics.f1_macro_multi_label",
        ],
    ),
    templates=TemplatesList(
        [
            InputOutputTemplate(
                input_format="""
                    This is a column type annotation task. The goal of this task is to choose the correct types for one selected column of the given input table from the given candidate types. The Wikipedia page, section and table caption (if any) provide important information for choosing the correct column types. \nPage Title: {page_title} \nSection Title: {section_title} \nTable caption: {table_caption} \nTable: \n{table_lin} \nSelected Column: {colname} \nCandidate Types: {vocab} \nOutput only the correct column types for this column (column name: {colname}) from the candidate types.
                """.strip(),
                output_format="{annotations}",
                postprocessors=["processors.to_list_by_comma"],
            ),
        ]
    ),
    __description__=(
        "This TURL dataset is a large-scale dataset based on WikiTables corpus for the task of column type annotation. Given a table T and a set of semantic types L, the task is to annotate a column in T with l ∈ L so that all entities in the column have type l. Note that a column can have multiple types. See the full description on the dataset page: https://github.com/sunlab-osu/TURL"
    ),
    __tags__={
        "modality": "table",
        "urls": {"arxiv": "https://arxiv.org/pdf/2006.14806"},
        "languages": ["english"],
    },
)

test_card(card)
add_to_catalog(card, "cards.turl_col_type", overwrite=True)