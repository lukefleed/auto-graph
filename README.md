# Automated graph generator for benchmarks

Developed for [morethantech.it](https://morethantech.it).

## Setup

```
git clone https://github.com/lukefleed/auto-graph.git
git checkout develop
pipenv install
```

## Usage

From the project's root:
1. Place the Excel spreadsheets inside the `input` folder (create it if it doesn't exist)
2. During development, run `pipenv run start` to execute the program
3. Check out the images in the `output` folder
4. Build for production with `pipenv run build`
5. Run the built executable with `./anakin` (Linux) or `anakin.exe` (Windows)

## TO DO

- Graph aesthetics
- Games benchmarks
- Documenting everything
- Make the program work when executed from a directory other than the project's root
- Add `input/example.xlsx` with some examples (it's already gitignored)
