"""
RMaxTS - Monte-Carlo Tree Search for Proof Exploration
Based on: DeepSeek-Prover-V2 architecture (2025)

This module implements tree search with truncate-and-resume for navigating
the proof space, using Lean compiler feedback for guidance.
"""

import random
import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class TacticState:
    goals: List[str]
    context: Dict[str, str]
    parent: Optional['TreeNode'] = None

@dataclass
class TreeNode:
    state: TacticState
    action: str  # Tactic that led here
    children: List['TreeNode'] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0
    novelty_bonus: float = 0.0

class LeanFeedback:
    """Simulates Lean 4 compiler feedback for tactics."""
    
    def __init__(self):
        self.valid_tactics = [
            "intro", "apply", "exact", "rfl", "simp", "ring",
            "linarith", "omega", "aesop", "trivial", "assumption"
        ]
    
    def execute_tactic(self, state: TacticState, tactic: str) -> tuple:
        """
        Execute a tactic and return (success, new_state, error_msg).
        In production, this would call Lean 4 REPL.
        """
        print(f"  [LEAN] Trying tactic: {tactic}")
        
        # Simulated feedback
        if tactic in self.valid_tactics:
            new_goals = state.goals[1:] if len(state.goals) > 0 else []
            new_state = TacticState(goals=new_goals, context=state.context)
            return (True, new_state, None)
        else:
            return (False, None, f"Unknown tactic: {tactic}")

class RMaxTSAgent:
    """
    Monte-Carlo Tree Search with Truncate-and-Resume.
    Uses intrinsic rewards for novel tactic state discovery.
    """
    
    def __init__(self, exploration_constant: float = 1.414):
        self.exploration_c = exploration_constant
        self.lean_feedback = LeanFeedback()
        self.visited_states: set = set()
        self.root: Optional[TreeNode] = None
    
    def ucb_score(self, node: TreeNode, parent_visits: int) -> float:
        """Upper Confidence Bound for tree selection."""
        if node.visits == 0:
            return float('inf')
        
        exploitation = node.value / node.visits
        exploration = self.exploration_c * math.sqrt(math.log(parent_visits) / node.visits)
        novelty = node.novelty_bonus
        
        return exploitation + exploration + novelty
    
    def select(self, node: TreeNode) -> TreeNode:
        """Select best child node using UCB."""
        if not node.children:
            return node
        
        best_child = max(node.children, key=lambda c: self.ucb_score(c, node.visits))
        return self.select(best_child)
    
    def expand(self, node: TreeNode) -> Optional[TreeNode]:
        """Expand node by trying a new tactic."""
        tactics_to_try = ["simp", "ring", "linarith", "aesop", "trivial"]
        
        for tactic in tactics_to_try:
            success, new_state, error = self.lean_feedback.execute_tactic(node.state, tactic)
            
            if success:
                # Calculate novelty bonus
                state_hash = str(new_state.goals)
                novelty = 0.5 if state_hash not in self.visited_states else 0.0
                self.visited_states.add(state_hash)
                
                child = TreeNode(
                    state=new_state,
                    action=tactic,
                    novelty_bonus=novelty
                )
                node.children.append(child)
                return child
        
        return None
    
    def backpropagate(self, node: TreeNode, reward: float):
        """Backpropagate reward up the tree."""
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.state.parent
    
    def truncate_and_resume(self, node: TreeNode, error_msg: str) -> TacticState:
        """
        Truncate proof at first error and resume from that state.
        Uses Lean's error position to determine truncation point.
        """
        print(f"[RMaxTS] Truncating at error: {error_msg}")
        return node.state
    
    def search(self, initial_goal: str, iterations: int = 100) -> List[str]:
        """
        Run MCTS search to find a proof.
        Returns list of tactics if proof found.
        """
        print(f"\n{'='*50}")
        print(f"[RMaxTS] Searching proof for: {initial_goal}")
        print('='*50)
        
        initial_state = TacticState(goals=[initial_goal], context={})
        self.root = TreeNode(state=initial_state, action="init")
        
        for i in range(iterations):
            # Selection
            selected = self.select(self.root)
            
            # Expansion
            expanded = self.expand(selected)
            
            if expanded is None:
                continue
            
            # Check if proof complete
            if len(expanded.state.goals) == 0:
                print(f"[RMaxTS] PROOF FOUND after {i+1} iterations!")
                return self._extract_proof(expanded)
            
            # Backpropagation
            reward = 0.1 + expanded.novelty_bonus
            self.backpropagate(expanded, reward)
        
        print(f"[RMaxTS] Search exhausted after {iterations} iterations.")
        return []
    
    def _extract_proof(self, node: TreeNode) -> List[str]:
        """Extract the sequence of tactics from root to proof node."""
        tactics = []
        current = node
        while current.action != "init":
            tactics.append(current.action)
            if current.state.parent:
                for child in current.state.parent.children:
                    if child is current:
                        current = TreeNode(state=current.state.parent, action="")
                        break
            else:
                break
        return list(reversed(tactics))
    
    def report_stats(self):
        """Report search statistics."""
        print(f"\n--- RMaxTS Statistics ---")
        print(f"Visited states: {len(self.visited_states)}")
        if self.root:
            print(f"Root visits: {self.root.visits}")

if __name__ == "__main__":
    agent = RMaxTSAgent()
    
    # Test proof search
    proof = agent.search("forall n : Nat, n + 0 = n", iterations=20)
    print(f"Proof tactics: {proof}")
    
    agent.report_stats()
