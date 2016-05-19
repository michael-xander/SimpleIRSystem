# SimpleIRSystem
## A simple IR system to index and query a collection.

### Collaborators
 - Charles Du
 - Michael Kyeyune
### Requirements
 - Python 3.4.3+
### Utilising this system
To utilise this system you need to generate a collection from a testbed, index the collection then compare MAP/Avg NDCG results for the modified and unmodified engine.
 - generate collection from testbed
   - ```python collect.py testbedx``` - x being the number of the testbed. This will generate a file ```testbedx_collection```
 - index testbed collection
   - ```python index.py testbedx_collection```
 - analyse modified and unmodified engine performance
   - ```python analyse.py testbedx```
 - finding optimal indicative terms and top k documents to utilise for blind relevance feedback (BRF) for a single testbed
   - ```python optimise.py -s testbedx 200``` 200 being the number of documents to consider in MAP/Avg NDCG calculations
 - finding optimal indicative terms and top k documents to utilise for BRF for all testbeds
   - ```python optimise.py -a 200```
### Important Notices
 - Documents that are not in UTF-8 format are ignored when generating the collection for a testbed
 - All testbeds must be indexed before attempting to optimise across all testbeds