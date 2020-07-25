from model import parameters
from model import person
from model import vaccine
from model import model

# person.Person()

# vaccine.Vaccine(10)

p = person.Person(age = 20)


print("       curr status: ", p.curr_status.value)
print("         age      : ", p.age)
print("         age group: ", p.age_group.value)
print("      route status: ", p.route_status.value)
p.route_status_rand()
print("route status again: ", p.route_status.value)
p.route_status_rand()
print("route status again: ", p.route_status.value)
p.route_status_rand()
print("route status again: ", p.route_status.value)
p.route_status_rand()
print("route status again: ", p.route_status.value)

print("youth contact rate: ", p.youth_contact_rate.value)
print("adult contact rate: ", p.adult_contact_rate.value)
print("elder contact rate: ", p.elder_contact_rate.value)
print("      vaccine rate: ", p.vaccine_rate.value)
print("    infection rate: ", p.infection_rate.value)
print("    vaccine status: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
p.vaccine_status_rand()
print("vaccine status again: ", p.vaccine_status)
print("medicine intake rate: ", p.medicine_intake_rate.value)
print("         severe rate: ", p.severe_rate.value)

print("       fatality rate: ", p.fatality_rate.value)
print("  effectiveness mild: ", p.effectiveness_mild.value)
print("effectiveness severe: ", p.effectiveness_severe.value)
print(" effectiveness death: ", p.effectiveness_death.value)

md = model.VaccineModel()
print("     md idx_case_num: ", md.idx_case_num)
print("          md sim_day: ", md.sim_day)
print("         md sim_time: ", md.sim_time)
print("       md cycle_days: ", md.cycle_days)
print("  md transmission_gp: ", md.transmission_gp)
print("     md treatment_gp: ", md.treatment_gp)
print("         md death_gp: ", md.death_gp)
print("      md recovery_gp: ", md.recovery_gp)
