import copy
import unittest
from trace_quality import audit, aggregate

class TraceQuality(unittest.TestCase):
    def example(self):
        names=['applicable_response_recorded','downstream_record_supplied','record_fits_objective']
        states=[False,False,None]
        locs=[['/events'],['/downstream'],['/downstream']]
        key={'unit_id':'x','objective':'recorded_stop','scope':'single-authored-packet-terminal-record','packet_digest':'digest',
             'reference':'unresolved','checks':{n:{'state':s,'locators':p} for n,s,p in zip(names,states,locs)}}
        result={'procedure':'trace','unit_id':'x','objective':key['objective'],'claim_scope':key['scope'],'packet_digest':'digest',
                'response':'unresolved','reason':'Required evidence is unresolved.','limits':['Synthetic record only.'],
                'outcome_locator':None,'checks':[{'check':n,'satisfied':s,'locators':p} for n,s,p in zip(names,states,locs)],'blockers':names}
        return key,result

    def test_dependent_unknown_is_not_a_third_material_blocker(self):
        key,result=self.example()
        row=audit(result,key)
        self.assertEqual((row['material_blockers'],row['omitted_blockers'],row['dependent_blocker_labels']), (2,0,1))
        self.assertEqual(row['incorrect_assertions'],0)

    def test_short_explanation_omits_one_of_two_blockers(self):
        key,result=self.example()
        result['procedure']='checklist';result['checks']=result['checks'][:1];result.pop('blockers')
        row=audit(result,key)
        self.assertEqual((row['material_blockers'],row['omitted_blockers']), (2,1))

    def test_unknown_claimed_as_false_is_an_assertion_error(self):
        key,result=self.example()
        result['checks'][2]['satisfied']=False
        row=audit(result,key)
        self.assertEqual(row['incorrect_assertions'],1)
        self.assertEqual(row['material_blockers'],2)

    def test_missing_required_locator_cannot_get_coverage_credit(self):
        key,result=self.example()
        key['checks']['applicable_response_recorded']['locators']=['/events/0','/events/1']
        result['checks'][0]['locators']=['/events/0']
        row=audit(result,key)
        self.assertEqual((row['locator_errors'],row['omitted_blockers']), (1,1))

    def test_unknown_duplicate_and_missing_fields_invalidate_audit(self):
        key,result=self.example()
        altered=copy.deepcopy(result);altered['checks'].append(altered['checks'][0])
        with self.assertRaises(ValueError):audit(altered,key)
        altered=copy.deepcopy(result);altered['checks'][0]['check']='new'
        with self.assertRaises(ValueError):audit(altered,key)
        altered=copy.deepcopy(result);altered.pop('reason')
        with self.assertRaises(ValueError):audit(altered,key)

    def test_label_mismatch_is_retained_separately(self):
        key,result=self.example()
        result['response']='effect_supported';result['outcome_locator']='/downstream'
        self.assertFalse(audit(result,key)['label_matches_key'])

    def test_empty_metric_denominators_are_not_zero_success(self):
        result=aggregate([])
        self.assertIsNone(result['omission_rate'])
        self.assertIsNone(result['assertion_error_rate'])
        self.assertIsNone(result['locator_error_rate'])
