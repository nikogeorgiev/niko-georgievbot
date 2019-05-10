import pywikibot
import pandas as pd


def ver_claims(reffile, property, target):

    refdata = pd.read_csv(reffile, index_col=False)
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    for index, item in refdata["PersID"].iteritems():

        itemwd = pywikibot.ItemPage(repo, item)
        itemwd = itemwd.get()
        label = itemwd
        itemaff = pywikibot.ItemPage(repo, refdata["SecID"][index])
        itemaff = itemaff.get()
        item_dict = itemwd["claims"]
        item_prop = item_dict[property]


        for claim in item_prop:

            claim_trgt = claim.getTarget()

            if claim_trgt.getID() == target:
                if claim.has_qualifier("P580", refdata["Year"][index]):
                    try:
                        print(itemwd["labels"]["en"], " HAS Start Time - ", refdata["Year"][index])
                    except KeyError:
                        print(item, " DOES NOT HAVE EN LABEL, ADDING LABEL ", refdata["name"][index])
                        print(item, " HAS Start Time - ", refdata["Year"][index])
                        label.editLabels(label = {'en' : refdata['name'][index]})
                else:
                    try:
                        print(itemwd["labels"]["en"], " DOES NOT HAVE Start Time - ", refdata["Year"][index])
                    except KeyError:
                        print(item, " DOES NOT HAVE EN LABEL")
                        print(item, " DOES NOT HAVE Start Time - ", refdata["Year"][index])
                    finally:
                        print("ADDING QUALIFIER P580 WITH VALUE ",  refdata["Year"][index], " TO ", item)
                        start_date = pywikibot.page.Claim(repo, 'P580', is_qualifier=True)
                        start_date.setTarget(pywikibot.WbTime(year=refdata["Year"][index]))
                        claim.addQualifier(start_date,  summary = 'Adding start date')
                if claim.has_qualifier("P1416", refdata["SecID"][index]):
                    try:
                        print(itemwd["labels"]["en"], " HAS Affiliation - ", itemaff["labels"]["en"])
                    except KeyError:
                        print(item, " DOES NOT HAVE EN LABEL")
                        print(item, " HAS Affiliation - ", itemaff["labels"]["en"])
                else:
                    try:
                        print(itemwd["labels"]["en"], " DOES NOT HAVE Affiliation - ", itemaff["labels"]["en"])
                    except KeyError:
                        print(item, " DOES NOT HAVE EN LABEL")
                        print(item, " DOES NOT HAVE Affiliation - ", itemaff["labels"]["en"])
                    finally:
                        print("ADDING QUALIFIER P1416 WITH VALUE ", itemaff["labels"]["en"], " TO ", item)
                        affiliation = pywikibot.page.Claim(repo, "P1416", is_qualifier= True)
                        affiliation.setTarget(pywikibot.ItemPage(repo, refdata["SecID"][index]))
                        claim.addQualifier(affiliation, summary = "Adding affiliation")

reffile = "~/Desktop/AEref.csv"

ver_claims(reffile,"P463","Q337234")






