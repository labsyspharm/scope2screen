# Scope2Screen 

Scope2Screen is an open-source web-application for focus+context exploration and annotation of whole-slide, high-plex, tissue images. The client -server application consists of a python [Flask](http://flask.pocoo.org/) backend and a [Node.js](https://nodejs.org/en/) javascript frontend. The server’s  restful  API  allows  to  retrieve  image  and  feature  data and to steer analytics.  The frontend is built using Bootstrap, D3.js, and [openseadragon](https://openseadragon.github.io/), a web-based zoomable imageviewer, which we extend significantly. Take a look at our [Wiki](https://github.com/labsyspharm/scope2screen/wiki) to find out more.

## Executables (for Users)
Releases can be found here:
https://github.com/labsyspharm/scope2screen/releases
These are executables for Windows and MacOS that can be run locally without any installations.

## Running as a Docker container

From the directory that contains your data files:

`docker run --rm -v "$PWD":/data -p 8000:8000 labsyspharm/scope2screen:0.74`

where
* `--rm` cleans up the container after it finishes executing
* `-v` mounts the "present working directory" (containing your data) to be `/data` inside the container
* `-p` forwards the port 8000
* `0.74` specifies the tool version (see [Releases](https://github.com/labsyspharm/scope2screen/releases))

Once the container is running, go to `http://localhost:8000/` in your web browser.

## Clone and Run Codebase (for Developers)
#### Checkout Project
`git clone https://github.com/labsyspharm/scope2screen.git`


#### 2. Conda Install Instructions. 
##### Install Conda
* Install [miniconda](https://conda.io/miniconda.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html). 
* Create env:  `conda env create -f requirements.yml`

##### Activate Environment
* Active environment: `conda activate scope2screen`


##### Start the Server

* `python run.py` - Runs the webserver

##### Access the Server

* Access the tool via `http://localhost:8000/`


## Packaging/Bundling Code as Executable (for Developers)

Any tagged commit to a branch will trigger a build. This will appear under releases. Note building may take ~10 min.

**Tagging Conventions:** All release tags should look like `v{version_number}_{branch_name}`.

* Tagging Example:  `git tag "vX.X_scope2screen"` (adds a tag) followed by `git push --tags` (pushes the tag)


## Publication
This tool prototype is part of the publication:
Jared Jessup+#, Robert Krueger+#, Simon Warchol#, John Hoffer#, Jeremy Muhlich#, Cecily C. Ritch, Giorgio Gaglia, Shannon Coy, Yu-An Chen, Jia-Ren Lin, Sandro Santagata, Peter K. Sorger, Hanspeter Pfister, "Scope2Screen: Focus+Context Techniques for Pathology Tumor Assessment in Multivariate Image Data," in IEEE Transactions on Visualization and Computer Graphics, (to appear in Transaction of Visualization and Computer Graphics, 2021).

<font size="1"> \+ contributed equally to this work</font>

<font size="1">\# have contributed code to the project</font>

## Data
To download an example dataset for Scope2Screen, go to
https://www.synapse.org/#!Synapse:syn26304730/wiki/613130 and register as a synapse user.
