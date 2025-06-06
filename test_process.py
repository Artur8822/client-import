import pytest
from process import import_clients, is_valid_client

### no parameters for this test
# #test 1: check validation logic (individual validation scenarios)
# def test_is_valid_client():
#     assert is_valid_client("Anna","anna@example.com", "30")
#     assert not is_valid_client("", "anna@example", "30")
#     assert not is_valid_client("Anna", "", "30")
#     assert not is_valid_client("Anna", "anna@example", "-5")
#     assert not is_valid_client("Anna", "anna@example", "abc")
#     assert not is_valid_client("Anna", "anna@example", "")


# using parametrization for better test coverage and readability
# test 1: check validation logic (individual validation scenarios)
@pytest.mark.parametrize(
    "name, email, age, expected",  # individual validation scenarios
    [
        ("Anna", "anna@example.com", "30", True),  # case is valid
        ("", "no_name@example.com", 30, False),  # empty name
        ("Anna", "", 30, False),  # empty email
        ("Anna", "anna@example", "-1", False),  # negative age
        ("Anna", "anna@example", "abc", False),  # non-integer age
        ("Anna", "anna@example", "", False),  # empty age
    ],
)

# pytest.mark.parametrize
def test_is_valid_client(name, email, age, expected):
    assert is_valid_client(name, email, age) == expected


# test 2: simulate importing real CSV file
def test_import_clients(tmp_path):
    # create temporary CSV file
    test_csv = tmp_path / "test_clients.csv"

    test_csv.write_text(
        "name,email,age\n"
        "John Doe,john@example.com,35\n"
        "Jane Smith,jane@example.com,abc\n"
    )

    # Import clients from the temporary CSV file
    valid, invalid = import_clients(test_csv)

    assert len(valid) == 1  # We expect only one valid row
    assert valid[0]["name"] == "John Doe"
    assert valid[0]["age"] == 35

    assert len(invalid) == 1  # We expect one invalid row
