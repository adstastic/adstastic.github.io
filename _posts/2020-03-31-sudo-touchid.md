---
layout: post
title: Authenticating sudo with TouchID
tags: [software]
---

TouchID is great - a seamless way to authenticate on the new Macbooks. I enjoy the ease of logins, admin passwords, unlocking apps, etc, but the one place I wish I had it is in the Terminal, to authenticate `sudo`.

My wish has been granted! 

1. Sudo open `/etc/pam.d/sudo`. The file should look something like:
```python
# sudo: auth account password session
auth       sufficient     pam_smartcard.so
auth       required       pam_opendirectory.so
account    required       pam_permit.so
password   required       pam_deny.so
session    required       pam_permit.so
```
2. Add `auth sufficient pam_tid.so` to the top of the file (below the comment):
```python
# sudo: auth account password session
auth       sufficient     pam_tid.so
auth       sufficient     pam_smartcard.so
auth       required       pam_opendirectory.so
account    required       pam_permit.so
password   required       pam_deny.so
session    required       pam_permit.so
```
3. Save, and enjoy TouchID authentication for sudo.
![TouchID authentication for sudo](/assets/touchid.png)