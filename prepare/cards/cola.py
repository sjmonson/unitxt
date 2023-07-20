from src.unitxt.blocks import (
    LoadHF,
    TemplatesList,
    InputOutputTemplate
)
from src.unitxt.catalog import add_to_catalog
from src.unitxt.test_utils.card import test_card
from src.unitxt.prepare_utils.card_types import create_2sentences_classification_card

card = create_2sentences_classification_card(
    loader=LoadHF(path='glue', name='cola'),
    preprocess_steps=
    ['splitters.small_no_test', ],
    label_name="label",
    label2string={"0": 'acceptable', "1": 'not acceptable'},
    inputs=['sentence1', 'sentence2'],
    metrics=['metrics.accuracy'],
    templates=TemplatesList([
        InputOutputTemplate(
            input_format="""
                    Given this sentence: {sentence1}, classify if this sentence: {sentence2} is {choices}.
                """.strip(),
            output_format='{label}',
        ),
    ])
)

test_card(card)
add_to_catalog(card, 'cards.cola', overwrite=True)
