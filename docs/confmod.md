Example

Suppose /etc/ssh/sshd_config contains:

PermitRootLogin yes

You could run:

sudo python3 confmod.py \
    /etc/ssh/sshd_config \
    "PermitRootLogin yes" \
    "PermitRootLogin no"

The script will:

Read the original file's UID.
Read the original GID.
Read the original permission bits.
Read the complete file.
Find the exact line.
Create /etc/ssh/sshd_config.bak.
Create a temporary file in /etc/.
Write the modified configuration to the temporary file.
Apply the original UID/GID.
Apply the original permission bits.
Flush the data to disk.
Atomically replace the original.
Run restorecon when available to restore the expected SELinux context.
Why not simply open the file with "w"?

You could do:

with open("/etc/example.conf", "w") as f:
    ...

and the existing ownership and permissions would generally remain because you're modifying the existing inode.

However, it has an important weakness: if the process crashes or the disk fills while writing, you can end up with a truncated configuration file.

The temporary-file + os.replace() approach is considerably safer for /etc/* configuration files.

One important consideration

os.replace() replaces the inode. Therefore, simply preserving chmod and chown isn't enough if you need to preserve every possible filesystem attribute associated with the original file. Linux configuration files can potentially have ACLs, extended attributes, capabilities, SELinux labels, etc.

For ordinary /etc files, the script above handles the most important properties:

- UID
- GID
- Unix permission bits
- SELinux context where restorecon is available
- Original file contents except for the requested replacement
- Newline style
- Atomic replacement
- Backup