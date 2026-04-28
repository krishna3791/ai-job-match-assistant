from app.evaluation import run_evaluations


def test_evaluation_cases_pass() -> None:
    results = run_evaluations()

    assert results
    assert all(result.passed for result in results)
