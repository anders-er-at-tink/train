from dataclasses import dataclass, InitVar
from typing import FrozenSet, Optional, Set, Tuple, Union


def unique(iterable, seen=None):
    seen = seen if seen is not None else set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


@dataclass(frozen=True)
class Commit:
    message: str = "root"
    parents: Tuple['Commit', ...] = ()
    _a: FrozenSet['Commit'] = frozenset()
    _n: int = 0

    @property
    def h(self):
        return (2 ** 64 + hash(self)) & ~0

    def __post_init__(self):
        a = frozenset(self)
        object.__setattr__(self, '_a', a)
        object.__setattr__(self, '_n', len(a))

    def __repr__(self):
        return f"Commit({self.message!r}, {self.parents!r})"

    def __str__(self):
        return f"{self.h & 0xffff:04x} {self.message}"

    def __lt__(self, other: 'Commit'):
        return self in other._a

    def __iter__(self):
        seen = {self}
        yield self
        for p in self.parents:
            yield from unique(p, seen)

    def __len__(self):
        return self._n

    def all(self):
        return self._a

    def __contains__(self, it: Union['Commit', str]):
        if isinstance(it, Commit):
            return it in self._a
        elif isinstance(it, str):
            return any(x.message == it for x in self._a)

    def __sub__(self, other):
        all = other.all()
        for commit in self:
            if commit in all:
                break
            yield commit

    def __getitem__(self, index):
        if type(index) is int:
            if index == 0:
                return self
            elif self.parents:
                return self.parents[0][index - 1]
            else:
                raise IndexError("wat")

    def commit(self, message="blah", *merges):
        return Commit(message=message, parents=(self,) + tuple(merges))

    def log(self):
        it = self
        while it:
            print(it)
            it = (it.parents or (None,))[0]

    def apply(self, other):
        return other(self.message)

    def rebase(self, trunk: 'Commit') -> Optional['Commit']:
        if self in trunk or not self.parents:
            return trunk
        else:
            return rebase(trunk, self.parents[0]).commit(self.message)


def rebase(trunk: Commit, branch: Commit) -> Optional[Commit]:
    if branch in trunk or not branch.parents:
        return trunk
    else:
        return rebase(trunk, branch.parents[0]).commit(branch.message)
