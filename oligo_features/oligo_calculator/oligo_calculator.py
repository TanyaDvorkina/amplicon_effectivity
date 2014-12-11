__author__ = 'Anton Bragin'

import logging
import logging.config
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

"""
Simple Python script that uses http://biophysics.idtdna.com for primer parameters calculation.

Requirements:
 - Python 3
 - BeautifulSoup 4 (for installation and details see: http://www.crummy.com/software/BeautifulSoup/)

"""


#Tune logging via configuration loading
logging.config.fileConfig('../logging.cfg')
logger = logging.getLogger('oligo_calculator')

class OligoCalculator:
    """
    Calculates oligonucleotide hybridization parameters with http://biophysics.idtdna.com/ resource
    """
    def __init__(self):
        logger.debug('Initialize oligonucleotide calculator')
        self.url = 'http://biophysics.idtdna.com/cgi-bin/meltCalculator.cgi'

    def caclulate(self, sequence,
                  oligo_concentration=0.2,
                  target_concentration=0.2,
                  na_concentration=50,
                  mg_concentration=0,
                  dntp_concentration=0
                  ):
        """
        Caclulate NN thermodynamics for given oligo.

        :param sequence: DNA sequence that consists of A, G, T, C bases
        :param oligo_concentration: oligonucleotide concentration
        :param target_concentration: target concentration
        :param na_concentration: Na+ concentration in solution
        :param mg_concentration: Mg2+ concentration in solution
        :param dntp_concentration: dNTP concentration in solution
        :return: Tm, dG, dH, dS as float values
        """
        logger.info('Analyzing sequence: %s', sequence.upper())
        logger.debug('Calculating malting parameters for sequence: %s'
                     '\nOligo concentration: %s'
                     '\nTarget concentration: %s'
                     '\nNa+ concentration: %s'
                     '\nMg2+ concentration: %s'
                     '\ndNTPs concentration: %s', sequence,
                                                    oligo_concentration,
                                                    target_concentration,
                                                    na_concentration,
                                                    mg_concentration,
                                                    dntp_concentration)
        request_parameters = {
            'OligoConc' : oligo_concentration,
            'TargetConc' : target_concentration,
            'NaConc' : na_concentration,
            'MgConc' : mg_concentration,
            'dNTPsConc' : dntp_concentration,
            #This parameter is essential for sending request
            'SubmitButton' : 'CALCULATE',
            'sequence' : sequence
        }

        request_data = urllib.parse.urlencode(request_parameters).encode('UTF-8')
        request = urllib.request.Request(self.url, request_data)
        response_data = urllib.request.urlopen(request).read()

        logger.debug('Received data from the server: %s', response_data)

        return self.parse(response_data)

    def parse(self, response_page):
        page = BeautifulSoup(response_page)

        logger.debug('Page in pretty print:\n%s', page.prettify())
        Tm = float(page.find(id="Seq1TmOut").get_text())
        dG = float(page.find(id="Seq1dGOut").get_text())
        dH = float(page.find(id="Seq1dHOut").get_text())
        dS = float(page.find(id="Seq1dSOut").get_text())

        logger.info('Got oligonucleotide parameters. Tm: %s, dG: %s', Tm, dG)

        return Tm, dG, dH, dS

if __name__ == "__main__":

    input = '../ForThermoBLAST_IAD30284.csv'
    output = '../OligoFeatures_IAD30284.csv'

    oligo_caclulator = OligoCalculator()

    #Use standart parameters for AmpliSeq primers temperature approximation (see Confluence discussion)
    with open(input) as f_in:
        with open(output, 'w') as f_out:
            header = f_in.readline().strip() + ','.join(['"Tm"', '"dG"', '"dH"', '"dS"']) + '\n'
            f_out.write(header)
            for line in f_in:
                sequence = line.split(',')[0][1:-1]
                tm, dg, dh, ds = oligo_caclulator.caclulate(sequence, oligo_concentration=0.05,
                                                target_concentration=0, na_concentration=100, mg_concentration=2.5,
                                                        dntp_concentration=0.2)
                out_line = line.strip() + ','.join(str(x) for x in ['', tm, dg, dh, ds]) + '\n'
                f_out.write(out_line)
                f_out.flush()
