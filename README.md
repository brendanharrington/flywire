# **FlyWire Community Detection**

## **Overview**
This project explores community detection in the FlyWire connectome dataset, a detailed neural connectivity map of *Drosophila melanogaster's* brain. By applying methods like the Stochastic Block Model (SBM) and its degree-corrected variant (DC-SBM), the goal is to identify biologically meaningful neural modules and assess the impact of degree correction in networks with heavy-tailed degree distributions.

## **Project Structure**
```
flywire/
├── data/               # Datasets (e.g., FlyWire CSV files)
├── src/                # Python scripts for processing and analysis
├── notebooks/          # Jupyter notebooks for exploration and visualization
├── outputs/            # Results (e.g., plots, community assignments)
├── docs/               # Documentation and notes
└── requirements.txt    # Python dependencies (excluding graph-tool)
```

## **Setup Instructions**

### Prerequisites
- **Python**: Version 3.12.7 or later
- **System Tools**:
  - `graph-tool`: Install using a package manager (instructions below)
  - `git`: For version control

### Install `graph-tool`
`graph-tool` cannot be installed via `pip`. Use the appropriate package manager for your operating system:

#### macOS
```bash
brew install graph-tool
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-graph-tool
```

#### Fedora
```bash
sudo dnf install python3-graph-tool
```

For other operating systems, refer to the official documentation: [Graph-tool Installation](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

### Clone the Repository
```bash
git clone https://github.com/brendanharrington/flywire.git
cd flywire
```

### Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## **How to Run**

### 1. **Data Loading**
- Place the FlyWire dataset in the `data/` directory.
- Use the `data_loader.py` script or corresponding notebook to preprocess the data.

### 2. **Community Detection**
- Run algorithms via `community_detection.py` or Jupyter notebooks in `notebooks/`.

### 3. **View Results**
- Generated outputs (e.g., plots and community assignments) will be saved in the `outputs/` directory for further analysis.

## **Project Goals**
1. **Data Exploration**: Investigate FlyWire’s connectome dataset to understand its structure and connectivity.
2. **Algorithm Implementation**: Apply and compare SBM and DC-SBM for community detection.
3. **Biological Insights**: Relate detected communities to functional neural modules.
4. **Performance Evaluation**: Assess whether degree correction enhances biological relevance.

## **Contributors**
- **Brendan Harrington** - [GitHub](https://github.com/brendanharrington)
- **Jackson Sutherland**

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.