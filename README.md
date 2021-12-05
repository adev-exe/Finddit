# Finddit

## Setup
**Before running python server:**

Create a file called secret.yaml in the root directory of the repository with the following contents:
```yaml
api_key : 'API key goes here'
```

Install dependencies:
```shell
pip install -r requirements.txt
```

Run the database init scrip:
```shell
set FLASK_APP=website
```
and then
```shell
python -m flask init-db
```

## Usage
Run the following in console:
```shell
python main.py
```
