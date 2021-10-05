# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['run.py'],
             pathex=['/opt/homebrew/anaconda3/envs/viewer', '/Users/swarchol/Research/scope2screen'],
             binaries=[],
             datas=[('scope2screen/client', 'scope2screen/client'), ('scope2screen/__init__.py', 'scope2screen/'), ('scope2screen/server', 'scope2screen/server'), ('/opt/homebrew/anaconda3/envs/viewer/lib/python3.7/site-packages/xmlschema/schemas', 'xmlschema/schemas')],
             hiddenimports=['scipy.spatial.transform._rotation_groups', 'sqlalchemy.sql.default_comparator', 'sklearn.utils._weight_vector', 'sklearn.neighbors._typedefs', 'sklearn.neighbors._partition_nodes', 'cmath'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
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
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
