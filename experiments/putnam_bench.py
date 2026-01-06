"""
PutnamBench - University-Level Problem Benchmark
Based on: MiniF2F, PutnamBench datasets (2025)

This module provides a benchmark suite for testing the neuro-symbolic
reasoning agents on university-level mathematical problems.
"""

from dataclasses import dataclass
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class BenchmarkProblem:
    id: str
    name: str
    statement: str
    difficulty: str  # easy, medium, hard, olympiad
    domain: str
    expected_solution: Optional[str] = None

class PutnamBench:
    """
    Benchmark suite for university-level mathematical reasoning.
    """
    
    def __init__(self):
        self.problems: List[BenchmarkProblem] = []
        self._load_problems()
    
    def _load_problems(self):
        """Load benchmark problems."""
        self.problems = [
            BenchmarkProblem(
                id="putnam_2020_a1",
                name="Putnam 2020 A1",
                statement="How many positive integers N satisfy all of the following: N is divisible by 2020, N has at most 2020 decimal digits, and the decimal digits of N are a string of consecutive ones followed by a string of consecutive zeros?",
                difficulty="medium",
                domain="number_theory"
            ),
            BenchmarkProblem(
                id="minif2f_algebra_1",
                name="MiniF2F Algebra 1",
                statement="Prove: For all real numbers a, b: (a + b)^2 = a^2 + 2*a*b + b^2",
                difficulty="easy",
                domain="algebra"
            ),
            BenchmarkProblem(
                id="imo_2019_p1",
                name="IMO 2019 Problem 1",
                statement="Let Z be the set of integers. Determine all functions f: Z -> Z such that for all integers a and b: f(2a) + 2f(b) = f(f(a+b))",
                difficulty="olympiad",
                domain="functional_equations"
            ),
            BenchmarkProblem(
                id="induction_sum",
                name="Sum of First N",
                statement="Prove: For all natural numbers n, 1 + 2 + ... + n = n*(n+1)/2",
                difficulty="easy",
                domain="induction"
            ),
            BenchmarkProblem(
                id="analysis_limit",
                name="Basic Limit",
                statement="Prove: lim(x -> 0) sin(x)/x = 1",
                difficulty="medium",
                domain="analysis"
            ),
        ]
    
    def get_problems_by_difficulty(self, difficulty: str) -> List[BenchmarkProblem]:
        """Filter problems by difficulty."""
        return [p for p in self.problems if p.difficulty == difficulty]
    
    def get_problems_by_domain(self, domain: str) -> List[BenchmarkProblem]:
        """Filter problems by domain."""
        return [p for p in self.problems if p.domain == domain]
    
    def run_benchmark(self, agent, max_problems: int = None):
        """
        Run the benchmark suite against a reasoning agent.
        """
        print("\n" + "="*60)
        print("PUTNAM BENCHMARK - Neuro-Symbolic Reasoning Evaluation")
        print("="*60)
        
        problems = self.problems[:max_problems] if max_problems else self.problems
        results = {"solved": 0, "failed": 0, "timeout": 0}
        
        for prob in problems:
            print(f"\n[BENCH] {prob.id}: {prob.name}")
            print(f"        Difficulty: {prob.difficulty} | Domain: {prob.domain}")
            print(f"        Statement: {prob.statement[:80]}...")
            
            try:
                # Attempt to solve using agent
                if hasattr(agent, 'search'):
                    proof = agent.search(prob.statement, iterations=50)
                    if proof:
                        print(f"        [SOLVED] Proof found!")
                        results["solved"] += 1
                    else:
                        print(f"        [FAILED] No proof found.")
                        results["failed"] += 1
                elif hasattr(agent, 'verify_step'):
                    result = agent.verify_step(prob.statement)
                    if result.status == "CORRECT":
                        results["solved"] += 1
                    else:
                        results["failed"] += 1
                else:
                    print(f"        [SKIP] Agent has no compatible method.")
                    results["failed"] += 1
            except Exception as e:
                print(f"        [ERROR] {str(e)}")
                results["timeout"] += 1
        
        # Report
        print("\n" + "="*60)
        print("BENCHMARK RESULTS")
        print("="*60)
        print(f"Solved:  {results['solved']}/{len(problems)}")
        print(f"Failed:  {results['failed']}/{len(problems)}")
        print(f"Timeout: {results['timeout']}/{len(problems)}")
        accuracy = results['solved'] / len(problems) * 100 if problems else 0
        print(f"Accuracy: {accuracy:.1f}%")
        print("="*60)
        
        return results

if __name__ == "__main__":
    bench = PutnamBench()
    
    print("Available problems:")
    for prob in bench.problems:
        print(f"  - {prob.id}: {prob.name} ({prob.difficulty})")
    
    # Test with RMaxTS agent
    try:
        from engines.search.rmax_ts import RMaxTSAgent
        agent = RMaxTSAgent()
        bench.run_benchmark(agent, max_problems=2)
    except ImportError:
        print("\n[INFO] Run from project root to test with agents.")
