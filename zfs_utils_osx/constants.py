
ZPOOL_TYPES = dict(
    raidz=lambda n: n - 1,
    raidz1=lambda n: n - 1,
    raidz2=lambda n: n - 2,
    raidz3=lambda n: n - 3,
    mirror=lambda n: 1,
)

ZPOOL_CREATE_MESSAGE = '''
Creating %(count)s images named %(name)s of size %(image_size)fGiB
for an effective size of %(effective_size)fGiB. The disk space used will be
%(physical_size)fGiB.
'''.strip()

ZPOOL_CREATE_IMAGE_COMMAND = '''
hdiutil create
    -size %(image_size)sg
    -volname %(name)s
    -type SPARSE
    -layout NONE
    %(extra_args)s
    %(name)s
'''
ZPOOL_ATTACH_IMAGE_COMMAND = '''
hdiutil attach
    -nomount
    %(extra_args)s
    %(name)s.sparseimage
'''
ZPOOL_CREATE_COMMAND = '''
sudo zpool create
    %(extra_args)s
    -f
    -m %(mountpoint)s
    %(pool_name)s
    %(type)s
    %(devices)s
'''

