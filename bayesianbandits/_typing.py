from typing import Any, Callable, Dict, Optional, Protocol, Union, runtime_checkable

import numpy as np
from numpy.typing import ArrayLike, NDArray


class Learner(Protocol):
    """Learner protocol for the model underlying each arm.

    Each Learner must implement the following methods:
    - `sample`
    - `partial_fit`

    """

    random_state: Union[np.random.Generator, int, None]

    def sample(
        self,
        X: NDArray[Any],
        size: int = 1,
    ) -> NDArray[np.float_]:
        ...

    def partial_fit(self, X: NDArray[Any], y: NDArray[Any]) -> "Learner":
        ...

    def set_params(self, **params: Any) -> "Learner":
        ...


@runtime_checkable
class ArmProtocol(Protocol):
    """Protocol for Arms and Bandits. Bandits themselves can be used as arms
    in other bandits, so both must implement the same minimal interface.

    Each Arm or Bandit must implement the following methods:
    - `pull`
    - `sample`
    - `update`

    """

    learner: Optional[Learner]

    def pull(self) -> None:
        ...

    def sample(self, X: Optional[ArrayLike] = None, size: int = 1) -> ArrayLike:
        ...

    def update(self, X: Optional[ArrayLike], y: Optional[ArrayLike] = None) -> None:
        ...

    def mean(self, X: Optional[ArrayLike] = None) -> float:
        ...


class ChoiceAlgorithm(Protocol):
    """Choice algorithm protocol for choosing which arm to pull.

    Each ChoiceAlgorithm must implement the following methods:
    - `__get__`
    - `choose`

    """

    def __get__(
        self, instance: Optional["BanditProtocol"], owner: type
    ) -> "ChoiceAlgorithm":
        ...

    def choose(self, X: Optional[ArrayLike]) -> ArmProtocol:
        ...


@runtime_checkable
class BanditProtocol(ArmProtocol, Protocol):
    """Protocol for Bandits.

    Each Bandit must implement the following methods:
    - `choose_and_pull`
    - `update`
    - `pull`
    - `sample`

    """

    arms: Dict[str, ArmProtocol]
    choice_algorithm: Callable[..., ArmProtocol]
    last_arm_pulled: Optional[ArmProtocol]
    rng: Union[np.random.Generator, int, None]

    def choose_and_pull(self) -> None:
        ...