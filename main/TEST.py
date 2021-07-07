# from model import parameters
from vmodel import person
from vmodel import vaccine
from vmodel import model

# person.Person(.value)

# vaccine.Vaccine(10.value)


## Vaccination = 0
p = person.Person(age = 98, params_file_path="/ssd/Howard/vaccine-cost-model/media/tmp/6a0e3b6edc2311eb8802e41f1345dc74/input_params.json", group_idx=1)

## Vaccination = 1
# p = person.Person(age = 98, params_file_path="/ssd/Howard/vaccine-cost-model/media/tmp/155504a8dc2411eb9c06e41f1345dc74/input_params.json", group_idx=1)

#
# print("           curr status: ", p.curr_status.value)
# print("                    id: ", p.id)
# print("    contactperson_rate: ", p.contactperson_rate.value)
# print("    seektreatment_rate: ", p.seektreatment_rate.value)
# print("           curr_status: ", p.curr_status.value)
# print("                   day: ", p.day)
# print("                   age: ", p.age)
# print("             age_group: ", p.age_group.value)
# print("    youth_contact_rate: ", p.youth_contact_rate.value)
# print("    adult_contact_rate: ", p.adult_contact_rate.value)
# print("    elder_contact_rate: ", p.elder_contact_rate.value)
# print("          vaccine_rate: ", p.vaccine_rate.value)
# print("        n_vaccine_rate: ", p.n_vaccine_rate.value)
# print("    vac_infection_rate: ", p.vac_infection_rate.value)
# print("  vac_n_infection_rate: ", p.vac_n_infection_rate.value)
# print("  n_vac_infection_rate: ", p.n_vac_infection_rate.value)
# print("n_vac_n_infection_rate: ", p.n_vac_n_infection_rate.value)
#
# # p.vaccine_status = p.set_vaccine_status(.value)
#
# print("                      smt_ipd_rate: ", p.smt_ipd_rate.value)
# print("                      smt_opd_rate: ", p.smt_opd_rate.value)
# print("                smt_ipd_death_rate: ", p.smt_ipd_death_rate.value)
# print("             smt_ipd_recovery_rate: ", p.smt_ipd_recovery_rate.value)
# print("             smt_opd_medicine_rate: ", p.smt_opd_medicine_rate.value)
# print("           smt_opd_n_medicine_rate: ", p.smt_opd_n_medicine_rate.value)
# print("                smt_opd_m_ipd_rate: ", p.smt_opd_m_ipd_rate.value)
# print("           smt_opd_m_recovery_rate: ", p.smt_opd_m_recovery_rate.value)
# print("          smt_opd_m_ipd_death_rate: ", p.smt_opd_m_ipd_death_rate.value)
# print("       smt_opd_m_ipd_recovery_rate: ", p.smt_opd_m_ipd_recovery_rate.value)
# print("               smt_opd_nm_ipd_rate: ", p.smt_opd_nm_ipd_rate.value)
# print("          smt_opd_nm_recovery_rate: ", p.smt_opd_nm_recovery_rate.value)
# print("        smt_opd_nm_ipd_death_srate: ", p.smt_opd_nm_ipd_death_rate.value)
# print("      smt_opd_nm_ipd_recovery_rate: ", p.smt_opd_nm_ipd_recovery_rate.value)

## Vaccination = 0
m = model.VaccineModel("/ssd/Howard/vaccine-cost-model/media/tmp/6a0e3b6edc2311eb8802e41f1345dc74/input_params.json", group_idx=1)

## Vaccination = 1
# m = model.VaccineModel("/ssd/Howard/vaccine-cost-model/media/tmp/155504a8dc2411eb9c06e41f1345dc74/input_params.json", group_idx=1)
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()
m.one_day_passed()

# print("         age      : ", p.age.value)
# print("         age group: ", p.age_group.value.value)
# print("      route status: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
# p.choose_route(.value)
# print("route status again: ", p.route_status.value.value)
#
#
# print("youth contact rate: ", p.youth_contact_rate.value.value)
# print("adult contact rate: ", p.adult_contact_rate.value.value)
# print("elder contact rate: ", p.elder_contact_rate.value.value)
# print("      vaccine rate: ", p.vaccine_rate.value.value)
# print("    vaccine status: ", p.vaccine_status.value)
# print("    infection rate: ", p.infection_rate.value.value)
# print("  infection status: ", p.infection_status.value)
#
# # print("  medicine_48_status: ", p.medicine_48_status.value)
# print(" seek treatment rate: ", p.seek_treatment_rate.value.value)
# print("seektreatment status: ", p.seek_treatment_status.value)
# print("medicine intake rate: ", p.medicine_intake_rate.value.value)
# print("medicine intake status: ", p.medicine_intake_status.value)
# print("         severe rate: ", p.severe_rate.value.value)
# print("       severe status: ", p.severe_status.value)
# print("       fatality rate: ", p.fatality_rate.value.value)
# print("  effectiveness mild: ", p.effectiveness_mild.value.value)
# print("effectiveness severe: ", p.effectiveness_severe.value.value)
# print(" effectiveness death: ", p.effectiveness_death.value.value)
#
# md = model.VaccineModel(.value)
# print("     md idx_case_num: ", md.idx_case_num.value)
# print("          md sim_day: ", md.sim_day.value)
# print("         md sim_time: ", md.sim_time.value)
# print("       md cycle_days: ", md.cycle_days.value)
# # print("  md transmission_gp: ", md.transmission_gp.value)
# # print("     md treatment_gp: ", md.treatment_gp.value)
# # print("         md death_gp: ", md.death_gp.value)
# # print("      md recovery_gp: ", md.recovery_gp.value)
#
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
# md.one_day_passed(.value)
