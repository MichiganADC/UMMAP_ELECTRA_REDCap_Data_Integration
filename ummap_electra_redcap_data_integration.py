#!/usr/bin/env python3

##################
# Import Modules #
##################

import numpy as np
import re
from datetime import date
import config as cfg
import helpers as hlps
import ummap_electra_redcap_data_integration_helpers as uerdi_hlps


####################
# Get ELECTRA Data #
####################

print("Retrieving ELECTRA data from WSU REDCap API...")

forms_el_raw = ["header",
                "ivp_a1",
                "ivp_a2",
                "ivp_a3",
                "ivp_a4",
                "ivp_a5",
                "ivp_b1",
                "ivp_b4",
                "ivp_b5",
                "ivp_b6",
                "ivp_b7",
                "ivp_b8",
                "ivp_b9",
                "ivp_c2",
                "ivp_d1",
                "ivp_d2",
                "ivp_z1",
                "fvp_a1",
                "fvp_a2",
                "fvp_a3",
                "fvp_a4",
                "fvp_a5",
                "fvp_b1",
                "fvp_b1",
                "fvp_b4",
                "fvp_b5",
                "fvp_b6",
                "fvp_b7",
                "fvp_b8",
                "fvp_b9",
                "fvp_c2",
                "fvp_d1",
                "fvp_d2",
                "fvp_z1",
                'tvp_t1',
                'tvp_a1',
                'tvp_a2',
                'tvp_a3',
                'tvp_a4',
                'tvp_b4',
                'tvp_b5',
                'tvp_b7',
                'tvp_b9',
                'tvp_d1',
                'tvp_d2',
                'ftld_a3a',
                'ftld_c2f',
                'ftld_c3f',
                'ftld_c4f',
                'ftld_c5f',
                'ftld_c6f',
                'ftld_e2f',
                'ftld_e3f',
                'ftld_z1f',
                'caregiver_questionnaire',
                'mac_q',
                'adco',
                'lsns6',
                'jolo',
                'hvlt',
                'emory_wcst',
                'wtar',
                'cowa_cfl',
                'financial_decision_making_self_efficacy_form',
                'lfdss_for_professionals',
                'behavioral_observations',
                'ivp_b1l',
                'ivp_b2l',
                'b3l',
                'ivp_b4l',
                'iv_b5l',
                'iv_b6l',
                'ivp_bl7',
                'iv_bl8',
                'iv_b9l',
                'c1l',
                'd1l',
                'ivp_e1l',
                'ivp_e2l',
                'ivp_e3l',
                'family_friends_interview_ffi',
                'cogstate',
                'ipad_tool_box',
                'tvp_t1',
                'tvp_a1',
                'tvp_a2',
                'tvp_a3',
                'tvp_a4',
                'tvp_b4',
                'tvp_b5',
                'tvp_b7',
                'tvp_b9',
                'tvp_d1',
                'tvp_d2',
                'tvp_z1',
                'm1'
                ]
# What other forms need to be imported from ELECTRA to UMMAP - UDS 3?

forms_el = ','.join(forms_el_raw)

df_el = hlps.export_redcap_records(uri=cfg.WSU_REDCAP_API_URI,
                                   token=cfg.WSU_REDCAP_API_ELECTRA_TOKEN,
                                   forms=forms_el)

######################
# Clean ELECTRA Data #
######################

print("Cleaning ELECTRA data to conform to UMMAP criteria...")

###################################
# Basic Cleaning / Transformation #

# Keep only merged records
ptid_merged = df_el['ptid'].str.match(r'^UM\d{8}$')
df_el_cln = df_el.loc[ptid_merged, :]

df_el_u3 = df_el_cln.copy()

# Use `ummap_visit_number` to match UMMAP - UDS3 `redcap_event_name`
df_el_u3.loc[:, 'redcap_event_name'] = df_el_u3['ummap_visit_number'].map(lambda x: "visit_" + x + "_arm_1")

###############
# Header Form #

print("  * Header Form")
# Drop `elid` field
del df_el_u3['elid']

# Drop `ummap_visit_number` field
del df_el_u3['ummap_visit_number']

# Ensure `mrn` values have 9 digits
mrn_len = 9
df_el_u3.loc[:, 'mrn'] = df_el_u3['mrn'].map(lambda x: uerdi_hlps.lengthen_str(x, length=mrn_len, leading_str="0"))

# Ensure `vstsqid` values have 3 digits
vstsqid_len = 3
df_el_u3.loc[:, 'vstsqid'] = \
    df_el_u3['vstsqid'].map(lambda x: uerdi_hlps.lengthen_str(x, length=vstsqid_len, leading_str="0"))

# Ensure `paper_visit_num` values have 3 digits
paper_visit_num_len = 3
df_el_u3.loc[:, 'paper_visit_num'] = \
    df_el_u3['paper_visit_num'].map(lambda x: uerdi_hlps.lengthen_str(x, length=paper_visit_num_len, leading_str="0"))

# Ensure `visitnum` values have 3 digits
visitnum_len = 3
df_el_u3.loc[:, 'visitnum'] = \
    df_el_u3['visitnum'].map(lambda x: uerdi_hlps.lengthen_str(x, length=visitnum_len, leading_str="0"))

########################
# Form A5 - `arthtype` #

print("  * Transforming Form A5 `arthtype` fields")
# arthtype___1  arthtype == 1  Rheumatoid
# arthtype___2	arthtype == 2  Osteoarthritis
# arthtype___3	arthtype == 3  Other
# arthtype___9	arthtype == 9  Unknown

