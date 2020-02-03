import helpers as hlps
import config as cfg
import importlib

importlib.reload(hlps)

df_el_dd = hlps.export_redcap_metadata(uri=cfg.WSU_REDCAP_API_URI,
                                       token=cfg.WSU_REDCAP_API_ELECTRA_TOKEN)

df_el_dd.columns
df_el_forms_arr = df_el_dd['form_name'].unique()
df_el_forms_arr

df_el_formmap = hlps.export_redcap_formmaps(uri=cfg.WSU_REDCAP_API_URI,
                                            token=cfg.WSU_REDCAP_API_ELECTRA_TOKEN)

df_el_formmap.columns
df_el_formmap.head()
bool_screenvisit = df_el_formmap['unique_event_name'].str.contains(r'sv\d_arm_1')
df_el_formmap_flt = df_el_formmap.loc[bool_screenvisit, :]

# df_el_formmap_arr = df_el_formmap['form'].sort_values(axis=0).unique()
df_el_formmap_arr = df_el_formmap['form'].unique()
len(df_el_formmap_arr)
df_el_formmap_arr
