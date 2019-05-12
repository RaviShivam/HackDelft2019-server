a = {"description": "Berghotel\nGrosse Scheidegg\n3818 Grindelwald\nFamilie R. Müller\nRech. Nr. 4572\nBar\n30.07.2007/13:29:17\nTisch 7/01\n2xLatte Hacchiato à 4.50 CHF 9.00\nà 5.00 CHF 5.00\n1xSchweinschnitzel à 22.00 CHF 22.00\nà 18.50 CHF 18.50\nxGloki\nixChässpätzl à\nTotal CHF 54,50\nIncl. 7.6 uSt 54.50 CHF 3.85\nEntspricht in Euro 36.33 EUR\nEs bediente Sie: Ursula\nMwSt N. 430 234\nTel 033 853 67 16\nFax. 033 853 67 19\nE-mail: grossescheideggb luewin.ch\n"}
a = a['description'].split('\n')

form = {}
for (i = 0; i < a.length; i++) {
	if(a[i].includes('Total')) {
		b = a[i].split(' ')
		form['currency'] = b[1]
		form['amount'] = parseFloat(b[2].replace(',', '.'))
	}
}
