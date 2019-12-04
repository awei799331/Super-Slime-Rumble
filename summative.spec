# -*- mode: python -*-

block_cipher = None

add_files = [
  ("resources/images/*.jpg", "resources/images"),
  ("resources/images/*.png", "resources/images"),
  ("resources/*.mp4", "resources"),
  ("resources/audio/*.wav", "resources/audio")
]

a = Analysis(['summative.py', 'spawners.py', 'Master.py', 'Bullet.py', 'Player.py', 'weapons.py'],
             pathex=['C:\\Users\\SUMMER_TONY\\programming\\programs\\ICS3UI\\summative_copy\\summative'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='summative',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='summative')
