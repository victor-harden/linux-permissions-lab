# Permission exercises

Work in a lab VM or container. The setup script only creates files inside a
temporary directory.

1. Create a file readable by everyone and writable only by you. Verify with `ls -l`.
2. Convert `rw-r-----` to octal by hand, then check with `permcalc.py`.
3. Create a directory where new files are automatically owned by a shared group
   (setgid bit).
4. Explain what `4755` does on an executable and why vendors avoid it for
   general-purpose tools.
5. Build a directory where only the owner may delete files, even if others can
   write (sticky bit).
6. Find every world-writable file in the practice tree.
7. Fix the practice tree so that no file is world-writable.
8. Write the `find` command that would list setuid binaries on the system, and
   explain why that output needs review rather than automatic deletion.
