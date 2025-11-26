# Rataitosk 🐿️

**Semantic alignment analysis for strategic documents**

Rataitosk compares two PDF strategy documents using sentence embeddings ([paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)) to measure semantic alignment across four theory-grounded dimensions. The tool runs completely offline and generates SAMS Scorecards (Semantic Alignment Matrices for Strategy) that combine quantitative scores with qualitative evidence, serving as discussion starters for institutional sensemaking.

Developed as part of a Bachelor's thesis in IT & Digitalization.

---

## What Rataitosk Measures

**1. Thematic Similarity**  
Overall semantic overlap using distributional semantics (Harris, 1954; Reimers & Gurevych, 2019). Provides baseline assessment of whether documents address similar themes regardless of rhetorical style.

**2. Temporal Positioning**  
How documents construct temporal narratives linking past initiatives, present commitments, and future goals. Grounded in Temporal Work Theory (Kaplan & Orlikowski, 2012) and narrative sensemaking (Weick, 1995).

**3. Operational Grounding**  
Emphasis on present capabilities, existing structures, and ongoing work. Based on exploitation logic (March, 1991) and strategic fit theory (Henderson & Venkatraman, 1993).

**4. Transformational Vision**  
Forward-looking ambition and growth beyond current capabilities. Draws from strategic intent theory (Hamel & Prahalad, 1994) and transformational ambition frameworks (Ahuja & Lampert, 2001).

### SAMS Scorecards: Discussion Starters, Not Discussion Enders

Rataitosk generates scorecards that function as boundary objects between computational analysis and human judgment. Each scorecard combines:
- Quantitative scores across all four semantic axes
- Qualitative evidence through matched text excerpts
- Interpretive guidance without prescribing conclusions

The tool detects patterns; institutional actors interpret meaning within their organizational context.

---

## Getting Started

### Prerequisites

- **Python 3.9 or newer**
- Dependencies listed in `requirements.txt`
- PDF documents for analysis

### Quick Validation

If you have Python 3.9+ installed:
```bash
python validate_rataitosk.py
```

This will:
- Check your Python version
- Download the MiniLM model on first run
- Verify the installation
- Report any missing dependencies

If validation passes, you're ready to use Rataitosk. Otherwise, follow the installation steps below.

### Installation

**Automated Setup (Recommended)**

Windows:
```bash
install_rataitosk.bat
```

Linux/macOS:
```bash
bash install_rataitosk.sh
```

The installation scripts will:
- Verify Python version (≥3.9)
- Create an isolated virtual environment
- Install all required dependencies including sentence-transformers
- Download the paraphrase-multilingual-MiniLM-L12-v2 model
- Run validation automatically

**Manual Installation**

If automated setup fails:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python validate_rataitosk.py
```

**Note:** The MiniLM model downloads automatically on first use.

---

## Usage

### Step 1: Prepare Documents
Place two PDF documents in the `input/` folder.

### Step 2: Run Analysis
```bash
python cli/run_rataitosk.py
```

### Step 3: Review Results
Find generated SAMS Scorecards in the `output/` folder:
- **HTML report:** Human-readable scorecard with visualizations
- **JSON data:** Machine-readable results for further processing

---

## Project Structure
```
rataitosk/
├── input/              # Place your PDF documents here
├── output/             # Generated SAMS Scorecards (HTML & JSON)
├── axes/               # Semantic axis implementations
│   ├── thematic_similarity.py
│   ├── temporal_positioning.py
│   ├── operational_grounding.py
│   └── transformational_vision.py
├── cli/                # Command-line interface
├── config/             # Configuration files
├── core/               # Core processing (chunking, embedding, scoring)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Design Philosophy

Rataitosk development was guided by two formal design principles:

1. **Conceptual Grounding** – Every metric traces to explicit theoretical constructs
2. **Data Sovereignty** – Institutions maintain complete control over strategic data

These principles emerged through iterative development and are detailed in the thesis (Chapter 7.3).
---

## Methodological Context

Rataitosk demonstrates Design Science Research (Hevner et al., 2004; Peffers et al., 2007) applied to semantic alignment analysis in strategic documents. The tool was developed and validated within Norwegian public sector university contexts, addressing the challenge of detecting semantic divergence beneath formal strategic alignment. All processing occurs locally using sentence transformers with the [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) model for cross-lingual semantic analysis.

---

## Limitations

Rataitosk measures semantic patterns in strategic texts. It does not:
- Measure actual organizational alignment or practice
- Assess stakeholder perceptions or institutional culture
- Prescribe strategic decisions or interpretations
- Replace human judgment in strategic planning

The tool provides computational pattern detection as input to institutional dialogue and sensemaking processes.

---

## Example Output
The tool generates SAMS Scorecards showing semantic alignment across four dimensions:
- Thematic Similarity: 53.83%
- Temporal Positioning: High future-orientation
- Operational Grounding: Strong implementation focus
- Transformational Vision: Moderate change ambition

Full interactive scorecard: See HTML file in `/output` folder.

---

## Troubleshooting

**Model download fails**
If the MiniLM model fails to download automatically, check your internet connection and retry. The model is retrieved from Hugging Face on first use.

**Module not found errors**
Ensure you're using the virtual environment Python:
```bash
# Windows
.\venv\Scripts\python.exe cli\run_rataitosk.py

# Linux/macOS
./venv/bin/python cli/run_rataitosk.py
```

**For additional issues:** See [validate_rataitosk.py](/validate_rataitosk.py) output for detailed diagnostics, or open an issue on GitHub.

## Citation

If you use Rataitosk in your research, please cite:
```
Aarnseth, T. (2025). Rataitosk: A Method for Assessing Strategic Coherence 
via Inter-Document Semantic Alignment. Bachelor's thesis, Høgskolen i Molde.
https://github.com/s0rlie/rataitosk
```

---

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for full terms.

---

## Contact

**Thomas Aarnseth**  
Høgskolen i Molde | NTNU  
https://www.ntnu.edu/employees/thomas.aarnseth

---

## Acknowledgments


This work was supervised by Professor Bjørn Jæger at Høgskolen i Molde. Professor Hans Solli-Sæther provided essential guidance on the strategy perspective.
