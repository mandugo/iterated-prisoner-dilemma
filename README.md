# Iterated Prisoner's Dilemma

Framework modulare per simulare tornei del Prisoner's Dilemma ripetuto.
Consultare `prisoners_dilemma/README.md` per istruzioni dettagliate.

## Setup dell'ambiente con Conda

1. Assicurarsi di avere [Conda](https://docs.conda.io) installato (Miniconda o Anaconda).
2. Creare un nuovo ambiente con una versione supportata di Python:
   ```bash
   conda create --name ipd-env python=3.11
   ```
3. Attivare l'ambiente appena creato:
   ```bash
   conda activate ipd-env
   ```
4. Installare le dipendenze del progetto tramite `pip` usando il file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
5. (Opzionale) Verificare che tutto funzioni eseguendo la suite di test:
   ```bash
   python -m pytest prisoners_dilemma/tests
   ```

Una volta completati i passaggi precedenti, è possibile utilizzare il pacchetto e gli script di esempio inclusi nel repository.
