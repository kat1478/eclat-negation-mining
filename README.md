# Eclat Algorithm with Negated Literals

Implementation of the Eclat algorithm for frequent itemset mining with support for negated literals.

## Project Structure

```
projekt_med/
├── data/                 # Dataset directory
├── notebooks/           # Jupyter notebooks with analysis
├── src/                 # Source code
├── docs/               # Documentation
├── presentation/       # Final presentation
└── README.md          # Project description
```

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

Basic example of using the Eclat algorithm:

```python
from src.eclat import Eclat

# Initialize the algorithm
eclat = Eclat(min_support=0.01, use_negation=True)

# Fit the model
eclat.fit(transactions)

# Get frequent itemsets
frequent_itemsets = eclat.transform()
```