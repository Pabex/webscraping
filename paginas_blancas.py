import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()


def get_contacts(name: str):
    contacts = []
    base_url = "http://www.paginasblancas.com.ar/persona/%s/"

    headers = {
        'User-Agent': user_agent.random
    }
    url = base_url % name
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, "html.parser")

    lis = bs.find_all("li", class_="m-results-business m-results-subscriber")
    for li in lis:
        # Name
        h3_name = li.find("h3", class_="m-results-business--name")
        a_name = h3_name.find("a")
        name = a_name.string

        # Address
        div_address = li.find("div", class_="m-results-business--address")
        spans_address = div_address.find_all("span")
        street_address = spans_address[0].string.strip()
        street_address = re.sub(' +', ' ', street_address)
        locality_address = spans_address[1].string.strip()
        postal_code_address = spans_address[2].string.strip()

        # Phone number
        div_number = li.find("div", class_="m-button--results-business--icon m-button--results-business--see-phone")
        onclick = div_number.attrs['onclick']
        match_number = re.search(r'\d+', onclick)
        phone_number = match_number.group() if match_number.group() else None

        dict_contact = {
            'name': name,
            'address': {
                'street': street_address,
                'locality': locality_address,
                'postal_code': postal_code_address
            },
            'phone_number': phone_number
        }

        contacts.append(dict_contact)
    return contacts


if __name__ == "__main__":
    name = input("Ingrese el nombre a buscar: ")
    name = name.replace(' ', '-')
    contacts = get_contacts(name)
    print("Nombre\t| Teléfono\t| Dirección")
    for contact in contacts:
        address = contact['address']['street'] + ' ' + contact['address']['locality'] + ' ' + contact['address']['postal_code']
        contact_str = "%s\t| %s\t| %s" % (contact['name'], contact['phone_number'], address)
        print(contact_str)
