https://github.com/Samsung/ONE/issues/8929
# Error occurred while upgrading one-compiler to latest version

When upgrading to the latest version on a daily basis, the following error occurs. It is presumed that this is a problem that occurs in the process of upgrading to the latest Python 3.8 based on the existing Python 3.6 based installation.

- OS: Ubuntu 18.04LTS
- Previously installed version : I can't say for sure, but approx `one-compiler/bionic-dev 1.20.0~22040118` or earlier
- Installing version : `one-compiler/bionic-dev 1.20.0~22041318` 
- Error log
```
sjlee@u1804:~ $ sudo apt upgrade
Reading package lists... Done
Building dependency tree
Reading state information... Done
Calculating upgrade... Done
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
6 not fully installed or removed.
After this operation, 0 B of additional disk space will be used.
Do you want to continue? [Y/n]
Setting up one-compiler (1.20.0~22041318) ...
WARNING: The directory '/home/sjlee/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
Requirement already satisfied: pip in /usr/share/one/bin/venv/lib/python3.6/site-packages (21.3.1)
Requirement already satisfied: setuptools in /usr/share/one/bin/venv/lib/python3.6/site-packages (59.6.0)
WARNING: The directory '/home/sjlee/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
ERROR: Could not find a version that satisfies the requirement tensorflow-cpu==2.8.0 (from versions: 1.15.0, 2.1.0, 2.1.1, 2.1.2, 2.1.3, 2.1.4, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.3.0, 2.3.1, 2.3.2, 2.3.3, 2.3.4, 2.4.0, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.5.0, 2.5.1, 2.5.2, 2.6.0, 2.6.1, 2.6.2)
ERROR: No matching distribution found for tensorflow-cpu==2.8.0
dpkg: error processing package one-compiler (--configure):
 installed one-compiler package post-installation script subprocess returned error exit status 1
dpkg: dependency problems prevent configuration of one-compiler-dev:amd64:
 one-compiler-dev:amd64 depends on one-compiler; however:
  Package one-compiler is not configured yet.

dpkg: error processing package one-compiler-dev:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest-dev:amd64:
 triv2-toolchain-latest-dev:amd64 depends on one-compiler-dev (= 1.20.0~22041318); however:
  Package one-compiler-dev:amd64 is not configured yet.

dpkg: error processing package triv2-toolchain-latest-dev:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest:amd64:
 triv2-toolchain-latest:amd64 depends on one-compiler (= 1.20.0~22041318); however:
  Package one-compiler is not configured yet.

dpkg: error processing package triv2-toolchain-latest:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of one-compiler-test:amd64:
 one-compiler-test:amd64 depends on one-compiler; however:
  Package one-compiler is not configured yet.

dpkg: error processing package one-compiler-test:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest-test:amd64:
 triv2-toolchain-latest-test:amd64 depends on triv2-toolchain-latest (= 1.1.0~22041320); however:
  Package triv2-toolchain-latest:amd64 is not configured yet.
 triv2-toolchain-latest-test:amd64 depends on one-compiler-test (= 1.20.0~22041318); however:
  Package one-compiler-test:amd64 is not configured yet.

dpkg: error processing package triv2-toolchain-latest-test:amd64 (--configure):
 dependency problems - leaving unconfigured
Errors were encountered while processing:
 one-compiler
 one-compiler-dev:amd64
 triv2-toolchain-latest-dev:amd64
 triv2-toolchain-latest:amd64
 one-compiler-test:amd64
 triv2-toolchain-latest-test:amd64
E: Sub-process /usr/bin/dpkg returned an error code (1)
sjlee@u1804:~ 100 $
```

<details><summary>full log</summary>

