# Monte carlo simulation for forecasting deadlines

## Talk
This repo is code behind the talk here:
https://docs.google.com/presentation/d/1xCI25Wa2eKsGYf_Qn0wRPcHhGSbaLntb7BU_Cd89wTw/edit?usp=sharing

## Running
You'll need python 3.7 and pipenv then run:

```bash
pipenv install
pipenv run python predict.py
```

## Example output

Script predicts how long an estimated 19 points of work would take for a team to do:

![Distribution](images/distribution.png)

The script considers the following "burn down" charts:

![Examples futures considered](images/examples.png)
