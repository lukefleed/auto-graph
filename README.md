# Automated graph generator for benchmarks

Developed for [morethantech.it](https://morethantech.it).

## Usage

1. Place the Excel spreadsheets inside the `input` folder (create it if it doesn't exist), in the same folder where the executable is
2. From a terminal in the executable folder, run `anakin.exe` (Windows) or `./anakin` (Linux)
3. Follow the prompts
4. Check out the images in the `output` folder

## Setup for development

```
git clone https://github.com/lukefleed/auto-graph.git
git checkout develop
pipenv install
```

### Usage during development

From the project's root:
1. Place the Excel spreadsheets inside the `input` folder (create it if it doesn't exist)
2. During development, run `pipenv run start` to execute the program
3. Check out the images in the `output` folder
4. Build for production with `pipenv run build`
5. Run the built executable with `./anakin` (Linux) or `anakin.exe` (Windows)

## TO DO

- Make the program work when executed from a directory other than the project's root
- Add `input/example.xlsx` with some examples (it's already gitignored)
