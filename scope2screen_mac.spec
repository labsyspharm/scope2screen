# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['scipy.spatial.transform._rotation_groups', 'sqlalchemy.sql.default_comparator', 'sklearn.metrics._pairwise_distances_reduction._datasets_pair', 'sklearn.neighbors._partition_nodes', 'sklearn.metrics._pairwise_distances_reduction._datasets_pair', 'cmath']
hiddenimports += collect_submodules('sklearn.utils')


block_cipher = None


a = Analysis(
    ['run.py'],
    pathex=['/opt/homebrew/Caskroom/miniforge/base/envs/scope2screen2'],
    binaries=[],
    datas=[('minerva_analysis/client', 'minerva_analysis/client'), ('minerva_analysis/__init__.py', 'minerva_analysis/'), ('minerva_analysis/server', 'minerva_analysis/server'), ('/opt/homebrew/Caskroom/miniforge/base/envs/scope2screen2/lib/python3.8/site-packages/xmlschema/schemas', 'xmlschema/schemas')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='scope2screen_mac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
