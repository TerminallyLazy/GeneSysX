"""
This testing module is to make sure that the prompts and the function
descriptions defined in `tools.pubmed` results in the behavior that we expect.
"""

import os
import pytest
import openai
from genesys import tools
from genesys.tools.pubmed import fetch_papers
import time


def test_perform_search():
    time.sleep(5)
    query = "genomics"
    result = fetch_papers(query=query)
    expected_result = [('37979127', 'Real-life diagnostic and therapeutic approach to CLL: a 2022 update from an expert panel in Tuscany.'), ('37979094', 'Correction to: The frequency of non‑motor symptoms in SCA3 and their association with disease severity and lifestyle factors.'), ('37979077', 'Single-cell transcriptomic analysis reveals transcriptional and cell subpopulation differences between human and pig immune cells.'), ('37979052', 'Molecular basis of retinal remodeling in a zebrafish model of retinitis pigmentosa.'), ('37979047', 'Cytosolic nucleic acid sensing and mitochondrial transcriptomic changes as early triggers of metabolic disease in db/db mice.'),
                       ('37979036', 'Atypical Modes of CTCF Binding Facilitate Tissue-Specific and Neuronal Activity-Dependent Gene Expression States.'), ('37979035', 'Causal Association of Cytokines and Growth Factors with Stroke and Its Subtypes: a Mendelian Randomization Study.'), ('37979006', 'Diabetes and artificial intelligence beyond the closed loop: a review of the landscape, promise and challenges.'), ('37978996', "Mapping of Rf20(t), a minor fertility restorer gene for rice wild abortive cytoplasmic male sterility in the maintainer line 'Zhenshan97B'."), ('37978887', 'Adapting cardiovascular risk prediction models to different populations: the need for recalibration.')]
    assert result == expected_result

def test_perform_search_2():
    time.sleep(5)
    query = "genomics, cancer, crispr"
    result = fetch_papers(query=query)
    expected_result = [('37977119', 'Active growth signaling promotes senescence and cancer cell sensitivity to CDK7 inhibition.'), ('37970920', 'Evidence of a synthetic lethality interaction between SETDB1 histone methyltransferase and CHD4 chromatin remodeling protein in a triple negative breast cancer cell line.'), ('37969391', 'The transcription activity of '), ('37968435', 'CRISPR/Cas12a trans-cleavage triggered by cleavage ligation of dumbbell DNA for specific detection of human 8-oxoguanine DNA glycosylase activity.'), ('37968405', 'Single-cell CRISPR screens in vivo map T cell fate regulomes in cancer.'), ('37964355', 'CRISPR/Cas9 system: recent applications in immuno-oncology and cancer immunotherapy.'), ('37961517', 'Germline '), ('37961138', 'Disparate pathways for extrachromosomal DNA biogenesis and genomic DNA repair.'), ('37958729', 'ASCL1 Is Involved in the Pathogenesis of Schizophrenia by Regulation of Genes Related to Cell Proliferation, Neuronal Signature Formation, and Neuroplasticity.'), ('37958549', 'The Role of Human Endogenous Retrovirus (HERV)-K119 ')]
    assert result == expected_result


if __name__ == "__main__":
    pytest.main()
