import random
from typing import List, Dict, Tuple

class WorksheetGenerator:
    """Generates math problems for worksheets."""
    
    def __init__(self):
        self.problems = []
    
    def generate_problems(self, operation: str, count: int, settings: Dict) -> List[Dict]:
        """Generate a list of math problems based on operation and settings."""
        problems = []
        
        for _ in range(count):
            if operation == "addition":
                problem = self._generate_addition(settings)
            elif operation == "subtraction":
                problem = self._generate_subtraction(settings)
            elif operation == "multiplication":
                problem = self._generate_multiplication(settings)
            elif operation == "division":
                problem = self._generate_division(settings)
            else:
                raise ValueError(f"Unsupported operation: {operation}")
            
            problems.append(problem)
        
        return problems
    
    def _generate_addition(self, settings: Dict) -> Dict:
        """Return a single addition problem (and its answer)."""
        max_num = settings.get("max_num", 100)

        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        answer = num1 + num2

        # Make sure the number with MORE digits is on top
        if len(str(num2)) > len(str(num1)):
            num1, num2 = num2, num1

        # Build a nicely‑aligned vertical layout that grows with width
        width = max(len(str(num1)), len(str(num2))) + 1      # +1 for the operator row
        formatted = (
            f"{str(num1).rjust(width)}\n"
            f"+{str(num2).rjust(width - 1)}\n"
            f"{'_' * width}"
        )

        return {
            "num1": num1,
            "num2": num2,
            "operation": "+",
            "answer": answer,
            "problem": f"{num1} + {num2}",
            "formatted_problem": formatted,
        }

    def _generate_subtraction(self, settings: Dict) -> Dict:
        """Generate subtraction problem (always positive result)."""
        max_num = settings.get("max_num", 100)
        
        # Ensure positive result by making num1 >= num2
        num2 = random.randint(1, max_num)
        num1 = random.randint(num2, max_num)
        answer = num1 - num2
        
        return {
            "num1": num1,
            "num2": num2,
            "operation": "-",
            "answer": answer,
            "problem": f"{num1} - {num2}",
            "formatted_problem": f"{num1:>4}\n-{num2:>3}\n____"
        }
    
    def _generate_multiplication(self, settings: Dict) -> Dict:
        """Generate multiplication problem."""
        digits_1 = settings.get("digits_1", 1)
        digits_2 = settings.get("digits_2", 1)
        
        # Generate numbers based on digit count
        min_1 = 10**(digits_1 - 1) if digits_1 > 1 else 1
        max_1 = 10**digits_1 - 1
        min_2 = 10**(digits_2 - 1) if digits_2 > 1 else 1
        max_2 = 10**digits_2 - 1
        
        num1 = random.randint(min_1, max_1)
        num2 = random.randint(min_2, max_2)
        answer = num1 * num2
        
        return {
            "num1": num1,
            "num2": num2,
            "operation": "×",
            "answer": answer,
            "problem": f"{num1} × {num2}",
            "formatted_problem": f"{num1:>4}\n×{num2:>3}\n____"
        }
    
    def _generate_division(self, settings: Dict) -> Dict:
        """Generate division problem."""
        max_dividend = settings.get("max_dividend", 100)
        max_divisor = settings.get("max_divisor", 10)
        remainder_type = settings.get("remainder_type", "No remainders")
        
        divisor = random.randint(2, max_divisor)
        
        if remainder_type == "No remainders":
            # Generate problems with no remainder
            quotient = random.randint(1, max_dividend // divisor)
            dividend = quotient * divisor
            remainder = 0
        
        elif remainder_type == "With remainders":
            # Generate problems with remainder
            quotient = random.randint(1, max_dividend // divisor)
            remainder = random.randint(1, divisor - 1)
            dividend = quotient * divisor + remainder
        
        else:  # Mixed
            # Randomly choose with or without remainder
            if random.choice([True, False]):
                quotient = random.randint(1, max_dividend // divisor)
                dividend = quotient * divisor
                remainder = 0
            else:
                quotient = random.randint(1, max_dividend // divisor)
                remainder = random.randint(1, divisor - 1)
                dividend = quotient * divisor + remainder
        
        # Format answer based on remainder
        if remainder == 0:
            answer_text = str(quotient)
        else:
            answer_text = f"{quotient} R{remainder}"

        
        return {
            "num1": dividend,
            "num2": divisor,
            "operation": "÷",
            "answer": quotient,
            "remainder": remainder,
            "answer_text": answer_text,
            "problem": f"{dividend} ÷ {divisor}",
            "formatted_problem": f"{divisor}){dividend}"
        }
    
    def shuffle_problems(self, problems: List[Dict]) -> List[Dict]:
        """Shuffle the order of problems."""
        shuffled = problems.copy()
        random.shuffle(shuffled)
        return shuffled
    
    def validate_settings(self, operation: str, settings: Dict) -> bool:
        """Validate that settings are appropriate for the operation."""
        try:
            if operation == "addition":
                max_num = settings.get("max_num", 100)
                return 1 <= max_num <= 999
            
            elif operation == "subtraction":
                max_num = settings.get("max_num", 100)
                return 1 <= max_num <= 999
            
            elif operation == "multiplication":
                digits_1 = settings.get("digits_1", 1)
                digits_2 = settings.get("digits_2", 1)
                return 1 <= digits_1 <= 4 and 1 <= digits_2 <= 4
            
            elif operation == "division":
                max_dividend = settings.get("max_dividend", 100)
                max_divisor = settings.get("max_divisor", 10)
                remainder_type = settings.get("remainder_type", "No remainders")
                
                return (10 <= max_dividend <= 999 and 
                       2 <= max_divisor <= 20 and
                       remainder_type in ["No remainders", "With remainders", "Mixed"])
            
            return False
            
        except (TypeError, ValueError):
            return False
    
    def get_difficulty_description(self, operation: str, settings: Dict) -> str:
        """Get a human-readable description of the difficulty settings."""
        if operation == "addition":
            return f"Numbers up to {settings.get('max_num', 100)}"
        
        elif operation == "subtraction":
            return f"Numbers up to {settings.get('max_num', 100)} (positive results only)"
        
        elif operation == "multiplication":
            d1, d2 = settings.get('digits_1', 1), settings.get('digits_2', 1)
            return f"{d1}-digit × {d2}-digit numbers"
        
        elif operation == "division":
            dividend = settings.get('max_dividend', 100)
            divisor = settings.get('max_divisor', 10)
            remainder = settings.get('remainder_type', 'No remainders')
            return f"Up to {dividend} ÷ {divisor}, {remainder.lower()}"
        
        return "Custom settings"
