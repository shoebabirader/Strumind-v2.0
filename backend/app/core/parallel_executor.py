"""
Parallel execution system for multi-core analysis
"""
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Callable, Any, Dict
import multiprocessing
import numpy as np
from datetime import datetime


class ParallelExecutor:
    """Manages parallel execution of analysis tasks"""
    
    def __init__(self, max_workers: int = None):
        if max_workers is None:
            max_workers = multiprocessing.cpu_count()
        
        self.max_workers = max_workers
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers)
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers * 2)
        self.active_tasks: Dict[str, dict] = {}
    
    async def execute_parallel(self, tasks: List[Callable], use_processes: bool = True) -> List[Any]:
        """
        Execute multiple tasks in parallel
        
        Args:
            tasks: List of callable functions
            use_processes: Use processes (CPU-bound) or threads (I/O-bound)
        
        Returns:
            List of results in same order as tasks
        """
        pool = self.process_pool if use_processes else self.thread_pool
        loop = asyncio.get_event_loop()
        
        # Execute all tasks in parallel
        futures = [loop.run_in_executor(pool, task) for task in tasks]
        results = await asyncio.gather(*futures)
        
        return results
    
    async def execute_batch_analysis(self, model_data: dict, load_cases: List[dict]) -> List[dict]:
        """
        Execute multiple load cases in parallel
        
        Args:
            model_data: Structural model data
            load_cases: List of load case definitions
        
        Returns:
            List of analysis results for each load case
        """
        from app.engine.analysis import analyze_structure
        
        # Create tasks for each load case
        tasks = []
        for i, load_case in enumerate(load_cases):
            task_id = f"analysis_{i}_{datetime.utcnow().timestamp()}"
            
            # Store task info
            self.active_tasks[task_id] = {
                "status": "pending",
                "load_case": load_case,
                "started_at": None,
                "completed_at": None
            }
            
            # Create analysis task
            def analyze_case(model=model_data, loads=load_case, tid=task_id):
                self.active_tasks[tid]["status"] = "running"
                self.active_tasks[tid]["started_at"] = datetime.utcnow()
                
                try:
                    result = analyze_structure(model, loads)
                    self.active_tasks[tid]["status"] = "completed"
                    self.active_tasks[tid]["completed_at"] = datetime.utcnow()
                    return result
                except Exception as e:
                    self.active_tasks[tid]["status"] = "failed"
                    self.active_tasks[tid]["error"] = str(e)
                    raise
            
            tasks.append(analyze_case)
        
        # Execute in parallel
        results = await self.execute_parallel(tasks, use_processes=True)
        
        return results
    
    async def execute_parametric_study(self, base_model: dict, 
                                      parameter_variations: List[dict]) -> List[dict]:
        """
        Execute parametric study with multiple parameter variations
        
        Args:
            base_model: Base structural model
            parameter_variations: List of parameter modifications
        
        Returns:
            List of results for each variation
        """
        tasks = []
        
        for variation in parameter_variations:
            def analyze_variation(model=base_model.copy(), params=variation):
                # Apply parameter variation
                modified_model = apply_parameters(model, params)
                
                # Run analysis
                from app.engine.analysis import analyze_structure
                return analyze_structure(modified_model, {})
            
            tasks.append(analyze_variation)
        
        results = await self.execute_parallel(tasks, use_processes=True)
        return results
    
    async def execute_optimization_iterations(self, model: dict, 
                                             objective_function: Callable,
                                             iterations: int = 10) -> dict:
        """
        Execute optimization iterations in parallel batches
        
        Args:
            model: Structural model
            objective_function: Function to optimize
            iterations: Number of iterations
        
        Returns:
            Optimization results
        """
        batch_size = self.max_workers
        best_result = None
        best_score = float('inf')
        
        for batch_start in range(0, iterations, batch_size):
            batch_end = min(batch_start + batch_size, iterations)
            batch_tasks = []
            
            for i in range(batch_start, batch_end):
                def optimize_iteration(iteration=i):
                    # Generate candidate solution
                    candidate = generate_candidate(model, iteration)
                    
                    # Evaluate
                    score = objective_function(candidate)
                    
                    return {"iteration": iteration, "candidate": candidate, "score": score}
                
                batch_tasks.append(optimize_iteration)
            
            # Execute batch
            batch_results = await self.execute_parallel(batch_tasks, use_processes=True)
            
            # Find best in batch
            for result in batch_results:
                if result["score"] < best_score:
                    best_score = result["score"]
                    best_result = result
        
        return best_result
    
    def get_task_status(self, task_id: str) -> dict:
        """Get status of a specific task"""
        return self.active_tasks.get(task_id, {"status": "not_found"})
    
    def get_all_tasks(self) -> dict:
        """Get status of all tasks"""
        return {
            "active_count": sum(1 for t in self.active_tasks.values() if t["status"] == "running"),
            "completed_count": sum(1 for t in self.active_tasks.values() if t["status"] == "completed"),
            "failed_count": sum(1 for t in self.active_tasks.values() if t["status"] == "failed"),
            "tasks": self.active_tasks
        }
    
    def shutdown(self):
        """Shutdown executor pools"""
        self.process_pool.shutdown(wait=True)
        self.thread_pool.shutdown(wait=True)


def apply_parameters(model: dict, parameters: dict) -> dict:
    """Apply parameter variations to model"""
    modified = model.copy()
    
    for key, value in parameters.items():
        if key in modified:
            modified[key] = value
    
    return modified


def generate_candidate(model: dict, iteration: int) -> dict:
    """Generate candidate solution for optimization"""
    # Simple example - in production, use proper optimization algorithms
    candidate = model.copy()
    
    # Add some random variation
    if "parameters" in candidate:
        for key in candidate["parameters"]:
            candidate["parameters"][key] *= (1 + np.random.uniform(-0.1, 0.1))
    
    return candidate


# Global executor instance
executor = ParallelExecutor()
