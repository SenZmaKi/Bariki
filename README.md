# Getting Started 

## Algorand resources

- [Dev site](https://developer.algorand.org/)
- [What is a blockchain](https://www.youtube.com/playlist?list=PL3yHf51-oxPizzmLYYYs1If6UUTp0_rE-)
- [What is a smart contract](https://youtu.be/ZE2HxTmxfrI?si=0Vv6f7KnOHJWvL3p)
- [Pyteal Tutorial](https://www.youtube.com/playlist?list=PLwRyHoehE435ttTjvFZA-DyqHYIYc26K_)
- [Beaker Tutorial](https://www.youtube.com/playlist?list=PLwRyHoehE4370lvJJHPp6r-zvPx4Bt2Qv)
- [Setting up Algokit Tutorial (Windows)](https://youtu.be/22RvINnZsRo?si=RukMmt5I5ujafCNj)

## Backend

### Setup (Windows)

```ps
powershell "iwr -Uri https://raw.githubusercontent.com/SenZmaKi/Bariki/master/src/backend/setup.ps1 -UseBasicParsing | iex"
```

### Start server

- Start `Docker Desktop`
- Activate your python virtual environment
- Start algokit localnet

```sh
algokit localnet start
```

- From `Bariki/src/backend`

```sh
python -m app
```
