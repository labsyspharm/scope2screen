pyinstaller -F --paths $env:CONDA_PREFIX --add-data "scope2screen/client;scope2screen/client" --add-data "scope2screen/server;scope2screen/server" --add-data "%CONDA_PREFIX%/Lib/site-packages/xmlschema/schemas;xmlschema/schemas" --hidden-import "scipy.spatial.transform._rotation_groups" --hidden-import "sqlalchemy.sql.default_comparator" --hidden-import "sklearn.utils._weight_vector" --hidden-import "sklearn.neighbors._typedefs" --hidden-import "sklearn.neighbors._partition_nodes" --hidden-import cmath --icon icon.ico  --name scope2screen_windows run.py