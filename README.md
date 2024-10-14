[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cawi-hro/DADM_lecture_STMC.git/HEAD)

# Synchrotron Techniques for Materials Characterisation - Course 

This repository collects supplementary materials to the master's course "Synchrotron Techniques for Materials Characterisation" (STMC) given by [Berit Zeller-Plumhoff](https://www.hereon.de/institutes/metallic_biomaterials/imaging_and_data_science/team/098931/index.php.de) - University of Rostock - Chair of Data-driven Analysis and Design of Materials, Rostock, Germany. ### TODO:Check ### The contents are provided as [Open Educational Resource](https://de.wikipedia.org/wiki/Open_Educational_Resources), so feel free to fork, share, teach and learn. You can give the project a Star if you like it. ### 

## Getting Started

The Jupyter notebooks are accessible in various ways

* Online as [static web pages](https://nbviewer.org/github/spatialaudio/data-driven-audio-signal-processing-lecture/blob/main/index.ipynb)
* Online for [interactive usage](https://mybinder.org/v2/gh/spatialaudio/data-driven-audio-signal-processing-lecture/HEAD?labpath=index.ipynb) with [binder](https://mybinder.org/)
* Local for interactive usage on your computer

Other online services (e.g. [Google Colaboratory](https://colab.research.google.com), [Microsoft Azure](https://azure.microsoft.com/), ...) provide environments for interactive execution of Jupyter notebooks as well.
Local execution on your computer requires a local Jupyter/IPython installation.
The [Anaconda distribution](https://www.continuum.io/downloads) can be considered as a convenient starting point.
Then, you'd have to [clone/download the notebooks from Github](https://github.com/cawi-hro/DADM_lecture_STMC).
Use a [Git](http://git-scm.org/) client to clone the notebooks and then start your local Jupyter server. For manual installation under OS X/Linux please refer to your packet manager.

## Usage and Contributing

The contents are provided as [Open Educational Resource](https://de.wikipedia.org/wiki/Open_Educational_Resources).
The text is licensed under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/), the code of the IPython examples under the [MIT license](https://opensource.org/licenses/MIT).
Feel free to use the entire collection, parts or even single notebooks for your own purposes.
I am curious on the usage of the provided resources, so feel free to drop a line or report to [berit.zeller-plumhoff@uni-rostock.de](mailto:berit.zeller-plumhoff@uni-rostock.de).

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    │    
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations 
    │
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── __init__.py 
```

--------