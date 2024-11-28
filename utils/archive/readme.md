# Clone this conda env to another machine

- On this machine: `conda env export > environment.yml`

- On the target machine: `conda env create -f environment.yml`
