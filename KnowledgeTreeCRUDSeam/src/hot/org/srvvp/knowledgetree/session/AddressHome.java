package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("addressHome")
public class AddressHome extends EntityHome<Address> {

	@In(create = true)
	CityHome cityHome;
	@In(create = true)
	DistrictHome districtHome;
	@In(create = true)
	PersonHome personHome;

	public void setAddressId(String id) {
		setId(id);
	}

	public String getAddressId() {
		return (String) getId();
	}

	@Override
	protected Address createInstance() {
		Address address = new Address();
		return address;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		City city = cityHome.getDefinedInstance();
		if (city != null) {
			getInstance().setCity(city);
		}
		District district = districtHome.getDefinedInstance();
		if (district != null) {
			getInstance().setDistrict(district);
		}
		Person person = personHome.getDefinedInstance();
		if (person != null) {
			getInstance().setPerson(person);
		}
	}

	public boolean isWired() {
		return true;
	}

	public Address getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
