"""
Module: 'uos' on micropython-...-rp2
"""
from typing import Any, Iterator, Optional, Union
from builtins import staticmethod

def remove(path: str) -> Any:
    """Remove a file."""
    ...


class VfsFat():
    """Create a filesystem object that uses the 
    FAT filesystem format. Storage of the FAT 
    filesystem is provided by ``block_dev``. 
    Objects created by this constructor can 
    be mounted using ``mount()``.
    """

    def __init__(self, *argv, **kwargs) -> None:
        ...

    def open(self, *args, **kwargs) -> Any:
        ...

    def remove(self, *args, **kwargs) -> Any:
        ...

    def chdir(self, *args, **kwargs) -> Any:
        ...

    def getcwd(self, *args, **kwargs) -> Any:
        ...

    def ilistdir(self, *args, **kwargs) -> Any:
        ...

    def mkdir(self, *args, **kwargs) -> Any:
        ...

    @staticmethod
    def mkfs(block_dev) -> Any:
        """Build a FAT filesystem on *block_dev*."""
        ...

    def mount(self, *args, **kwargs) -> Any:
        ...

    def rename(self, *args, **kwargs) -> Any:
        ...

    def rmdir(self, *args, **kwargs) -> Any:
        ...

    def stat(self, *args, **kwargs) -> Any:
        ...

    def statvfs(self, *args, **kwargs) -> Any:
        ...

    def umount(self, *args, **kwargs) -> Any:
        ...


class VfsLfs2():
    """Filesystem object that uses the littlefs v2 filesystem format"""

    def __init__(self, block_dev, readsize: int=32, progsize: int=32, lookahead: int=32, mtime: bool=True) -> None:
        """Create a filesystem object that uses the 
        littlefs v2 filesystem format. Storage of the 
        littlefs filesystem is provided by *block_dev*, 
        which must support the extended interface. 
        Objects created by this constructor can be 
        mounted using ``mount()``."""
        ...

    def open(self, *args, **kwargs) -> Any:
        ...

    def remove(self, *args, **kwargs) -> Any:
        ...

    def chdir(self, *args, **kwargs) -> Any:
        ...

    def getcwd(self, *args, **kwargs) -> Any:
        ...

    def ilistdir(self, *args, **kwargs) -> Any:
        ...

    def mkdir(self, *args, **kwargs) -> Any:
        ...

    @staticmethod
    def mkfs(block_dev, readsize: int=32, progsize: int=32, lookahead: int=32) -> Any:
        """Build a Lfs2 filesystem on *block_dev*."""
        ...

    def mount(self, *args, **kwargs) -> Any:
        ...

    def rename(self, *args, **kwargs) -> Any:
        ...

    def rmdir(self, *args, **kwargs) -> Any:
        ...

    def stat(self, *args, **kwargs) -> Any:
        ...

    def statvfs(self, *args, **kwargs) -> Any:
        ...

    def umount(self, *args, **kwargs) -> Any:
        ...

def chdir(path: str) -> None:
    """Remove a file."""
    ...

def dupterm(steam_object, index=0,/) -> Any:
    """Duplicate or switch the MicroPython terminal (the REPL) on 
    the given stream-like object. The stream_object argument must 
    be a native stream object, or derive from io.IOBase and 
    implement the readinto() and write() methods. The stream 
    should be in non-blocking mode and readinto() should return 
    None if there is no data available for reading.
    After calling this function all terminal output is repeated 
    on this stream, and any input that is available on the stream 
    is passed on to the terminal input.
    The index parameter should be a non-negative integer and 
    specifies which duplication slot is set. A given port may 
    implement more than one slot (slot 0 will always be available) 
    and in that case terminal input and output is duplicated on all 
    the slots that are set.
    If None is passed as the stream_object then duplication is 
    cancelled on the slot given by index.
    The function returns the previous stream-like object in the 
    given slot.
    """
    ...

def getcwd() -> str:
    """Get the current directory."""
    ...

