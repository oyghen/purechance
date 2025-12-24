import random
from contextlib import nullcontext
from typing import TypeAlias

import pytest

import purechance

ContextManager: TypeAlias = nullcontext[None] | pytest.RaisesExc[ValueError]


class TestCoinflip:
    @pytest.mark.parametrize(
        "bias, ctx",
        [
            (0.25, nullcontext()),
            (0.5, nullcontext()),
            (0.75, nullcontext()),
            (-0.1, pytest.raises(ValueError)),
            (1.1, pytest.raises(ValueError)),
            (11, pytest.raises(ValueError)),
        ],
    )
    def test_coinflip(self, bias: float, ctx: ContextManager, rng: random.Random):
        with ctx:
            num_trials = 30
            result = [purechance.coinflip(bias, seed=rng) for _ in range(num_trials)]
            assert len(result) == num_trials
            assert set(result) == {False, True}

    def test_coinflip_always_false(self, rng: random.Random):
        num_trials = 30
        result = [purechance.coinflip(0.0, seed=rng) for _ in range(num_trials)]
        assert len(result) == num_trials
        assert set(result) == {False}

    def test_coinflip_always_true(self, rng: random.Random):
        num_trials = 30
        result = [purechance.coinflip(1.0, seed=rng) for _ in range(num_trials)]
        assert len(result) == num_trials
        assert set(result) == {True}

    def test_coinflip_biased(self, rng: random.Random):
        bias = 0.55
        num_trials = 30

        result = [purechance.coinflip(bias, seed=rng) for _ in range(num_trials)]
        assert len(result) == num_trials
        assert set(result) == {False, True}

        k = 3  # standard deviations
        observed_bias = sum(result) / num_trials
        expected_stddev = (bias * (1 - bias) / num_trials) ** 0.5
        assert observed_bias == pytest.approx(bias, abs=k * expected_stddev)

    @pytest.fixture(scope="class")
    def rng(self) -> random.Random:
        return purechance.get_rng(101)


class TestRandomDraw:
    @pytest.mark.parametrize(
        "replace, size, expected",
        [
            (True, 5, ["b", "a", "c", "c", "b"]),
            (False, 2, ["c", "a"]),
            (False, 3, ["c", "a", "b"]),
        ],
    )
    def test_basic_behavior(self, replace: bool, size: int, expected: list[str]):
        items = ["a", "b", "c"]
        result = purechance.draw(items, replace, size, seed=101)
        assert result == expected

    @pytest.mark.parametrize("replace, size", [(False, 1), (True, 1)])
    def test_empty_items_returns_empty_list(self, replace: bool, size: int):
        result = purechance.draw([], replace, size)
        assert result == []

    @pytest.mark.parametrize("replace, size", [(False, 0), (True, 0)])
    def test_size_zero_returns_empty_list(self, replace: bool, size: int):
        items = [1, 2, 3]
        result = purechance.draw(items, replace, size)
        assert result == []

    @pytest.mark.parametrize("replace, size", [(False, -1), (True, -1)])
    def test_negative_size_raises_value_error(self, replace: bool, size: int):
        items = [1, 2, 3]
        with pytest.raises(ValueError):
            purechance.draw(items, replace, size)

    def test_no_replacement_size_greater_than_num_items_raises(self):
        items = ["a", "b"]
        with pytest.raises(ValueError):
            purechance.draw(items, replace=False, size=3)

    def test_draw_beyond_number_of_items(self):
        items = ["x", "y", "z"]
        result = purechance.draw(items, replace=True, size=5, seed=101)
        assert result == ["y", "x", "z", "z", "y"]


@pytest.mark.parametrize(
    "seed, ctx",
    [
        (None, nullcontext()),
        (0, nullcontext()),
        (random.Random(1), nullcontext()),
        ("invalid seed", pytest.raises(ValueError)),
        (3.0, pytest.raises(ValueError)),
    ],
    ids=["none", "int_zero", "Random_inst", "bad_string", "bad_float"],
)
def test_get_rng(seed: purechance.Seed, ctx: ContextManager):
    with ctx:
        rng = purechance.get_rng(seed)
        assert isinstance(rng, random.Random)


@pytest.mark.parametrize(
    "size, lower, upper, ctx",
    [
        (30, 0, 2, nullcontext()),
        (30, 0, 10, nullcontext()),
        (99, 1, 100, nullcontext()),
        (30, -2, 2, nullcontext()),
        (30, -10, -2, nullcontext()),
        (1, 5, 5, pytest.raises(ValueError, match=r"empty range for randrange")),
        (1, 100, 10, pytest.raises(ValueError, match=r"empty range for randrange")),
    ],
    ids=[
        "0-1 values only",
        "small_range",
        "large_range",
        "one_negative",
        "two_negative",
        "lower == upper -> zero randrange",
        "lower > upper -> negative randrange",
    ],
)
def test_integers(
    size: int,
    lower: int,
    upper: int,
    ctx: ContextManager,
    request: pytest.FixtureRequest,
):
    with ctx:
        random_integers = tuple(purechance.integers(size, lower, upper))
        test_id = request.node.callspec.id
        if test_id == "0-1 values only":
            assert set(random_integers) == {0, 1}
        assert len(random_integers) == size
        assert min(random_integers) >= lower
        assert min(random_integers) < upper


class TestRandomShuffle:
    def test_basic_behavior(self):
        items = [10, 20, 30]
        result = purechance.shuffle(items, seed=101)
        assert result == [30, 10, 20]
        assert result is not items
        # ensure original list is not modified
        assert items == [10, 20, 30]

    def test_shuffle_empty_list(self):
        items = []
        result = purechance.shuffle(items, seed=101)
        assert result == []
        assert result is not items

    def test_shuffle_single_element(self):
        items = [42]
        result = purechance.shuffle(items, seed=101)
        assert result == [42]
        assert result is not items
        # ensure original list is not modified
        assert items == [42]

    def test_new_list_is_returned(self):
        items = [10, 20, 30]
        result = purechance.shuffle(items, seed=101)
        expected = [30, 10, 20]
        assert result == expected
        assert result is not items

        items.pop(-1)
        assert items == [10, 20]
        assert len(result) == 3
        assert result == expected
