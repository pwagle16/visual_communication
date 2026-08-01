from viscomm import CATEGORICAL, CHROME, contrast_ink


def test_categorical_palette_has_eight_distinct_hues():
    assert len(CATEGORICAL) == 8
    assert len(set(CATEGORICAL)) == 8


def test_contrast_ink_picks_dark_on_light_and_white_on_dark():
    assert contrast_ink("#f2e8d5") == CHROME["primary_ink"]  # dark ink on a light fill
    assert contrast_ink("#0b0b0b") == "#ffffff"              # white on a dark fill
