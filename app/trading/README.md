
# Installation
```bash
$ brew install postgresql
$ poetry install
```

### For M1
```bash
$ CFLAGS="-I$(brew --prefix)/include" LDFLAGS="-L$(brew --prefix)/lib" poetry install
```