```
sjlee@u1804:~/triv/NPU_Compiler (master) $ sudo apt update
[sudo] password for sjlee:
Get:1 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev InRelease [2,477 B]
Get:2 https://packages.microsoft.com/ubuntu/18.04/prod bionic InRelease [4,003 B]
Hit:3 https://deb.nodesource.com/node_16.x bionic InRelease
Hit:4 http://ppa.launchpad.net/jonathonf/vim/ubuntu bionic InRelease
Hit:5 http://archive.ubuntu.com/ubuntu bionic InRelease
Get:6 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Get:7 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 Packages [156 kB]
Get:8 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
Get:9 https://packages.microsoft.com/ubuntu/18.04/prod bionic/main amd64 Packages [274 kB]
Get:10 https://packages.microsoft.com/ubuntu/18.04/prod bionic/main amd64 Contents (deb) [3,628 kB]
Get:11 http://security.ubuntu.com/ubuntu bionic-security/main amd64 Packages [2,695 kB]
Get:12 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
Get:13 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [3,134 kB]
Get:14 http://security.ubuntu.com/ubuntu bionic-security amd64 Contents (deb) [175 MB]
Get:15 http://archive.ubuntu.com/ubuntu bionic-updates amd64 Contents (deb) [186 MB]
Get:16 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [1,490 kB]
Get:17 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages [2,268 kB]
Fetched 375 MB in 1min 16s (4,948 kB/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done
13 packages can be upgraded. Run 'apt list --upgradable' to see them.
sjlee@u1804:~/triv/NPU_Compiler (master) $ sudo apt upgrade
Reading package lists... Done
Building dependency tree
Reading state information... Done
Calculating upgrade... Done
The following NEW packages will be installed:
  libpython3.8-minimal libpython3.8-stdlib python3.8 python3.8-minimal python3.8-venv
The following packages will be upgraded:
  git git-man gzip liblzma5 one-compiler one-compiler-dev one-compiler-test triv2-compiler triv2-mte triv2-toolchain-latest triv2-toolchain-latest-dev
  triv2-toolchain-latest-test xz-utils
13 upgraded, 5 newly installed, 0 to remove and 0 not upgraded.
5 standard security updates
Need to get 18.7 MB of archives.
After this operation, 18.9 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 triv2-toolchain-latest-test amd64 1.1.0~22041320 [2,248 B]
Get:2 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 triv2-toolchain-latest-dev amd64 1.1.0~22041320 [2,268 B]
Get:3 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 triv2-toolchain-latest amd64 1.1.0~22041320 [2,648 B]
Get:4 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 one-compiler amd64 1.20.0~22041318 [2,879 kB]
Get:5 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 one-compiler-test amd64 1.20.0~22041318 [47.5 kB]
Get:6 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 one-compiler-dev amd64 1.20.0~22041318 [2,491 kB]
Get:7 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 triv2-mte amd64 1.4.0~22041315 [363 kB]
Get:8 https://art.sec.samsung.net/artifactory/list/aip_debian bionic-dev/universe amd64 triv2-compiler amd64 1.4.0~22041315 [3,327 kB]
Get:9 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 gzip amd64 1.6-5ubuntu1.2 [90.3 kB]
Get:10 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 libpython3.8-minimal amd64 3.8.0-3ubuntu1~18.04.2 [704 kB]
Get:11 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 python3.8-minimal amd64 3.8.0-3ubuntu1~18.04.2 [1,807 kB]
Get:12 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 liblzma5 amd64 5.2.2-1.3ubuntu0.1 [91.1 kB]
Get:13 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 xz-utils amd64 5.2.2-1.3ubuntu0.1 [83.8 kB]
Get:14 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 git-man all 1:2.17.1-1ubuntu0.10 [804 kB]
Get:15 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 git amd64 1:2.17.1-1ubuntu0.10 [3,923 kB]
Get:16 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 libpython3.8-stdlib amd64 3.8.0-3ubuntu1~18.04.2 [1,676 kB]
Get:17 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 python3.8 amd64 3.8.0-3ubuntu1~18.04.2 [355 kB]
Get:18 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 python3.8-venv amd64 3.8.0-3ubuntu1~18.04.2 [5,304 B]
Fetched 18.7 MB in 3s (5,492 kB/s)
(Reading database ... 76968 files and directories currently installed.)
Preparing to unpack .../gzip_1.6-5ubuntu1.2_amd64.deb ...
Unpacking gzip (1.6-5ubuntu1.2) over (1.6-5ubuntu1.1) ...
Setting up gzip (1.6-5ubuntu1.2) ...
Selecting previously unselected package libpython3.8-minimal:amd64.
(Reading database ... 76968 files and directories currently installed.)
Preparing to unpack .../libpython3.8-minimal_3.8.0-3ubuntu1~18.04.2_amd64.deb ...
Unpacking libpython3.8-minimal:amd64 (3.8.0-3ubuntu1~18.04.2) ...
Selecting previously unselected package python3.8-minimal.
Preparing to unpack .../python3.8-minimal_3.8.0-3ubuntu1~18.04.2_amd64.deb ...
Unpacking python3.8-minimal (3.8.0-3ubuntu1~18.04.2) ...
Preparing to unpack .../liblzma5_5.2.2-1.3ubuntu0.1_amd64.deb ...
Unpacking liblzma5:amd64 (5.2.2-1.3ubuntu0.1) over (5.2.2-1.3) ...
Setting up liblzma5:amd64 (5.2.2-1.3ubuntu0.1) ...
(Reading database ... 77248 files and directories currently installed.)
Preparing to unpack .../00-xz-utils_5.2.2-1.3ubuntu0.1_amd64.deb ...
Unpacking xz-utils (5.2.2-1.3ubuntu0.1) over (5.2.2-1.3) ...
Preparing to unpack .../01-git-man_1%3a2.17.1-1ubuntu0.10_all.deb ...
Unpacking git-man (1:2.17.1-1ubuntu0.10) over (1:2.17.1-1ubuntu0.9) ...
Preparing to unpack .../02-git_1%3a2.17.1-1ubuntu0.10_amd64.deb ...
Unpacking git (1:2.17.1-1ubuntu0.10) over (1:2.17.1-1ubuntu0.9) ...
Selecting previously unselected package libpython3.8-stdlib:amd64.
Preparing to unpack .../03-libpython3.8-stdlib_3.8.0-3ubuntu1~18.04.2_amd64.deb ...
Unpacking libpython3.8-stdlib:amd64 (3.8.0-3ubuntu1~18.04.2) ...
Selecting previously unselected package python3.8.
Preparing to unpack .../04-python3.8_3.8.0-3ubuntu1~18.04.2_amd64.deb ...
Unpacking python3.8 (3.8.0-3ubuntu1~18.04.2) ...
Selecting previously unselected package python3.8-venv.
Preparing to unpack .../05-python3.8-venv_3.8.0-3ubuntu1~18.04.2_amd64.deb ...
Unpacking python3.8-venv (3.8.0-3ubuntu1~18.04.2) ...
Preparing to unpack .../06-triv2-toolchain-latest-test_1.1.0~22041320_amd64.deb ...
Unpacking triv2-toolchain-latest-test:amd64 (1.1.0~22041320) over (1.1.0~22040720) ...
Preparing to unpack .../07-triv2-toolchain-latest-dev_1.1.0~22041320_amd64.deb ...
Unpacking triv2-toolchain-latest-dev:amd64 (1.1.0~22041320) over (1.1.0~22040720) ...
Preparing to unpack .../08-triv2-toolchain-latest_1.1.0~22041320_amd64.deb ...
Unpacking triv2-toolchain-latest:amd64 (1.1.0~22041320) over (1.1.0~22040720) ...
Preparing to unpack .../09-one-compiler_1.20.0~22041318_amd64.deb ...
Unpacking one-compiler (1.20.0~22041318) over (1.20.0~22040618) ...
Preparing to unpack .../10-one-compiler-test_1.20.0~22041318_amd64.deb ...
Unpacking one-compiler-test:amd64 (1.20.0~22041318) over (1.20.0~22040618) ...
Preparing to unpack .../11-one-compiler-dev_1.20.0~22041318_amd64.deb ...
Unpacking one-compiler-dev:amd64 (1.20.0~22041318) over (1.20.0~22040618) ...
Preparing to unpack .../12-triv2-mte_1.4.0~22041315_amd64.deb ...
Unpacking triv2-mte:amd64 (1.4.0~22041315) over (1.4.0~22040715) ...
Preparing to unpack .../13-triv2-compiler_1.4.0~22041315_amd64.deb ...
Unpacking triv2-compiler:amd64 (1.4.0~22041315) over (1.4.0~22040715) ...
Setting up git-man (1:2.17.1-1ubuntu0.10) ...
Setting up libpython3.8-minimal:amd64 (3.8.0-3ubuntu1~18.04.2) ...
Setting up triv2-mte:amd64 (1.4.0~22041315) ...
Setting up python3.8-minimal (3.8.0-3ubuntu1~18.04.2) ...
update-binfmts: warning: Couldn't load the binfmt_misc module.
Setting up xz-utils (5.2.2-1.3ubuntu0.1) ...
Setting up triv2-compiler:amd64 (1.4.0~22041315) ...
Setting up git (1:2.17.1-1ubuntu0.10) ...
Setting up libpython3.8-stdlib:amd64 (3.8.0-3ubuntu1~18.04.2) ...
Setting up python3.8 (3.8.0-3ubuntu1~18.04.2) ...
Setting up python3.8-venv (3.8.0-3ubuntu1~18.04.2) ...
Setting up one-compiler (1.20.0~22041318) ...
WARNING: The directory '/home/sjlee/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
Requirement already satisfied: pip in /usr/share/one/bin/venv/lib/python3.6/site-packages (21.3.1)
Requirement already satisfied: setuptools in /usr/share/one/bin/venv/lib/python3.6/site-packages (59.6.0)
WARNING: The directory '/home/sjlee/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
ERROR: Could not find a version that satisfies the requirement tensorflow-cpu==2.8.0 (from versions: 1.15.0, 2.1.0, 2.1.1, 2.1.2, 2.1.3, 2.1.4, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.3.0, 2.3.1, 2.3.2, 2.3.3, 2.3.4, 2.4.0, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.5.0, 2.5.1, 2.5.2, 2.6.0, 2.6.1, 2.6.2)
ERROR: No matching distribution found for tensorflow-cpu==2.8.0
dpkg: error processing package one-compiler (--configure):
 installed one-compiler package post-installation script subprocess returned error exit status 1
dpkg: dependency problems prevent configuration of one-compiler-dev:amd64:
 one-compiler-dev:amd64 depends on one-compiler; however:
  Package one-compiler is not configured yet.

dpkg: error processing package one-compiler-dev:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest-dev:amd64:
 triv2-toolchain-latest-dev:amd64 depends on one-compiler-dev (= 1.20.0~22041318); however:
  Package one-compiler-dev:amd64 is not configured yet.

dpkg: error processing package triv2-toolchain-latest-dev:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest:amd64:
 triv2-toolchain-latest:amd64 depends on one-compiler (= 1.20.0~22041318); however:
  Package one-compiler is not configured yet.

dpkg: error processing package triv2-toolchain-latest:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of one-compiler-test:amd64:
 one-compiler-test:amd64 depends on one-compiler; however:
  Package one-compiler is not configured yet.

dpkg: error processing package one-compiler-test:amd64 (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of triv2-toolchain-latest-test:amd64:
 triv2-toolchain-latest-test:amd64 depends on triv2-toolchain-latest (= 1.1.0~22041320); however:
  Package triv2-toolchain-latest:amd64 is not configured yet.
 triv2-toolchain-latest-test:amd64 depends on one-compiler-test (= 1.20.0~22041318); however:
  Package one-compiler-test:amd64 is not configured yet.

dpkg: error processing package triv2-toolchain-latest-test:amd64 (--configure):
 dependency problems - leaving unconfigured
Processing triggers for mime-support (3.60ubuntu1) ...
Processing triggers for install-info (6.5.0.dfsg.1-2) ...
Processing triggers for libc-bin (2.27-3ubuntu1.5) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
Errors were encountered while processing:
 one-compiler
 one-compiler-dev:amd64
 triv2-toolchain-latest-dev:amd64
 triv2-toolchain-latest:amd64
 one-compiler-test:amd64
 triv2-toolchain-latest-test:amd64
E: Sub-process /usr/bin/dpkg returned an error code (1)
sjlee@u1804:~/triv/NPU_Compiler (master) 100 $
```
</details>
