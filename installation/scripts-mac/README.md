# Installation on macOS

1. Install [Homebrew](https://brew.sh), which is used to install all
   helper packages:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

2. Go to the scripts-mac directory.

```
cd scripts-mac
```

3. Install prerequisites. This requires root permission.

```
./install-prereq-mac.sh
```

4. Register on the Gurobi website and download gurobi package.

```
http://www.gurobi.com
```

3. Register on the [Gurobi website](http://www.gurobi.com) and download
   the Gurobi package.

- Go to Download/Gurobi Optimizer and download package version 5.1.1
  appropriate for your environment.

- Go to Download/License and get a Gurobi license key. Save the key in a
  safe place.

4. Download [Boxer
model](https://github.com/chbrown/candc/blob/gh-pages/downloads/models-1.02.tgz)
   (the "models trained on CCGbank 02-21 and MUC 7")

5. Install ADP package.

```
./deploy-all-mac.sh installation_directory gurobi_file_location \
    gurobi_license_key boxer_username boxer_password \
    boxer_models_file_location
```

- `installation_directory`: this is the directory where the package will
  be installed. Should be in a location where you have write permission
  (e.g., `/Users/me/adp_home`)
- `gurobi_file_location`: full path for gurobi package downloaded in Step
  3 (e.g., `/Users/me/package/gurobi5.0.1_linux64.tar.gz`)
- `gurobi_license_key`: license key generated in Step 3.
- `boxer_username`: username for boxer website (Step 4)
- `boxer_password`: password for boxer website (Step 4)
- `boxer_models_file_location`: models downloaded in Step 4
  (e.g., `/Users/me/package/models-1.02.tgz`)

6. Test your installation.

```
./test_install-mac.sh installation-directory
```

7. Set permanent environment variables.

```
./setenv-mac.py installation-directory
```

- `installation_directory`: this is the directory where the package has
  been installed. Should be the same as the installation-directory
  provided above.
