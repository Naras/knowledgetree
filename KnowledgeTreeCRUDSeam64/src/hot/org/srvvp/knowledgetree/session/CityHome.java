package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("cityHome")
public class CityHome extends EntityHome<City> {

	@In(create = true)
	StateHome stateHome;

	public void setCityId(CityId id) {
		setId(id);
	}

	public CityId getCityId() {
		return (CityId) getId();
	}

	public CityHome() {
		setCityId(new CityId());
	}

	@Override
	public boolean isIdDefined() {
		if (getCityId().getCountryId() == null
				|| "".equals(getCityId().getCountryId()))
			return false;
		if (getCityId().getId() == null || "".equals(getCityId().getId()))
			return false;
		if (getCityId().getStateId() == null
				|| "".equals(getCityId().getStateId()))
			return false;
		return true;
	}

	@Override
	protected City createInstance() {
		City city = new City();
		city.setId(new CityId());
		return city;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		State state = stateHome.getDefinedInstance();
		if (state != null) {
			getInstance().setState(state);
		}
	}

	public boolean isWired() {
		if (getInstance().getState() == null)
			return false;
		return true;
	}

	public City getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<Address> getAddresses() {
		return getInstance() == null ? null : new ArrayList<Address>(
				getInstance().getAddresses());
	}

}
