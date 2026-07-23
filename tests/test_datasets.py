import viscomm as vc
from viscomm import datasets


def test_loaders_are_deterministic():
    # Same call twice returns identical data (fixed seed).
    assert datasets.monthly_active_users() == datasets.monthly_active_users()
    assert datasets.spend_vs_signups() == datasets.spend_vs_signups()


def test_line_dataset_shapes_match_chart_api():
    d = datasets.monthly_active_users()
    assert len(d.x) == 12
    assert all(len(vals) == 12 for vals in d.series.values())
    # Plots without error through the real chart function.
    vc.line(d.x, series=d.series, title=d.title, ylabel=d.ylabel)


def test_bar_dataset_shapes_match_chart_api():
    d = datasets.quarterly_revenue_by_region()
    assert all(len(vals) == len(d.categories) for vals in d.series.values())
    vc.bar(d.categories, series=d.series, title=d.title)


def test_scatter_dataset_within_group_cap():
    d = datasets.spend_vs_signups()
    assert len(d.series) <= 3  # scatter's supported maximum
    for xs, ys in d.series.values():
        assert len(xs) == len(ys)
    vc.scatter(None, None, series=d.series, title=d.title)


def test_pie_dataset_shapes_match_chart_api():
    d = datasets.traffic_by_channel()
    assert len(d.labels) == len(d.values)
    vc.pie(d.labels, d.values, title=d.title)


def test_export_csv_writes_all_datasets(tmp_path):
    paths = datasets.export_csv(str(tmp_path))
    assert set(paths) == set(datasets.ALL_LOADERS)
    for path in paths.values():
        assert tmp_path.joinpath(path.split("/")[-1]).exists()
