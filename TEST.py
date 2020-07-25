from model import parameters
from model import person
from model import vaccine

# person.Person()

# vaccine.Vaccine(10)

p = person.Person(age = 20)


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
print("       get vaccine: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
p.get_vaccine_random(p.get_vaccine)
print(" get vaccine again: ", p.get_vaccine)
