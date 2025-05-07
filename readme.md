# Full setup from scratch

## 0. Enable modules (on cluster)
module load mpi4py python/3.13.2

## 1. Clone this project from github
git clone git@github.com:Thaerious/euchre_bots.git
cd euchre_bots

## 2. Create virtual environment
python3 -m venv venv

## 3. Activate it
source venv/bin/activate   # On Windows: venv\Scripts\activate

## 4. Upgrade pip (recommended)
pip install --upgrade pip

## 5. Install all dependencies (includes your GitHub project)
pip install -r requirements.txt