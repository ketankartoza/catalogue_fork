Setup notes on a fresh server:

Add to ~/.pip/pip.conf :

```
[global]
download_cache = 
```

And make the pip dir:

```
mkdir ~/.cache/pip
```

Create the virtualenv:

```
virtualenv env
```

Manually install gdal:

```
source virtualenv/bin/activate
pip install --no-install GDAL
cd venv/build/GDAL/
python setup.py build_ext --include-dirs=/usr/include/gdal/
pip install --no-download GDAL
```


