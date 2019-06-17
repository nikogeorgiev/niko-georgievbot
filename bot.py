import pywikibot
import pandas as pd
import time
import os
reference = "~/Desktop/AEref.csv"
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


def ver_claims(reffile, property, target):

    refdata = pd.read_csv(reffile, index_col=False)

    for index, item in refdata["PersID"].iteritems():
        itemwd = pywikibot.ItemPage(repo, item)
        itemcheck = itemwd
        if itemcheck.isRedirectPage():
            itemcheck = itemcheck.getRedirectTarget()
            itemcheck = itemcheck.getID()
            itemwd = pywikibot.ItemPage(repo, itemcheck)
            itemcheck = itemwd
            itemwd = itemwd.get()
            item_dict = itemwd['claims']
            item_prop = item_dict[property]
            print(itemcheck, ' IS a redirect, changing to -> ', itemwd['labels']['en'])
        else:
            itemwd = itemwd.get()
            item_dict = itemwd['claims']
            try:
                item_prop = item_dict[property]
            except KeyError:
                memof = pywikibot.page.Claim(repo, 'P463', is_qualifier=False)
                memof.setTarget(pywikibot.ItemPage(repo, target))
                itemcheck.addClaim(memof)
                time.sleep(5)
                itemwd = itemcheck
                itemwd = itemwd.get()
                item_dict = itemwd['claims']
                item_prop = item_dict[property]
        for claim in item_prop:
            claim_trgt = claim.getTarget()
            if claim_trgt.getID() == target:
                try:
                    itemwd['labels']['en']
                except KeyError:
                    itemcheck.editLabels({'en': refdata['name'][index]})
                if not claim.has_qualifier("P580", refdata["Year"][index]):
                    start_date = pywikibot.page.Claim(repo, 'P580', is_qualifier=True)
                    start_date.setTarget(pywikibot.WbTime(year=refdata["Year"][index]))
                    claim.addQualifier(start_date)
                if not claim.has_qualifier("P1416", refdata["SecID"][index]):
                    affiliation = pywikibot.page.Claim(repo, "P1416", is_qualifier=True)
                    affiliation.setTarget(pywikibot.ItemPage(repo, refdata["SecID"][index]))
                    claim.addQualifier(affiliation)

ver_claims(reference, "P463", "Q337234")
