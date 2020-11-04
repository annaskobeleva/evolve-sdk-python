#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.traversals.queue import Queue
from zepben.cimbend.traversals.tracing import BaseTraversal
from zepben.cimbend.traversals.tracker import Tracker
from typing import Callable, Set, TypeVar, Optional
import copy

__all__ = ["BranchRecursiveTraversal"]
T = TypeVar('T')


class BranchRecursiveTraversal(BaseTraversal[T]):

    queue_next: Callable[[T, BaseTraversal[T], Set[T]], None]
    """A callable for each item encountered during the trace, that should queue the next items found on the given traversal's `process_queue`. 
    The first argument will be the current item, the second this traversal, and the third a set of already visited items that can be used as an optional 
    optimisation to skip queuing."""

    branch_queue: Queue
    """Queue containing branches to be processed"""

    process_queue: Queue
    """Queue containing the items to process for this branch"""

    tracker: Tracker = Tracker()
    """Tracker for the items in this branch"""

    parent: Optional[BaseTraversal] = None
    """The parent branch for this branch, None implies this branch has no parent"""

    on_branch_start: Optional[Callable[[T], None]] = None
    """A function to call at the start of each branches processing"""

    def __lt__(self, other):
        """
        This Traversal is Less than `other` if the starting item is less than other's starting item.
        This is used to dictate which branch is next to traverse in the branch_queue.
        """
        if self.start_item is not None and other.start_item is not None:
            return self.start_item < other.start_item
        elif self.start_item is None and other.start_item is None:
            return False
        elif other.start_item is None:
            return True
        else:
            return False

    def has_visited(self, item: T):
        """
        Check whether item has been visited before. An item is visited if this traversal or any parent has visited it.

        `item` The item to check
        Returns True if the item has been visited once.
        """
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(item):
                return True
            parent = parent.parent

        return self.tracker.has_visited(item)

    def visit(self, item: T):
        """
        Visit an item.
        `item` Item to visit
        Returns True if we visit the item. False if this traversal or any parent has previously visited this item.
        """
        parent = self.parent
        while parent is not None:
            if parent.tracker.has_visited(item):
                return False
            parent = parent.parent
        return self.tracker.visit(item)

    async def traverse_branches(self):
        """
        Start a new traversal for the next branch in the queue.
        on_branch_start will be called on the start_item for the branch.
        """
        while not self.branch_queue.empty():
            t = self.branch_queue.get()
            if t is not None:
                if self.on_branch_start is not None:
                    self.on_branch_start(t.start_item)
                await t.trace()

    def reset(self):
        """Reset the run state, queues and tracker for this this traversal"""
        self._reset_run_flag()
        self.process_queue.queue.clear()
        self.branch_queue.queue.clear()
        self.tracker.clear()

    def create_branch(self):
        """
        Create a branch for this `Traversal`. Will take copies of queues, actions, conditions, and tracker, and
        pass this `Traversal` as the parent. The new Traversal will be :meth:`reset` prior to being returned.
        Returns A new `BranchRecursiveTraversal` the same as this, but with this Traversal as its parent
        """
        branch = BranchRecursiveTraversal(queue_next=self.queue_next,
                                          branch_queue=copy.copy(self.branch_queue),
                                          tracker=copy.copy(self.tracker),
                                          parent=self,
                                          on_branch_start=self.on_branch_start,
                                          process_queue=copy.copy(self.process_queue),
                                          step_actions=list(self.step_actions),
                                          stop_conditions=list(self.stop_conditions))
        branch.reset()
        return branch

    async def _run_trace(self, can_stop_on_start_item: bool = True):
        """
        Run's the trace. Stop conditions and step_actions are called with await, so you can utilise asyncio when performing a trace if your step actions or
        conditions are IO intensive. Stop conditions and step actions will always be called for each item in the order provided.
        `can_stop_on_start_item` Whether the trace can stop on the start_item. Actions will still be applied to the start_item.
        """
        # Unroll first iteration of loop to handle can_stop_on_start_item = True
        if self.start_item is None:
            try:
                self.start_item = self.process_queue.get()
            except IndexError:
                # Our start point may very well be a branch - if so we don't need to process this branch.
                await self.traverse_branches()
                return

        self.tracker.visit(self.start_item)
        # If we can't stop on the start item we don't run any stop conditions. if this causes a problem for you,
        # work around it by running the stop conditions for the start item prior to running the trace.
        stopping = can_stop_on_start_item and await self.matches_stop_condition(self.start_item)
        await self.apply_step_actions(self.start_item, stopping)
        if not stopping:
            self.queue_next(self.start_item, self, self.tracker.visited)

        while not self.process_queue.empty():
            current = self.process_queue.get()
            if self.visit(current):
                stopping = await self.matches_stop_condition(current)
                await self.apply_step_actions(current, stopping)
                if not stopping:
                    self.queue_next(current, self, self.tracker.visited)

        await self.traverse_branches()