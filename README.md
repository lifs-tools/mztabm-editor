# LipidCompass mzTab-M Editor

## Installing the dependencies

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Running the application

    streamlit run LipidCompass_Submission_Editor.py

You can use the Brain Lipidome XLSX file for testing:

https://github.com/lifs-tools/lipidcompass-submissions/blob/master/submissions/LCE00000014/data/brain_lipidome.xlsx

In the same directory, you will find a python code base that was used to combine the inidividual tables into the final mzTab-m file. Not all of that has been implemented here yet.

## Implementation hints

Since Streamlit reevaluates the whole script from top to bottom on every change (here: one page=one script), we need to use the session state to store objects. Long running or resource intensive methods may be cached, so that they are only run once. We use the @functools.cache annotation on those methods.

## The ebi-ols-client currently does not install without issues

    pip install streamlit ols-client