df_el_u3 = df_el_u3.assign(arthtype___1=np.where(df_el_u3['arthtype'] == "1", "1", ""))
df_el_u3 = df_el_u3.assign(arthtype___2=np.where(df_el_u3['arthtype'] == "2", "1", ""))
df_el_u3 = df_el_u3.assign(arthtype___3=np.where(df_el_u3['arthtype'] == "3", "1", ""))
df_el_u3 = df_el_u3.assign(arthtype___9=np.where(df_el_u3['arthtype'] == "9", "1", ""))
del df_el_u3['arthtype']

df_el_u3 = df_el_u3.assign(fu_arthtype___1=np.where(df_el_u3['fu_arthtype'] == "1", "1", ""))
df_el_u3 = df_el_u3.assign(fu_arthtype___2=np.where(df_el_u3['fu_arthtype'] == "2", "1", ""))
df_el_u3 = df_el_u3.assign(fu_arthtype___3=np.where(df_el_u3['fu_arthtype'] == "3", "1", ""))
df_el_u3 = df_el_u3.assign(fu_arthtype___9=np.where(df_el_u3['fu_arthtype'] == "9", "1", ""))
del df_el_u3['fu_arthtype']

######################
# Form D2 - `artype` #

print("  * Transforming Form D2 `artype` fields")
# artype___1  artype == 1 Rheumatoid
# artype___2  artype == 2 Osteoarthritis
# artype___3  artype == 3 Other (SPECIFY BELOW):
# artype___9  artype == 9 Unknown

df_el_u3 = df_el_u3.assign(artype___1=np.where(df_el_u3['artype'] == "1", "1", ""))
df_el_u3 = df_el_u3.assign(artype___2=np.where(df_el_u3['artype'] == "2", "1", ""))
df_el_u3 = df_el_u3.assign(artype___3=np.where(df_el_u3['artype'] == "3", "1", ""))
df_el_u3 = df_el_u3.assign(artype___9=np.where(df_el_u3['artype'] == "9", "1", ""))
del df_el_u3['artype']

df_el_u3 = df_el_u3.assign(fu_artype___1=np.where(df_el_u3['fu_artype'] == "1", "1", ""))
df_el_u3 = df_el_u3.assign(fu_artype___2=np.where(df_el_u3['fu_artype'] == "2", "1", ""))
df_el_u3 = df_el_u3.assign(fu_artype___3=np.where(df_el_u3['fu_artype'] == "3", "1", ""))
df_el_u3 = df_el_u3.assign(fu_artype___9=np.where(df_el_u3['fu_artype'] == "9", "1", ""))
del df_el_u3['fu_artype']

df_el_u3 = df_el_u3.assign(tele_artype___1=np.where(df_el_u3['tele_artype'] == "1", "1", ""))
df_el_u3 = df_el_u3.assign(tele_artype___2=np.where(df_el_u3['tele_artype'] == "2", "1", ""))
df_el_u3 = df_el_u3.assign(tele_artype___3=np.where(df_el_u3['tele_artype'] == "3", "1", ""))
df_el_u3 = df_el_u3.assign(tele_artype___9=np.where(df_el_u3['tele_artype'] == "9", "1", ""))
del df_el_u3['tele_artype']

####################################
# Correct `ivp_XX_complete` Fields #

# For example, if a record is not an initial visit, set `ivp_a1_complete` to NaN
# for form in filter(lambda f: re.match(r'^ivp_\w{2}$', f), forms_el_raw):
for form in [f for f in forms_el_raw if re.match(r'^ivp_\w{2}$', f)]:
    form_complete = form + "_complete"
    print("  * Correcting `" + form_complete + "` field")
    kwargs = {form_complete: (df_el_u3[form_complete]).where(df_el_u3['redcap_event_name'] == "visit_1_arm_1", np.NaN)}
    df_el_u3 = df_el_u3.assign(**kwargs)

####################################
# Correct `fvp_XX_complete` Fields #

# For example, if a records is not a follow-up visit, set `fvp_a1_complete` to NaN
for form in [f for f in forms_el_raw if re.match(r'^fvp_\w{2}$', f)]:
    form_complete = form + "_complete"
    print("  * Correctiong `" + form_complete + "` field")
    kwargs = {form_complete: (df_el_u3[form_complete]).where(df_el_u3['redcap_event_name'] != "visit_1_arm_1", np.NaN)}
    df_el_u3 = df_el_u3.assign(**kwargs)

####################################
# Correct `tvp_XX_complete` Fields #

# For example, if a records is not a follow-up visit, set `fvp_a1_complete` to NaN
for form in [f for f in forms_el_raw if re.match(r'^fvp_\w{2}$', f)]:
    form_complete = form + "_complete"
    print("  * Correcting `" + form_complete + "` field")
    kwargs = {form_complete: (df_el_u3[form_complete]).where(df_el_u3['redcap_event_name'] != "visit_1_arm_1", np.NaN)}
    df_el_u3 = df_el_u3.assign(**kwargs)

################################
# Add Missing Center ID Values #

michigan_adc_id = 43
df_el_u3.loc[:, 'adcid'] = michigan_adc_id

#################################
# Write Transformed Data to CSV #
#################################

print("Writing cleaned and transformed ELECTRA data to CSV...")

today = date.today()
month_str = str(today.month) if len(str(today.month)) == 2 else "0" + str(today.month)
day_str = str(today.day) if len(str(today.day)) == 2 else "0" + str(today.day)
today_str = f"{today.year}-{month_str}-{day_str}"
df_el_u3.to_csv(f"./electra_data_to_import/{today_str}-electra_data_to_import.csv", index=False)

print("Done.")
