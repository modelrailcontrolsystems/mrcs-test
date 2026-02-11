# mrcs-test

_Model Rail Control Systems (MRCS) end-to-end and integration tests_

---

### Repos

Requires MRCS repos:

* **[mrcs-api](https://github.com/modelrailcontrolsystems/mrcs-api)**
* **[mrcs-cli](https://github.com/modelrailcontrolsystems/mrcs-cli)**
* **[mrcs-control](https://github.com/modelrailcontrolsystems/mrcs-control)**
* **[mrcs-core](https://github.com/modelrailcontrolsystems/mrcs-core)**

---

### .env

In order to run MRCS command-line utilities as subprocesses, a .env file is required, such as:

```
HOME=/Users/bruno
MRCS=Documents/Development/Python/MRCS/MRCSMacProject
VENV=.venv14
```

* HOME - user home
* MRCS - the relative path from the user home to the repo clones
* VENV - the active Python virtual environment

The `.env` file is not included in the repo.
