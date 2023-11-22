
from business_rules.variables import BaseVariables
from business_rules.variables import select_rule_variable
from business_rules.actions import BaseActions
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT
from business_rules import export_rule_data
from business_rules import run_all
import json
import os
    
class Claim:

    def __init__(self, treatmentType,
                 claimantName,
                 treatment, 
                 accepted = False, 
                 rejected = False,
                 verify = False):
        self.treatmentType = treatmentType
        self.claimantName = claimantName
        self.treatment = treatment
        self.accepted = accepted
        self.rejected = rejected
        self.verify = verify
        print('claim init ::', self.treatment)
    
    def accept(self):
        print('accepting')
        self.accepted = True

    def reject(self):
        print('rejecting')
        self.rejected = True

    def send_to_verification(self):
        print('verifying')
        self.verify = True

class ClaimVariables(BaseVariables):

    def __init__(self, claim):
        print('variable init ::', claim)
        self.claim = claim

    @select_rule_variable(label="Treatment")
    def treatment(self):
        print('select rule :: treatment', self.claim.treatment)
        return self.claim.treatment
    
class ClaimActions(BaseActions):

    def __init__(self, claim):
        print('action init', claim)
        self.claim = claim

    @rule_action(label="Accept Bill")
    def accept_bill(self):
        print('action: acceting bill')
        self.claim.accept()

    @rule_action(label="Reject Bill")
    def reject_bill(self):
        print('action: rejecting bill')
        self.claim.reject()

    @rule_action(label="Verify Bill")
    def verify_bill(self):
        print('action: verify bill')
        self.claim.send_to_verification()

def _export_rule_data():
    print('exporting rule data')
    export_rule_data(ClaimVariables, ClaimActions)

def run_rules(claim):
    _export_rule_data()
    print(os.getcwd())
    with open(os.getcwd()+"\\rules.json", "r") as file:
        rules = json.load(file)
        print('loaded json rules :: ', rules)
    run_all(rule_list=rules,
            defined_variables=ClaimVariables(claim),
            defined_actions=ClaimActions(claim),
            stop_on_first_trigger=True)
    print('rules are executed')
    return claim

#_claim = Claim(treatment='Dental Bleaching')
#run_rules(_claim)