def ilistdir(dir: Optional[str] = None) -> Iterator[Union[tuple[str, int, int], tuple[str, int, int, int]]]:
    """This function returns an iterator which then yields 
    tuples corresponding to the entries in the directory 
    that it is listing. With no argument it lists the current 
    directory, otherwise it lists the directory given by dir.
    The tuples have the form (name, type, inode[, size]):
    - *name* is a string (or bytes if dir is a bytes object) 
    and is the name of the entry;
    - *type* is an integer that specifies the type of the entry, with 0x4000 for directories and 0x8000 for regular files;
    - *inode* is an integer corresponding to the inode of the file, and may be 0 for filesystems that don't have such a notion.
    - Some platforms may return a 4-tuple that includes the entry's *size*. For file entries, size is an integer representing the size of the file or -1 if unknown. Its meaning is currently undefined for directory entries.
    """
    ...

def listdir(dir: Optional[str] = None) -> list[str]:
    """With no argument, list the current directory. 
    Otherwise list the given directory.
    """
    ...

def mkdir(path: str) -> None:
    """Create a new directory."""
    ...

def mount(fsobj, mount_point, *, readonly: bool) -> Any:
    """Mount the filesystem object fsobj at the location in the VFS 
    given by the mount_point string. fsobj can be a a VFS object that 
    has a ``mount()`` method, or a block device. If it's a block device 
    then the filesystem type is automatically detected (an exception 
    is raised if no filesystem was recognised). mount_point may 
    be ``'/'`` to mount fsobj at the root, or ``'/<name>'`` to mount 
    it at a subdirectory under the root.
    If readonly is ``True`` then the filesystem is mounted read-only.
    During the mount process the method ``mount()`` is called on the filesystem object.
    Will raise ``OSError(EPERM)`` if mount_point is already mounted.
    """
    ...

def rename(old_path: str, new_path: str) -> None:
    """Rename a file."""
    ...

def rmdir(path: str) -> Any:
    """Remove a directory."""
    ...

def stat(path: str) -> Any:
    """Get the status of a file or directory."""
    ...

def statvfs(path: str) -> tuple[str, str, str, str, str, str, str, str, str, str]:
    """Get the status of a fileystem.
    Returns a tuple with the filesystem information in the following order:
    - ``f_bsize`` - file system block size
    - ``f_frsize`` - fragment size
    - ``f_blocks`` - size of fs in f_frsize units
    - ``f_bfree`` - number of free blocks
    - ``f_bavail`` - number of free blocks for unprivileged users
    - ``f_files`` - number of inodes
    - ``f_ffree`` - number of free inodes
    - ``f_favail`` - number of free inodes for unprivileged users
    - ``f_flag`` - mount flags
    - ``f_namemax`` - maximum filename length
    Parameters related to inodes: ``f_files``, ``f_ffree``, ``f_avail`` 
    and the ``f_flags`` parameter may return ``0`` as they can be unavailable 
    in a port-specific implementation.
    """
    ...

def sync():
    """Sync all filesystems.
    """
    ...

def umount(mount_point) -> Any:
    """Unmount a filesystem. mount_point can be a string naming 
    the mount location, or a previously-mounted filesystem object. 
    During the unmount process the method ``umount()`` is called 
    on the filesystem object.
    Will raise ``OSError(EINVAL)`` if mount_point is not found.
    """
    ...

def uname() -> tuple[str, str, str, str, str]:
    """Return a tuple (possibly a named tuple) containing information about 
    the underlying machine and/or its operating system. The tuple has five 
    fields in the following order, each of them being a string:
    - ``sysname`` - the name of the underlying system
    - ``nodename`` - the network name (can be the same as ``sysname``)
    - ``release`` - the version of the underlying system
    - ``version`` - the MicroPython version and build date
    - ``machine`` - an identifier for the underlying hardware (eg board, CPU)
    """
    ...

def unlink(*args, **kwargs) -> Any:
    ...

def urandom(n: int) -> bytes:
    """Return a bytes object with n random bytes. Whenever 
    possible, it is generated by the hardware random 
    number generator.
    """
    ...
